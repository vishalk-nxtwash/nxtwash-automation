import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("UI")
@allure.title("OVERVIEW-UI-001/002 Overview shell redirects and loads")
@pytest.mark.smoke
@pytest.mark.prod_smoke
def test_overview_shell_redirects_and_loads(overview_page):
    assert overview_page.has_expected_url()
    assert not overview_page.is_redirected_to_login()
    assert overview_page.get_overview_text() == "Overview"
    assert overview_page.shell_has_content()
    assert overview_page.legacy_dashboard_iframe_is_present()
    assert not overview_page.has_broken_state_text()


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("UI")
@allure.title("OVERVIEW-UI-013 Support button visible")
@pytest.mark.sanity
@pytest.mark.xfail(
    reason="Third-party support widget does not load in headless mode or on staging.",
    strict=False,
)
def test_overview_support_button_is_visible(overview_page):
    assert overview_page.support_button_is_visible()


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("UI")
@allure.title("OVERVIEW-UI-003 Dashboard filter controls visible")
@pytest.mark.sanity
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=False,
)
def test_overview_dashboard_filter_controls_visible(overview_page):
    assert overview_page.dashboard_has_all_texts(
        ["Site", "Date", "Single Day"]
    )


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("UI")
@allure.title("OVERVIEW-UI-004/005 Export buttons visible")
@pytest.mark.export
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=False,
)
def test_overview_export_buttons_visible(overview_page):
    assert overview_page.dashboard_has_all_texts(overview_page.EXPORT_LABELS)


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("UI")
@allure.title("OVERVIEW-UI-006 through OVERVIEW-UI-012 dashboard widgets visible")
@pytest.mark.sanity
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=False,
)
def test_overview_dashboard_widgets_visible(overview_page):
    assert overview_page.dashboard_has_all_texts(
        overview_page.DASHBOARD_WIDGET_LABELS
    )
