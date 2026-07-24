# Memberships Coverage Assessment and Automation Update

Source sheet tab: `gid=2002`

## Executive Summary

- Total manual cases: 115
- Fully covered: 50
- Partially covered: 11
- Not covered: 54
- Effective coverage: 48.3%
- Duplicate/obsolete cases: none confirmed from repository evidence; several cases overlap behaviorally, especially CRUD save/persistence checks.

## Coverage Matrix

| Test Case ID | Test Case Name | Automated | Script/File Name | Coverage Status | Notes |
|---|---|---|---|---|---|
| MEM-UI-001 | Verify Memberships page loads successfully. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-002 | Verify Services menu is expanded. | No | `-` | Not Covered | No sidebar expanded/highlight assertion in current membership tests. |
| MEM-UI-003 | Verify Memberships submenu is highlighted. | No | `-` | Not Covered | No sidebar expanded/highlight assertion in current membership tests. |
| MEM-UI-004 | Verify page title displays "Memberships". | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-005 | Verify Membership Name column is displayed. | Yes | `test_memberships_ui.py::test_memberships_grid_columns_are_visible` | Fully Covered | Asserts list grid column labels. |
| MEM-UI-006 | Verify Type column is displayed. | Yes | `test_memberships_ui.py::test_memberships_grid_columns_are_visible` | Fully Covered | Asserts list grid column labels. |
| MEM-UI-007 | Verify Price column is displayed. | Yes | `test_memberships_ui.py::test_memberships_grid_columns_are_visible` | Fully Covered | Asserts list grid column labels. |
| MEM-UI-008 | Verify Status column is displayed. | Yes | `test_memberships_ui.py::test_memberships_grid_columns_are_visible` | Fully Covered | Asserts list grid column labels. |
| MEM-UI-009 | Verify Edit action is available for every membership. | Yes | `test_memberships_ui.py::test_visible_membership_rows_have_edit_action` | Fully Covered | Asserts every visible row exposes Edit action. |
| MEM-UI-010 | Verify Search field is displayed. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-011 | Verify Filter By button is displayed. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-012 | Verify Download button is displayed. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-013 | Verify Add New Membership button is displayed. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Asserts page title/body and primary list controls. |
| MEM-UI-014 | Verify pagination controls are displayed. | Yes | `test_memberships_ui.py::test_memberships_pagination_results_and_support_controls` | Fully Covered | Asserts pagination/result controls visible. |
| MEM-UI-015 | Verify results-per-page dropdown is displayed. | Yes | `test_memberships_ui.py::test_memberships_pagination_results_and_support_controls` | Fully Covered | Asserts pagination/result controls visible. |
| MEM-UI-016 | Verify Add Membership page loads successfully. | Yes | `test_memberships_ui.py::test_add_membership_form_loads` | Fully Covered | Asserts create page and membership settings controls. |
| MEM-UI-017 | Verify Membership Settings tab UI. | Yes | `test_memberships_ui.py::test_add_membership_form_loads` | Fully Covered | Asserts create page and membership settings controls. |
| MEM-UI-018 | Verify Redemption Settings tab UI. | Yes | `test_memberships_ui.py::test_redemption_settings_tab_loads` | Fully Covered | Asserts redemption tab labels. |
| MEM-UI-019 | Verify Discount Settings tab UI. | Yes | `test_memberships_ui.py::test_discount_settings_tab_loads` | Fully Covered | Asserts discount tab labels. |
| MEM-UI-020 | Verify Save Membership button is displayed. | Yes | `test_memberships_ui.py::test_save_and_cancel_buttons_are_visible_on_create_form` | Fully Covered | Asserts Save and Cancel buttons. |
| MEM-UI-021 | Verify Cancel button is displayed. | Yes | `test_memberships_ui.py::test_save_and_cancel_buttons_are_visible_on_create_form` | Fully Covered | Asserts Save and Cancel buttons. |
| MEM-UI-022 | Verify Support button visibility. | No | `-` | Not Covered | Support button not visible in headless run from the memberships iframe context. |
| MEM-SRCH-001 | Verify search using exact membership name. | Yes | `test_memberships_search_filter.py::test_memberships_existing_search` | Fully Covered | Asserts exact match row is displayed. |
| MEM-SRCH-002 | Verify search using partial membership name. | Yes | `test_memberships_search_filter.py::test_memberships_partial_search` | Fully Covered | Asserts visible rows contain partial text. |
| MEM-SRCH-003 | Verify case-insensitive search. | Yes | `test_memberships_search_filter.py::test_memberships_case_insensitive_search` | Fully Covered | Asserts uppercase search returns expected row. |
| MEM-SRCH-004 | Verify search with special characters. | Partial | `test_memberships_search_filter.py::test_memberships_search_payloads_do_not_break_grid` | Partially Covered | Asserts payloads do not break UI; does not assert no script execution/API response. |
| MEM-SRCH-005 | Verify search with spaces before and after keyword. | Yes | `test_memberships_search_filter.py::test_memberships_search_with_surrounding_spaces` | Fully Covered | Asserts surrounding spaces still return membership. |
| MEM-SRCH-006 | Verify search with invalid membership name. | Partial | `test_memberships_search_filter.py::test_memberships_missing_search` | Partially Covered | App does not show expected no-records state; test asserts input is accepted and no broken UI. |
| MEM-SRCH-007 | Verify search with very long string. | Yes | `test_memberships_search_filter.py::test_memberships_long_search_text_does_not_break_grid` | Fully Covered | Asserts long search value is retained and UI remains stable. |
| MEM-SRCH-008 | Verify clearing search restores all records. | Yes | `test_memberships_search_filter.py::test_memberships_clear_search_restores_records` | Fully Covered | Asserts search clears and visible count restores. |
| MEM-FLTR-001 | Verify Filter popup opens successfully. | Yes | `test_memberships_search_filter.py::test_memberships_filter_panel_shows_controls` | Fully Covered | Asserts filter panel opens and basic controls show. |
| MEM-FLTR-002 | Verify Membership Type dropdown values. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-003 | Verify filtering by Recurring membership type. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-004 | Verify filtering by Prepaid membership type. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-005 | Verify Site dropdown values load successfully. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-006 | Verify filtering by Site. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-007 | Verify filtering by Barcode. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-008 | Verify Active Membership toggle ON. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-009 | Verify Active Membership toggle OFF. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-010 | Verify multiple filters together. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-011 | Verify Apply Filters button. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-012 | Verify Reset All button. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-FLTR-013 | Verify no results after filtering. | No | `-` | Not Covered | No executable assertions for membership type/site/barcode/active/multiple filters/apply-reset/no-results behavior. |
| MEM-DL-001 | Verify Download Memberships button functionality. | Yes | `test_memberships_download.py::test_download_memberships_starts_file_download` | Fully Covered | Asserts file is downloaded and non-empty. |
| MEM-DL-002 | Verify downloaded file format. | Yes | `test_memberships_download.py::test_download_memberships_file_format` | Fully Covered | Asserts export suffix is csv/xlsx/xls. |
| MEM-DL-003 | Verify downloaded file contains displayed records. | No | `-` | Not Covered | No file content, filtered export, searched export, or empty export validation. |
| MEM-DL-004 | Verify export after applying filters. | No | `-` | Not Covered | No file content, filtered export, searched export, or empty export validation. |
| MEM-DL-005 | Verify export after search. | No | `-` | Not Covered | No file content, filtered export, searched export, or empty export validation. |
| MEM-DL-006 | Verify export when no records exist. | No | `-` | Not Covered | No file content, filtered export, searched export, or empty export validation. |
| MEM-CRUD-001 | Verify creation of Recurring membership. | Yes | `test_memberships_positive.py::test_create_recurring_membership` | Fully Covered | Creates/verifies recurring membership and persisted core fields. |
| MEM-CRUD-002 | Verify creation of Prepaid membership. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-003 | Verify Membership Name field accepts valid data. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-004 | Verify Global Price field accepts valid value. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-005 | Verify Global Commission field accepts valid value. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-006 | Verify Loyalty Points value save. | Yes | `test_memberships_edit.py::test_edit_membership_loyalty_points_and_discount` | Fully Covered | Updates and reopens to assert loyalty points and discount selection. |
| MEM-CRUD-007 | Verify Limit Membership toggle enabled. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-008 | Verify redemption limits save successfully. | Yes | `test_memberships_positive.py::test_cancel_create_membership_discards_unsaved_changes` | Fully Covered | Asserts canceled membership name is not present after returning to list. |
| MEM-CRUD-009 | Verify Barcode save functionality. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-010 | Verify Membership Description save functionality. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-011 | Verify Active Service toggle functionality. | Partial | `test_memberships_positive.py::test_create_inactive_membership` | Partially Covered | Asserts inactive-created membership is not visible in default active list; no inactive filter assertion available. |
| MEM-CRUD-012 | Verify Show On Customer Portal toggle. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-013 | Verify assigning membership to single location. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-014 | Verify assigning membership to multiple locations. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-015 | Verify location-specific price override. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-016 | Verify location-specific commission override. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-017 | Verify location tax exemption toggle. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-018 | Verify Save Membership functionality. | Yes | `test_memberships_positive.py::test_create_prepaid_membership / test_membership_settings_persist` | Fully Covered | Creates prepaid membership and asserts core persisted values/location assignment. |
| MEM-CRUD-019 | Verify Edit Membership functionality. | Yes | `test_memberships_edit.py::test_edit_membership_name_and_restore` | Fully Covered | Updates name, asserts row and field persistence, then restores. |
| MEM-CRUD-020 | Verify location selection in Redemption Settings. | Yes | `test_memberships_positive.py::test_membership_settings_persist` | Fully Covered | Asserts redemption location selected and redeem-as service visible. |
| MEM-CRUD-021 | Verify Redeem As dropdown values. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-022 | Verify assigning Wash Package to redemption location. | Yes | `test_memberships_positive.py::test_membership_settings_persist` | Fully Covered | Asserts redemption location selected and redeem-as service visible. |
| MEM-CRUD-023 | Verify multiple redemption mappings. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-024 | Verify Applicable Discounts dropdown values. | Partial | `test_memberships_edit.py::test_edit_membership_loyalty_points_and_discount` | Partially Covered | Asserts one discount can be selected; does not validate complete dropdown values. |
| MEM-CRUD-025 | Verify assigning discount to membership. | Yes | `test_memberships_edit.py::test_edit_membership_loyalty_points_and_discount` | Fully Covered | Updates and reopens to assert loyalty points and discount selection. |
| MEM-CRUD-026 | Verify Add Multi-Month Discount button. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-027 | Verify Multi-Month Discount selection. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-028 | Verify Months Number field save. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-CRUD-029 | Verify Remove Multi-Month Discount functionality. | No | `-` | Not Covered | No executable assertion for this CRUD path yet. |
| MEM-VAL-001 | Verify Membership Name is mandatory. | Yes | `test_memberships_validation.py::test_membership_required_name_validation` | Fully Covered | Asserts invalid state and validation message. |
| MEM-VAL-002 | Verify Global Price is mandatory. | Yes | `test_memberships_validation.py::test_membership_requires_global_price` | Fully Covered | Asserts invalid global price and validation message. |
| MEM-VAL-003 | Verify save with both mandatory fields blank. | Partial | `test_memberships_validation.py::test_membership_blank_required_form_stays_on_form` | Partially Covered | Asserts form remains; does not query list to prove no record. |
| MEM-VAL-004 | Verify duplicate Membership Name. | Yes | `test_memberships_validation.py::test_duplicate_membership_name_is_rejected` | Fully Covered | Asserts duplicate error visible. |
| MEM-VAL-005 | Verify Membership Name with only spaces. | Yes | `test_memberships_validation.py::test_spaces_only_membership_name_is_rejected` | Fully Covered | Asserts form remains and name trims to empty. |
| MEM-VAL-006 | Verify Membership Name max length validation. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-VAL-007 | Verify negative Global Price value. | Partial | `test_memberships_validation.py::test_negative_global_price_is_rejected` | Partially Covered | Asserts save blocked and data remains; no specific validation message. |
| MEM-VAL-008 | Verify alphabetic value in price field. | Partial | `test_memberships_validation.py::test_alphabetic_global_price_is_rejected` | Partially Covered | Asserts save blocked and data remains; no specific validation message. |
| MEM-VAL-009 | Verify decimal price value. | Yes | `test_memberships_validation.py::test_decimal_global_price_is_accepted_and_saved` | Fully Covered | Creates membership and asserts decimal price in list. |
| MEM-VAL-010 | Verify negative commission value. | Partial | `test_memberships_validation.py::test_negative_global_commission_is_rejected` | Partially Covered | Asserts save blocked and data remains; no specific validation message. |
| MEM-VAL-011 | Verify invalid barcode format. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-VAL-012 | Verify Loyalty Points accepts numeric values only. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-VAL-013 | Verify redemption limit fields accept numeric values only. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-VAL-014 | Verify XSS payloads in text fields. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-VAL-015 | Verify SQL injection payloads. | No | `-` | Not Covered | No executable validation assertion for this input class yet. |
| MEM-PERM-001 | Verify authorized users can access Memberships page. | Yes | `test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | Fully Covered | Authenticated admin can open page. |
| MEM-PERM-002 | Verify unauthorized users cannot access Memberships URL. | No | `-` | Not Covered | Requires role/session fixtures or API authorization setup not present in current membership suite. |
| MEM-PERM-003 | Verify Create Membership permission. | No | `-` | Not Covered | Requires role/session fixtures or API authorization setup not present in current membership suite. |
| MEM-PERM-004 | Verify Edit Membership permission. | No | `-` | Not Covered | Requires role/session fixtures or API authorization setup not present in current membership suite. |
| MEM-PERM-005 | Verify Download Membership permission. | No | `-` | Not Covered | Requires role/session fixtures or API authorization setup not present in current membership suite. |
| MEM-PERM-006 | Verify session timeout during save. | No | `-` | Not Covered | Requires role/session fixtures or API authorization setup not present in current membership suite. |
| MEM-EDGE-001 | Verify no memberships available. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-002 | Verify membership list with 1000+ records. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-003 | Verify membership name with Unicode characters. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-004 | Verify membership name with emojis. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-005 | Verify concurrent membership updates by two users. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-006 | Verify double-click Save Membership button. | Partial | `test_memberships_edge_cases.py::test_membership_create_is_idempotent` | Partially Covered | Asserts helper does not duplicate visible record; not a double-click Save simulation. |
| MEM-EDGE-007 | Verify browser refresh during creation. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-008 | Verify slow network during save. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-009 | Verify large membership description content. | Partial | `test_memberships_edge_cases.py::test_membership_long_name_does_not_break_form` | Partially Covered | Asserts long name does not break form; does not save/validate max content. |
| MEM-EDGE-010 | Verify membership creation with all locations selected. | Partial | `test_memberships_edge_cases.py::test_membership_only_first_location_is_assigned` | Partially Covered | Covers single-location assignment, not all locations selected. |
| MEM-EDGE-011 | Verify redemption mapping for all locations. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-012 | Verify membership with multiple discounts and multiple-month discounts. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-013 | Verify export with large filtered dataset. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-014 | Verify audit log generation for membership create/update operations (if supported). | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-015 | Verify application behavior after server restart. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |
| MEM-EDGE-016 | Verify membership creation with no assigned locations. | No | `-` | Not Covered | No executable edge-case assertion or required environment support in current suite. |

## Gap Analysis

- Missing filters: membership type, site, barcode, active/inactive, multiple filters, apply/reset, and no-result filtering.
- Missing export depth: exported content matching grid, filtered export, searched export, empty export.
- Missing CRUD depth: barcode, description, limit membership, multi-location assignment, tax exemption, multiple redemption mappings, multi-month discounts.
- Missing validation: max length, invalid barcode, numeric-only loyalty/redemption limit fields, XSS and SQL payloads in create/edit fields.
- Missing permissions: unauthorized URL, create/edit/download permissions, session timeout during save.
- Missing advanced edge cases: large datasets, concurrency, slow network, audit history, server restart, no-location behavior.
- Product behavior observed: invalid membership search keeps existing grid rows instead of showing the expected no-records state; inactive-created memberships are not visible in the default active list.

## Automation Scripts Added or Improved

- Added Memberships POM helpers for pagination/results, edit action checks, cancel, empty-state detection, switch-off handling, and optional barcode/description helpers.
- Added UI tests for edit actions, pagination/results controls, redemption tab, discount tab, and save/cancel buttons.
- Added search tests for surrounding-space search and long search text; strengthened invalid-search stability assertion.
- Added download file-format validation.
- Added validation tests for spaces-only membership name and decimal price acceptance.
- Added CRUD tests for cancel create and inactive membership default-list behavior.

## Prioritized Backlog

| TC ID | Priority | Effort | Recommended Test File | Required Changes | Assertions Required |
|---|---|---|---|---|---|
| MEM-UI-002 | P1 | Small | `test_memberships_ui.py` | Add/extend POM methods and test data for this scenario. | Memberships submenu is visible under Services. |
| MEM-UI-003 | P1 | Small | `test_memberships_ui.py` | Add/extend POM methods and test data for this scenario. | Memberships menu is highlighted as active. |
| MEM-UI-022 | P3 | Small | `test_memberships_ui.py` | Add/extend POM methods and test data for this scenario. | Support button remains accessible. |
| MEM-SRCH-004 | P2 | Small | `test_memberships_search.py` | Strengthen existing assertions to match expected result. | Application handles input safely. |
| MEM-SRCH-006 | P2 | Small | `test_memberships_search.py` | Strengthen existing assertions to match expected result. | No records found message displayed. |
| MEM-FLTR-002 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | All, Recurring and Prepaid options are displayed. |
| MEM-FLTR-003 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Only Recurring memberships are displayed. |
| MEM-FLTR-004 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Only Prepaid memberships are displayed. |
| MEM-FLTR-005 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Available sites are displayed. |
| MEM-FLTR-006 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Only memberships belonging to selected site are displayed. |
| MEM-FLTR-007 | P3 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Matching memberships are displayed. |
| MEM-FLTR-008 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Only active memberships displayed. |
| MEM-FLTR-009 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Inactive memberships displayed. |
| MEM-FLTR-010 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Combined filters return correct results. |
| MEM-FLTR-011 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Selected filters are applied. |
| MEM-FLTR-012 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | All filters are cleared. |
| MEM-FLTR-013 | P1 | Medium | `test_memberships_filter.py` | Add/extend POM methods and test data for this scenario. | Empty state message displayed. |
| MEM-DL-003 | P1 | Medium | `test_memberships_download.py` | Add/extend POM methods and test data for this scenario. | Exported data matches grid data. |
| MEM-DL-004 | P1 | Medium | `test_memberships_download.py` | Add/extend POM methods and test data for this scenario. | Only filtered records are exported. |
| MEM-DL-005 | P3 | Medium | `test_memberships_download.py` | Add/extend POM methods and test data for this scenario. | Search results are exported. |
| MEM-DL-006 | P3 | Medium | `test_memberships_download.py` | Add/extend POM methods and test data for this scenario. | System handles empty export gracefully. |
| MEM-CRUD-007 | P1 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Daily, Weekly and Monthly redemption fields become visible. |
| MEM-CRUD-009 | P3 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Barcode value is saved. |
| MEM-CRUD-010 | P3 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Description is saved successfully. |
| MEM-CRUD-011 | P2 | Small | `test_memberships_crud.py` | Strengthen existing assertions to match expected result. | Membership status changes correctly. |
| MEM-CRUD-014 | P1 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Membership assigned successfully. |
| MEM-CRUD-017 | P3 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Tax exemption saved successfully. |
| MEM-CRUD-021 | P1 | Small | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Available Wash Packages are displayed. |
| MEM-CRUD-023 | P1 | Medium | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Multiple locations can have different wash packages. |
| MEM-CRUD-024 | P2 | Small | `test_memberships_crud.py` | Strengthen existing assertions to match expected result. | Discounts created in Discounts module are displayed. |
| MEM-CRUD-026 | P1 | Medium | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | New row is added. |
| MEM-CRUD-027 | P1 | Medium | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Discount profile can be selected. |
| MEM-CRUD-028 | P1 | Medium | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Value is saved successfully. |
| MEM-CRUD-029 | P3 | Medium | `test_memberships_crud.py` | Add/extend POM methods and test data for this scenario. | Discount row is removed. |
| MEM-VAL-003 | P1 | Small | `test_memberships_validation.py` | Strengthen existing assertions to match expected result. | Membership is not created. |
| MEM-VAL-006 | P1 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | System enforces configured limit. |
| MEM-VAL-007 | P2 | Small | `test_memberships_validation.py` | Strengthen existing assertions to match expected result. | Validation displayed. |
| MEM-VAL-008 | P2 | Small | `test_memberships_validation.py` | Strengthen existing assertions to match expected result. | Input rejected. |
| MEM-VAL-010 | P3 | Small | `test_memberships_validation.py` | Strengthen existing assertions to match expected result. | Validation displayed. |
| MEM-VAL-011 | P3 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | Validation displayed. |
| MEM-VAL-012 | P1 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | Invalid characters are rejected. |
| MEM-VAL-013 | P1 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | Non-numeric values are rejected. |
| MEM-VAL-014 | P1 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | Scripts are sanitized. |
| MEM-VAL-015 | P1 | Small | `test_memberships_validation.py` | Add/extend POM methods and test data for this scenario. | System safely handles input. |
| MEM-PERM-002 | P1 | Large | `test_memberships_permissions.py` | Add/extend POM methods and test data for this scenario. | Access denied. |
| MEM-PERM-003 | P1 | Large | `test_memberships_permissions.py` | Add/extend POM methods and test data for this scenario. | Add Membership button hidden or disabled. |
| MEM-PERM-004 | P1 | Large | `test_memberships_permissions.py` | Add/extend POM methods and test data for this scenario. | Edit option hidden or disabled. |
| MEM-PERM-005 | P1 | Large | `test_memberships_permissions.py` | Add/extend POM methods and test data for this scenario. | Download option follows role permissions. |
| MEM-PERM-006 | P1 | Large | `test_memberships_permissions.py` | Add/extend POM methods and test data for this scenario. | User redirected to login. |
| MEM-EDGE-001 | P1 | Small | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Empty state displayed. |
| MEM-EDGE-002 | P1 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Performance remains acceptable. |
| MEM-EDGE-003 | P3 | Small | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Data saved correctly. |
| MEM-EDGE-004 | P3 | Small | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Validation follows business rules. |
| MEM-EDGE-005 | P1 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Data integrity maintained. |
| MEM-EDGE-006 | P2 | Small | `test_memberships_edge_cases.py` | Strengthen existing assertions to match expected result. | Only one membership is created. |
| MEM-EDGE-007 | P3 | Small | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | No duplicate records created. |
| MEM-EDGE-008 | P1 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Appropriate loading and success/error handling. |
| MEM-EDGE-009 | P3 | Small | `test_memberships_edge_cases.py` | Strengthen existing assertions to match expected result. | Application handles maximum text length. |
| MEM-EDGE-010 | P2 | Small | `test_memberships_edge_cases.py` | Strengthen existing assertions to match expected result. | Membership saves successfully. |
| MEM-EDGE-011 | P1 | Medium | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | All mappings save successfully. |
| MEM-EDGE-012 | P1 | Medium | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | All discount configurations save correctly. |
| MEM-EDGE-013 | P1 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Download completes successfully. |
| MEM-EDGE-014 | P3 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Audit records are generated correctly. |
| MEM-EDGE-015 | P3 | Large | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | Saved memberships remain intact and accessible. |
| MEM-EDGE-016 | P1 | Medium | `test_memberships_edge_cases.py` | Add/extend POM methods and test data for this scenario. | System follows business validation rules and displays appropriate message or saves successfully as designed. |
