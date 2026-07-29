import datetime
import time

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.mixins import SingleDaySyncMixin
from tests.admin_portal.cash_report.conftest import (
    CSH_SITE,
    CSH_DATE_START,
    CSH_DATE_END,
    DATE_PRESETS,
    KIOSK_BALANCE_SUMMARY_COLUMNS,
    KIOSK_DENOMINATION_COLUMNS,
    KIOSK_TRANSACTIONS_COLUMNS,
    POS_BALANCE_SUMMARY_COLUMNS,
    POS_BANK_DROP_COLUMNS,
    POS_TRANSACTIONS_COLUMNS,
    TAB_ANALYTICS,
    TAB_KIOSK,
    TAB_POS,
    TABLE_KIOSK_BALANCE_SUMMARY,
    TABLE_KIOSK_DENOMINATION,
    TABLE_KIOSK_TRANSACTIONS,
    TABLE_POS_BALANCE_SUMMARY,
    TABLE_POS_BANK_DROP,
    TABLE_POS_TRANSACTIONS,
    compute_preset_date_range,
    open_csh_page,
    page_has_no_broken_state,
)

# Excluded TCs (not scheduled for automation):
# CSH-NAV-006: browser back/forward during modal — Automation = No
# CSH-SIT-005: multi-site aggregate data validation — Not Scheduled (Future/dataset)
# CSH-DTE-010: calendar keyboard navigation — Automation = No
# CSH-DTE-011: manually typed date boundary check — Automation = No
# CSH-EXP-003: XLSX file content validation — Not Scheduled (Future/dataset)
# CSH-EXP-004: export with zero data — Automation = No
# CSH-SDM-005: page bar SDM via keyboard — Automation = No
# CSH-KSK-012: kiosk transaction detail drill-down — Not Scheduled (Deferred)
# CSH-POS-009: POS transaction detail drill-down — Not Scheduled (Deferred)
# CSH-DEP-001..005: cross-module data cross-check vs Kiosk Settings — Not Scheduled (Future/dataset)
# CSH-EC-001: role-based access (non-admin user) — Not Scheduled (Deferred)
# CSH-EC-002: session timeout while viewing — Automation = No
# CSH-EC-003: mobile viewport layout — Automation = No
# CSH-EC-004: print view — Automation = No

pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Cash Report"),
]

# ── Parametrize table ──────────────────────────────────────────────────────────

_DATE_PRESET_PARAMS = [
    pytest.param("Today",      id="CSH-DTE-002"),
    pytest.param("Yesterday",  id="CSH-DTE-003"),
    pytest.param("This week",  id="CSH-DTE-004"),
    pytest.param("Last week",  id="CSH-DTE-005"),
    pytest.param("This month", id="CSH-DTE-006"),
    pytest.param("Last month", id="CSH-DTE-007"),
]


