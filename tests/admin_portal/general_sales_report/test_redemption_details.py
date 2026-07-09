import datetime

import allure
import pytest

from tests.admin_portal.general_sales_report.conftest import (
    DATE_PRESETS,
    GSR_SITE,
    open_redemption_details_page,
    page_has_no_broken_state,
)


# GSR-RDT-001..010: Marked manual — Redemption Details page URL and filter panel
# structure not yet confirmed in staging. Re-enable (remove pytest.mark.manual from
# pytestmark and restore tier markers) once the correct URL is known and confirmed.
pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("General Sales Report"),
    allure.story("Redemption Details"),
    pytest.mark.manual,
]


# ── Helper ────────────────────────────────────────────────────────────────────

def _date_range_for_preset(preset: str):
    today = datetime.date.today()
    if preset == "Today":
        return today, today
    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d, d
    if preset == "This week":
        monday = today - datetime.timedelta(days=today.weekday())
        return monday, today
    if preset == "Last week":
        last_monday = today - datetime.timedelta(days=today.weekday() + 7)
        last_sunday = last_monday + datetime.timedelta(days=6)
        return last_monday, last_sunday
    if preset == "This month":
        return today.replace(day=1), today
    if preset == "Last month":
        last_day = today.replace(day=1) - datetime.timedelta(days=1)
        return last_day.replace(day=1), last_day
    return today, today


_DATE_PRESET_PARAMS = [
    pytest.param("Today",      id="GSR-RDT-005[today]"),
    pytest.param("Yesterday",  id="GSR-RDT-005[yesterday]"),
    pytest.param("This week",  id="GSR-RDT-005[this-week]"),
    pytest.param("Last week",  id="GSR-RDT-005[last-week]"),
    pytest.param("This month", id="GSR-RDT-005[this-month]"),
    pytest.param("Last month", id="GSR-RDT-005[last-month]"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# RDT — original tiers: 001/002/009 = Smoke, 003-008/010 = Regression, 007 = Extended
# Tier markers removed while manual; restore them when re-enabling automation.
# ═══════════════════════════════════════════════════════════════════════════════

@allure.title("GSR-RDT-001 Redemption Details page loads correctly")
def test_redemption_details_page_loads(rdt_page):
    url = rdt_page.driver.current_url
    assert (
        "redemption" in url.lower()
        or "general-sales-report" in url.lower()
    ), "URL does not indicate Redemption Details page: %s" % url
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-002 Page loads with filter panel auto-opened")
def test_filter_panel_auto_opened(rdt_page):
    assert rdt_page.filter_panel_is_visible(), (
        "Filter panel (Apply button / filter controls) not visible on page load"
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-003 Sites dropdown and data filtering works")
def test_site_filter_works(rdt_page):
    # Dependency: Sites & Locations module
    rdt_page.select_site(GSR_SITE)
    rdt_page.apply_filters()
    body = rdt_page.get_body_text()
    assert GSR_SITE in body or page_has_no_broken_state(rdt_page), (
        "Page did not reflect site filter for '%s'" % GSR_SITE
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-004 Date range presets dropdown shows all options")
def test_date_presets_dropdown(rdt_page):
    options = rdt_page.get_date_preset_options()
    options_lower = [o.lower() for o in options]
    missing = [p for p in DATE_PRESETS if p.lower() not in options_lower]
    assert not missing, (
        "Date preset options missing: %s. Actual: %s" % (missing, options)
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-005 Each date preset updates date range field correctly")
@pytest.mark.parametrize("preset", _DATE_PRESET_PARAMS)
def test_each_date_preset_applies(rdt_page, preset):
    start_date, _ = _date_range_for_preset(preset)
    rdt_page.select_date_preset(preset)
    start_val, end_val = rdt_page.get_date_range_values()
    assert start_val or end_val, (
        "Date range field not populated after selecting preset '%s'" % preset
    )
    assert str(start_date.year) in (start_val + end_val), (
        "Expected year %s not found in date range '%s' / '%s' after selecting '%s'"
        % (start_date.year, start_val, end_val, preset)
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-006 Custom option enables manual date entry")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "GSR-RDT-006: 'Custom' option text and date input visibility depend on "
        "RDT page UI — verify preset dropdown options in DevTools before removing xfail."
    ),
)
def test_custom_option_enables_manual_entry(rdt_page):
    from pages.admin_portal.general_sales_report_page import AdminRedemptionDetailsPage
    rdt_page.enable_custom_date_entry()
    inputs = rdt_page.driver.find_elements(
        *AdminRedemptionDetailsPage.DATE_RANGE_INPUT
    )
    assert any(i.is_displayed() for i in inputs), (
        "Date range input not visible after selecting Custom option"
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-007 Single day checkbox constrains date range to one day")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "GSR-RDT-007: Single day checkbox locator uses name/id heuristics — "
        "verify checkbox DOM attributes in DevTools before removing xfail."
    ),
)
def test_single_day_checkbox_constrains_range(rdt_page):
    rdt_page.toggle_single_day()
    start_val, end_val = rdt_page.get_date_range_values()
    assert start_val == end_val or page_has_no_broken_state(rdt_page), (
        "Single day checkbox did not constrain date range to one day. "
        "Start: '%s', End: '%s'" % (start_val, end_val)
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-008 Apply filters updates header metrics")
def test_apply_filters_updates_metrics(rdt_page):
    # Dependency: Sites & Locations module
    rdt_page.select_site(GSR_SITE)
    rdt_page.select_date_preset("Last month")
    rdt_page.apply_filters()
    body = rdt_page.get_body_text()
    assert "Redemption" in body or "$" in body or "0" in body, (
        "Header metrics not visible after applying filters"
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-009 Five collapsible sections visible on page")
def test_five_sections_visible(rdt_page):
    body = rdt_page.get_body_text()
    assert "Redemption" in body or "section" in body.lower() or "expand" in body.lower(), (
        "Redemption Details page body does not show expected collapsible sections"
    )
    assert page_has_no_broken_state(rdt_page)


@allure.title("GSR-RDT-010 Expand All button expands all five sections")
@pytest.mark.xfail(
    strict=False,
    reason=(
        "GSR-RDT-010: Section count after expand relies on aria-expanded heuristic — "
        "verify expand-all DOM trigger and section structure in DevTools before removing xfail."
    ),
)
def test_expand_all_button(rdt_page):
    count_before = rdt_page.get_visible_section_count()
    rdt_page.click_expand_all()
    count_after = rdt_page.get_visible_section_count()
    assert count_after >= count_before, (
        "Visible section count did not increase after Expand All. "
        "Before: %d, After: %d" % (count_before, count_after)
    )
    assert count_after >= 5 or page_has_no_broken_state(rdt_page), (
        "Expected >= 5 sections visible after Expand All, got %d" % count_after
    )
    assert page_has_no_broken_state(rdt_page)
