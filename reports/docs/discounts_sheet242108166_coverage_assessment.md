# Discounts Coverage Assessment - Sheet gid 242108166

## Executive Summary
- Manual inventory extracted from CSV export: 60 rows.
- The sheet has a reduced schema: TC ID, Feature, Suite, Priority, Automation, Scenario, Expected Result, Future Integration.
- Requirement ID, Test File, Marker, Execution Tier, Allure Epic/Feature/Story, Data Strategy, Cleanup Strategy, and Automation Complexity are not present in this sheet tab.
- Coverage is marked only where executable Selenium/Pytest assertions exist in the repository.
- Existing Discount tests were updated with Allure metadata and pytest markers; one new clear-search regression was added.
- Full Allure report generated: `reports/allure-report-discounts-sheet242108166-full`.

## Framework Summary
- Language: Python.
- Automation: Selenium WebDriver with Pytest.
- Design pattern: Page Object Model.
- Reporting: Allure via `allure-pytest`; root framework captures screenshots, page source, current URL, and logs on failure.
- Environment handling: existing `open_admin_path` helper is used; no hardcoded application URLs were added.
- Stability rule followed: no custom login retry logic was added.
- Data strategy: Discounts use an existing managed fixture in `tests/admin_portal/discounts/conftest.py` via `managed_discount`; idempotent setup is used for `VK AD02`.

## Test Execution
- Command: `venv/bin/pytest tests/admin_portal/discounts --headless --close-browser --alluredir=reports/allure-results-discounts-sheet242108166-full --clean-alluredir`
- Result: 21 passed, 1 xfailed in 494.22s.
- The xfail is intentional for `DS-RG-002 Partial Search`, because the product currently returns no records for a known partial discount search.

## Files Changed
- `pages/admin_portal/discounts_page.py`: added `clear_discount_search`, `get_visible_discount_names`, and stale-element retry in `open_edit_discount`.
- Discount test files: added Allure metadata/markers and `test_discounts_exact_search_clear_restores_records`.

## Coverage Metrics
- Total manual tests: 60
- Fully Covered: 9
- Partially Covered: 11
- Not Covered: 40
- Framework Non-Compliant: 0
- Coverage %: 15.00%

### Suite Coverage
| Suite | Total | Fully Covered | Partially Covered | Not Covered | Framework Non-Compliant |
| --- | ---: | ---: | ---: | ---: | ---: |
| Combination | 6 | 1 | 0 | 5 | 0 |
| Dependency | 5 | 0 | 0 | 5 | 0 |
| Edge | 8 | 0 | 1 | 7 | 0 |
| Edit Flow | 6 | 0 | 0 | 6 | 0 |
| Export | 4 | 0 | 1 | 3 | 0 |
| Filter | 6 | 1 | 5 | 0 | 0 |
| Future E2E | 5 | 0 | 0 | 5 | 0 |
| Happy Path | 7 | 4 | 1 | 2 | 0 |
| Negative | 5 | 0 | 1 | 4 | 0 |
| Persistence | 4 | 2 | 0 | 2 | 0 |
| Search | 4 | 1 | 2 | 1 | 0 |

## Gap Analysis
- Missing automation: percentage discount creation, all-location persistence, deactivate/reactivate status transitions, end-date scheduling, export file validation, dependency flows, POS/Kiosk/Reports/Dashboard integration, and most edit/edge combinations.
- Partial coverage: filter panel visibility exists, but filtered record correctness is not asserted. Export button visibility exists, but exported content is not parsed or compared.
- Framework compliance gaps: mapped Discount tests now include Allure metadata and pytest markers.
- Data gaps: inactive discount, all-location discount, percentage discount, and end-date fixtures are not managed. Cross-module dependencies need stable service category/site fixtures.
- Product/contract gap: partial discount search is captured as a strict xfail because the current UI returned zero records for a known partial search.

