# Overview Automation Coverage Assessment - Sheet gid 1234567

Source: Google Sheet `1O9J30uR_LYABPJqcOGnX6Ve5RkE18uoiwliue_eOhDI`, tab `gid=1234567`

Generated: 2026-06-11

## 1. Executive Summary

The sheet tab contains 83 manual test cases for the Admin Portal Overview page. The current application shell at `https://staging.nxtwash.com/` loads successfully after login and mounts a legacy dashboard iframe, but the iframe body is empty in the automation run. Because of that, only the Overview shell, URL, support widget, browser back behavior, and new-tab shell behavior can be validated as passing automation today.

To avoid false coverage, the framework now includes strict `xfail` tests for the dashboard areas that are expected by the manual suite but not available in the current DOM: filters, exports, widgets, report navigation, data parity, no-data states, network failure handling, and rapid filter switching. These are executable traceability tests, but they are not counted as fully automated coverage until the underlying UI/API/test-data blockers are resolved.

Execution result:

`venv/bin/pytest tests/admin_portal/overview --headless --close-browser --alluredir=reports/allure-results-overview --clean-alluredir`

Result: `4 passed, 16 xfailed`

Allure report: `reports/allure-report-overview`

## 2. Framework Summary

| Area | Finding |
| --- | --- |
| Language | Python |
| UI automation | Selenium WebDriver |
| Test runner | Pytest |
| Reporting | Allure via `allure-pytest` |
| Design pattern | Page Object Model |
| Main page object | `pages/admin_portal/overview_page.py` |
| Tests | `tests/admin_portal/overview/` |
| Session setup | `tests/admin_portal/admin_session.py::ensure_admin_logged_in` |
| Synchronization | Explicit waits through `BasePage.wait` and Selenium expected conditions |
| Markers used | `smoke`, `sanity`, `regression`, `export` |

## 3. Code Evidence Summary

| Evidence | Reference |
| --- | --- |
| Overview shell waits | `pages/admin_portal/overview_page.py:73` |
| URL assertion helper | `pages/admin_portal/overview_page.py:86` |
| Legacy dashboard iframe detection | `pages/admin_portal/overview_page.py:134` |
| Dashboard iframe text extraction | `pages/admin_portal/overview_page.py:138` |
| Support widget assertion helper | `pages/admin_portal/overview_page.py:149` |
| Dashboard text helpers | `pages/admin_portal/overview_page.py:160`, `:164`, `:169` |
| Shared Overview login fixture | `tests/admin_portal/overview/conftest.py:7` |
| Shell and UI tests | `tests/admin_portal/overview/test_overview_ui.py:10` |
| Filter tests | `tests/admin_portal/overview/test_overview_filters.py:14` |
| Export tests | `tests/admin_portal/overview/test_overview_exports.py:14` |
| Widget tests | `tests/admin_portal/overview/test_overview_widgets.py:14` |
| Report tests | `tests/admin_portal/overview/test_overview_reports.py:14` |
| Navigation tests | `tests/admin_portal/overview/test_overview_navigation.py:10` |
| Data parity tests | `tests/admin_portal/overview/test_overview_data_validation.py:14` |
| Negative tests | `tests/admin_portal/overview/test_overview_negative.py:14` |

## 4. Coverage Matrix

Status meanings:

- Fully Automated: implemented and passed with assertions covering the expected result.
- Partially Automated: executable coverage exists, but one or more expected manual validations are missing or blocked.
- Not Fully Automated - Product Blocked: executable strict `xfail` exists, but the app did not expose the required dashboard element.
- Not Fully Automated - Framework Blocked: additional framework/test-data support is required.

