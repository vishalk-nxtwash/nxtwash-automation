# NxtWash Admin Portal - Memberships Automation Coverage Review

Source manual sheet: Google Sheet gid 2002, exported as CSV on 2026-06-11.
Scope note: the provided sheet tab contains Memberships test cases only. Other modules were inventoried in the repo but not present in this sheet export.

## 1. Executive Summary

- Total manual Memberships cases reviewed: 115
- Actual Memberships automated test methods found: 18
- Fully automated: 26
- Partially automated: 19
- Incorrectly automated: 4
- Not automated: 66
- Effective full automation coverage: 22.6%
- Effective implemented-or-partial coverage: 42.6%
- Key risk: the manual sheet marks 111 cases as automated, but many are not present as executable tests in the current repository.

## 2. Coverage Matrix

| TC ID | Module | Test Scenario | Automation File | Test Method | Coverage Status | Comments |
|---|---|---|---|---|---|---|
| MEM-UI-001 | Memberships | Verify Memberships page loads successfully. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-002 | Memberships | Verify Services menu is expanded. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-003 | Memberships | Verify Memberships submenu is highlighted. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-004 | Memberships | Verify page title displays "Memberships". | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-005 | Memberships | Verify Membership Name column is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_grid_columns_are_visible | Fully Automated | Grid column text is asserted. |
| MEM-UI-006 | Memberships | Verify Type column is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_grid_columns_are_visible | Fully Automated | Grid column text is asserted. |
| MEM-UI-007 | Memberships | Verify Price column is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_grid_columns_are_visible | Fully Automated | Grid column text is asserted. |
| MEM-UI-008 | Memberships | Verify Status column is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_grid_columns_are_visible | Fully Automated | Grid column text is asserted. |
| MEM-UI-009 | Memberships | Verify Edit action is available for every membership. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-010 | Memberships | Verify Search field is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-011 | Memberships | Verify Filter By button is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-012 | Memberships | Verify Download button is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-013 | Memberships | Verify Add New Membership button is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Primary controls and page health are asserted. |
| MEM-UI-014 | Memberships | Verify pagination controls are displayed. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-015 | Memberships | Verify results-per-page dropdown is displayed. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-016 | Memberships | Verify Add Membership page loads successfully. | tests/admin_portal/memberships/test_memberships_ui.py | test_add_membership_form_loads | Partially Automated | Create form loads, but default selected tab is not explicitly asserted. |
| MEM-UI-017 | Memberships | Verify Membership Settings tab UI. | tests/admin_portal/memberships/test_memberships_ui.py | test_add_membership_form_loads | Partially Automated | Core fields are asserted; all controls/save enabled state are not fully checked. |
| MEM-UI-018 | Memberships | Verify Redemption Settings tab UI. | pages/admin_portal/memberships_page.py | open_redemption_settings/open_discount_settings | Partially Automated | POM supports tab waits and later flows use them, but no dedicated UI assertions cover all controls. |
| MEM-UI-019 | Memberships | Verify Discount Settings tab UI. | pages/admin_portal/memberships_page.py | open_redemption_settings/open_discount_settings | Partially Automated | POM supports tab waits and later flows use them, but no dedicated UI assertions cover all controls. |
| MEM-UI-020 | Memberships | Verify Save Membership button is displayed. | tests/admin_portal/memberships/test_memberships_ui.py | test_add_membership_form_loads | Partially Automated | Core fields are asserted; all controls/save enabled state are not fully checked. |
| MEM-UI-021 | Memberships | Verify Cancel button is displayed. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-UI-022 | Memberships | Verify Support button visibility. | - | - | Not Automated | No assertion for menu expansion/highlight, every-row edit action, pagination/results dropdown, cancel, or support button. |
| MEM-SRCH-001 | Memberships | Verify search using exact membership name. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_existing_search | Fully Automated | Exact existing search is asserted. |
| MEM-SRCH-002 | Memberships | Verify search using partial membership name. | - | - | Not Automated | No partial/case-insensitive/trim/long/clear-search result validation. |
| MEM-SRCH-003 | Memberships | Verify case-insensitive search. | - | - | Not Automated | No partial/case-insensitive/trim/long/clear-search result validation. |
| MEM-SRCH-004 | Memberships | Verify search with special characters. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_search_payloads_do_not_break_grid | Partially Automated | Special payloads are smoke-tested for broken state; result correctness is not asserted. |
| MEM-SRCH-005 | Memberships | Verify search with spaces before and after keyword. | - | - | Not Automated | No partial/case-insensitive/trim/long/clear-search result validation. |
| MEM-SRCH-006 | Memberships | Verify search with invalid membership name. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_missing_search | Partially Automated | Missing value absence is asserted; empty-state message is not asserted. |
| MEM-SRCH-007 | Memberships | Verify search with very long string. | - | - | Not Automated | No partial/case-insensitive/trim/long/clear-search result validation. |
| MEM-SRCH-008 | Memberships | Verify clearing search restores all records. | - | - | Not Automated | No partial/case-insensitive/trim/long/clear-search result validation. |
| MEM-FLTR-001 | Memberships | Verify Filter popup opens successfully. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_filter_panel_shows_controls | Fully Automated | Filter panel opens and core buttons are asserted. |
| MEM-FLTR-002 | Memberships | Verify Membership Type dropdown values. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-003 | Memberships | Verify filtering by Recurring membership type. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-004 | Memberships | Verify filtering by Prepaid membership type. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-005 | Memberships | Verify Site dropdown values load successfully. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_filter_panel_shows_controls | Partially Automated | Controls are visible but option values/apply/reset behavior are not asserted. |
| MEM-FLTR-006 | Memberships | Verify filtering by Site. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-007 | Memberships | Verify filtering by Barcode. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-008 | Memberships | Verify Active Membership toggle ON. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-009 | Memberships | Verify Active Membership toggle OFF. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-010 | Memberships | Verify multiple filters together. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-FLTR-011 | Memberships | Verify Apply Filters button. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_filter_panel_shows_controls | Partially Automated | Controls are visible but option values/apply/reset behavior are not asserted. |
| MEM-FLTR-012 | Memberships | Verify Reset All button. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_filter_panel_shows_controls | Partially Automated | Controls are visible but option values/apply/reset behavior are not asserted. |
| MEM-FLTR-013 | Memberships | Verify no results after filtering. | - | - | Not Automated | Filter behavior is not validated beyond panel visibility. |
| MEM-DL-001 | Memberships | Verify Download Memberships button functionality. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Partially Automated | Download button is clickable; no file/download-content validation. |
| MEM-DL-002 | Memberships | Verify downloaded file format. | - | - | Not Automated | No downloaded file type/content/filter/search/empty export validation. |
| MEM-DL-003 | Memberships | Verify downloaded file contains displayed records. | - | - | Not Automated | No downloaded file type/content/filter/search/empty export validation. |
| MEM-DL-004 | Memberships | Verify export after applying filters. | - | - | Not Automated | No downloaded file type/content/filter/search/empty export validation. |
| MEM-DL-005 | Memberships | Verify export after search. | - | - | Not Automated | No downloaded file type/content/filter/search/empty export validation. |
| MEM-DL-006 | Memberships | Verify export when no records exist. | - | - | Not Automated | No downloaded file type/content/filter/search/empty export validation. |
| MEM-CRUD-001 | Memberships | Verify creation of Recurring membership. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-002 | Memberships | Verify creation of Prepaid membership. | tests/admin_portal/memberships/test_memberships_positive.py | test_create_prepaid_membership | Fully Automated | Prepaid create and list verification are asserted. |
| MEM-CRUD-003 | Memberships | Verify Membership Name field accepts valid data. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-004 | Memberships | Verify Global Price field accepts valid value. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-005 | Memberships | Verify Global Commission field accepts valid value. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-006 | Memberships | Verify Loyalty Points value save. | tests/admin_portal/memberships/test_memberships_edit.py | test_edit_membership_loyalty_points_and_discount | Fully Automated | Loyalty points persistence is asserted. |
| MEM-CRUD-007 | Memberships | Verify Limit Membership toggle enabled. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-008 | Memberships | Verify redemption limits save successfully. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-009 | Memberships | Verify Barcode save functionality. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-010 | Memberships | Verify Membership Description save functionality. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-011 | Memberships | Verify Active Service toggle functionality. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-012 | Memberships | Verify Show On Customer Portal toggle. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-013 | Memberships | Verify assigning membership to single location. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-014 | Memberships | Verify assigning membership to multiple locations. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-015 | Memberships | Verify location-specific price override. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-016 | Memberships | Verify location-specific commission override. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-017 | Memberships | Verify location tax exemption toggle. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-018 | Memberships | Verify Save Membership functionality. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Fully Automated | Persistence is asserted through edit form/list checks. |
| MEM-CRUD-019 | Memberships | Verify Edit Membership functionality. | tests/admin_portal/memberships/test_memberships_edit.py | test_edit_membership_loyalty_points_and_discount | Partially Automated | Edit path is covered for loyalty/discount only, not general edit coverage. |
| MEM-CRUD-020 | Memberships | Verify location selection in Redemption Settings. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Partially Automated | First redemption row and selected service text are asserted; dropdown values are not fully validated. |
| MEM-CRUD-021 | Memberships | Verify Redeem As dropdown values. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-022 | Memberships | Verify assigning Wash Package to redemption location. | tests/admin_portal/memberships/test_memberships_positive.py | test_membership_settings_persist | Partially Automated | First redemption row and selected service text are asserted; dropdown values are not fully validated. |
| MEM-CRUD-023 | Memberships | Verify multiple redemption mappings. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-024 | Memberships | Verify Applicable Discounts dropdown values. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-025 | Memberships | Verify assigning discount to membership. | tests/admin_portal/memberships/test_memberships_edit.py | test_edit_membership_loyalty_points_and_discount | Fully Automated | Applicable discount assignment is asserted. |
| MEM-CRUD-026 | Memberships | Verify Add Multi-Month Discount button. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-027 | Memberships | Verify Multi-Month Discount selection. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-028 | Memberships | Verify Months Number field save. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-CRUD-029 | Memberships | Verify Remove Multi-Month Discount functionality. | - | - | Not Automated | No matching automated CRUD assertion for this scenario. |
| MEM-VAL-001 | Memberships | Verify Membership Name is mandatory. | tests/admin_portal/memberships/test_memberships_validation.py | test_membership_required_name_validation | Fully Automated | Native required validation is asserted. |
| MEM-VAL-002 | Memberships | Verify Global Price is mandatory. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-003 | Memberships | Verify save with both mandatory fields blank. | tests/admin_portal/memberships/test_memberships_validation.py | test_membership_blank_required_form_stays_on_form | Partially Automated | Form remains open; global price required validation is not asserted. |
| MEM-VAL-004 | Memberships | Verify duplicate Membership Name. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-005 | Memberships | Verify Membership Name with only spaces. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-006 | Memberships | Verify Membership Name max length validation. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-007 | Memberships | Verify negative Global Price value. | tests/admin_portal/memberships/test_memberships_validation.py | test_membership_invalid_numeric_values_do_not_break_form | Incorrectly Automated | Only page stability is asserted; invalid numeric rejection/validation message is not asserted. |
| MEM-VAL-008 | Memberships | Verify alphabetic value in price field. | tests/admin_portal/memberships/test_memberships_validation.py | test_membership_invalid_numeric_values_do_not_break_form | Incorrectly Automated | Only page stability is asserted; invalid numeric rejection/validation message is not asserted. |
| MEM-VAL-009 | Memberships | Verify decimal price value. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-010 | Memberships | Verify negative commission value. | tests/admin_portal/memberships/test_memberships_validation.py | test_membership_invalid_numeric_values_do_not_break_form | Incorrectly Automated | Only page stability is asserted; invalid numeric rejection/validation message is not asserted. |
| MEM-VAL-011 | Memberships | Verify invalid barcode format. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-012 | Memberships | Verify Loyalty Points accepts numeric values only. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-013 | Memberships | Verify redemption limit fields accept numeric values only. | - | - | Not Automated | Required validation is missing for this field/rule. |
| MEM-VAL-014 | Memberships | Verify XSS payloads in text fields. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_search_payloads_do_not_break_grid | Partially Automated | Payloads are tested only in search, not create/edit text fields. |
| MEM-VAL-015 | Memberships | Verify SQL injection payloads. | tests/admin_portal/memberships/test_memberships_search_filter.py | test_memberships_search_payloads_do_not_break_grid | Partially Automated | Payloads are tested only in search, not create/edit text fields. |
| MEM-PERM-001 | Memberships | Verify authorized users can access Memberships page. | tests/admin_portal/memberships/test_memberships_ui.py | test_memberships_page_loads_with_primary_controls | Fully Automated | Authorized admin page load is covered. |
| MEM-PERM-002 | Memberships | Verify unauthorized users cannot access Memberships URL. | - | - | Not Automated | No role/permission/session-timeout test exists for Memberships. |
| MEM-PERM-003 | Memberships | Verify Create Membership permission. | - | - | Not Automated | No role/permission/session-timeout test exists for Memberships. |
| MEM-PERM-004 | Memberships | Verify Edit Membership permission. | - | - | Not Automated | No role/permission/session-timeout test exists for Memberships. |
| MEM-PERM-005 | Memberships | Verify Download Membership permission. | - | - | Not Automated | No role/permission/session-timeout test exists for Memberships. |
| MEM-PERM-006 | Memberships | Verify session timeout during save. | - | - | Not Automated | No role/permission/session-timeout test exists for Memberships. |
| MEM-EDGE-001 | Memberships | Verify no memberships available. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-002 | Memberships | Verify membership list with 1000+ records. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-003 | Memberships | Verify membership name with Unicode characters. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-004 | Memberships | Verify membership name with emojis. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-005 | Memberships | Verify concurrent membership updates by two users. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-006 | Memberships | Verify double-click Save Membership button. | tests/admin_portal/memberships/test_memberships_edge_cases.py | test_membership_create_is_idempotent | Partially Automated | Idempotent helper prevents duplicates; double-click save is not directly simulated. |
| MEM-EDGE-007 | Memberships | Verify browser refresh during creation. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-008 | Memberships | Verify slow network during save. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-009 | Memberships | Verify large membership description content. | tests/admin_portal/memberships/test_memberships_edge_cases.py | test_membership_long_name_does_not_break_form | Partially Automated | Long name field is tested; description max content is not. |
| MEM-EDGE-010 | Memberships | Verify membership creation with all locations selected. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-011 | Memberships | Verify redemption mapping for all locations. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-012 | Memberships | Verify membership with multiple discounts and multiple-month discounts. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-013 | Memberships | Verify export with large filtered dataset. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-014 | Memberships | Verify audit log generation for membership create/update operations (if supported). | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-015 | Memberships | Verify application behavior after server restart. | - | - | Not Automated | No matching automated assertion found. |
| MEM-EDGE-016 | Memberships | Verify membership creation with no assigned locations. | tests/admin_portal/memberships/test_memberships_edge_cases.py | test_membership_only_first_location_is_assigned | Incorrectly Automated | Test verifies only first location assigned, not no-location behavior. |