## Prioritized Improvement Plan
| Rank | Test Case IDs | Impact | Coverage Gain | Effort | Recommendation |
| ---: | --- | --- | --- | --- | --- |
| 1 | DS-HP-002, DS-CMB-003, DS-CMB-004 | High | High | Medium | Add percentage-discount POM support and managed percentage fixture. |
| 2 | DS-HP-003, DS-CMB-001, DS-UPD-010, DS-UPD-011 | High | High | Medium | Add all-locations/selected-locations reversible managed tests. |
| 3 | DS-HP-007, DS-PER-004, DS-SRH-004, DS-FLT-006 | High | Medium | Medium | Add active/inactive state fixture and status transition assertions. |
| 4 | DS-RG-005, EXP-006..008 | Medium | Medium | Medium | Add download directory fixture and CSV/XLS parser to verify export content. |
| 5 | DS-NG-001..005 | Medium | Medium | Medium | Add scenario-specific validation message/save-block checks. |
| 6 | DS-DEP-001..005, FUT-001..005 | High | Medium | Large | Add cross-module/API fixtures before POS/Kiosk/Reports/Dashboard integration coverage. |

## Coverage Matrix
| TC ID | Feature | Suite | Priority | Automation Flag | Scenario | Expected Result | Status | Evidence | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS-HP-001 | Discount | Happy Path | P0 | Yes | Create Amount Discount | Created successfully | Fully Covered | tests/admin_portal/discounts/test_discounts_positive.py::test_create_amount_discount line 21; POM create_discount/fill_discount_form in pages/admin_portal/discounts_page.py; fixture create_discount_if_missing line 42 | Creates/ensures amount discount, asserts row displayed and Active status. |
| DS-HP-002 | Discount | Happy Path | P0 | Yes | Create Percentage Discount | Created successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-HP-003 | Discount | Happy Path | P0 | Yes | Assign All Locations | Saved correctly | Partially Covered | pages/admin_portal/discounts_page.py::ensure_all_locations_switch_on exists, but create flow uses selected first location | All-location switch support exists in POM, but no test asserts all-location save/persistence. |
| DS-HP-004 | Discount | Happy Path | P0 | Yes | Assign Specific Locations | Saved correctly | Fully Covered | tests/admin_portal/discounts/test_discounts_edge_cases.py::test_discount_first_location_settings_persist line 29; POM location_is_assigned_by_index/get_location_discount_value_by_index | Specific first-location assignment and value persistence are asserted. |
| DS-HP-005 | Discount | Happy Path | P0 | Yes | Edit Discount Value | Updated successfully | Fully Covered | tests/admin_portal/discounts/test_discounts_edit.py::test_edit_discount_reapplies_expected_settings line 24; POM open_edit_discount line 230 and update_discount | Edit/update flow asserts name, amount type, amount value, and active state. |
| DS-HP-006 | Discount | Happy Path | P0 | Yes | Activate Discount | Available | Fully Covered | tests/admin_portal/discounts/test_discounts_positive.py::test_create_amount_discount line 21; get_discount_status assertion | Active discount status is asserted after create/ensure. |
| DS-HP-007 | Discount | Happy Path | P0 | Yes | Deactivate Discount | Unavailable | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-CMB-001 | Discount | Combination | P0 | Yes | Amount + All Locations + Active | Saved correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-CMB-002 | Discount | Combination | P0 | Yes | Amount + Selected Locations + Active | Saved correctly | Fully Covered | tests/admin_portal/discounts/test_discounts_edge_cases.py::test_discount_first_location_settings_persist line 29 and test_discounts_positive.py::test_discount_settings_persist line 33 | Amount + selected location + active behavior is asserted for the idempotent test record. |
| DS-CMB-003 | Discount | Combination | P0 | Yes | Percentage + All Locations + Active | Saved correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-CMB-004 | Discount | Combination | P0 | Yes | Percentage + Selected Locations + Active | Saved correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-CMB-005 | Discount | Combination | P1 | Yes | Percentage + Future Start Date | Scheduled correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-CMB-006 | Discount | Combination | P1 | Yes | Amount + End Date | Expiry retained | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-RG-001 | Discount | Search | P1 | Yes | Search Exact Discount | Correct result | Fully Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_existing_search line 21 | Exact search asserts expected row is displayed. |
| DS-RG-002 | Discount | Search | P1 | Yes | Search Partial Discount | Matching results | Not Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_partial_search_blocker line 56 is strict xfail | Partial search currently returns no records for a known discount; visible product/contract gap, not counted as covered. |
| DS-RG-003 | Discount | Filter | P1 | Yes | Filter Active | Correct records | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | Filter panel controls are asserted, but active-filter result correctness is not asserted. |
| DS-RG-004 | Discount | Filter | P1 | Yes | Filter By Site | Correct records | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | Filter panel availability is covered; filtered result correctness for this scenario is not asserted. |
| DS-RG-005 | Discount | Export | P1 | Yes | Export Discounts | Export matches grid | Partially Covered | tests/admin_portal/discounts/test_discounts_ui.py::test_discounts_page_loads_with_primary_controls line 17; POM download_button_is_clickable | Download button is asserted clickable; downloaded file/grid parity is not automated. |
| DS-NG-001 | Discount | Negative | P1 | Yes | Create Without Category | Validation shown | Not Covered | Validation tests exist but do not match this scenario exactly | Scenario-specific validation message/save-block behavior is not automated. |
| DS-NG-002 | Discount | Negative | P1 | Yes | Create Without Value | Validation shown | Partially Covered | tests/admin_portal/discounts/test_discounts_validation.py::test_discount_invalid_amount_does_not_break_form line 40 | Invalid amount stability is checked, but required value validation message is not asserted. |
| DS-NG-003 | Discount | Negative | P1 | Yes | Start Date After End Date | Validation shown | Not Covered | Validation tests exist but do not match this scenario exactly | Scenario-specific validation message/save-block behavior is not automated. |
| DS-NG-004 | Discount | Negative | P1 | Yes | Percentage Above Limit | Rule enforced | Not Covered | Validation tests exist but do not match this scenario exactly | Scenario-specific validation message/save-block behavior is not automated. |
| DS-NG-005 | Discount | Negative | P1 | Yes | No Location When Required | Validation shown | Not Covered | Validation tests exist but do not match this scenario exactly | Scenario-specific validation message/save-block behavior is not automated. |
| DS-EC-001 | Discount | Edge | P1 | Yes | 0 Percent Discount | Boundary handled | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-002 | Discount | Edge | P1 | Yes | 100 Percent Discount | Boundary handled | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-003 | Discount | Edge | P1 | Yes | Future Start Date | Retained correctly | Partially Covered | tests/admin_portal/discounts/test_discounts_positive.py::test_discount_settings_persist line 33; START_VALUE assertion | Configured start date is retained, but broad future-date scheduling behavior is not fully covered. |
| DS-EC-004 | Discount | Edge | P1 | Yes | Discount Expiring Today | Handled correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-005 | Discount | Edge | P1 | Yes | Amount To Percentage | Updated correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-006 | Discount | Edge | P1 | Yes | Percentage To Amount | Updated correctly | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-007 | Discount | Edge | P1 | Yes | Remove Assigned Location | Assignment removed | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-EC-008 | Discount | Edge | P1 | Yes | Add Location To Existing Discount | Assignment saved | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-006 | Discount | Edit Flow | P1 | Yes | Change Discount Name | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-007 | Discount | Edit Flow | P1 | Yes | Change Start Date | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-008 | Discount | Edit Flow | P1 | Yes | Change End Date | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-009 | Discount | Edit Flow | P1 | Yes | Change Category Assignment | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-010 | Discount | Edit Flow | P1 | Yes | Selected Locations To All Locations | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-UPD-011 | Discount | Edit Flow | P1 | Yes | All Locations To Selected Locations | Updated successfully | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-PER-001 | Discount | Persistence | P1 | Yes | Create Then Refresh | Data persists | Fully Covered | tests/admin_portal/discounts/test_discounts_positive.py::test_discount_settings_persist line 33 | Created/ensured discount is reopened and persisted fields are asserted. |
| DS-PER-002 | Discount | Persistence | P1 | Yes | Create Then Re-login | Data persists | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-PER-003 | Discount | Persistence | P1 | Yes | Edit Then Refresh | Changes persist | Fully Covered | tests/admin_portal/discounts/test_discounts_edit.py::test_edit_discount_reapplies_expected_settings line 24 | Edit flow saves and reopens the discount to assert persisted values. |
| DS-PER-004 | Discount | Persistence | P1 | Yes | Deactivate Then Refresh | Status persists | Not Covered | No executable test method mapped | No matching executable automation with all required steps and expected result assertions exists. |
| DS-SRH-004 | Discount | Search | P2 | Yes | Search Inactive Discount | Correct result | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py search tests lines 21, 32, 56, 66, 93 | Exact/missing/payload/clear coverage exists; this specific search scenario is not fully asserted. |
| DS-SRH-005 | Discount | Search | P2 | Yes | Search After Edit | Updated result | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py search tests lines 21, 32, 56, 66, 93 | Exact/missing/payload/clear coverage exists; this specific search scenario is not fully asserted. |
| DS-FLT-005 | Discount | Filter | P2 | Yes | Filter Active + Site | Correct subset | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | Filter panel availability is covered; filtered result correctness for this scenario is not asserted. |
| DS-FLT-006 | Discount | Filter | P2 | Yes | Filter Inactive + Site | Correct subset | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | Filter panel availability is covered; filtered result correctness for this scenario is not asserted. |
| DS-FLT-007 | Discount | Filter | P2 | Yes | Clear Filters | Grid resets | Fully Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_exact_search_clear_restores_records line 32; POM clear_discount_search line 168 | Search clear restores grid records. Filter clear itself is not covered. |
| DS-FLT-008 | Discount | Filter | P2 | Yes | Search + Filter Together | Correct subset | Partially Covered | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | Filter panel availability is covered; filtered result correctness for this scenario is not asserted. |
| EXP-006 | Discount | Export | P2 | Yes | Export After Filter | Matches filter | Not Covered | No file download/parsing assertion exists | Export scenarios require download directory control and CSV/XLS parsing utility; only button visibility is covered elsewhere. |
| EXP-007 | Discount | Export | P2 | Yes | Verify Export Record Count | Count matches grid | Not Covered | No file download/parsing assertion exists | Export scenarios require download directory control and CSV/XLS parsing utility; only button visibility is covered elsewhere. |
| EXP-008 | Discount | Export | P2 | Yes | Verify Export Data Matches Grid | Data matches | Not Covered | No file download/parsing assertion exists | Export scenarios require download directory control and CSV/XLS parsing utility; only button visibility is covered elsewhere. |
| DS-DEP-001 | Discount | Dependency | P0 | Yes | Category To Discount Flow | Linked correctly | Not Covered | No executable cross-module automation mapped | Requires cross-module service/category/site/POS/Kiosk/report workflow and controlled fixtures not present in current module. |
| DS-DEP-002 | Discount | Dependency | P0 | Yes | Rename Linked Category | Link maintained | Not Covered | No executable cross-module automation mapped | Requires cross-module service/category/site/POS/Kiosk/report workflow and controlled fixtures not present in current module. |
| DS-DEP-003 | Discount | Dependency | P0 | Yes | Deactivate Linked Category | Rule enforced | Not Covered | No executable cross-module automation mapped | Requires cross-module service/category/site/POS/Kiosk/report workflow and controlled fixtures not present in current module. |
| DS-DEP-004 | Discount | Dependency | P0 | Yes | Deactivate Assigned Site | Handled correctly | Not Covered | No executable cross-module automation mapped | Requires cross-module service/category/site/POS/Kiosk/report workflow and controlled fixtures not present in current module. |
| DS-DEP-005 | Discount | Dependency | P0 | Yes | Edit Site Assignment | Retained correctly | Not Covered | No executable cross-module automation mapped | Requires cross-module service/category/site/POS/Kiosk/report workflow and controlled fixtures not present in current module. |
| FUT-001 | Future | Future E2E | P0 | Planned | Category To Future Service Config | Pending | Not Covered | No executable Admin Portal automation mapped | Future/POS/Kiosk/Reports/Dashboard integration scenario is planned and outside current Admin Portal UI coverage. |
| FUT-002 | Future | Future E2E | P0 | Planned | Discount Visible In POS | Pending | Not Covered | No executable Admin Portal automation mapped | Future/POS/Kiosk/Reports/Dashboard integration scenario is planned and outside current Admin Portal UI coverage. |
| FUT-003 | Future | Future E2E | P0 | Planned | Discount Visible In Kiosk | Pending | Not Covered | No executable Admin Portal automation mapped | Future/POS/Kiosk/Reports/Dashboard integration scenario is planned and outside current Admin Portal UI coverage. |
| FUT-004 | Future | Future E2E | P0 | Planned | Discount Reflected In Reports | Pending | Not Covered | No executable Admin Portal automation mapped | Future/POS/Kiosk/Reports/Dashboard integration scenario is planned and outside current Admin Portal UI coverage. |
| FUT-005 | Future | Future E2E | P0 | Planned | Discount Reflected In Dashboard | Pending | Not Covered | No executable Admin Portal automation mapped | Future/POS/Kiosk/Reports/Dashboard integration scenario is planned and outside current Admin Portal UI coverage. |