| TC ID | Module | Manual Scenario | Automation File | Test Method | Coverage Status | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVERVIEW-UI-001 | UI | Redirect to Overview after login | test_overview_ui.py | test_overview_shell_redirects_and_loads | Partially Automated | Lines 10-16 | Shell, URL, iframe mount asserted. Dashboard content is blocked by empty iframe. |
| OVERVIEW-UI-002 | UI | Verify page URL | test_overview_ui.py | test_overview_shell_redirects_and_loads | Fully Automated | Lines 10-16 | URL asserted by `has_expected_url`. |
| OVERVIEW-UI-003 | UI | Filter controls displayed | test_overview_ui.py | test_overview_dashboard_filter_controls_visible | Not Fully Automated - Product Blocked | Lines 37-40 | Strict xfail because iframe body is empty. |
| OVERVIEW-UI-004 | UI | XLSX export button visible | test_overview_ui.py | test_overview_export_buttons_visible | Not Fully Automated - Product Blocked | Lines 52-53 | Strict xfail because export labels are unavailable. |
| OVERVIEW-UI-005 | UI | CSV export button visible | test_overview_ui.py | test_overview_export_buttons_visible | Not Fully Automated - Product Blocked | Lines 52-53 | Strict xfail because export labels are unavailable. |
| OVERVIEW-UI-006 | UI | Cars Washed widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Strict xfail because widget labels are unavailable. |
| OVERVIEW-UI-007 | UI | Revenue widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-008 | UI | Average Wash Ticket widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-009 | UI | Membership widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-010 | UI | Employees widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-011 | UI | Gift Cards widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-012 | UI | Labor widget visible | test_overview_ui.py | test_overview_dashboard_widgets_visible | Not Fully Automated - Product Blocked | Lines 65-68 | Same blocker. |
| OVERVIEW-UI-013 | UI | Support button visible | test_overview_ui.py | test_overview_support_button_is_visible | Fully Automated | Lines 24-25 | Support iframe text asserted. |
| OVERVIEW-FILTER-001 | Filter | Site dropdown opens | test_overview_filters.py | test_overview_site_filter_dropdown_opens | Not Fully Automated - Product Blocked | Lines 14-15 | Site control unavailable in empty iframe. |
| OVERVIEW-FILTER-002 | Filter | Site selection updates dashboard | test_overview_filters.py | test_overview_site_filter_updates_switches_and_persists | Not Fully Automated - Product Blocked | Lines 27-28 | Site control and dashboard values unavailable. |
| OVERVIEW-FILTER-003 | Filter | Switching sites shows correct data | test_overview_filters.py | test_overview_site_filter_updates_switches_and_persists | Not Fully Automated - Product Blocked | Lines 27-28 | Same blocker. |
| OVERVIEW-FILTER-004 | Filter | Site filter persists after refresh | test_overview_filters.py | test_overview_site_filter_updates_switches_and_persists | Not Fully Automated - Product Blocked | Lines 27-28 | Same blocker. |
| OVERVIEW-FILTER-005 | Filter | Today filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Date presets unavailable. |
| OVERVIEW-FILTER-006 | Filter | Yesterday filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-007 | Filter | This Week filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-008 | Filter | Last Week filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-009 | Filter | This Month filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-010 | Filter | Last Month filter | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-011 | Filter | Custom filter enables date picker | test_overview_filters.py | test_overview_date_preset_filters_are_available | Not Fully Automated - Product Blocked | Lines 40-51 | Same blocker. |
| OVERVIEW-FILTER-012 | Filter | Custom start/end date refreshes data | test_overview_filters.py | test_overview_date_range_filters_are_available | Not Fully Automated - Product Blocked | Lines 63-64 | Date range controls unavailable. |
| OVERVIEW-FILTER-013 | Filter | Same date range generates single-day report | test_overview_filters.py | test_overview_date_range_filters_are_available | Not Fully Automated - Product Blocked | Lines 63-64 | Same blocker. |
| OVERVIEW-FILTER-014 | Filter | Future date no-data/validation | test_overview_filters.py | test_overview_date_range_filters_are_available | Not Fully Automated - Product Blocked | Lines 63-64 | Same blocker; no no-data fixture. |
| OVERVIEW-FILTER-015 | Filter | Large one-year date range | test_overview_filters.py | test_overview_date_range_filters_are_available | Not Fully Automated - Product Blocked | Lines 63-64 | Same blocker. |
| OVERVIEW-FILTER-016 | Filter | Enable Single Day checkbox | test_overview_filters.py | test_overview_single_day_checkbox_is_available | Not Fully Automated - Product Blocked | Lines 76-77 | Checkbox unavailable. |
| OVERVIEW-FILTER-017 | Filter | Disable Single Day checkbox | test_overview_filters.py | test_overview_single_day_checkbox_is_available | Not Fully Automated - Product Blocked | Lines 76-77 | Same blocker. |
| OVERVIEW-EXPORT-001 | Export | XLSX button clickable | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Export controls unavailable. |
| OVERVIEW-EXPORT-002 | Export | XLSX downloaded | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Export control unavailable; download verification utility not used. |
| OVERVIEW-EXPORT-003 | Export | XLSX filename | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Same blocker. |
| OVERVIEW-EXPORT-004 | Export | XLSX data matches filters | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Framework Blocked | Lines 14-15 | Needs export file parser plus rendered dashboard. |
| OVERVIEW-EXPORT-005 | Export | CSV export | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Export controls unavailable. |
| OVERVIEW-EXPORT-006 | Export | CSV filename | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Same blocker. |
| OVERVIEW-EXPORT-007 | Export | CSV content | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Framework Blocked | Lines 14-15 | Needs CSV parser plus rendered dashboard. |
| OVERVIEW-EXPORT-008 | Export | Export after site filter | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Site filter/export controls unavailable. |
| OVERVIEW-EXPORT-009 | Export | Export after custom date range | test_overview_exports.py | test_overview_exports_are_available_and_filter_aware | Not Fully Automated - Product Blocked | Lines 14-15 | Date/export controls unavailable. |
| OVERVIEW-WIDGET-001 | Widget | Cars Washed card visible | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Widgets unavailable. |
| OVERVIEW-WIDGET-002 | Widget | Cars Washed metrics | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-003 | Widget | Cars graph renders | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker; graph-specific canvas/SVG assertion needed later. |
| OVERVIEW-WIDGET-004 | Widget | Graph updates after filter | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-005 | Widget | Revenue card visible | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-006 | Widget | Revenue values displayed | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-007 | Widget | Pie chart renders | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker; chart assertion needed later. |
| OVERVIEW-WIDGET-008 | Widget | Membership toggle available | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-009 | Widget | Toggle updates chart | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-010 | Widget | AWT metrics | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-011 | Widget | Breakdown list | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-012 | Widget | Membership metrics | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-013 | Widget | Progress bars | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker; progress assertion needed later. |
| OVERVIEW-WIDGET-014 | Widget | Employees table | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-015 | Widget | Employee columns | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-016 | Widget | Employee table scrolling | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-017 | Widget | Gift Card Sales | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-018 | Widget | Redemptions | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-019 | Widget | Total Labor % | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-020 | Widget | Dollars per car | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-WIDGET-021 | Widget | Cars per labor hour | test_overview_widgets.py | test_overview_widgets_and_metrics_render | Not Fully Automated - Product Blocked | Lines 14-30 | Same blocker. |
| OVERVIEW-REPORT-001 | Report | Cars Washed full report opens | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Full report links unavailable. |
| OVERVIEW-REPORT-002 | Report | Filter modal displayed | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Report link/modal unavailable. |
| OVERVIEW-REPORT-003 | Report | Apply filters works | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-REPORT-004 | Report | Report reflects filters | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-REPORT-005 | Report | Revenue full report opens | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-REPORT-006 | Report | Revenue report data loads | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-REPORT-007 | Report | Employee full report opens | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-REPORT-008 | Report | Labor full report opens | test_overview_reports.py | test_overview_full_report_links_are_available | Not Fully Automated - Product Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-NAV-001 | Navigation | Cars Washed Full Report URL | test_overview_navigation.py | test_overview_report_navigation_is_available | Not Fully Automated - Product Blocked | Lines 43-46 | Report link unavailable. |
| OVERVIEW-NAV-002 | Navigation | Browser back returns to Overview | test_overview_navigation.py | test_overview_browser_back_returns_to_overview | Fully Automated | Lines 10-17 | Back navigation and shell state asserted. |
| OVERVIEW-NAV-003 | Navigation | Refresh on report page functional | test_overview_navigation.py | test_overview_report_navigation_is_available | Not Fully Automated - Product Blocked | Lines 43-46 | Report page unavailable. |
| OVERVIEW-NAV-004 | Navigation | Open report in new tab | test_overview_navigation.py | test_overview_opens_in_new_tab | Partially Automated | Lines 25-31 | New tab shell works; report-specific new-tab flow blocked by missing report links. |
| OVERVIEW-DATA-001 | Data | Cars Washed equals API | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Requires Overview API client and rendered widget. |
| OVERVIEW-DATA-002 | Data | Revenue equals API | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-DATA-003 | Data | Membership totals equal API | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-DATA-004 | Data | Employee count matches API | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Same blocker. |
| OVERVIEW-DATA-005 | Data | CSV equals dashboard | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Needs CSV parser and rendered dashboard. |
| OVERVIEW-DATA-006 | Data | XLSX equals dashboard | test_overview_data_validation.py | test_overview_dashboard_data_matches_api_and_exports | Not Fully Automated - Framework Blocked | Lines 14-17 | Needs XLSX parser and rendered dashboard. |
| OVERVIEW-NEG-001 | Negative | Site with no data | test_overview_negative.py | test_overview_no_data_states_are_handled | Not Fully Automated - Product Blocked | Lines 14-15 | Needs no-data site fixture and dashboard controls. |
| OVERVIEW-NEG-002 | Negative | Future date range | test_overview_negative.py | test_overview_no_data_states_are_handled | Not Fully Automated - Product Blocked | Lines 14-15 | Needs date controls and no-data state. |
| OVERVIEW-NEG-003 | Negative | Network disconnect during filters | test_overview_negative.py | test_overview_network_failure_is_handled | Not Fully Automated - Framework Blocked | Lines 27-28 | Needs network interception helper. |
| OVERVIEW-NEG-004 | Negative | Export no data | test_overview_negative.py | test_overview_no_data_states_are_handled | Not Fully Automated - Product Blocked | Lines 14-15 | Needs export controls and no-data state. |
| OVERVIEW-NEG-005 | Negative | Rapidly switch filters | test_overview_negative.py | test_overview_rapid_filter_switching_does_not_crash | Not Fully Automated - Product Blocked | Lines 40-42 | Needs available filter controls. |

