import pytest

from core.driver_factory import DriverFactory


@pytest.fixture
def browser(request):

    driver = DriverFactory.get_driver()

    yield driver

    if request.config.getoption("--close-browser"):
        driver.quit()


# Bydefault broser will close, to keep it open we need to pass this flag in terminal(--keep-browser-open)
"""
import pytest

from core.driver_factory import DriverFactory


@pytest.fixture
def browser(request):

    driver = DriverFactory.get_driver()

    yield driver

    if not request.config.getoption("--keep-browser-open"):
        driver.quit()
"""