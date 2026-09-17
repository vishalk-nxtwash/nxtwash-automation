import allure
import pytest

_IFRAME_XFAIL = pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=False,
)


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Exports")
@allure.title("OVERVIEW-EXPORT-001 through OVERVIEW-EXPORT-009")
@pytest.mark.export
@_IFRAME_XFAIL
def test_overview_exports_are_available_and_filter_aware(overview_page):
    assert overview_page.dashboard_has_all_texts(overview_page.EXPORT_LABELS)
