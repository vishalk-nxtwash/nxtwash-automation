import os
import signal
import subprocess

import pytest
from selenium.webdriver.common.service import Service as _SeleniumService

from core.driver_factory import DriverFactory


# ---------------------------------------------------------------------------
# Selenium's Service._terminate_process() hard-codes process.wait(60).
# When Chrome/ChromeDriver freezes, that 60-second wait blocks every
# subsequent test in the run.  Patching the CLASS (not an instance) means
# the fix applies to every service object, including ones created during a
# failed driver setup that are later garbage-collected via __del__ →
# stop() → _terminate_process().
# ---------------------------------------------------------------------------
def _fast_terminate_process(self) -> None:
    try:
        for stream in (self.process.stdin, self.process.stdout, self.process.stderr):
            try:
                stream.close()
            except AttributeError:
                pass
        self.process.terminate()
        try:
            self.process.wait(3)  # was 60 seconds
        except subprocess.TimeoutExpired:
            self.process.kill()
    except OSError:
        pass


_SeleniumService._terminate_process = _fast_terminate_process


def _descendant_pids(pid):
    """Return pid's current descendant PIDs (whole subtree, not just direct
    children), via `ps` -- no new dependency, POSIX-only (every runner here
    is Linux or macOS). Must be called while the process tree we care about
    still has its original parent/child links intact -- see the call site's
    comment for why that means capturing this immediately, not after the
    fact.
    """
    try:
        listing = subprocess.run(
            ["ps", "-eo", "pid,ppid"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:  # noqa: BLE001
        return []

    children_by_parent = {}
    for line in listing.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) != 2:
            continue
        try:
            child_pid, parent_pid = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        children_by_parent.setdefault(parent_pid, []).append(child_pid)

    stack = [pid]
    descendants = []
    while stack:
        current = stack.pop()
        for child_pid in children_by_parent.get(current, []):
            descendants.append(child_pid)
            stack.append(child_pid)
    return descendants


def _command_names(pids):
    """Return {pid: command name} for whichever of pids are still running.

    One batched `ps -eo pid,comm` call for the whole set, not one process
    per PID -- this runs on every test's teardown, so an N-subprocess
    version would add real overhead across a suite this size.
    """
    if not pids:
        return {}
    try:
        listing = subprocess.run(
            ["ps", "-eo", "pid,comm"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:  # noqa: BLE001
        return {}

    wanted = set(pids)
    names = {}
    for line in listing.stdout.splitlines()[1:]:
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        try:
            line_pid = int(parts[0])
        except ValueError:
            continue
        if line_pid in wanted:
            names[line_pid] = parts[1]
    return names


def _kill_pids(pids):
    """Best-effort SIGKILL of each PID in pids that's still a Chrome process.

    Guards against PID reuse: by the time teardown gets around to this call
    the original Chrome process usually already exited on its own (the
    common case -- quit() worked), and an OS could in principle have handed
    that same PID number to an unrelated process in the meantime. Checking
    the command name first means we only ever SIGKILL something that still
    looks like Chrome.
    """
    names = _command_names(pids)
    for target_pid in pids:
        if "chrome" not in names.get(target_pid, "").lower():
            continue
        try:
            os.kill(target_pid, signal.SIGKILL)
        except OSError:
            pass


def _is_headless(config):
    """Headless if --headless is passed or HEADLESS env is truthy."""
    if config.getoption("--headless", default=False):
        return True
    return os.getenv("HEADLESS", "").strip().lower() in ("1", "true", "yes")


def browser_scope(fixture_name, config):
    """Decide how often a browser is created.

    Always uses function scope (one browser per test) so that a Chrome crash
    in one test never cascades to the rest of the suite.  Pass --single-window
    to opt into session scope when you explicitly want one shared window.
    """
    if config.getoption("--single-window", default=False):
        return "session"

    return "function"


@pytest.fixture(scope=browser_scope)
def browser(request):

    headless = _is_headless(request.config)

    driver = DriverFactory.get_driver(
        headless=headless,
        detach=False,
    )
    driver.set_page_load_timeout(60)

    # Expose the driver to the failure hook even when the test only requests
    # a page fixture that depends on `browser` (item.funcargs misses those).
    request.node._browser_driver = driver

    # Snapshot the Chrome process(es) chromedriver has just spawned, while
    # the parent/child link is guaranteed intact -- if chromedriver later
    # has to be SIGKILLed (see teardown below), it gets no chance to close
    # this Chrome process itself, and if we tried to rediscover it *after*
    # the fact via the process tree, an already-orphaned child may have
    # been reparented (its ppid no longer points at chromedriver) and
    # become unfindable that way. Recording the actual PIDs now means
    # teardown can kill them directly regardless of chromedriver's fate.
    service_process = getattr(getattr(driver, "service", None), "process", None)
    chrome_pids = _descendant_pids(service_process.pid) if service_process else []

    yield driver

    # Navigate away before quitting so Chrome doesn't hang on a download
    # dialog or a frozen renderer.  Short page-load timeout prevents this
    # navigation from itself blocking if Chrome is already unresponsive.
    try:
        driver.set_page_load_timeout(5)
        driver.get("about:blank")
    except Exception:  # noqa: BLE001
        pass

    try:
        driver.quit()
    except Exception:  # noqa: BLE001
        pass

    # Belt-and-braces: quit() above (and _fast_terminate_process, patched in
    # on the Service class) normally leave nothing behind. If the chromedriver
    # process is somehow still alive after both -- e.g. it was too starved to
    # respond before escalating straight to SIGKILL -- explicitly kill it,
    # rather than trusting implicit garbage collection to get to it
    # eventually. No-ops (service_process is already gone) whenever the
    # existing cleanup already worked, which is every run on GitHub Actions
    # and the overwhelming majority of runs everywhere else.
    if service_process is not None:
        try:
            still_running = service_process.poll() is None
        except Exception:  # noqa: BLE001
            still_running = False
        if still_running:
            try:
                service_process.kill()
            except Exception:  # noqa: BLE001
                pass

    # Kill the Chrome process(es) snapshotted above unconditionally, whether
    # or not chromedriver itself needed killing: quit() (and the above
    # fallback) only guarantee chromedriver's own process dies, not the
    # Chrome process it spawned -- that gap is exactly what let orphaned
    # Chrome processes accumulate across a run and progressively starve a
    # resource-constrained host (confirmed reproducing identically on the
    # AWS self-hosted runner on 2026-10-09, -17, -19 before this fix).
    _kill_pids(chrome_pids)
