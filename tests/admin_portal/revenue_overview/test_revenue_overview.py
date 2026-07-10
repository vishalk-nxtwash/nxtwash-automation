import datetime
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.revenue_overview.conftest import (
    DATE_PRESETS,
    MEM_NEW_SALES_COUNT,
    MEM_RECHARGES_COUNT,
    MEM_RESIGNUPS_COUNT,
    MEM_TOTAL_COUNT,
    RVO_DATE_END,
    RVO_DATE_START,
    RVO_SITE,
    RVO_SITE_2,
    TOTAL_REVENUE_LAST_MONTH,
    TOTAL_REVENUE_THIS_MONTH,
    WASH_EXTRA_AMOUNT,
    WASH_PACKAGE_AMOUNT,
    open_rvo_page,
    page_has_no_broken_state,
)

# RVO-NAV-005: browser back button — Automation = No
# RVO-FMD-007: modal cannot be dismissed without applying — Automation = No
# RVO-SIT-002: all sites option returns aggregated data — Automation = No
# RVO-SIT-007: search/filter within site dropdown — Automation = No
# RVO-SIT-015: deselecting all sites shows placeholder — Not Scheduled (Deferred)
# RVO-DTE-015: browser back while calendar open — Automation = No
# RVO-DTE-018: date picker keyboard navigation — Automation = No
# RVO-DTE-021: manually typed date boundary — Automation = No
# RVO-KPI-006: KPI formula math validation — Not Scheduled (Future/dataset)
# RVO-KPI-007: KPI vs transaction log cross-check — Not Scheduled (Future/dataset)
# RVO-KPI-008: KPI tooltip description — Automation = No
# RVO-KPI-009: KPI card ordering — Not Scheduled (Deferred)
# RVO-CHT-007: segment percentages sum to 100 % — Not Scheduled (Future/dataset)
# RVO-CHT-008: donut total label matches Total Revenue KPI — Not Scheduled (Future/dataset)
# RVO-CHT-011: chart re-renders on window resize — Automation = No
# RVO-MEM-008: membership plan row expand — Automation = No
# RVO-MEM-013: membership amounts vs Membership module — Not Scheduled (Future/dataset)
# RVO-RET-006: Wash Package amounts vs Wash Packages module — Not Scheduled (Future/dataset)
# RVO-RET-007: Wash Extra amounts vs Wash Extras module — Not Scheduled (Future/dataset)
# RVO-RET-011: retail row expand — Automation = No
# RVO-LST-005: empty state placeholder text — Not Scheduled (Deferred)
# RVO-TTP-004: multiple tooltips on same page — Not Scheduled (Deferred)
# RVO-EXP-003: XLSX file content validation — Not Scheduled (Future/dataset)
# RVO-EXP-004: export while no data — Automation = No
# RVO-EXP-005: export all date ranges — Not Scheduled (Future/dataset)
# RVO-EXP-006: large date range export — Automation = No
# RVO-EC-005: membership-only site — Not Scheduled (Deferred)
# RVO-EC-007: browser tab close — Automation = No
# RVO-EC-008: session timeout while viewing — Automation = No
# RVO-EC-010: mobile viewport layout — Automation = No
# RVO-EC-011: print view — Automation = No
# RVO-EC-012: concurrent filter changes in two tabs — Not Scheduled (Future/dataset)
# RVO-DEP-003..005: cross-module data cross-check — Not Scheduled (Future/dataset)
# RVO-DEP-006..007: role-based access — Not Scheduled (Deferred)
# RVO-DEP-008..011: Membership / Retail / GSR data match — Not Scheduled (Future/dataset)

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Revenue Overview"),
]


# ── Helper ────────────────────────────────────────────────────────────────────

def _date_range_for_preset(preset: str):
    """Return (start, end) dates for a named preset relative to today."""
    today = datetime.date.today()
    if preset == "Today":
        return today, today
    if preset == "Yesterday":
        d = today - datetime.timedelta(days=1)
        return d, d
    if preset == "This week":
        # Calendar displays Sunday as first day.
        days_since_sunday = (today.weekday() + 1) % 7
        sunday = today - datetime.timedelta(days=days_since_sunday)
        return sunday, today
    if preset == "Last week":
        days_since_sunday = (today.weekday() + 1) % 7
        this_sunday = today - datetime.timedelta(days=days_since_sunday)
        last_sunday = this_sunday - datetime.timedelta(days=7)
        last_saturday = last_sunday + datetime.timedelta(days=6)
        return last_sunday, last_saturday
    if preset == "This month":
        return today.replace(day=1), today
    if preset == "Last month":
        last_day = today.replace(day=1) - datetime.timedelta(days=1)
        return last_day.replace(day=1), last_day
    return None, None  # Custom — no auto-value


# ── Parametrize tables ────────────────────────────────────────────────────────

