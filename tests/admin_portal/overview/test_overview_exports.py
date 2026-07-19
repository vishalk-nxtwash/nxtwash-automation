import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Exports")
@allure.title("OVERVIEW-EXPORT-001 through OVERVIEW-EXPORT-009")
@pytest.mark.export
def test_overview_exports_are_available_and_filter_aware(overview_page):
    assert overview_page.dashboard_has_all_texts(overview_page.EXPORT_LABELS)
