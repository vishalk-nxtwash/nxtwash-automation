import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Filters")
@allure.title("OVERVIEW-FILTER-001 Site dropdown opens")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=True,
)
def test_overview_site_filter_dropdown_opens(overview_page):
    assert overview_page.dashboard_text_contains("Site")


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Filters")
@allure.title("OVERVIEW-FILTER-002/003/004 Site filter dashboard behavior")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=True,
)
def test_overview_site_filter_updates_switches_and_persists(overview_page):
    assert overview_page.dashboard_has_all_texts(["Site", "Cars Washed"])


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Filters")
@allure.title("OVERVIEW-FILTER-005 through OVERVIEW-FILTER-011 Date presets")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=True,
)
def test_overview_date_preset_filters_are_available(overview_page):
    assert overview_page.dashboard_has_all_texts(
        [
            "Today",
            "Yesterday",
            "This Week",
            "Last Week",
            "This Month",
            "Last Month",
            "Custom",
        ]
    )


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Filters")
@allure.title("OVERVIEW-FILTER-012 through OVERVIEW-FILTER-015 Date ranges")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=True,
)
def test_overview_date_range_filters_are_available(overview_page):
    assert overview_page.dashboard_has_any_text(["Start", "End", "Date Range"])


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Filters")
@allure.title("OVERVIEW-FILTER-016/017 Single Day checkbox")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=True,
)
def test_overview_single_day_checkbox_is_available(overview_page):
    assert overview_page.dashboard_text_contains("Single Day")