## 3. Automation Suitability Matrix

| TC ID | Test Scenario | Recommendation | Priority | Reason |
|---|---|---|---|---|
| MEM-UI-001 | Verify Memberships page loads successfully. | Must Automate | P1 | High regression/business value. |
| MEM-UI-002 | Verify Services menu is expanded. | Must Automate | P1 | High regression/business value. |
| MEM-UI-003 | Verify Memberships submenu is highlighted. | Must Automate | P1 | High regression/business value. |
| MEM-UI-004 | Verify page title displays "Memberships". | Must Automate | P1 | High regression/business value. |
| MEM-UI-005 | Verify Membership Name column is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-006 | Verify Type column is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-007 | Verify Price column is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-008 | Verify Status column is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-009 | Verify Edit action is available for every membership. | Must Automate | P1 | High regression/business value. |
| MEM-UI-010 | Verify Search field is displayed. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-UI-011 | Verify Filter By button is displayed. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-UI-012 | Verify Download button is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-013 | Verify Add New Membership button is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-014 | Verify pagination controls are displayed. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-UI-015 | Verify results-per-page dropdown is displayed. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-UI-016 | Verify Add Membership page loads successfully. | Must Automate | P1 | High regression/business value. |
| MEM-UI-017 | Verify Membership Settings tab UI. | Must Automate | P1 | High regression/business value. |
| MEM-UI-018 | Verify Redemption Settings tab UI. | Must Automate | P1 | High regression/business value. |
| MEM-UI-019 | Verify Discount Settings tab UI. | Must Automate | P1 | High regression/business value. |
| MEM-UI-020 | Verify Save Membership button is displayed. | Must Automate | P1 | High regression/business value. |
| MEM-UI-021 | Verify Cancel button is displayed. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-UI-022 | Verify Support button visibility. | Low Priority | P3 | Lower ROI or mostly visual/support check. |
| MEM-SRCH-001 | Verify search using exact membership name. | Must Automate | P1 | High regression/business value. |
| MEM-SRCH-002 | Verify search using partial membership name. | Must Automate | P1 | High regression/business value. |
| MEM-SRCH-003 | Verify case-insensitive search. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-SRCH-004 | Verify search with special characters. | Must Automate | P1 | High regression/business value. |
| MEM-SRCH-005 | Verify search with spaces before and after keyword. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-SRCH-006 | Verify search with invalid membership name. | Must Automate | P1 | High regression/business value. |
| MEM-SRCH-007 | Verify search with very long string. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-SRCH-008 | Verify clearing search restores all records. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-FLTR-001 | Verify Filter popup opens successfully. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-002 | Verify Membership Type dropdown values. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-003 | Verify filtering by Recurring membership type. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-004 | Verify filtering by Prepaid membership type. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-005 | Verify Site dropdown values load successfully. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-006 | Verify filtering by Site. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-007 | Verify filtering by Barcode. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-FLTR-008 | Verify Active Membership toggle ON. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-009 | Verify Active Membership toggle OFF. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-010 | Verify multiple filters together. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-011 | Verify Apply Filters button. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-012 | Verify Reset All button. | Must Automate | P1 | High regression/business value. |
| MEM-FLTR-013 | Verify no results after filtering. | Must Automate | P1 | High regression/business value. |
| MEM-DL-001 | Verify Download Memberships button functionality. | Must Automate | P1 | High regression/business value. |
| MEM-DL-002 | Verify downloaded file format. | Must Automate | P1 | High regression/business value. |
| MEM-DL-003 | Verify downloaded file contains displayed records. | Must Automate | P1 | High regression/business value. |
| MEM-DL-004 | Verify export after applying filters. | Must Automate | P1 | High regression/business value. |
| MEM-DL-005 | Verify export after search. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-DL-006 | Verify export when no records exist. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-001 | Verify creation of Recurring membership. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-002 | Verify creation of Prepaid membership. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-003 | Verify Membership Name field accepts valid data. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-004 | Verify Global Price field accepts valid value. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-005 | Verify Global Commission field accepts valid value. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-006 | Verify Loyalty Points value save. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-007 | Verify Limit Membership toggle enabled. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-008 | Verify redemption limits save successfully. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-009 | Verify Barcode save functionality. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-010 | Verify Membership Description save functionality. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-011 | Verify Active Service toggle functionality. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-012 | Verify Show On Customer Portal toggle. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-013 | Verify assigning membership to single location. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-014 | Verify assigning membership to multiple locations. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-015 | Verify location-specific price override. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-016 | Verify location-specific commission override. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-017 | Verify location tax exemption toggle. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-CRUD-018 | Verify Save Membership functionality. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-019 | Verify Edit Membership functionality. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-020 | Verify location selection in Redemption Settings. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-021 | Verify Redeem As dropdown values. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-022 | Verify assigning Wash Package to redemption location. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-023 | Verify multiple redemption mappings. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-024 | Verify Applicable Discounts dropdown values. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-025 | Verify assigning discount to membership. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-026 | Verify Add Multi-Month Discount button. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-027 | Verify Multi-Month Discount selection. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-028 | Verify Months Number field save. | Must Automate | P1 | High regression/business value. |
| MEM-CRUD-029 | Verify Remove Multi-Month Discount functionality. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-VAL-001 | Verify Membership Name is mandatory. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-002 | Verify Global Price is mandatory. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-003 | Verify save with both mandatory fields blank. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-004 | Verify duplicate Membership Name. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-005 | Verify Membership Name with only spaces. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-006 | Verify Membership Name max length validation. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-007 | Verify negative Global Price value. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-008 | Verify alphabetic value in price field. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-009 | Verify decimal price value. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-010 | Verify negative commission value. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-VAL-011 | Verify invalid barcode format. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-VAL-012 | Verify Loyalty Points accepts numeric values only. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-013 | Verify redemption limit fields accept numeric values only. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-014 | Verify XSS payloads in text fields. | Must Automate | P1 | High regression/business value. |
| MEM-VAL-015 | Verify SQL injection payloads. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-001 | Verify authorized users can access Memberships page. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-002 | Verify unauthorized users cannot access Memberships URL. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-003 | Verify Create Membership permission. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-004 | Verify Edit Membership permission. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-005 | Verify Download Membership permission. | Must Automate | P1 | High regression/business value. |
| MEM-PERM-006 | Verify session timeout during save. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-001 | Verify no memberships available. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-002 | Verify membership list with 1000+ records. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-003 | Verify membership name with Unicode characters. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-004 | Verify membership name with emojis. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-005 | Verify concurrent membership updates by two users. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-006 | Verify double-click Save Membership button. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-007 | Verify browser refresh during creation. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-008 | Verify slow network during save. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-009 | Verify large membership description content. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-010 | Verify membership creation with all locations selected. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-011 | Verify redemption mapping for all locations. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-012 | Verify membership with multiple discounts and multiple-month discounts. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-013 | Verify export with large filtered dataset. | Must Automate | P1 | High regression/business value. |
| MEM-EDGE-014 | Verify audit log generation for membership create/update operations (if supported). | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-015 | Verify application behavior after server restart. | Good Candidate | P2 | Useful regression candidate; automate after P1 gaps. |
| MEM-EDGE-016 | Verify membership creation with no assigned locations. | Must Automate | P1 | High regression/business value. |

