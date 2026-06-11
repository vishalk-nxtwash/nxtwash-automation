import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Reports")
@allure.title("OVERVIEW-REPORT-001 through OVERVIEW-REPORT-008")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty; report links are unavailable.",
    strict=True,
)
def test_overview_full_report_links_are_available(overview_page):
    assert overview_page.dashboard_has_any_text(
        overview_page.FULL_REPORT_LABELS
    )
