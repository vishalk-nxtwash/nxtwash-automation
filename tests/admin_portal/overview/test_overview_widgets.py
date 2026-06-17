import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Widgets")
@allure.title("OVERVIEW-WIDGET-001 through OVERVIEW-WIDGET-021")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty; widgets are unavailable.",
    strict=True,
)
def test_overview_widgets_and_metrics_render(overview_page):
    assert overview_page.dashboard_has_all_texts(
        overview_page.DASHBOARD_WIDGET_LABELS
    )
    assert overview_page.dashboard_has_any_text(
        [
            "Total",
            "Avg Daily",
            "Avg Hourly",
            "Active",
            "Sales",
            "Cancellations",
            "Employee",
            "Commission",
            "Total Labor",
        ]
    )