## 5. Coverage Metrics

| Metric | Count |
| --- | ---: |
| Total manual test cases | 83 |
| Fully automated and passing | 3 |
| Partially automated and passing | 2 |
| Strict xfail product-blocked traceability tests | 68 |
| Strict xfail framework/test-data-blocked traceability tests | 10 |
| Not mapped to executable test | 0 |
| Duplicate manual cases identified | 7 near-duplicate/overlapping scenarios |
| Obsolete manual cases identified | 0 confirmed |

Coverage percentage: `3 / 83 * 100 = 3.61%`

Effective passing coverage including partial shell-only checks: `5 / 83 * 100 = 6.02%`

Executable traceability exists for all 83 cases, but 78 cases are not counted as automated coverage because their expected behavior cannot currently be validated.

## 6. Gap Analysis

### Missing or Blocked Coverage

- Dashboard iframe content is empty in automation, blocking filters, widgets, exports, reports, no-data states, and rapid filter behavior.
- No Overview API client exists for data parity tests.
- No CSV/XLSX parser is currently wired into Overview assertions.
- No no-data site fixture exists.
- No network interception utility exists for Overview filter request failure testing.
- Report page locators and page objects cannot be completed until report links render.

### Duplicate Manual Cases

| Manual Cases | Recommendation |
| --- | --- |
| OVERVIEW-UI-006 and OVERVIEW-WIDGET-001 | Keep one widget visibility test and make UI test a shell-level smoke assertion. |
| OVERVIEW-UI-007 and OVERVIEW-WIDGET-005 | Same consolidation pattern. |
| OVERVIEW-UI-009 and OVERVIEW-WIDGET-012 | Same consolidation pattern. |
| OVERVIEW-FILTER-014 and OVERVIEW-NEG-002 | Consolidate future-date no-data validation. |
| OVERVIEW-EXPORT-004 and OVERVIEW-DATA-006 | Keep export file generation and data parity as separate assertions in one export parity test. |
| OVERVIEW-EXPORT-007 and OVERVIEW-DATA-005 | Same pattern for CSV. |
| OVERVIEW-REPORT-001 and OVERVIEW-NAV-001 | Use one report navigation helper and assert both URL and page load. |