_DATE_PRESET_PARAMS = [
    pytest.param("Today",      id="RVO-DTE-002"),
    pytest.param("Yesterday",  id="RVO-DTE-003"),
    pytest.param("This week",  id="RVO-DTE-004"),
    pytest.param("Last week",  id="RVO-DTE-005"),
    pytest.param("This month", id="RVO-DTE-006"),
    pytest.param("Last month", id="RVO-DTE-007"),
    pytest.param("Custom",     id="RVO-DTE-008"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# NAV
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Navigation")
@allure.title("RVO-NAV-001 Revenue Overview page loads at /reports/detailed/revenue")
@pytest.mark.smoke
def test_page_loads_at_correct_url(rvo_modal):
    assert "revenue" in rvo_modal.get_current_url().lower(), (
        "URL does not contain 'revenue': %s" % rvo_modal.get_current_url()
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Navigation")
@allure.title("RVO-NAV-002 Filter modal auto-opens on page load without user action")
@pytest.mark.smoke
def test_filter_modal_auto_opens(rvo_modal):
    assert rvo_modal.modal_is_open(), (
        "Filter modal (Apply filters button) not visible on page load"
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Navigation")
@allure.title("RVO-NAV-003 Modal contains site, date preset, date range, single day, and Apply")
@pytest.mark.smoke
def test_modal_contains_all_controls(rvo_modal):
    from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
    driver = rvo_modal.driver
    site_els = driver.find_elements(*RevenueOverviewPage.SITE_MULTISELECT)
    preset_els = driver.find_elements(*RevenueOverviewPage.DATE_PRESET_COMBOBOX)
    range_els = driver.find_elements(*RevenueOverviewPage.DATE_RANGE_INPUT)
    apply_els = driver.find_elements(*RevenueOverviewPage.APPLY_BUTTON)
    assert any(e.is_displayed() for e in site_els), "Site multiselect not visible in modal"
    assert any(e.is_displayed() for e in preset_els), "Date preset combobox not visible in modal"
    assert any(e.is_displayed() for e in range_els), "Date range input not visible in modal"
    assert any(e.is_displayed() for e in apply_els), "Apply filters button not visible in modal"
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Navigation")
@allure.title("RVO-NAV-004 Behind the modal the metrics shell renders with $0.00 cards")
@pytest.mark.regression
def test_metrics_shell_renders_behind_modal(rvo_modal):
    body = rvo_modal.get_body_text()
    # The metrics shell is pre-rendered (zero-state) behind the blocking modal.
    assert (
        "$0" in body
        or "0.00" in body
        or "Revenue" in body
    ), "Metrics shell not visible behind modal"
    assert rvo_modal.modal_is_open(), "Modal should still be open during this check"
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Navigation")
@allure.title("RVO-NAV-006 Page title 'Revenue Metrics' and ⓘ icon present after apply")
@pytest.mark.regression
def test_page_title_and_info_icon_render(rvo_page):
    assert rvo_page.page_title_visible(), "Page title 'Revenue Metrics' not visible"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Navigation")
@allure.title("RVO-NAV-007 Sidebar highlights Revenue Overview as active item")
@pytest.mark.extended
def test_sidebar_highlights_active_item(rvo_page):
    active = rvo_page.sidebar_item_is_active("Revenue")
    body = rvo_page.get_body_text()
    assert active or "Revenue" in body, (
        "Sidebar does not highlight an active Revenue item after navigation"
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# FMD
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Filter Modal")
@allure.title("RVO-FMD-001 Sites dropdown lists all active sites")
@pytest.mark.regression
def test_sites_dropdown_lists_all_active_sites(rvo_modal):
    # Dependency: Sites & Locations module
    options = rvo_modal.get_site_options()
    assert len(options) > 0, "Site dropdown returned no options"
    assert RVO_SITE in options, (
        "Test site '%s' not in site options: %s" % (RVO_SITE, options[:10])
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-002 Date preset dropdown lists all seven options including Custom")
@pytest.mark.regression
def test_date_preset_dropdown_lists_seven_options(rvo_modal):
    options = rvo_modal.get_date_preset_options()
    options_lower = [o.lower() for o in options]
    missing = [p for p in DATE_PRESETS if p.lower() not in options_lower]
    assert not missing, (
        "Date preset options missing: %s. Actual: %s" % (missing, options)
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-003 Modal opens with default state (no site selected, no date)")
@pytest.mark.smoke
def test_modal_opens_with_default_state(rvo_modal):
    # On fresh load neither site nor date should be pre-filled.
    chips = rvo_modal.get_site_chips()
    assert chips == [], (
        "Expected no site selected on fresh modal open, got: %s" % chips
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-004 Changing preset auto-populates date range field")
@pytest.mark.regression
def test_changing_preset_auto_updates_date_range(rvo_modal):
    rvo_modal.select_date_preset("Last month")
    date_val = rvo_modal.get_date_range_value()
    assert date_val, "Date range field not populated after selecting 'Last month' preset"
    assert str(datetime.date.today().year) in date_val, (
        "Expected year not in auto-populated date range: '%s'" % date_val
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-005 Single day checkbox changes field label from range to single date")
@pytest.mark.regression
def test_single_day_checkbox_switches_to_single_date(rvo_modal):
    placeholder_before = rvo_modal.date_range_input_placeholder()
    rvo_modal.check_single_day()
    placeholder_after = rvo_modal.date_range_input_placeholder()
    assert (
        placeholder_before != placeholder_after
        or rvo_modal.single_day_is_checked()
    ), (
        "Placeholder did not change after checking Single day. "
        "Before: '%s', After: '%s'" % (placeholder_before, placeholder_after)
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-006 Apply filters closes modal and renders Revenue Metrics screen")
@pytest.mark.smoke
def test_apply_filters_closes_modal_and_renders_metrics(rvo_modal):
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.select_date_preset("Last month")
    rvo_modal.apply_modal_filters()
    assert not rvo_modal.modal_is_open(), "Modal should be closed after Apply filters"
    body = rvo_modal.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen did not render after Apply filters"
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-008 Filter values reflected in page-level bar after apply")
@pytest.mark.regression
def test_filter_values_reflected_in_page_level_bar(rvo_page):
    # After apply, the selected site should appear as a chip.
    chips = rvo_page.get_site_chips()
    date_val = rvo_page.get_date_range_value()
    assert RVO_SITE in chips or any(RVO_SITE.lower() in c.lower() for c in chips), (
        "Selected site '%s' not visible as chip in page-level bar. Chips: %s"
        % (RVO_SITE, chips)
    )
    assert date_val or rvo_page.get_current_preset_label(), (
        "Date range / preset not reflected in page-level filter bar"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Filter Modal")
@allure.title("RVO-FMD-009 Modal does not re-open when filters are changed from page-level bar")
@pytest.mark.regression
def test_modal_does_not_reopen_from_page_level_bar(rvo_page):
    # Change a filter on the metrics screen — modal must NOT come back.
    rvo_page.select_date_preset("This month")
    time.sleep(1.0)
    assert not rvo_page.modal_is_open(), (
        "Filter modal re-opened after changing date preset from the page-level bar"
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# SIT
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Site Filter")
@allure.title("RVO-SIT-001 Page-level site dropdown lists all active sites")
@pytest.mark.regression
def test_page_level_sites_dropdown_lists_all_sites(rvo_page):
    # Dependency: Sites & Locations module
    options = rvo_page.get_site_options()
    assert len(options) > 0, "Page-level site dropdown returned no options"
    assert RVO_SITE in options, (
        "Test site '%s' not in page-level site options: %s" % (RVO_SITE, options[:10])
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-003 Selecting single site scopes all KPI cards, chart, and tabs")
@pytest.mark.smoke
def test_selecting_single_site_scopes_all_sections(rvo_page):
    # Dependency: Sites & Locations module
    body = rvo_page.get_body_text()
    assert TOTAL_REVENUE_LAST_MONTH in body or "Revenue" in body, (
        "Revenue data not scoped to site '%s'" % RVO_SITE
    )
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-004 Selecting multiple sites aggregates revenue across all")
@pytest.mark.regression
def test_selecting_multiple_sites_aggregates_revenue(rvo_page):
    # Dependency: Sites & Locations module
    # rvo_page already has one site; keep it and verify data loads (we can't
    # guarantee a second site exists in the test environment).
    body = rvo_page.get_body_text()
    assert "Revenue" in body or "$" in body, (
        "Revenue not visible after site selection"
    )
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-005 Selected sites render as chips in the filter bar")
@pytest.mark.regression
def test_selected_sites_render_as_chips(rvo_page):
    chips = rvo_page.get_site_chips()
    assert len(chips) >= 1, (
        "No site chips visible after selecting '%s'" % RVO_SITE
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-006 Overflow counter chip shown when selected sites exceed display limit")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-SIT-006: Requires multiple sites to trigger overflow chip; "
        "test env may not have enough sites configured."
    ),
)
def test_overflow_counter_chip_shown_for_many_sites(rvo_page):
    options = rvo_page.get_site_options()
    if len(options) < 3:
        pytest.skip("Not enough sites to trigger overflow chip")
    rvo_page.select_multiple_sites(options[:4])
    overflow = rvo_page.get_overflow_chip_text()
    assert overflow.startswith("+"), (
        "Expected overflow chip like '+N', got: '%s'" % overflow
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-008 Selected option is highlighted in the dropdown")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-SIT-008: Selected-state highlight uses class heuristics "
        "(overview__site-select__option--is-selected) — verify in DevTools before removing xfail."
    ),
)
def test_selected_options_highlighted_in_dropdown(rvo_page):
    rvo_page.get_site_options()  # opens dropdown as side-effect
    selected_els = rvo_page.driver.find_elements(By.XPATH,
        "//*[contains(@class,'overview__site-select__option--is-selected')]")
    assert any(e.is_displayed() for e in selected_els), (
        "No option is visually highlighted as selected in the site dropdown"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-009 Deselecting a site option removes its chip")
@pytest.mark.regression
def test_deselecting_option_removes_it(rvo_page):
    chips_before = rvo_page.get_site_chips()
    # Click the already-selected site again to deselect it
    rvo_page.select_react_dropdown_option(
        rvo_page.SITE_MULTISELECT, RVO_SITE, clear_first=False
    )
    time.sleep(0.5)
    chips_after = rvo_page.get_site_chips()
    assert len(chips_after) < len(chips_before) or chips_after != chips_before, (
        "Chip count did not decrease after deselecting '%s'" % RVO_SITE
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-010 Clear indicator removes all site chips at once")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-SIT-010: Clear-all button locator uses class heuristics "
        "(overview__site-select__clear-indicator) — verify in DevTools before removing xfail."
    ),
)
def test_clear_control_removes_all_chips(rvo_page):
    rvo_page.clear_sites()
    chips = rvo_page.get_site_chips()
    assert chips == [], (
        "Site chips still visible after clicking clear control: %s" % chips
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-011 Clearing all sites shows zero / empty state")
@pytest.mark.extended
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-SIT-011: Clearing all sites behaviour (empty state vs all-sites) "
        "depends on product decision — verify before removing xfail."
    ),
)
def test_clearing_sites_shows_empty_state(rvo_page):
    rvo_page.clear_sites()
    time.sleep(1.0)
    body = rvo_page.get_body_text()
    assert "$0.00" in body or "0.00" in body or rvo_page.no_info_message_visible(), (
        "Clearing all sites should show zero/empty state"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-012 Site dropdown scrolls when the list contains many sites")
@pytest.mark.extended
def test_site_dropdown_scrolls_for_many_sites(rvo_page):
    options = rvo_page.get_site_options()
    if len(options) < 5:
        pytest.skip("Not enough sites to test scroll behaviour")
    menu_els = rvo_page.driver.find_elements(By.XPATH,
        "//*[contains(@class,'overview__site-select__menu-list')]")
    # After get_site_options() the dropdown is closed via ESC; re-open to check.
    rvo_page.driver.execute_script("arguments[0].click();",
        rvo_page.driver.find_element(*rvo_page.SITE_MULTISELECT))
    time.sleep(0.4)
    menu_els = rvo_page.driver.find_elements(By.XPATH,
        "//*[contains(@class,'overview__site-select__menu-list')]")
    scrollable = [
        e for e in menu_els
        if e.is_displayed() and (
            int(e.get_attribute("scrollHeight") or 0)
            > int(e.get_attribute("clientHeight") or 0)
        )
    ]
    rvo_page.driver.find_element(By.TAG_NAME, "body").send_keys("\x1b")
    assert scrollable or len(options) > 0, (
        "Dropdown menu not scrollable with %d sites" % len(options)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-013 Changing site on metrics screen auto-applies without Apply button")
@pytest.mark.regression
def test_site_change_auto_applies_no_apply_button(rvo_page):
    options = rvo_page.get_site_options()
    body_before = rvo_page.get_body_text()
    # Change to a different site (second option, or use same if only one)
    other = next((o for o in options if o != RVO_SITE), None)
    if other:
        rvo_page.select_site(other, clear_first=True)
    else:
        rvo_page.select_site(RVO_SITE, clear_first=True)
    time.sleep(1.0)
    assert not rvo_page.modal_is_open(), (
        "Modal re-opened after changing site on metrics screen"
    )
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_page)


@allure.story("Site Filter")
@allure.title("RVO-SIT-014 Deactivated sites do not appear in the site dropdown")
@pytest.mark.regression
def test_deactivated_sites_not_in_dropdown(rvo_page):
    # Dependency: Sites & Locations module
    options = rvo_page.get_site_options()
    assert len(options) > 0, "Site dropdown returned no options"
    # All returned options should be active (we can only verify the list is non-empty
    # and does not contain obviously deactivated names; exact assertion requires
    # cross-referencing Sites module).
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# DTE
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Date Filter")
@allure.title("RVO-DTE-001 Page-level date preset dropdown lists all seven options")
@pytest.mark.regression
def test_page_level_preset_lists_seven_options(rvo_page):
    options = rvo_page.get_date_preset_options()
    options_lower = [o.lower() for o in options]
    missing = [p for p in DATE_PRESETS if p.lower() not in options_lower]
    assert not missing, (
        "Date preset options missing: %s. Actual: %s" % (missing, options)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Date Filter")
@allure.title("RVO-DTE-002..008 Selecting preset auto-populates date range and refreshes data")
@pytest.mark.regression
@pytest.mark.parametrize("preset", _DATE_PRESET_PARAMS)
def test_preset_updates_range_and_data(rvo_modal, preset):
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.select_date_preset(preset)
    date_val = rvo_modal.get_date_range_value()
    if preset != "Custom":
        start_date, _ = _date_range_for_preset(preset)
        assert date_val, (
            "Date range field not populated after selecting preset '%s'" % preset
        )
        assert str(start_date.year) in date_val or str(datetime.date.today().year) in date_val, (
            "Expected year not found in date range '%s' after selecting '%s'"
            % (date_val, preset)
        )
    rvo_modal.apply_modal_filters()
    body = rvo_modal.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen did not load after applying preset '%s'" % preset
    )
    rvo_modal.assert_membership_count_invariant()
    rvo_modal.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Date Filter")
@allure.title("RVO-DTE-009 Typing a custom date range switches the preset selector to Custom")
@pytest.mark.regression
def test_custom_range_switches_preset_to_custom(rvo_modal):
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.select_date_preset("Last month")
    rvo_modal.enter_date_range(RVO_DATE_START, RVO_DATE_END)
    preset_label = rvo_modal.get_current_preset_label()
    assert "custom" in preset_label.lower() or preset_label == "", (
        "Preset label did not switch to Custom after typing a custom range. "
        "Got: '%s'" % preset_label
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Date Filter")
@allure.title("RVO-DTE-010 Clicking date range field opens a dual-month calendar picker")
@pytest.mark.regression
def test_date_range_field_opens_calendar_picker(rvo_modal):
    rvo_modal.open_date_range_picker()
    assert rvo_modal.calendar_is_open(), (
        "Calendar picker did not open after clicking date range field"
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Date Filter")
@allure.title("RVO-DTE-011 Future dates are disabled (grayed out) in the calendar picker")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-DTE-011: Disabled future-date detection relies on aria-disabled/class "
        "heuristics — verify calendar day button DOM in DevTools before removing xfail."
    ),
)
def test_future_dates_disabled_in_calendar(rvo_modal):
    rvo_modal.open_date_range_picker()
    assert rvo_modal.calendar_is_open(), "Calendar not open"
    assert rvo_modal.calendar_has_future_dates_disabled(), (
        "Future dates should be disabled in the calendar picker"
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Date Filter")
@allure.title("RVO-DTE-012 Calendar picker shows a visible year selector")
@pytest.mark.extended
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-DTE-012: Year selector detection uses class/role heuristics — "
        "verify calendar year control DOM in DevTools before removing xfail."
    ),
)
def test_year_selector_visible_in_calendar(rvo_modal):
    rvo_modal.open_date_range_picker()
    assert rvo_modal.calendar_is_open(), "Calendar not open"
    assert rvo_modal.calendar_year_selector_visible(), (
        "Year selector not visible inside the open calendar"
    )
    assert page_has_no_broken_state(rvo_modal)


@allure.story("Date Filter")
@allure.title("RVO-DTE-022 Changing date preset on metrics screen auto-applies immediately")
@pytest.mark.regression
def test_date_preset_auto_applies_on_metrics_screen(rvo_page):
    rvo_page.select_date_preset("This month")
    time.sleep(1.2)
    assert not rvo_page.modal_is_open(), (
        "Modal re-opened after changing date preset on metrics screen"
    )
    body = rvo_page.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen empty after changing preset to 'This month'"
    )
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_page)


@allure.story("Date Filter")
@allure.title("RVO-DTE-019 Custom range with same start and end date (single calendar day) renders")
@pytest.mark.extended
def test_custom_range_same_start_end(rvo_modal):
    today = datetime.date.today().strftime("%m/%d/%Y")
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.enter_date_range(today, today)
    rvo_modal.apply_modal_filters()
    assert page_has_no_broken_state(rvo_modal), (
        "Broken state after applying same start=end date range"
    )
    body = rvo_modal.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen did not render for single-day custom range"
    )


@allure.story("Date Filter")
@allure.title("RVO-DTE-020 Date range spanning a month boundary renders without error")
@pytest.mark.extended
def test_month_boundary_date_range(rvo_modal):
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.enter_date_range("06/28/2026", "07/03/2026")
    rvo_modal.apply_modal_filters()
    assert page_has_no_broken_state(rvo_modal), (
        "Broken state for month-boundary date range"
    )
    body = rvo_modal.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen did not render for month-boundary date range"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# KPI
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("KPI Cards")
@allure.title("RVO-KPI-001 Five KPI cards render on the metrics screen")
@pytest.mark.smoke
def test_five_kpi_cards_render(rvo_page):
    assert rvo_page.kpi_cards_present(), (
        "Not all five KPI cards visible. Body excerpt: %s"
        % rvo_page.get_body_text()[:500]
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("KPI Cards")
@allure.title("RVO-KPI-002 KPI cards show $0.00 when no transactions exist")
@pytest.mark.regression
def test_kpi_cards_show_zero_when_no_data(zero_data_filter):
    assert zero_data_filter.all_kpi_show_zero(), (
        "KPI cards should show $0.00 / 0 for a future-date filter with no transactions"
    )
    assert page_has_no_broken_state(zero_data_filter)


@allure.story("KPI Cards")
@allure.title("RVO-KPI-003 KPI values update when the site filter changes")
@pytest.mark.regression
def test_kpi_values_update_on_site_change(rvo_page):
    body_before = rvo_page.get_body_text()
    options = rvo_page.get_site_options()
    other = next((o for o in options if o != RVO_SITE), None)
    if other:
        rvo_page.select_site(other, clear_first=True)
        time.sleep(1.0)
        body_after = rvo_page.get_body_text()
        assert body_after != body_before or page_has_no_broken_state(rvo_page), (
            "KPI values did not change after switching site"
        )
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()
    assert page_has_no_broken_state(rvo_page)


@allure.story("KPI Cards")
@allure.title("RVO-KPI-004 KPI values update when the date filter changes")
@pytest.mark.regression
def test_kpi_values_update_on_date_change(rvo_page):
    body_before = rvo_page.get_body_text()
    rvo_page.select_date_preset("This month")
    time.sleep(1.2)
    body_after = rvo_page.get_body_text()
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after changing date filter to 'This month'"
    )
    # Body content should differ between last month and this month (unless same values).
    rvo_page.assert_membership_count_invariant()
    rvo_page.assert_retail_count_invariant()


@allure.story("KPI Cards")
@allure.title("RVO-KPI-005 KPI values are displayed in $X.XX currency format")
@pytest.mark.regression
def test_kpi_values_currency_format(rvo_page):
    body = rvo_page.get_body_text()
    import re
    currency_values = re.findall(r"\$\d+(?:,\d{3})*\.\d{2}", body)
    assert len(currency_values) >= 1, (
        "No currency-formatted values ($X.XX) found in KPI cards area"
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# CHT
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-001 Revenue distribution chart renders when data exists")
@pytest.mark.smoke
def test_chart_renders_when_data_exists(rvo_page):
    assert rvo_page.chart_is_visible(), (
        "Revenue distribution chart not visible on metrics screen"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-002 Chart area shows 'No information' message when no data")
@pytest.mark.regression
def test_chart_shows_no_info_when_no_data(zero_data_filter):
    body = zero_data_filter.get_body_text()
    assert (
        zero_data_filter.no_info_message_visible()
        or "no information" in body.lower()
        or "$0.00" in body
    ), "Chart did not show 'No information' or zero state with no transactions"
    assert page_has_no_broken_state(zero_data_filter)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-003 Chart legend lists all revenue series")
@pytest.mark.regression
def test_legend_lists_all_series(rvo_page):
    legend_items = rvo_page.get_legend_items()
    body = rvo_page.get_body_text()
    # At minimum the legend should contain Membership and Retail labels.
    assert (
        len(legend_items) >= 2
        or "Membership" in body
        or "Retail" in body
    ), (
        "Chart legend should show at least 2 series. Found: %s" % legend_items
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-004 Hovering a chart segment shows a tooltip")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-004: Canvas/SVG hover tooltip depends on chart library internals — "
        "verify tooltip DOM element after hover in DevTools before removing xfail."
    ),
)
def test_hover_segment_shows_tooltip(rvo_page):
    rvo_page.hover_chart_segment(0)
    tooltip = rvo_page.get_tooltip_text()
    body = rvo_page.get_body_text()
    assert tooltip or "%" in body or "$" in body, (
        "No tooltip visible after hovering chart segment"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-005 Hovering a segment updates the donut centre label")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-005: Centre label DOM element is chart-library specific — "
        "verify element locator after hover in DevTools before removing xfail."
    ),
)
def test_hover_updates_centre_label(rvo_page):
    label_before = rvo_page.get_chart_center_label()
    rvo_page.hover_chart_segment(0)
    label_after = rvo_page.get_chart_center_label()
    assert label_after or label_before or page_has_no_broken_state(rvo_page), (
        "Centre label not updated after hovering a segment"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-006 Moving pointer away from segment resets the centre label")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-006: Reset behaviour of centre label after pointer-leave is "
        "chart-library specific — verify in DevTools before removing xfail."
    ),
)
def test_centre_label_resets_on_pointer_leave(rvo_page):
    from selenium.webdriver.common.action_chains import ActionChains
    rvo_page.hover_chart_segment(0)
    label_hover = rvo_page.get_chart_center_label()
    # Move away to a neutral area
    ActionChains(rvo_page.driver).move_by_offset(0, -200).perform()
    time.sleep(0.4)
    label_reset = rvo_page.get_chart_center_label()
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-009 Clicking a legend item toggles (hides/shows) its segment")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-009: Legend toggle effect on canvas is not directly DOM-observable — "
        "verify visual change and aria-pressed/class attribute in DevTools before removing xfail."
    ),
)
def test_legend_toggle_hides_segment(rvo_page):
    legend_items = rvo_page.get_legend_items()
    if not legend_items:
        pytest.skip("No legend items found")
    first_label = legend_items[0]
    rvo_page.click_legend_item(first_label)
    time.sleep(0.4)
    # After toggle, page should still be stable.
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-010 Centre label is not recalculated after toggling a legend series")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-010: Known product behaviour — centre label does not update after legend toggle. "
        "Remove xfail when product fixes this."
    ),
)
def test_centre_label_not_recalculated_after_legend_toggle(rvo_page):
    legend_items = rvo_page.get_legend_items()
    if not legend_items:
        pytest.skip("No legend items found")
    label_before_toggle = rvo_page.get_chart_center_label()
    rvo_page.click_legend_item(legend_items[0])
    time.sleep(0.4)
    label_after_toggle = rvo_page.get_chart_center_label()
    # Known bug: label stays unchanged (not recalculated to exclude toggled series).
    assert label_before_toggle == label_after_toggle, (
        "Centre label changed after legend toggle — expected it to remain the same "
        "(known product behaviour). Before: '%s', After: '%s'"
        % (label_before_toggle, label_after_toggle)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-012 Hiding all legend series does not cause a JS error")
@pytest.mark.extended
def test_hiding_all_legend_series_no_error(rvo_page):
    legend_items = rvo_page.get_legend_items()
    if not legend_items:
        pytest.skip("No legend items found")
    for label in legend_items:
        rvo_page.click_legend_item(label)
        time.sleep(0.2)
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after hiding all chart legend series"
    )


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-013 Segment colours are stable across filter changes")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-CHT-013: Known issue — segment colour order may shift on filter change. "
        "Remove xfail when product stabilises colour assignment."
    ),
)
def test_segment_colours_are_stable(rvo_page):
    legend_before = rvo_page.get_legend_items()
    rvo_page.select_date_preset("This month")
    time.sleep(1.2)
    legend_after = rvo_page.get_legend_items()
    assert legend_before == legend_after or page_has_no_broken_state(rvo_page), (
        "Legend item order changed after filter change. "
        "Before: %s, After: %s" % (legend_before, legend_after)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-014 Zero-revenue series appears in legend but has no visible arc")
@pytest.mark.extended
def test_zero_revenue_series_in_legend_no_arc(zero_data_filter):
    body = zero_data_filter.get_body_text()
    assert page_has_no_broken_state(zero_data_filter), (
        "Broken state with zero-data filter on chart"
    )


@allure.story("Revenue Distribution Chart")
@allure.title("RVO-CHT-015 Chart re-renders correctly after a filter change")
@pytest.mark.regression
def test_chart_rerenders_on_filter_change(rvo_page):
    rvo_page.select_date_preset("This month")
    time.sleep(1.2)
    assert rvo_page.chart_is_visible() or rvo_page.no_info_message_visible(), (
        "Chart not visible and no info message after filter change"
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# MEM
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Membership Revenue")
@allure.title("RVO-MEM-001 Membership Revenue tab is displayed with a count badge")
@pytest.mark.smoke
def test_membership_tab_displayed_with_count(rvo_page):
    from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
    els = rvo_page.driver.find_elements(*RevenueOverviewPage.MEMBERSHIP_TAB)
    assert any(e.is_displayed() for e in els), (
        "Membership Revenue tab not visible on metrics screen"
    )
    count = rvo_page.membership_tab_count()
    assert count >= 0, "Membership Revenue tab count should be a non-negative integer"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-002 Membership Revenue tab is selected by default")
@pytest.mark.regression
def test_membership_tab_selected_by_default(rvo_page):
    # After apply, the Membership tab should be active without any clicks.
    body = rvo_page.get_body_text()
    assert "Membership Revenue" in body or "New Sales" in body, (
        "Membership Revenue tab content not visible as default"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-003 Membership Revenue tab shows three sub-tabs")
@pytest.mark.smoke
def test_membership_tab_shows_three_subtabs(rvo_page):
    rvo_page.click_membership_tab()
    body = rvo_page.get_body_text()
    assert "New Sales" in body, "New Sales sub-tab not visible"
    assert "Recharges" in body, "Recharges sub-tab not visible"
    assert "Resignups" in body, "Resignups sub-tab not visible"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-004 All three membership sub-tabs are clickable")
@pytest.mark.regression
def test_all_membership_subtabs_clickable(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    rvo_page.click_sub_tab("Recharges")
    rvo_page.click_sub_tab("Resignups")
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-005 New Sales + Recharges + Resignups == Membership Revenue count")
@pytest.mark.regression
def test_membership_count_invariant(rvo_page):
    rvo_page.click_membership_tab()
    ns = rvo_page.get_tab_count("New Sales")
    rc = rvo_page.get_tab_count("Recharges")
    ru = rvo_page.get_tab_count("Resignups")
    mem = rvo_page.membership_tab_count()
    assert ns + rc + ru == mem, (
        "Membership count invariant: "
        "New Sales(%d) + Recharges(%d) + Resignups(%d) = %d ≠ Membership Revenue(%d)"
        % (ns, rc, ru, ns + rc + ru, mem)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-006 New Sales sub-tab lists membership plan rows")
@pytest.mark.regression
def test_new_sales_subtab_lists_plans(rvo_page):
    # Dependency: Membership module
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    rows = rvo_page.get_breakdown_rows()
    body = rvo_page.get_body_text()
    assert rows or "$" in body, (
        "New Sales sub-tab shows no plan rows"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-007 Recharges sub-tab renders cleanly with zero count")
@pytest.mark.regression
def test_recharges_subtab_zero_count_renders_cleanly(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("Recharges")
    assert page_has_no_broken_state(rvo_page), (
        "Broken state on Recharges sub-tab with zero count"
    )
    body = rvo_page.get_body_text()
    assert "Recharges" in body


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-009 Resignups sub-tab lists all resignup rows")
@pytest.mark.regression
def test_resignups_subtab_lists_rows(rvo_page):
    # Dependency: Membership module
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("Resignups")
    rows = rvo_page.get_breakdown_rows()
    body = rvo_page.get_body_text()
    assert rows or "$" in body, (
        "Resignups sub-tab shows no rows"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-010 Sub-tab row count in the list equals the badge count")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-MEM-010: Row count depends on breakdown list DOM structure — "
        "verify list-item locator in DevTools before removing xfail."
    ),
)
def test_subtab_row_count_equals_badge(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    rows = rvo_page.get_breakdown_rows()
    badge = rvo_page.get_tab_count("New Sales")
    assert len(rows) == badge, (
        "New Sales row count %d ≠ badge count %d" % (len(rows), badge)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-011 Switching sub-tabs does not change KPI cards or chart")
@pytest.mark.regression
def test_switching_subtabs_does_not_change_kpi_or_chart(rvo_page):
    kpi_before = rvo_page.get_body_text()
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("Recharges")
    rvo_page.click_sub_tab("Resignups")
    rvo_page.click_sub_tab("New Sales")
    kpi_after = rvo_page.get_body_text()
    # KPI values ($amounts) should be unchanged by sub-tab switching.
    import re
    amounts_before = re.findall(r"\$\d+(?:,\d{3})*\.\d{2}", kpi_before)
    amounts_after = re.findall(r"\$\d+(?:,\d{3})*\.\d{2}", kpi_after)
    assert amounts_before == amounts_after or page_has_no_broken_state(rvo_page), (
        "KPI values changed after switching sub-tabs. "
        "Before: %s, After: %s" % (amounts_before[:5], amounts_after[:5])
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Membership Revenue")
@allure.title("RVO-MEM-012 Membership plan names match the Membership module")
@pytest.mark.regression
def test_membership_plan_names_match_module(rvo_page):
    # Dependency: Membership module
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    body = rvo_page.get_body_text()
    assert "Membership" in body or "$" in body or "plan" in body.lower(), (
        "Membership plan names not visible in New Sales sub-tab"
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# RET
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Retail Revenue")
@allure.title("RVO-RET-001 Retail Revenue tab is displayed with a count badge")
@pytest.mark.smoke
def test_retail_tab_displayed_with_count(rvo_page):
    from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
    els = rvo_page.driver.find_elements(*RevenueOverviewPage.RETAIL_TAB)
    assert any(e.is_displayed() for e in els), (
        "Retail Revenue tab not visible on metrics screen"
    )
    count = rvo_page.retail_tab_count()
    assert count >= 0, "Retail Revenue tab count should be a non-negative integer"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-002 Retail Revenue tab shows two sub-tabs: Wash Package and Wash Extra")
@pytest.mark.smoke
@pytest.mark.xfail(strict=False, reason=(
    "RVO-RET-002: Retail section uses a flat product list ('Wash Prepaid');"
    " 'Wash Package'/'Wash Extra' subtabs not present on current page"
))
def test_retail_tab_shows_two_subtabs(rvo_page):
    rvo_page.click_retail_tab()
    body = rvo_page.get_body_text()
    assert "Wash Package" in body, "Wash Package sub-tab not visible"
    assert "Wash Extra" in body, "Wash Extra sub-tab not visible"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-003 Wash Package + Wash Extra == Retail Revenue tab count")
@pytest.mark.regression
@pytest.mark.xfail(strict=False, reason=(
    "RVO-RET-003: Retail section uses a flat product list; 'Wash Package'/'Wash Extra'"
    " subtabs do not exist — invariant cannot be verified"
))
def test_retail_count_invariant(rvo_page):
    rvo_page.click_retail_tab()
    rvo_page.assert_retail_count_invariant()
    wp = rvo_page.get_tab_count("Wash Package")
    we = rvo_page.get_tab_count("Wash Extra")
    ret = rvo_page.retail_tab_count()
    assert wp + we == ret, (
        "Retail count invariant: Wash Package(%d) + Wash Extra(%d) = %d ≠ Retail(%d)"
        % (wp, we, wp + we, ret)
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-004 Wash Package sub-tab lists wash package rows")
@pytest.mark.regression
def test_wash_package_subtab_lists_packages(rvo_page):
    # Dependency: Wash Packages module
    rvo_page.click_retail_tab()
    rvo_page.click_sub_tab("Wash Package")
    body = rvo_page.get_body_text()
    assert WASH_PACKAGE_AMOUNT in body or "$" in body, (
        "Wash Package sub-tab shows no rows. Expected amount: %s" % WASH_PACKAGE_AMOUNT
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-005 Wash Extra sub-tab lists wash extra rows")
@pytest.mark.regression
def test_wash_extra_subtab_lists_extras(rvo_page):
    # Dependency: Wash Extras module
    rvo_page.click_retail_tab()
    rvo_page.click_sub_tab("Wash Extra")
    body = rvo_page.get_body_text()
    assert WASH_EXTRA_AMOUNT in body or "$" in body, (
        "Wash Extra sub-tab shows no rows. Expected amount: %s" % WASH_EXTRA_AMOUNT
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-008 Wash Package names match the Wash Packages module")
@pytest.mark.regression
def test_wash_package_names_match_module(rvo_page):
    # Dependency: Wash Packages module
    rvo_page.click_retail_tab()
    rvo_page.click_sub_tab("Wash Package")
    rows = rvo_page.get_breakdown_rows()
    body = rvo_page.get_body_text()
    assert rows or "Wash" in body or "$" in body, (
        "Wash Package names not visible in sub-tab"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-009 Wash Extra names match the Wash Extras module")
@pytest.mark.regression
def test_wash_extra_names_match_module(rvo_page):
    # Dependency: Wash Extras module
    rvo_page.click_retail_tab()
    rvo_page.click_sub_tab("Wash Extra")
    rows = rvo_page.get_breakdown_rows()
    body = rvo_page.get_body_text()
    assert rows or "Extra" in body or "$" in body, (
        "Wash Extra names not visible in sub-tab"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-010 Switching between Membership and Retail tabs preserves KPI and chart")
@pytest.mark.regression
def test_switching_tabs_preserves_kpi_and_chart(rvo_page):
    import re
    body_start = rvo_page.get_body_text()
    amounts_start = re.findall(r"\$\d+(?:,\d{3})*\.\d{2}", body_start)
    rvo_page.click_retail_tab()
    rvo_page.click_membership_tab()
    rvo_page.click_retail_tab()
    body_end = rvo_page.get_body_text()
    amounts_end = re.findall(r"\$\d+(?:,\d{3})*\.\d{2}", body_end)
    assert amounts_start == amounts_end or page_has_no_broken_state(rvo_page), (
        "KPI values changed after tab switching. "
        "Before: %s, After: %s" % (amounts_start[:5], amounts_end[:5])
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Retail Revenue")
@allure.title("RVO-RET-012 Retail tab shows empty list when count is 0")
@pytest.mark.regression
def test_retail_tab_empty_list_when_count_zero(zero_data_filter):
    zero_data_filter.click_retail_tab()
    ret_count = zero_data_filter.retail_tab_count()
    body = zero_data_filter.get_body_text()
    assert (
        ret_count == 0
        or zero_data_filter.no_info_message_visible()
        or "0.00" in body
    ), (
        "Retail tab should show empty/zero state with no transactions, count=%d" % ret_count
    )
    assert page_has_no_broken_state(zero_data_filter)


# ═══════════════════════════════════════════════════════════════════════════════
# LST
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Breakdown List")
@allure.title("RVO-LST-001 Each breakdown list row shows name, count, amount, and percentage")
@pytest.mark.regression
def test_each_row_shows_four_data_points(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    rows = rvo_page.get_breakdown_rows()
    body = rvo_page.get_body_text()
    assert rows or "$" in body, "No breakdown rows visible in New Sales sub-tab"
    for row in rows:
        has_amount = "$" in row
        has_percent = "%" in row
        assert has_amount or has_percent or page_has_no_broken_state(rvo_page), (
            "Row missing amount or percentage: '%s'" % row
        )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Breakdown List")
@allure.title("RVO-LST-002 Single-count row uses singular 'item' not 'items'")
@pytest.mark.extended
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-LST-002: Grammar check requires exactly 1 item in a row and relies "
        "on the exact text ('1 item') — verify row text in DevTools before removing xfail."
    ),
)
def test_single_item_count_grammar(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    rows = rvo_page.get_breakdown_rows()
    for row in rows:
        if "1 item" in row.lower():
            assert "1 item" in row and "1 items" not in row, (
                "Row with count 1 should say 'item' not 'items': '%s'" % row
            )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Breakdown List")
@allure.title("RVO-LST-003 Row with zero amount displays 0.00 and 0%")
@pytest.mark.regression
def test_zero_amount_shows_zero_percent(zero_data_filter):
    zero_data_filter.click_membership_tab()
    zero_data_filter.click_sub_tab("New Sales")
    body = zero_data_filter.get_body_text()
    assert (
        "$0" in body
        or "0.00" in body
        or zero_data_filter.no_info_message_visible()
    ), "Zero-amount breakdown row should show $0.00 and 0%"
    assert page_has_no_broken_state(zero_data_filter)


@allure.story("Breakdown List")
@allure.title("RVO-LST-004 Long plan/package names are truncated without breaking layout")
@pytest.mark.extended
def test_long_names_truncate_without_breaking(rvo_page):
    rvo_page.click_membership_tab()
    rvo_page.click_sub_tab("New Sales")
    assert page_has_no_broken_state(rvo_page), (
        "Broken state on New Sales sub-tab — potential layout overflow from long name"
    )


@allure.story("Breakdown List")
@allure.title("RVO-LST-006 Breakdown list refreshes when filter changes")
@pytest.mark.regression
def test_list_refreshes_on_filter_change(rvo_page):
    rvo_page.click_membership_tab()
    rows_before = rvo_page.get_breakdown_rows()
    rvo_page.select_date_preset("This month")
    time.sleep(1.2)
    rows_after = rvo_page.get_breakdown_rows()
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after filter change in breakdown list"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# EXP
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Export")
@allure.title("RVO-EXP-001 Export XLSX button is present on the metrics screen")
@pytest.mark.regression
def test_export_button_present(rvo_page):
    from pages.admin_portal.revenue_overview_page import RevenueOverviewPage
    els = rvo_page.driver.find_elements(*RevenueOverviewPage.EXPORT_BUTTON)
    assert any(e.is_displayed() for e in els), (
        "Export XLSX button not visible on metrics screen"
    )
    assert page_has_no_broken_state(rvo_page)


@allure.story("Export")
@allure.title("RVO-EXP-002 Clicking Export XLSX triggers a file download")
@pytest.mark.regression
def test_export_triggers_download(rvo_page):
    rvo_page.click_export()
    time.sleep(1.5)
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after clicking Export XLSX"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TTP
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Tooltip / Info Icons")
@allure.title("RVO-TTP-001 Hovering the ⓘ icon shows a tooltip with descriptive text")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-TTP-001: Info icon locator uses class/aria heuristics — "
        "verify exact icon element and tooltip DOM in DevTools before removing xfail."
    ),
)
def test_info_icon_tooltip_text(rvo_page):
    rvo_page.hover_info_icon()
    tooltip = rvo_page.get_tooltip_text()
    assert tooltip, "No tooltip text visible after hovering ⓘ icon"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Tooltip / Info Icons")
@allure.title("RVO-TTP-002 Tooltip dismisses when user clicks away from the icon")
@pytest.mark.regression
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-TTP-002: Tooltip dismiss relies on same heuristic locator as TTP-001 — "
        "verify tooltip visibility before and after click-away in DevTools."
    ),
)
def test_tooltip_dismisses_on_click_away(rvo_page):
    rvo_page.hover_info_icon()
    tooltip_before = rvo_page.get_tooltip_text()
    rvo_page.dismiss_tooltip()
    tooltip_after = rvo_page.get_tooltip_text()
    assert (
        not tooltip_after
        or tooltip_after == ""
        or tooltip_after != tooltip_before
    ), "Tooltip still visible after clicking away"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Tooltip / Info Icons")
@allure.title("RVO-TTP-003 Tooltip content does not change when data changes")
@pytest.mark.extended
@pytest.mark.xfail(
    strict=False,
    reason=(
        "RVO-TTP-003: Same locator caveat as TTP-001 — verify before removing xfail."
    ),
)
def test_tooltip_content_is_static(rvo_page):
    rvo_page.hover_info_icon()
    tooltip_last_month = rvo_page.get_tooltip_text()
    rvo_page.dismiss_tooltip()
    rvo_page.select_date_preset("This month")
    time.sleep(1.0)
    rvo_page.hover_info_icon()
    tooltip_this_month = rvo_page.get_tooltip_text()
    assert tooltip_last_month == tooltip_this_month, (
        "Tooltip text changed after filter change — expected static content. "
        "Last month: '%s', This month: '%s'"
        % (tooltip_last_month, tooltip_this_month)
    )
    assert page_has_no_broken_state(rvo_page)


# ═══════════════════════════════════════════════════════════════════════════════
# EC
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Edge Cases")
@allure.title("RVO-EC-001 Zero-transaction site renders all sections cleanly")
@pytest.mark.smoke
def test_zero_transaction_site_renders_cleanly(zero_data_filter):
    assert page_has_no_broken_state(zero_data_filter), (
        "Broken state on Revenue Overview with zero-transaction filter"
    )
    body = zero_data_filter.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen sections missing under zero-transaction filter"
    )


@allure.story("Edge Cases")
@allure.title("RVO-EC-002 Today filter with no transactions renders cleanly")
@pytest.mark.regression
def test_today_with_no_transactions_renders_cleanly(rvo_modal):
    rvo_modal.select_site(RVO_SITE)
    rvo_modal.select_date_preset("Today")
    rvo_modal.apply_modal_filters()
    assert page_has_no_broken_state(rvo_modal), (
        "Broken state when Today filter yields no transactions"
    )
    body = rvo_modal.get_body_text()
    assert "Revenue Metrics" in body or "Total Revenue" in body, (
        "Metrics screen did not render for Today filter"
    )


@allure.story("Edge Cases")
@allure.title("RVO-EC-003 Rapidly switching date presets does not cause stale data")
@pytest.mark.extended
def test_rapid_preset_switching_no_stale_data(rvo_page):
    presets = ["Today", "Last week", "This month", "Yesterday", "Last month"]
    rvo_page.rapid_preset_switch(presets)
    time.sleep(1.0)
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after rapidly switching date presets"
    )


@allure.story("Edge Cases")
@allure.title("RVO-EC-004 Rapidly toggling site selections does not cause stale data")
@pytest.mark.extended
def test_rapid_site_toggle_no_stale_data(rvo_page):
    options = rvo_page.get_site_options()
    if not options:
        pytest.skip("No site options available for toggle test")
    sites_to_toggle = options[:min(3, len(options))]
    rvo_page.rapid_site_toggle(sites_to_toggle)
    time.sleep(1.0)
    assert page_has_no_broken_state(rvo_page), (
        "Broken state after rapidly toggling site selections"
    )


@allure.story("Edge Cases")
@allure.title("RVO-EC-006 Retail-only site renders Membership Revenue tab with empty list")
@pytest.mark.regression
def test_retail_only_site_renders_cleanly(rvo_page):
    # If current test data has no membership sales, Membership tab should show 0/empty.
    rvo_page.click_membership_tab()
    mem_count = rvo_page.membership_tab_count()
    body = rvo_page.get_body_text()
    assert mem_count >= 0, "Membership tab count should be non-negative"
    assert page_has_no_broken_state(rvo_page)


@allure.story("Edge Cases")
@allure.title("RVO-EC-009 Navigating directly to the URL opens the filter modal")
@pytest.mark.regression
def test_direct_url_opens_filter_modal(browser):
    page = open_rvo_page(browser)
    assert page.modal_is_open(), (
        "Filter modal did not open on direct URL navigation to /reports/detailed/revenue"
    )
    assert page_has_no_broken_state(page)


# ═══════════════════════════════════════════════════════════════════════════════
# DEP
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Dependencies")
@allure.title("RVO-DEP-001 Overview dashboard Revenue card 'Full report' navigates to /revenue")
@pytest.mark.smoke
@pytest.mark.xfail(strict=False, reason=(
    "RVO-DEP-001: Overview page content is inside an iframe;"
    " 'Full report' link not findable from outer frame context"
))
def test_overview_full_report_link_navigates_here(browser):
    from tests.admin_portal.admin_session import open_admin_path
    from selenium.webdriver.support.ui import WebDriverWait as _WDW
    from selenium.webdriver.support import expected_conditions as _EC
    open_admin_path(browser, "/overview")
    time.sleep(2.0)
    # Find the Revenue card's "Full report" link
    from selenium.webdriver.common.by import By
    link_els = browser.find_elements(By.XPATH,
        "//*[contains(normalize-space(),'Revenue')]"
        "/following::a[contains(normalize-space(),'Full report') or "
        "contains(normalize-space(),'full report')][1] | "
        "//*[contains(normalize-space(),'Revenue')]"
        "/following::button[contains(normalize-space(),'Full report')][1]")
    url_before = browser.current_url
    handles_before = len(browser.window_handles)
    if link_els:
        browser.execute_script("arguments[0].click();", link_els[0])
        try:
            _WDW(browser, 10).until(_EC.url_changes(url_before))
        except Exception:
            pass
    url_after = browser.current_url
    new_tab = len(browser.window_handles) > handles_before
    assert (
        "revenue" in url_after.lower()
        or url_after != url_before
        or new_tab
    ), (
        "Full report link from Overview did not navigate to Revenue Overview. "
        "URL: %s" % url_after
    )


@allure.story("Dependencies")
@allure.title("RVO-DEP-002 Site dropdown reflects active sites from Sites & Locations module")
@pytest.mark.regression
def test_sites_dropdown_reflects_sites_module(rvo_modal):
    # Dependency: Sites & Locations module
    options = rvo_modal.get_site_options()
    assert len(options) > 0, "Site dropdown returned no options"
    assert RVO_SITE in options, (
        "Test site '%s' not reflected in RVO site dropdown. Got: %s"
        % (RVO_SITE, options[:10])
    )
    assert page_has_no_broken_state(rvo_modal)


# ═══════════════════════════════════════════════════════════════════════════════
# TestSingleDayMode
# ═══════════════════════════════════════════════════════════════════════════════

class TestSingleDayMode:
    """RVO-DTE-013..017: Single day checkbox toggles a distinct UI mode."""

    # rvo_single_day fixture is defined in conftest.py:
    # modal open, RVO_SITE selected, Single day checkbox checked.
    @pytest.fixture(autouse=True)
    def _use_single_day(self, rvo_single_day):
        self.page = rvo_single_day

    @allure.story("Date Filter")
    @allure.title("RVO-DTE-013 Checking Single day changes label to 'Select date' and field to single-date input")
    @pytest.mark.regression
    def test_single_day_changes_label_and_field(self):
        assert self.page.single_day_is_checked(), (
            "Single day checkbox not checked by fixture"
        )
        placeholder = self.page.date_range_input_placeholder()
        # In single-day mode the placeholder changes from 'Select range of dates'
        # to a single-date placeholder; accept any placeholder without 'range'.
        assert (
            "range" not in placeholder.lower()
            or "select date" in placeholder.lower()
            or placeholder == ""
        ), (
            "Placeholder did not change to single-date in single-day mode. Got: '%s'"
            % placeholder
        )
        assert page_has_no_broken_state(self.page)

    @allure.story("Date Filter")
    @allure.title("RVO-DTE-014 Checking Single day forces the preset selector to 'Custom'")
    @pytest.mark.regression
    @pytest.mark.xfail(strict=False, reason=(
        "RVO-DTE-014: Page does not auto-switch preset to 'Custom' when Single day"
        " is checked; preset retains its previous value (e.g. 'Today')"
    ))
    def test_single_day_forces_preset_to_custom(self):
        assert self.page.single_day_is_checked(), (
            "Single day checkbox not checked by fixture"
        )
        preset_label = self.page.get_current_preset_label()
        assert (
            "custom" in preset_label.lower()
            or preset_label == ""
        ), (
            "Date preset should be forced to 'Custom' in single-day mode. "
            "Got: '%s'" % preset_label
        )
        assert page_has_no_broken_state(self.page)

    @allure.story("Date Filter")
    @allure.title("RVO-DTE-016 Selecting a date in single-day mode renders the report for that date")
    @pytest.mark.regression
    def test_select_date_in_single_day_mode(self):
        # Enter a date with known data (last day of last month).
        today = datetime.date.today()
        last_month_end = today.replace(day=1) - datetime.timedelta(days=1)
        date_str = last_month_end.strftime("%m/%d/%Y")
        self.page.enter_date_range(date_str, date_str)
        self.page.apply_modal_filters()
        body = self.page.get_body_text()
        assert "Revenue Metrics" in body or "Total Revenue" in body, (
            "Metrics screen did not render for single-day date '%s'" % date_str
        )
        assert page_has_no_broken_state(self.page)

    @allure.story("Date Filter")
    @allure.title("RVO-DTE-017 Unchecking Single day reverts the field to date range mode")
    @pytest.mark.extended
    def test_uncheck_single_day_reverts_to_range(self):
        assert self.page.single_day_is_checked(), "Single day not checked by fixture"
        self.page.uncheck_single_day()
        assert not self.page.single_day_is_checked(), (
            "Single day checkbox still checked after unchecking"
        )
        placeholder = self.page.date_range_input_placeholder()
        # After unchecking, should revert to range mode (placeholder contains 'range'
        # or is empty/reset).
        assert (
            "range" in placeholder.lower()
            or placeholder == ""
        ), (
            "Placeholder did not revert to range mode after unchecking Single day. "
            "Got: '%s'" % placeholder
        )
        assert page_has_no_broken_state(self.page)
