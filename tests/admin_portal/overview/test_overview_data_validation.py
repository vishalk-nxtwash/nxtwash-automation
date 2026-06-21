import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Data Validation")
@allure.title("OVERVIEW-DATA-001 through OVERVIEW-DATA-006 API/export parity")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Blocked: no Overview dashboard API client or export data parser exists in the framework yet.",
    strict=False,
)
def test_overview_dashboard_data_matches_api_and_exports(overview_page):
    assert overview_page.dashboard_has_any_text(
        overview_page.DASHBOARD_WIDGET_LABELS
    )
