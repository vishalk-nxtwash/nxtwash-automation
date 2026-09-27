import copy
import os
import shutil
import socket
import tempfile
import time

from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from core.network_capture import chrome_logging_capabilities

# Set a 60-second default socket timeout so ChromeDriver HTTP requests don't
# block indefinitely when Chrome freezes.  Without this, a frozen Chrome
# prevents both thread-based and signal-based pytest timeouts from firing.
socket.setdefaulttimeout(60)

# Pinned path for the ChromeDriver binary that matches Chrome 153.0.8010.x.
# CI can override with CHROMEDRIVER_PATH env var pointing to the system binary.
_PINNED_CHROMEDRIVER = os.environ.get(
    "CHROMEDRIVER_PATH",
    os.path.expanduser(
        "~/.wdm/drivers/chromedriver/mac64/"
        "153.0.8010.52/chromedriver-mac-arm64/chromedriver"
    ),
)


class DriverFactory:

    # Resolve the chromedriver binary once per process and reuse the path.
    # With a function-scoped browser fixture this otherwise runs a version
    # check / download on every single test; cache it so each xdist worker
    # pays the cost at most once.
    _driver_path = None

    @classmethod
    def _chromedriver_path(cls):
        if cls._driver_path is None:
            if os.path.isfile(_PINNED_CHROMEDRIVER):
                cls._driver_path = _PINNED_CHROMEDRIVER
            else:
                cls._driver_path = ChromeDriverManager().install()
        return cls._driver_path

    @classmethod
    def get_driver(cls, headless=False, detach=True):

        options = webdriver.ChromeOptions()

        if headless:
            # Headless flags suited for CI / servers without a display.
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-background-timer-throttling")
            options.add_argument("--disable-renderer-backgrounding")
            options.add_argument("--disable-backgrounding-occluded-windows")
            options.add_argument("--disable-ipc-flooding-protection")
            options.add_argument("--disable-hang-monitor")
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-translate")
            options.add_argument("--metrics-recording-only")
            options.add_argument("--mute-audio")
            options.add_argument("--no-first-run")
            options.add_argument("--safebrowsing-disable-auto-update")
        elif detach:
            # Keep the browser open after script execution (local debugging).
            options.add_experimental_option("detach", True)

        chrome_logging_capabilities(options)

        # Explicit profile dir under tempfile.gettempdir() (honours TMPDIR on
        # every OS; Chrome's own default ignores it on macOS). CI points TMPDIR
        # at a per-job directory so cleanup can target this job's browsers
        # only, on hosts shared by several runners.
        # Chrome occasionally fails to launch under load ("session not
        # created: chrome not reachable") — retry once with a fresh profile.
        for attempt in range(2):
            profile_dir = tempfile.mkdtemp(prefix="nxtwash-chrome-")
            launch_options = copy.deepcopy(options)
            launch_options.add_argument("--user-data-dir=%s" % profile_dir)
            try:
                driver = webdriver.Chrome(
                    service=Service(cls._chromedriver_path()),
                    options=launch_options
                )
                break
            except SessionNotCreatedException:
                shutil.rmtree(profile_dir, ignore_errors=True)
                if attempt == 1:
                    raise
                time.sleep(2)

        original_quit = driver.quit

        def _quit_and_remove_profile():
            try:
                original_quit()
            finally:
                shutil.rmtree(profile_dir, ignore_errors=True)

        driver.quit = _quit_and_remove_profile

        if not headless:
            driver.maximize_window()

        return driver