### Duplicate Automation Removed

The legacy shell-only `tests/admin_portal/overview/test_overview.py` was removed after its shell checks were consolidated into the structured Overview suite.

## 7. Automation Improvement Plan

| Priority Rank | Test Cases | Business Impact | Effort | Recommendation |
| ---: | --- | --- | --- | --- |
| 1 | UI-003 to UI-012, FILTER-001 to FILTER-017 | High | Large | Fix legacy dashboard iframe rendering or expose dashboard in the current app shell. Then replace xfail assertions with direct POM interactions. |
| 2 | EXPORT-001 to EXPORT-009 | High | Medium | Add download helper, filename assertions, CSV/XLSX readers, and filter-aware export validation. |
| 3 | WIDGET-001 to WIDGET-021 | High | Large | Add widget-specific locators, chart render assertions, numeric value assertions, and filter-update comparisons. |
| 4 | REPORT-001 to REPORT-008, NAV-001, NAV-003, NAV-004 | Medium | Large | Add Overview report page objects once report links render; assert URLs, modals, filters, and refresh/new-tab behavior. |
| 5 | DATA-001 to DATA-006 | Medium | Large | Add authenticated API client for Overview metrics and compare UI/export values with API responses. |
| 6 | NEG-001, NEG-002, NEG-004, NEG-005 | Medium | Medium | Add no-data fixture and dashboard filter helpers. |
| 7 | NEG-003 | Medium | Medium | Add Selenium/CDP or proxy-based network interception utility for request failure validation. |

## 8. Generated Automation

The following production-ready automation assets were added:

- `tests/admin_portal/overview/conftest.py`
- `tests/admin_portal/overview/test_overview_ui.py`
- `tests/admin_portal/overview/test_overview_filters.py`
- `tests/admin_portal/overview/test_overview_exports.py`
- `tests/admin_portal/overview/test_overview_widgets.py`
- `tests/admin_portal/overview/test_overview_reports.py`
- `tests/admin_portal/overview/test_overview_navigation.py`
- `tests/admin_portal/overview/test_overview_data_validation.py`
- `tests/admin_portal/overview/test_overview_negative.py`

The strict `xfail` tests intentionally preserve traceability without creating false positives. When the dashboard becomes accessible, the `xfail` markers should be removed and each test expanded from text presence assertions into direct field-level interactions and value assertions.

## 9. Risks and Blockers

- Google Sheet CSV export does not expose hidden/grouped/filtered row metadata; hidden rows cannot be independently verified from CSV.
- The legacy dashboard iframe is empty during automation, which blocks most functional Overview coverage.
- API parity tests require API endpoints, auth reuse, and stable fixture data.
- Export parity tests require controlled download directory setup and file parsers.
- Network failure tests require a reusable network interception utility.

