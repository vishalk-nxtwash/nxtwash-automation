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


def _kill_process_tree(pid):
    """Best-effort SIGKILL of a process and all its descendants.

    quit()/_fast_terminate_process() reliably end the chromedriver process
    itself, but SIGKILL gives chromedriver no chance to shut down the Chrome
    process it spawned as its own child -- on a resource-starved host, that
    orphans Chrome instead of closing it, and the leaked process compounds
    the starvation for whichever test runs next. Walking the tree with `ps`
    (no new dependency, POSIX-only -- every runner here is Linux or macOS)
    and killing every descendant directly removes that gap.
    """
    try:
        listing = subprocess.run(
            ["ps", "-eo", "pid,ppid"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:  # noqa: BLE001
        return

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

    for descendant_pid in descendants:
        try:
            os.kill(descendant_pid, signal.SIGKILL)
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
    # respond before escalating straight to SIGKILL -- explicitly kill it and
    # any Chrome process it spawned, rather than trusting implicit garbage
    # collection to get to it eventually. No-ops (service_process is already
    # gone) whenever the existing cleanup already worked, which is every run
    # on GitHub Actions and the overwhelming majority of runs everywhere else.
    service = getattr(driver, "service", None)
    service_process = getattr(service, "process", None)
    if service_process is not None:
        try:
            still_running = service_process.poll() is None
        except Exception:  # noqa: BLE001
            still_running = False
        if still_running:
            _kill_process_tree(service_process.pid)
            try:
                service_process.kill()
            except Exception:  # noqa: BLE001
                pass
