import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Navigation")
@allure.title("OVERVIEW-NAV-002 Browser back returns to Overview")
@pytest.mark.regression
def test_overview_browser_back_returns_to_overview(overview_page):
    overview_page.driver.get("https://staging.nxtwash.com/sites")
    overview_page.driver.back()
    overview_page.wait_for_loaded()

    assert overview_page.has_expected_url()
    assert overview_page.shell_has_content()
    assert not overview_page.has_broken_state_text()


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Navigation")
@allure.title("OVERVIEW-NAV-004 Overview opens in new tab")
@pytest.mark.regression
def test_overview_opens_in_new_tab(overview_page):
    overview_page.open_overview_in_new_tab()
    overview_page.wait_for_loaded()

    assert overview_page.has_expected_url()
    assert overview_page.shell_has_content()
    assert not overview_page.has_broken_state_text()


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Navigation")
@allure.title("OVERVIEW-NAV-001/003 Report navigation")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty; report links are unavailable.",
    strict=True,
)
def test_overview_report_navigation_is_available(overview_page):
    assert overview_page.dashboard_has_any_text(
        overview_page.FULL_REPORT_LABELS
    )
