import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Discounts"),
    allure.story("Future E2E"),
]

_FUTURE_SKIP = (
    "Future E2E: requires integration with a system not yet covered by this "
    "automation suite. Implement once the relevant page objects are available."
)


@allure.title("FUT-001 Category to future service config flow")
@pytest.mark.regression
@pytest.mark.skip(reason=_FUTURE_SKIP + " (Service Config)")
def test_future_category_to_service_config(browser):
    pass


@allure.title("FUT-002 Discount visible in POS")
@pytest.mark.regression
@pytest.mark.skip(reason=_FUTURE_SKIP + " (POS)")
def test_future_discount_visible_in_pos(browser):
    pass


@allure.title("FUT-003 Discount visible in Kiosk")
@pytest.mark.regression
@pytest.mark.skip(reason=_FUTURE_SKIP + " (Kiosk)")
def test_future_discount_visible_in_kiosk(browser):
    pass


@allure.title("FUT-004 Discount reflected in Reports")
@pytest.mark.regression
@pytest.mark.skip(reason=_FUTURE_SKIP + " (Reports)")
def test_future_discount_reflected_in_reports(browser):
    pass


@allure.title("FUT-005 Discount reflected in Dashboard")
@pytest.mark.regression
@pytest.mark.skip(reason=_FUTURE_SKIP + " (Dashboard)")
def test_future_discount_reflected_in_dashboard(browser):
    pass