## Traceability Matrix
| Test Case ID | Manual Test | Automated Test | File | Status |
| --- | --- | --- | --- | --- |
| DS-HP-001 | Create Amount Discount | tests/admin_portal/discounts/test_discounts_positive.py::test_create_amount_discount line 21 | tests/admin_portal/discounts + pages/admin_portal/discounts_page.py | Fully Covered |
| DS-HP-002 | Create Percentage Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-HP-003 | Assign All Locations | pages/admin_portal/discounts_page.py::ensure_all_locations_switch_on exists, but create flow uses selected first location | tests/admin_portal/discounts + pages/admin_portal/discounts_page.py | Partially Covered |
| DS-HP-004 | Assign Specific Locations | tests/admin_portal/discounts/test_discounts_edge_cases.py::test_discount_first_location_settings_persist line 29 | tests/admin_portal/discounts | Fully Covered |
| DS-HP-005 | Edit Discount Value | tests/admin_portal/discounts/test_discounts_edit.py::test_edit_discount_reapplies_expected_settings line 24 | tests/admin_portal/discounts | Fully Covered |
| DS-HP-006 | Activate Discount | tests/admin_portal/discounts/test_discounts_positive.py::test_create_amount_discount line 21 | tests/admin_portal/discounts | Fully Covered |
| DS-HP-007 | Deactivate Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-CMB-001 | Amount + All Locations + Active | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-CMB-002 | Amount + Selected Locations + Active | tests/admin_portal/discounts/test_discounts_edge_cases.py::test_discount_first_location_settings_persist line 29 and test_discounts_positive.py::test_discount_settings_persist line 33 | tests/admin_portal/discounts | Fully Covered |
| DS-CMB-003 | Percentage + All Locations + Active | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-CMB-004 | Percentage + Selected Locations + Active | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-CMB-005 | Percentage + Future Start Date | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-CMB-006 | Amount + End Date | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-RG-001 | Search Exact Discount | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_existing_search line 21 | tests/admin_portal/discounts | Fully Covered |
| DS-RG-002 | Search Partial Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-RG-003 | Filter Active | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | tests/admin_portal/discounts | Partially Covered |
| DS-RG-004 | Filter By Site | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | tests/admin_portal/discounts | Partially Covered |
| DS-RG-005 | Export Discounts | tests/admin_portal/discounts/test_discounts_ui.py::test_discounts_page_loads_with_primary_controls line 17 | tests/admin_portal/discounts | Partially Covered |
| DS-NG-001 | Create Without Category | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-NG-002 | Create Without Value | tests/admin_portal/discounts/test_discounts_validation.py::test_discount_invalid_amount_does_not_break_form line 40 | tests/admin_portal/discounts | Partially Covered |
| DS-NG-003 | Start Date After End Date | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-NG-004 | Percentage Above Limit | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-NG-005 | No Location When Required | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-001 | 0 Percent Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-002 | 100 Percent Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-003 | Future Start Date | tests/admin_portal/discounts/test_discounts_positive.py::test_discount_settings_persist line 33 | tests/admin_portal/discounts | Partially Covered |
| DS-EC-004 | Discount Expiring Today | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-005 | Amount To Percentage | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-006 | Percentage To Amount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-007 | Remove Assigned Location | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-EC-008 | Add Location To Existing Discount | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-006 | Change Discount Name | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-007 | Change Start Date | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-008 | Change End Date | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-009 | Change Category Assignment | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-010 | Selected Locations To All Locations | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-UPD-011 | All Locations To Selected Locations | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-PER-001 | Create Then Refresh | tests/admin_portal/discounts/test_discounts_positive.py::test_discount_settings_persist line 33 | tests/admin_portal/discounts | Fully Covered |
| DS-PER-002 | Create Then Re-login | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-PER-003 | Edit Then Refresh | tests/admin_portal/discounts/test_discounts_edit.py::test_edit_discount_reapplies_expected_settings line 24 | tests/admin_portal/discounts | Fully Covered |
| DS-PER-004 | Deactivate Then Refresh | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-SRH-004 | Search Inactive Discount | tests/admin_portal/discounts/test_discounts_search_filter.py search tests lines 21, 32, 56, 66, 93 | tests/admin_portal/discounts | Partially Covered |
| DS-SRH-005 | Search After Edit | tests/admin_portal/discounts/test_discounts_search_filter.py search tests lines 21, 32, 56, 66, 93 | tests/admin_portal/discounts | Partially Covered |
| DS-FLT-005 | Filter Active + Site | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | tests/admin_portal/discounts | Partially Covered |
| DS-FLT-006 | Filter Inactive + Site | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | tests/admin_portal/discounts | Partially Covered |
| DS-FLT-007 | Clear Filters | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_exact_search_clear_restores_records line 32 | tests/admin_portal/discounts | Fully Covered |
| DS-FLT-008 | Search + Filter Together | tests/admin_portal/discounts/test_discounts_search_filter.py::test_discounts_filter_panel_shows_controls line 78 | tests/admin_portal/discounts | Partially Covered |
| EXP-006 | Export After Filter | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| EXP-007 | Verify Export Record Count | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| EXP-008 | Verify Export Data Matches Grid | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-DEP-001 | Category To Discount Flow | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-DEP-002 | Rename Linked Category | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-DEP-003 | Deactivate Linked Category | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-DEP-004 | Deactivate Assigned Site | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| DS-DEP-005 | Edit Site Assignment | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| FUT-001 | Category To Future Service Config | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| FUT-002 | Discount Visible In POS | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| FUT-003 | Discount Visible In Kiosk | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| FUT-004 | Discount Reflected In Reports | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |
| FUT-005 | Discount Reflected In Dashboard | Not implemented; see gap notes | tests/admin_portal/discounts | Not Covered |

## Assumptions, Blockers, Dependencies
- The Google Sheet was read through CSV export; CSV export does not expose hidden/grouped/filtered row state, so this audit accounts for all exported rows.
- Sheet metadata required by the prompt is partially unavailable in this tab; missing metadata is documented rather than invented.
- Tests marked xfail are not counted as covered.
- Export coverage needs a download-path fixture and file parser before exported data can be compared to the grid.
- POS/Kiosk/Reports/Dashboard scenarios are future integration tests and require cross-application fixtures or APIs.