## 4. Script Review Findings

| Severity | File | Issue | Recommendation |
|---|---|---|---|
| Critical | tests/admin_portal/memberships/* | Sheet automation status is overstated: 111 cases are marked Yes, but only 18 Memberships test methods exist. | Update the sheet based on executable mapping and add missing tests before claiming coverage. |
| Critical | tests/admin_portal/memberships/test_memberships_validation.py | Invalid price/commission tests assert page stability instead of rejection or validation message. | Assert field validity, error message, save blocking, and no record creation. |
| Major | tests/admin_portal/memberships/test_memberships_search_filter.py | Filter tests open the panel only; they do not apply membership type, site, active/inactive, barcode, or combined filters. | Add data-driven filter tests with known fixtures and row-level assertions. |
| Major | tests/admin_portal/memberships/test_memberships_ui.py | Download test only checks button clickability, not file creation, format, or exported content. | Use a controlled download directory and validate file type/content for unfiltered, filtered, and searched exports. |
| Major | tests/admin_portal/memberships/test_memberships_positive.py | Create coverage handles Prepaid only; Recurring membership creation is missing. | Add separate recurring create/edit persistence flow. |
| Major | tests/admin_portal/memberships/test_memberships_positive.py | Multiple location assignment, tax exemption, barcode, description, limit membership, and multi-month discount are not covered. | Extend POM and add focused CRUD tests for each business setting. |
| Major | tests/admin_portal/memberships | No role-based or unauthorized access coverage exists for Memberships. | Add permission fixtures/users and validate access, add/edit/download controls, and session timeout. |
| Minor | pages/common/base_page.py | Duplicate wait_for_url method and nested import inside BasePage. | Clean up BasePage and centralize common waits/input setters. |
| Minor | tests/admin_portal/memberships/conftest.py | Test data name is static: VK MA2, which can collide with staging data. | Use shared increment/name factory and cleanup or restore strategy. |

## 5. Coverage Metrics

| Metric | Value |
|---|---:|
| Total Manual Test Cases | 115 |
| Fully Automated | 26 |
| Partially Automated | 19 |
| Incorrectly Automated | 4 |
| Not Automated | 66 |
| Automation Coverage % - Full only | 22.6% |
| Automation Coverage % - Full + Partial | 39.1% |
| Smoke Coverage % | 75.0% estimated: login + page load + basic create/search covered; export/permissions missing |
| Regression Coverage % | 39.1% |

### Module-wise Coverage

| Area | Total | Fully | Partial | Incorrect | Not Automated | Full Coverage % |
|---|---:|---:|---:|---:|---:|---:|
| UI | 22 | 10 | 5 | 0 | 7 | 45.5% |
| SRCH | 8 | 1 | 2 | 0 | 5 | 12.5% |
| FLTR | 13 | 1 | 3 | 0 | 9 | 7.7% |
| DL | 6 | 0 | 1 | 0 | 5 | 0.0% |
| CRUD | 29 | 12 | 3 | 0 | 14 | 41.4% |
| VAL | 15 | 1 | 3 | 3 | 8 | 6.7% |
| PERM | 6 | 1 | 0 | 0 | 5 | 16.7% |
| EDGE | 16 | 0 | 2 | 1 | 13 | 0.0% |

## 6. Gap Analysis

- Missing high-priority automation: recurring creation, most filter combinations, export content validation, role/permission checks, duplicate-name validation, global price required validation, and multi-month discount workflows.
- Missing negative scenarios: duplicate membership name, blank global price, spaces-only name, invalid barcode, invalid loyalty/redemption limit values, field-level XSS/SQL payloads.
- Missing CRUD coverage: barcode, description, limit membership, redemption limits, multiple locations, tax exemption, multiple redemption mappings, multi-month discounts.
- Missing search/filter coverage: partial search, case-insensitive search, trim behavior, clear-search restore, membership type filters, site filter, active/inactive toggle, barcode filter, combined filters, no-result empty state.
- Missing role-based validations: unauthorized URL access, add/edit/download permission gating, session timeout during save.

## 7. Recommended Automation Backlog

| Priority | TC ID(s) | Backlog Item |
|---|---|---|
| P1 | MEM-CRUD-001 | Create recurring membership with persistence assertions. |
| P1 | MEM-VAL-002/MEM-VAL-004 | Add required global price and duplicate membership validation tests. |
| P1 | MEM-FLTR-002 to MEM-FLTR-013 | Implement real filter application/reset/result assertions. |
| P1 | MEM-DL-001 to MEM-DL-006 | Add download directory fixture and exported file validation. |
| P1 | MEM-PERM-002 to MEM-PERM-006 | Add role/session permission coverage. |
| P1 | MEM-CRUD-014/MEM-CRUD-023 | Cover multiple location and redemption mappings. |
| P2 | MEM-CRUD-007 to MEM-CRUD-010 | Cover limit membership, barcode, and description persistence. |
| P2 | MEM-CRUD-026 to MEM-CRUD-029 | Cover multi-month discount add/select/month/remove. |
| P2 | MEM-SRCH-002/003/005/007/008 | Complete search variations and clear-search restore. |
| P2 | MEM-EDGE-005/008/015 | Plan API or controlled-environment tests for concurrency, slow network, restart persistence. |

## 8. Framework Improvement Suggestions

- Add markers: pytest smoke, regression, permissions, export, and destructive markers.
- Add reusable download fixture with temp download directory and file-content assertions.
- Add reusable React Select, grid checkbox, numeric input, toast/error, and filter-panel helpers.
- Add a test-data factory that increments names consistently and records created IDs for cleanup/restoration.
- Add role-based login fixtures for admin, restricted admin, inactive/unauthorized users.
- Add Allure labels, steps, and links mapping tests to manual TC IDs.
- Split smoke suite to include page load, create prepaid/recurring, exact search, required validation, and edit persistence.
- Keep full CRUD, exports, filters, permissions, and edge/performance in regression suite.