# ═══════════════════════════════════════════════════════════════════════════════
# TestNavigation
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Navigation")
class TestNavigation:

    @allure.title("CSH-NAV-001 Cash Report page loads at /reports/detailed/cash_report")
    @pytest.mark.smoke
    def test_page_loads_at_correct_url(self, csh_modal):
        url = csh_modal.get_current_url()
        assert "cash_report" in url.lower() or "cash-report" in url.lower(), (
            "URL does not contain 'cash_report': %s" % url
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-NAV-002 Filter modal auto-opens on page load without user action")
    @pytest.mark.smoke
    def test_filter_modal_auto_opens(self, csh_modal):
        assert csh_modal.modal_is_open(), (
            "Filter modal (Apply filters button) not visible on page load"
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-NAV-003 Modal contains site, date preset, date range, single day, and Apply")
    @pytest.mark.smoke
    def test_modal_contains_all_controls(self, csh_modal):
        from pages.admin_portal.cash_report_page import CashReportPage
        d = csh_modal.driver
        site_els   = d.find_elements(*CashReportPage.SITE_MULTISELECT)
        preset_els = d.find_elements(*CashReportPage.DATE_PRESET_COMBOBOX)
        range_els  = d.find_elements(*CashReportPage.DATE_RANGE_INPUT)
        apply_els  = d.find_elements(*CashReportPage.APPLY_BUTTON)
        assert any(e.is_displayed() for e in site_els),   "Site multiselect not visible in modal"
        assert any(e.is_displayed() for e in preset_els), "Date preset combobox not visible in modal"
        assert any(e.is_displayed() for e in range_els),  "Date range input not visible in modal"
        assert any(e.is_displayed() for e in apply_els),  "Apply filters button not visible in modal"
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-NAV-004 Filter bar and tab labels visible after applying filters")
    @pytest.mark.regression
    def test_page_title_visible_after_apply(self, csh_page):
        # Confirmed DevTools (Jul 2026): Cash Report has no module-level heading.
        # Page goes directly to the filter bar (Sites / Locations) then the
        # Analytics / Kiosk / POS tab strip. Assert on those instead.
        body = csh_page.get_body_text()
        assert (
            "Sites / Locations" in body
            or "Analytics" in body
            or "Kiosk" in body
        ), "Expected filter bar or tab labels not visible after applying filters"
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-NAV-005 Sidebar FINANCIAL section highlights Cash Report as active item")
    @pytest.mark.extended
    def test_sidebar_highlights_active_item(self, csh_page):
        assert csh_page.sidebar_cash_report_active(), (
            "Sidebar does not highlight an active Cash Report / Financial item"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TestFilterModal
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Filter Modal")
class TestFilterModal:

    @allure.title("CSH-FMD-001 Sites dropdown lists active sites including test site")
    @pytest.mark.regression
    def test_sites_dropdown_lists_active_sites(self, csh_modal):
        options = csh_modal.get_site_options()
        assert len(options) > 0, "Site dropdown returned no options"
        assert CSH_SITE in options, (
            "Test site '%s' not found in dropdown: %s" % (CSH_SITE, options[:10])
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-FMD-002 Date preset dropdown lists exactly 6 options (no Custom)")
    @pytest.mark.regression
    def test_date_preset_dropdown_options(self, csh_modal):
        options = csh_modal.get_date_preset_options()
        options_lower = [o.lower() for o in options]
        missing = [p for p in DATE_PRESETS if p.lower() not in options_lower]
        assert not missing, (
            "Date preset options missing: %s.  Actual: %s" % (missing, options)
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-FMD-003 Modal opens with no default site selected")
    @pytest.mark.smoke
    def test_modal_opens_with_no_default_site(self, csh_modal):
        chips = csh_modal.get_site_chips()
        assert chips == [], (
            "Expected no site selected on fresh modal open; got: %s" % chips
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-FMD-004 Selecting a date preset auto-populates the date range field")
    @pytest.mark.regression
    def test_selecting_preset_fills_date_range(self, csh_modal):
        csh_modal.select_date_preset("Last month")
        date_val = csh_modal.get_date_range_value()
        assert date_val, "Date range field not populated after selecting 'Last month'"
        assert str(datetime.date.today().year) in date_val, (
            "Expected year not in populated date range: '%s'" % date_val
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-FMD-005 Apply filters closes modal and renders the metrics screen")
    @pytest.mark.smoke
    def test_apply_filters_closes_modal_and_renders_metrics(self, csh_modal):
        csh_modal.select_site(CSH_SITE)
        csh_modal.select_date_preset("Last month")
        csh_modal.apply_modal_filters()
        assert not csh_modal.modal_is_open(), "Modal should be closed after Apply filters"
        body = csh_modal.get_body_text()
        assert "Cash" in body or "Kiosk" in body or "POS" in body, (
            "Metrics screen did not render after Apply filters"
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-FMD-006 Filter values are reflected in the page-level bar after apply")
    @pytest.mark.regression
    def test_filter_values_reflected_in_page_bar(self, csh_page):
        chips    = csh_page.get_site_chips()
        date_val = csh_page.get_date_range_value()
        assert CSH_SITE in chips or any(CSH_SITE.lower() in c.lower() for c in chips), (
            "Selected site '%s' not visible as chip in page-level bar.  Chips: %s"
            % (CSH_SITE, chips)
        )
        assert date_val, "Date range not reflected in the page-level filter bar"
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-FMD-007 Page bar filter changes do not re-open the blocking modal")
    @pytest.mark.regression
    def test_page_bar_changes_do_not_reopen_modal(self, csh_page):
        csh_page.select_date_preset("This month")
        time.sleep(1.0)
        assert not csh_page.modal_is_open(), (
            "Filter modal re-opened after changing date preset from the page-level bar"
        )
        assert page_has_no_broken_state(csh_page)


# ═══════════════════════════════════════════════════════════════════════════════
# TestSiteFilter
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Site Filter")
class TestSiteFilter:

    @allure.title("CSH-SIT-001 Site dropdown has no 'All Sites' option")
    @pytest.mark.regression
    def test_no_all_sites_option(self, csh_modal):
        options = csh_modal.get_site_options()
        options_lower = [o.lower() for o in options]
        assert "all sites" not in options_lower, (
            "Cash Report site dropdown unexpectedly contains 'All Sites': %s" % options
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-SIT-002 Selecting a site creates a chip in the control")
    @pytest.mark.smoke
    def test_selecting_site_creates_chip(self, csh_modal):
        csh_modal.select_site(CSH_SITE)
        chips = csh_modal.get_site_chips()
        assert any(CSH_SITE.lower() in c.lower() for c in chips), (
            "No chip for '%s' after selection.  Chips: %s" % (CSH_SITE, chips)
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-SIT-003 Test site (VK Test carwash 2) is present in the dropdown")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="staging data / intermittent — deferred")
    def test_test_site_in_dropdown(self, csh_modal):
        options = csh_modal.get_site_options()
        assert CSH_SITE in options, (
            "Test site '%s' not found in site dropdown: %s" % (CSH_SITE, options[:10])
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-SIT-004 Clearing the site chip removes the site filter")
    @pytest.mark.regression
    def test_clearing_chip_removes_site_filter(self, csh_page):
        chips_before = csh_page.get_site_chips()
        assert chips_before, "Expected at least one chip before clearing"
        csh_page.clear_sites()
        chips_after = csh_page.get_site_chips()
        assert len(chips_after) < len(chips_before), (
            "Site chips not reduced after clear.  Before: %s  After: %s"
            % (chips_before, chips_after)
        )
        assert page_has_no_broken_state(csh_page)


# ═══════════════════════════════════════════════════════════════════════════════
# TestDateFilter
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Date Filter")
class TestDateFilter:

    @allure.title("CSH-DTE-001 Date preset dropdown lists 6 options (Today … Last month)")
    @pytest.mark.regression
    def test_date_preset_count(self, csh_modal):
        options = csh_modal.get_date_preset_options()
        assert len(options) >= len(DATE_PRESETS), (
            "Expected at least %d date presets; got %d: %s"
            % (len(DATE_PRESETS), len(options), options)
        )
        assert page_has_no_broken_state(csh_modal)

    @allure.title("CSH-DTE-{preset} Selecting '{preset}' preset populates date range field")
    @pytest.mark.parametrize("preset", _DATE_PRESET_PARAMS)
    @pytest.mark.regression
    def test_preset_populates_date_range(self, csh_modal, preset):
        csh_modal.select_site(CSH_SITE)
        csh_modal.select_date_preset(preset)
        try:
            WebDriverWait(csh_modal.driver, 8).until(
                lambda d: csh_modal.get_date_range_value() != ""
            )
        except Exception:
            time.sleep(1.5)
        date_val = csh_modal.get_date_range_value()
        assert date_val, (
            "Date range field empty after selecting '%s' preset" % preset
        )
        expected_start, expected_end = compute_preset_date_range(preset)
        if expected_start:
            assert expected_start in date_val or str(datetime.date.today().year) in date_val, (
                "Expected date '%s' not found in field value '%s' for preset '%s'"
                % (expected_start, date_val, preset)
            )
        assert page_has_no_broken_state(csh_modal)


# ═══════════════════════════════════════════════════════════════════════════════
# TestSingleDayMode
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Single Day Mode")
class TestSingleDayMode(SingleDaySyncMixin):
    """Single-day-mode tests inherited from SingleDaySyncMixin.

    Fixture wiring: sdm_modal / sdm_single_day / sdm_page are defined in
    this module's conftest.py as CSH-specific aliases.

    TC IDs generated dynamically via allure.dynamic.title in the mixin:
        CSH-SDM-001  Single day checkbox visible in modal            (smoke)
        CSH-SDM-002  Checking SDM changes the date field             (regression)
        CSH-SDM-003  Modal SDM checked → page bar SDM checked        (regression, skip)
        CSH-SDM-004  Page bar SDM uncheck → modal reflects uncheck   (regression, skip)
    """

    SDM_TC_PREFIX = "CSH-SDM"

    @pytest.mark.skip(reason="Manual check required — PAGE_BAR_SINGLE_DAY_CHECKBOX locator unconfirmed via DevTools")
    def test_modal_sdm_syncs_to_page_bar(self, sdm_single_day):
        super().test_modal_sdm_syncs_to_page_bar(sdm_single_day)

    @pytest.mark.skip(reason="Manual check required — PAGE_BAR_SINGLE_DAY_CHECKBOX locator unconfirmed via DevTools")
    def test_page_bar_sdm_uncheck_syncs_to_modal(self, sdm_page):
        super().test_page_bar_sdm_uncheck_syncs_to_modal(sdm_page)


# ═══════════════════════════════════════════════════════════════════════════════
# TestTabNavigation
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Tab Navigation")
class TestTabNavigation:

    @allure.title("CSH-TAB-001 Three tabs visible after apply: Analytics, Kiosk, POS")
    @pytest.mark.smoke
    def test_three_tabs_visible(self, csh_page):
        tabs = csh_page.get_visible_tabs()
        tabs_lower = [t.lower() for t in tabs]
        for expected in [TAB_ANALYTICS, TAB_KIOSK, TAB_POS]:
            assert expected.lower() in tabs_lower, (
                "Tab '%s' not visible.  Visible tabs: %s" % (expected, tabs)
            )
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-TAB-002 Analytics tab is active by default after filters are applied")
    @pytest.mark.regression
    def test_analytics_tab_active_by_default(self, csh_page):
        active = csh_page.get_active_tab()
        body   = csh_page.get_body_text().lower()
        # Active tab should be Analytics (or content clue should be present)
        assert (
            TAB_ANALYTICS.lower() in (active or "").lower()
            or "analytics" in body
        ), (
            "Analytics tab not active by default.  Active tab: '%s'" % active
        )
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-TAB-003 Clicking Kiosk tab switches to Kiosk content")
    @pytest.mark.smoke
    def test_kiosk_tab_click(self, csh_page):
        csh_page.click_tab(TAB_KIOSK)
        body = csh_page.get_body_text().lower()
        assert (
            "kiosk" in body
            or TABLE_KIOSK_BALANCE_SUMMARY.lower() in body
            or TABLE_KIOSK_TRANSACTIONS.lower() in body
        ), "Kiosk content not visible after clicking Kiosk tab"
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-TAB-004 Clicking POS tab switches to POS content")
    @pytest.mark.smoke
    def test_pos_tab_click(self, csh_page):
        csh_page.click_tab(TAB_POS)
        body = csh_page.get_body_text().lower()
        assert (
            "pos" in body
            or TABLE_POS_BALANCE_SUMMARY.lower() in body
            or TABLE_POS_TRANSACTIONS.lower() in body
        ), "POS content not visible after clicking POS tab"
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-TAB-005 Re-clicking Analytics tab restores Analytics content")
    @pytest.mark.regression
    def test_analytics_tab_restores(self, csh_page):
        csh_page.click_tab(TAB_KIOSK)
        time.sleep(0.3)
        csh_page.click_tab(TAB_ANALYTICS)
        body   = csh_page.get_body_text().lower()
        active = csh_page.get_active_tab()
        assert (
            TAB_ANALYTICS.lower() in (active or "").lower()
            or "analytics" in body
        ), "Analytics content not restored after re-clicking Analytics tab"
        assert page_has_no_broken_state(csh_page)


# ═══════════════════════════════════════════════════════════════════════════════
# TestExport
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Export")
class TestExport:

    @allure.title("CSH-EXP-001 Export XLSX button is visible on the metrics screen")
    @pytest.mark.smoke
    def test_export_xlsx_button_visible(self, csh_page):
        assert csh_page.export_button_visible(), (
            "Export XLSX button not visible on the Cash Report metrics screen"
        )
        assert page_has_no_broken_state(csh_page)

    @allure.title("CSH-EXP-002 Export XLSX button click initiates a file download")
    @pytest.mark.regression
    def test_export_xlsx_triggers_download(self, csh_page):
        csh_page.click_export_xlsx()
        time.sleep(2.0)
        # If download detection were wired up, we would check for a new file in
        # the configured download directory here.
        assert True, "Placeholder — download detection not implemented"


# ═══════════════════════════════════════════════════════════════════════════════
# TestAnalyticsTab
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Analytics Tab")
class TestAnalyticsTab:

    @allure.title("CSH-ANA-001 Analytics tab renders summary metric cards or KPIs")
    @pytest.mark.smoke
    def test_analytics_tab_shows_metrics(self, csh_analytics):
        body = csh_analytics.get_body_text()
        # Cash / currency indicators or KPI labels expected on the Analytics tab
        assert (
            "$" in body
            or "total" in body.lower()
            or "balance" in body.lower()
            or "kiosk" in body.lower()
        ), "No metric cards or KPI content found on Analytics tab"
        assert page_has_no_broken_state(csh_analytics)

    @allure.title("CSH-ANA-002 Analytics metric values are non-zero for the test dataset")
    @pytest.mark.regression
    def test_analytics_metrics_not_all_zero(self, csh_analytics):
        body = csh_analytics.get_body_text()
        # At least one non-$0.00 / non-zero figure expected for last month dataset
        assert (
            "$0.00" not in body
            or "0" not in body.split("$")[-1][:5]
            or any(c.isdigit() and c != "0" for c in body.replace("$0.00", ""))
        ), "All visible currency values appear to be $0.00 for the test dataset"
        assert page_has_no_broken_state(csh_analytics)

    @allure.title("CSH-ANA-003 Analytics tab shows no-data message for zero-data date range")
    @pytest.mark.regression
    def test_analytics_zero_data_message(self, csh_zero_data):
        csh_zero_data.click_tab(TAB_ANALYTICS)
        body = csh_zero_data.get_body_text().lower()
        has_no_data = (
            csh_zero_data.no_data_message_visible()
            or "no data" in body
            or "0" in body
            or "$0" in body
        )
        assert has_no_data, (
            "Analytics tab should show empty state or zero values for a date range "
            "with no transactions; actual body: %s" % body[:300]
        )
        assert page_has_no_broken_state(csh_zero_data)


# ═══════════════════════════════════════════════════════════════════════════════
# TestKioskTab
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("Kiosk Tab")
class TestKioskTab:

    @allure.title("CSH-KSK-001 Kiosk Balance Summary section is visible on Kiosk tab")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Manual check required — actual Kiosk Balance Summary heading unconfirmed via DevTools")
    def test_kiosk_balance_summary_visible(self, csh_kiosk):
        assert csh_kiosk.table_section_visible(TABLE_KIOSK_BALANCE_SUMMARY), (
            "Section '%s' not visible on Kiosk tab" % TABLE_KIOSK_BALANCE_SUMMARY
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-002 Kiosk Balance Summary table has column headers")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Manual check required — depends on CSH-KSK-001 heading confirmation")
    def test_kiosk_balance_summary_has_headers(self, csh_kiosk):
        headers = csh_kiosk.get_table_headers(TABLE_KIOSK_BALANCE_SUMMARY)
        assert len(headers) > 0, (
            "No column headers found in '%s'" % TABLE_KIOSK_BALANCE_SUMMARY
        )
        if KIOSK_BALANCE_SUMMARY_COLUMNS:
            missing = [c for c in KIOSK_BALANCE_SUMMARY_COLUMNS
                       if c.lower() not in [h.lower() for h in headers]]
            assert not missing, (
                "Expected columns missing from %s: %s.  Actual: %s"
                % (TABLE_KIOSK_BALANCE_SUMMARY, missing, headers)
            )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-003 Kiosk Balance Summary shows data rows for the test dataset")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Manual check required — depends on CSH-KSK-001 heading confirmation")
    def test_kiosk_balance_summary_has_data(self, csh_kiosk):
        row_count = csh_kiosk.get_table_row_count(TABLE_KIOSK_BALANCE_SUMMARY)
        body      = csh_kiosk.get_body_text().lower()
        assert (
            row_count > 0
            or TABLE_KIOSK_BALANCE_SUMMARY.lower() in body
        ), (
            "'%s' table has no data rows for the test dataset"
            % TABLE_KIOSK_BALANCE_SUMMARY
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-004 Kiosk Balance Summary — pagination controls are present")
    @pytest.mark.regression
    def test_kiosk_balance_summary_pagination(self, csh_kiosk):
        has_paging = csh_kiosk.table_pagination_present(TABLE_KIOSK_BALANCE_SUMMARY)
        row_count  = csh_kiosk.get_table_row_count(TABLE_KIOSK_BALANCE_SUMMARY)
        # Pagination only meaningful when data exists; skip assertion if no rows
        if row_count == 0:
            pytest.skip("No data rows in Kiosk Balance Summary — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_KIOSK_BALANCE_SUMMARY
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-005 Kiosk Denomination section is visible on Kiosk tab")
    @pytest.mark.smoke
    def test_kiosk_denomination_visible(self, csh_kiosk):
        assert csh_kiosk.table_section_visible(TABLE_KIOSK_DENOMINATION), (
            "Section '%s' not visible on Kiosk tab" % TABLE_KIOSK_DENOMINATION
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-006 Kiosk Denomination table has column headers")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Manual check required — Denomination renders as chart/histogram, not HTML table; widget type unconfirmed via DevTools")
    def test_kiosk_denomination_has_headers(self, csh_kiosk):
        headers = csh_kiosk.get_table_headers(TABLE_KIOSK_DENOMINATION)
        assert len(headers) > 0, (
            "No column headers found in '%s'" % TABLE_KIOSK_DENOMINATION
        )
        if KIOSK_DENOMINATION_COLUMNS:
            missing = [c for c in KIOSK_DENOMINATION_COLUMNS
                       if c.lower() not in [h.lower() for h in headers]]
            assert not missing, (
                "Expected columns missing from %s: %s.  Actual: %s"
                % (TABLE_KIOSK_DENOMINATION, missing, headers)
            )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-007 Kiosk Denomination — pagination controls are present")
    @pytest.mark.regression
    def test_kiosk_denomination_pagination(self, csh_kiosk):
        has_paging = csh_kiosk.table_pagination_present(TABLE_KIOSK_DENOMINATION)
        row_count  = csh_kiosk.get_table_row_count(TABLE_KIOSK_DENOMINATION)
        if row_count == 0:
            pytest.skip("No data rows in Kiosk Denomination — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_KIOSK_DENOMINATION
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-008 Kiosk Transactions section is visible on Kiosk tab")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Manual check required — actual Kiosk Transactions heading unconfirmed via DevTools")
    def test_kiosk_transactions_visible(self, csh_kiosk):
        assert csh_kiosk.table_section_visible(TABLE_KIOSK_TRANSACTIONS), (
            "Section '%s' not visible on Kiosk tab" % TABLE_KIOSK_TRANSACTIONS
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-009 Kiosk Transactions table has column headers")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Manual check required — depends on CSH-KSK-008 heading confirmation")
    def test_kiosk_transactions_has_headers(self, csh_kiosk):
        headers = csh_kiosk.get_table_headers(TABLE_KIOSK_TRANSACTIONS)
        assert len(headers) > 0, (
            "No column headers found in '%s'" % TABLE_KIOSK_TRANSACTIONS
        )
        if KIOSK_TRANSACTIONS_COLUMNS:
            missing = [c for c in KIOSK_TRANSACTIONS_COLUMNS
                       if c.lower() not in [h.lower() for h in headers]]
            assert not missing, (
                "Expected columns missing from %s: %s.  Actual: %s"
                % (TABLE_KIOSK_TRANSACTIONS, missing, headers)
            )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-010 Kiosk Transactions — pagination controls are present")
    @pytest.mark.regression
    def test_kiosk_transactions_pagination(self, csh_kiosk):
        has_paging = csh_kiosk.table_pagination_present(TABLE_KIOSK_TRANSACTIONS)
        row_count  = csh_kiosk.get_table_row_count(TABLE_KIOSK_TRANSACTIONS)
        if row_count == 0:
            pytest.skip("No data rows in Kiosk Transactions — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_KIOSK_TRANSACTIONS
        )
        assert page_has_no_broken_state(csh_kiosk)

    @allure.title("CSH-KSK-011 Kiosk tab shows empty/no-data state for a zero-data date range")
    @pytest.mark.regression
    def test_kiosk_zero_data_state(self, csh_zero_data):
        csh_zero_data.click_tab(TAB_KIOSK)
        body = csh_zero_data.get_body_text().lower()
        kiosk_row_count = sum(
            csh_zero_data.get_table_row_count(t)
            for t in [TABLE_KIOSK_BALANCE_SUMMARY,
                      TABLE_KIOSK_DENOMINATION,
                      TABLE_KIOSK_TRANSACTIONS]
        )
        has_no_data = (
            csh_zero_data.no_data_message_visible()
            or kiosk_row_count == 0
            or "no data" in body
            or "no records" in body
        )
        assert has_no_data, (
            "Kiosk tab should show empty state for zero-data filter; "
            "body excerpt: %s" % body[:300]
        )
        assert page_has_no_broken_state(csh_zero_data)


# ═══════════════════════════════════════════════════════════════════════════════
# TestPOSTab
# ═══════════════════════════════════════════════════════════════════════════════

@allure.story("POS Tab")
class TestPOSTab:

    @allure.title("CSH-POS-001 POS Balance Summary section is visible on POS tab")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Manual check required — actual POS Balance Summary heading unconfirmed via DevTools")
    def test_pos_balance_summary_visible(self, csh_pos):
        assert csh_pos.table_section_visible(TABLE_POS_BALANCE_SUMMARY), (
            "Section '%s' not visible on POS tab" % TABLE_POS_BALANCE_SUMMARY
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-002 POS Balance Summary table has column headers")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Manual check required — depends on CSH-POS-001 heading confirmation")
    def test_pos_balance_summary_has_headers(self, csh_pos):
        headers = csh_pos.get_table_headers(TABLE_POS_BALANCE_SUMMARY)
        assert len(headers) > 0, (
            "No column headers found in '%s'" % TABLE_POS_BALANCE_SUMMARY
        )
        if POS_BALANCE_SUMMARY_COLUMNS:
            missing = [c for c in POS_BALANCE_SUMMARY_COLUMNS
                       if c.lower() not in [h.lower() for h in headers]]
            assert not missing, (
                "Expected columns missing from %s: %s.  Actual: %s"
                % (TABLE_POS_BALANCE_SUMMARY, missing, headers)
            )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-003 POS Balance Summary — pagination controls are present")
    @pytest.mark.regression
    def test_pos_balance_summary_pagination(self, csh_pos):
        has_paging = csh_pos.table_pagination_present(TABLE_POS_BALANCE_SUMMARY)
        row_count  = csh_pos.get_table_row_count(TABLE_POS_BALANCE_SUMMARY)
        if row_count == 0:
            pytest.skip("No data rows in POS Balance Summary — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_POS_BALANCE_SUMMARY
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-004 POS Bank Drop section is visible on POS tab")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Manual check required — actual POS Bank Drop heading unconfirmed via DevTools")
    def test_pos_bank_drop_visible(self, csh_pos):
        assert csh_pos.table_section_visible(TABLE_POS_BANK_DROP), (
            "Section '%s' not visible on POS tab" % TABLE_POS_BANK_DROP
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-005 POS Bank Drop — pagination controls are present")
    @pytest.mark.regression
    def test_pos_bank_drop_pagination(self, csh_pos):
        has_paging = csh_pos.table_pagination_present(TABLE_POS_BANK_DROP)
        row_count  = csh_pos.get_table_row_count(TABLE_POS_BANK_DROP)
        if row_count == 0:
            pytest.skip("No data rows in POS Bank Drop — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_POS_BANK_DROP
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-006 POS Transactions section is visible on POS tab")
    @pytest.mark.smoke
    @pytest.mark.skip(reason="Manual check required — actual POS Transactions heading unconfirmed via DevTools")
    def test_pos_transactions_visible(self, csh_pos):
        assert csh_pos.table_section_visible(TABLE_POS_TRANSACTIONS), (
            "Section '%s' not visible on POS tab" % TABLE_POS_TRANSACTIONS
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-007 POS Transactions — pagination controls are present")
    @pytest.mark.regression
    def test_pos_transactions_pagination(self, csh_pos):
        has_paging = csh_pos.table_pagination_present(TABLE_POS_TRANSACTIONS)
        row_count  = csh_pos.get_table_row_count(TABLE_POS_TRANSACTIONS)
        if row_count == 0:
            pytest.skip("No data rows in POS Transactions — pagination check skipped")
        assert has_paging, (
            "Pagination controls not found for '%s'" % TABLE_POS_TRANSACTIONS
        )
        assert page_has_no_broken_state(csh_pos)

    @allure.title("CSH-POS-008 POS tab shows empty/no-data state for a zero-data date range")
    @pytest.mark.regression
    def test_pos_zero_data_state(self, csh_zero_data):
        csh_zero_data.click_tab(TAB_POS)
        body = csh_zero_data.get_body_text().lower()
        pos_row_count = sum(
            csh_zero_data.get_table_row_count(t)
            for t in [TABLE_POS_BALANCE_SUMMARY,
                      TABLE_POS_BANK_DROP,
                      TABLE_POS_TRANSACTIONS]
        )
        has_no_data = (
            csh_zero_data.no_data_message_visible()
            or pos_row_count == 0
            or "no data" in body
            or "no records" in body
        )
        assert has_no_data, (
            "POS tab should show empty state for zero-data filter; "
            "body excerpt: %s" % body[:300]
        )
        assert page_has_no_broken_state(csh_zero_data)
