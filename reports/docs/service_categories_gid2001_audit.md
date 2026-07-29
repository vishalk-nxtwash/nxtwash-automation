# Service Categories Automation Coverage Audit

Source sheet tab: `gid=2001` from `https://docs.google.com/spreadsheets/d/1O9J30uR_LYABPJqcOGnX6Ve5RkE18uoiwliue_eOhDI/edit?gid=2001#gid=2001`

Audit scope: Service Categories only. Coverage is marked only where executable Pytest/Selenium code exists and asserts the expected behavior. Sheet automation flags were not treated as proof of coverage.

## 1. Executive Summary

- Total manual test cases reviewed: 87
- Executable Service Categories tests found: 13
- Manual sheet marks 78 cases as automated, but repository evidence supports only 23 cases with full or partial executable coverage, plus 1 incorrectly automated case.
- Strongest coverage areas: basic page load, exact search, basic create active category, basic edit name, required name validation.
- Weakest coverage areas: filters, permissions, inactive status update, cancel/back navigation, duplicate validation, XSS/SQL category-name validation, large data, concurrency, audit history.
- No Allure annotations or logging were found in the Service Categories test files.

## 2. Coverage Matrix

| TC ID | Scenario | Priority | Test File | Test Method | Coverage Status |
|---|---|---:|---|---|---|
| SC-UI-001 | Verify Service Categories page loads successfully. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Fully Automated |
| SC-UI-002 | Verify Services menu is expanded by default when Service Categories page is opened. | High | - | - | Not Automated |
| SC-UI-003 | Verify Service Categories submenu is highlighted. | High | - | - | Not Automated |
| SC-UI-004 | Verify page title displays as "Service categories". | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Partially Automated |
| SC-UI-005 | Verify search field is visible. | Medium | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Partially Automated |
| SC-UI-006 | Verify Filter By button is visible. | Medium | `pages/admin_portal/service_categories_page.py` | `FILTER_BUTTON` locator only | Partially Automated |
| SC-UI-007 | Verify Add New Category button is visible. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Partially Automated |
| SC-UI-008 | Verify service category grid displays correctly. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Partially Automated |
| SC-UI-009 | Verify status badge formatting. | Medium | - | - | Not Automated |
| SC-UI-010 | Verify Edit action is displayed for every record. | High | - | - | Not Automated |
| SC-UI-011 | Verify pagination controls are displayed. | Medium | - | - | Not Automated |
| SC-UI-012 | Verify Results Per Page dropdown is visible. | Medium | - | - | Not Automated |
| SC-UI-013 | Verify Support button is displayed. | Low | - | - | Not Automated |
| SC-UI-014 | Verify responsive layout on browser resize. | Medium | - | - | Not Automated |
| SC-UI-015 | Verify Add New Category page loads successfully. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_add_service_category_form_loads` | Partially Automated |
| SC-UI-016 | Verify Category Name field is displayed. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_add_service_category_form_loads` | Partially Automated |
| SC-UI-017 | Verify Active Service toggle is displayed. | Medium | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_add_service_category_form_loads` | Partially Automated |
| SC-UI-018 | Verify Save New Category button is visible. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_add_service_category_form_loads` | Partially Automated |
| SC-UI-019 | Verify Cancel button is visible. | Medium | - | - | Not Automated |
| SC-UI-020 | Verify Back navigation icon is visible. | Medium | - | - | Not Automated |
| SC-SRCH-001 | Verify search by exact category name. | High | `tests/admin_portal/service_categories/test_service_categories_search_filter.py` | `test_service_categories_existing_search` | Fully Automated |
| SC-SRCH-002 | Verify partial search. | High | - | - | Not Automated |
| SC-SRCH-003 | Verify search is case insensitive. | Medium | - | - | Not Automated |
| SC-SRCH-004 | Verify search using leading spaces. | Medium | - | - | Not Automated |
| SC-SRCH-005 | Verify search using trailing spaces. | Medium | - | - | Not Automated |
| SC-SRCH-006 | Verify search with special characters. | High | `tests/admin_portal/service_categories/test_service_categories_search_filter.py` | `test_service_categories_special_character_search_stays_usable` | Partially Automated |
| SC-SRCH-007 | Verify search with numeric values. | Medium | - | - | Not Automated |
| SC-SRCH-008 | Verify search with invalid value. | High | `tests/admin_portal/service_categories/test_service_categories_search_filter.py` | `test_service_categories_missing_search` | Incorrectly Automated |
| SC-SRCH-009 | Verify search with blank value. | Medium | - | - | Not Automated |
| SC-SRCH-010 | Verify search persists after page refresh. | Low | - | - | Not Automated |
| SC-SRCH-011 | Verify search with very long text. | High | - | - | Not Automated |
| SC-FLTR-001 | Verify Filter popup opens. | High | - | - | Not Automated |
| SC-FLTR-002 | Verify Active Service toggle is enabled by default. | Medium | - | - | Not Automated |
| SC-FLTR-003 | Verify filtering active categories. | High | - | - | Not Automated |
| SC-FLTR-004 | Verify filtering inactive categories. | High | - | - | Not Automated |
| SC-FLTR-005 | Verify Apply Filters button functionality. | High | - | - | Not Automated |
| SC-FLTR-006 | Verify Reset All button functionality. | High | - | - | Not Automated |
| SC-FLTR-007 | Verify filter count updates. | Medium | - | - | Not Automated |
| SC-FLTR-008 | Verify filter remains applied after pagination. | Medium | - | - | Not Automated |
| SC-FLTR-009 | Verify filter remains applied after search. | Medium | - | - | Not Automated |
| SC-FLTR-010 | Verify no records scenario after filtering. | High | - | - | Not Automated |
| SC-CRUD-001 | Verify user can create a new category. | Critical | `tests/admin_portal/service_categories/test_service_categories_positive.py` | `test_create_active_service_category` | Partially Automated |
| SC-CRUD-002 | Verify category creation with Active Service enabled. | High | `tests/admin_portal/service_categories/test_service_categories_positive.py` | `test_create_active_service_category` | Fully Automated |
| SC-CRUD-003 | Verify category creation with Active Service disabled. | High | - | - | Not Automated |
| SC-CRUD-004 | Verify newly created category appears in list. | Critical | `tests/admin_portal/service_categories/test_service_categories_positive.py` | `test_create_active_service_category` | Fully Automated |
| SC-CRUD-005 | Verify Edit category functionality. | Critical | `tests/admin_portal/service_categories/test_service_categories_edit.py` | `test_edit_service_category_name_and_restore` | Partially Automated |
| SC-CRUD-006 | Verify category name update. | High | `tests/admin_portal/service_categories/test_service_categories_edit.py` | `test_edit_service_category_name_and_restore` | Fully Automated |
| SC-CRUD-007 | Verify Active status update. | High | - | - | Not Automated |
| SC-CRUD-008 | Verify Cancel button on create screen. | Medium | - | - | Not Automated |
| SC-CRUD-009 | Verify browser back button during create. | Medium | - | - | Not Automated |
| SC-CRUD-010 | Verify duplicate save prevention. | High | - | - | Not Automated |
| SC-CRUD-011 | Verify refresh after successful save. | High | `tests/admin_portal/service_categories/test_service_categories_positive.py` | `test_service_category_settings_persist` | Partially Automated |
| SC-CRUD-012 | Verify concurrent edit handling. | High | - | - | Not Automated |
| SC-VAL-001 | Verify Category Name is mandatory. | Critical | `tests/admin_portal/service_categories/test_service_categories_validation.py` | `test_service_category_required_name_validation` | Fully Automated |
| SC-VAL-002 | Verify save without entering category name. | Critical | `tests/admin_portal/service_categories/test_service_categories_validation.py` | `test_service_category_blank_required_form_stays_on_form` | Partially Automated |
| SC-VAL-003 | Verify category name accepts valid text. | High | `tests/admin_portal/service_categories/test_service_categories_positive.py` | `test_create_active_service_category` | Fully Automated |
| SC-VAL-004 | Verify category name with minimum length. | Medium | - | - | Not Automated |
| SC-VAL-005 | Verify category name with maximum allowed length. | High | `tests/admin_portal/service_categories/test_service_categories_edge_cases.py` | `test_service_category_long_name_does_not_break_form` | Partially Automated |
| SC-VAL-006 | Verify category name with only spaces. | High | - | - | Not Automated |
| SC-VAL-007 | Verify duplicate category name creation. | Critical | - | - | Not Automated |
| SC-VAL-008 | Verify category name with special characters. | Medium | - | - | Not Automated |
| SC-VAL-009 | Verify category name with Unicode characters. | Medium | - | - | Not Automated |
| SC-VAL-010 | Verify XSS payload entry. | Critical | - | - | Not Automated |
| SC-VAL-011 | Verify SQL injection payload entry. | Critical | - | - | Not Automated |
| SC-VAL-012 | Verify save when network connection is interrupted. | High | - | - | Not Automated |
| SC-PERM-001 | Verify authorized users can access Service Categories page. | High | `tests/admin_portal/service_categories/test_service_categories_ui.py` | `test_service_categories_page_loads_with_primary_controls` | Fully Automated |
| SC-PERM-002 | Verify unauthorized users cannot access page URL directly. | Critical | - | - | Not Automated |
| SC-PERM-003 | Verify create permission enforcement. | High | - | - | Not Automated |
| SC-PERM-004 | Verify edit permission enforcement. | High | - | - | Not Automated |
| SC-PERM-005 | Verify read-only users can view list. | Medium | - | - | Not Automated |
| SC-PERM-006 | Verify API authorization during create operation. | Critical | - | - | Not Automated |
| SC-PERM-007 | Verify session timeout during save. | High | - | - | Not Automated |
| SC-EDGE-001 | Verify page behavior with no categories available. | High | - | - | Not Automated |
| SC-EDGE-002 | Verify page behavior with one category. | Medium | - | - | Not Automated |
| SC-EDGE-003 | Verify page behavior with 1000+ categories. | High | - | - | Not Automated |
| SC-EDGE-004 | Verify pagination with large dataset. | High | - | - | Not Automated |
| SC-EDGE-005 | Verify simultaneous category creation by multiple users. | High | - | - | Not Automated |
| SC-EDGE-006 | Verify simultaneous edit on same category. | High | - | - | Not Automated |
| SC-EDGE-007 | Verify browser refresh during create operation. | Medium | - | - | Not Automated |
| SC-EDGE-008 | Verify browser refresh during edit operation. | Medium | - | - | Not Automated |
| SC-EDGE-009 | Verify application behavior after server restart. | Medium | - | - | Not Automated |
| SC-EDGE-010 | Verify category name with mixed language characters. | Medium | - | - | Not Automated |
| SC-EDGE-011 | Verify category name containing emojis. | Medium | - | - | Not Automated |
| SC-EDGE-012 | Verify user opens multiple category creation tabs. | Medium | - | - | Not Automated |
| SC-EDGE-013 | Verify save operation under slow network conditions. | High | - | - | Not Automated |
| SC-EDGE-014 | Verify category list after cache clear and re-login. | Medium | - | - | Not Automated |
| SC-EDGE-015 | Verify audit history generation for create/update actions (if supported). | Medium | - | - | Not Automated |

## 3. Evidence-Based Traceability Matrix

| TC ID | Status | Automation Evidence | Assertions Present | Missing Validations | Confidence |
|---|---|---|---|---|---:|
| SC-UI-001 | Fully Automated | `test_service_categories_page_loads_with_primary_controls`, lines 5-13. Uses `open_service_categories_page`; asserts page body and no broken state. | Lines 10-13 assert category text, status text, add button text, and no broken UI state. | Does not assert browser console/API errors. | 90% |
| SC-UI-004 | Partially Automated | Same test, lines 5-13. POM has exact page title locator at `service_categories_page.py:28` and waits for it at lines 57-65. | Test asserts `"Service category"` at line 10. | Does not assert exact title text `"Service categories"`. | 70% |
| SC-UI-005 | Partially Automated | POM search locator `service_categories_page.py:29`; invoked by search tests through `search_category`, lines 135-145. | Search tests indirectly require the input to be visible. | No UI-only assertion for placeholder `Category Name`. | 65% |
| SC-UI-006 | Partially Automated | POM filter locator exists at `service_categories_page.py:30`. | None in tests. | No test clicks or asserts the filter button is visible/clickable. | 25% |
| SC-UI-007 | Partially Automated | UI test lines 10-13; POM waits for add button clickable at `service_categories_page.py:63-64`. | Line 12 asserts `"Add new category"` appears. | Does not assert button enabled/clickable in test assertion. | 75% |
| SC-UI-008 | Partially Automated | UI test lines 10-13. | Lines 10-11 assert category/status text. | Edit column/action and full grid structure are not asserted. | 60% |
| SC-UI-015 | Partially Automated | `test_add_service_category_form_loads`, lines 16-23. | Lines 21-23 assert field labels and active switch default. | Does not assert a named `Category Information` section. | 70% |
| SC-UI-016 | Partially Automated | Same test, lines 16-23; POM waits for input at `service_categories_page.py:72`. | Line 21 asserts `"Category name"` visible. | Editable state is not explicitly asserted. | 70% |
| SC-UI-017 | Partially Automated | Same test, lines 16-23; POM `active_switch_is_on`, lines 207-212. | Line 23 asserts active switch is on. | Toggle functionality is not exercised. | 65% |
| SC-UI-018 | Partially Automated | Same test opens create form; POM waits for save button clickable at `service_categories_page.py:72-73`. | No direct assertion. | Save button text/visibility is not asserted by test. | 50% |
| SC-SRCH-001 | Fully Automated | `test_service_categories_existing_search`, lines 7-12. POM `search_category`, lines 135-145. | Line 12 asserts matching row is displayed. | None for exact search. | 95% |
| SC-SRCH-006 | Partially Automated | `test_service_categories_special_character_search_stays_usable`, lines 23-28. | Line 28 asserts page has no broken state after searching SQL-like text. | Does not assert safe empty result, no script execution, or backend response. | 55% |
| SC-SRCH-008 | Incorrectly Automated | `test_service_categories_missing_search`, lines 15-20. | Line 20 asserts the missing search value is not in body text. | Expected result requires a no-records message; current assertion can pass even if search is broken. | 30% |
| SC-CRUD-001 | Partially Automated | `test_create_active_service_category`, lines 5-11, via `create_category_if_missing`. | Lines 10-11 assert row and active status. | Helper may skip actual create when record already exists; no save-success message asserted. | 70% |
| SC-CRUD-002 | Fully Automated | Same test, lines 5-11. | Line 11 asserts status equals `Active`. | Inactive contrast not covered. | 90% |
| SC-CRUD-004 | Fully Automated | Same test, lines 5-11. | Line 10 asserts created/existing row is displayed after save/search. | Idempotent helper may reduce fresh-create evidence on repeat runs. | 85% |
| SC-CRUD-005 | Partially Automated | `test_edit_service_category_name_and_restore`, lines 6-19. POM `update_category_name`, lines 246-252. | Line 14 asserts updated row displayed. | Does not assert success toast, old row removal, status edit, or field persistence after reopening. | 75% |
| SC-CRUD-006 | Fully Automated | Same test, lines 10-14. | Line 14 asserts updated category name is displayed in the list. | Does not verify DB/API layer. | 90% |
| SC-CRUD-011 | Partially Automated | `test_service_category_settings_persist`, lines 14-20. | Lines 19-20 assert name and active switch on edit screen. | Does not refresh browser after save before validation. | 60% |
| SC-VAL-001 | Fully Automated | `test_service_category_required_name_validation`, lines 5-12. POM validity methods at `service_categories_page.py:187-205`. | Lines 11-12 assert invalid state and validation message. | Browser-native validation only; exact message not asserted. | 90% |
| SC-VAL-002 | Partially Automated | `test_service_category_blank_required_form_stays_on_form`, lines 15-22. | Lines 21-22 assert form remains and page has no broken state. | Does not assert no record was created in list. | 65% |
| SC-VAL-003 | Fully Automated | `test_create_active_service_category`, lines 5-11. | Lines 10-11 assert valid category is saved and active. | Uses fixed data, not parametrized valid names. | 85% |
| SC-VAL-005 | Partially Automated | `test_service_category_long_name_does_not_break_form`, lines 5-12. | Lines 11-12 assert no broken state and form still visible. | Does not assert max length rule, validation message, or saved/rejected behavior. | 45% |
| SC-PERM-001 | Fully Automated | `test_service_categories_page_loads_with_primary_controls`, lines 5-13, using authenticated browser fixture. | Lines 10-13 assert page content visible to authenticated user. | Does not assert role identity explicitly. | 85% |

### Not Automated Rationale

All cases marked `Not Automated` have no matching executable Service Categories test method with assertions in `tests/admin_portal/service_categories/`. In many cases the POM also lacks required methods, especially for filter popup controls, inactive toggling, cancel/back behavior, permissions, network interruption, concurrency, pagination, export/download, and audit-history validation.

Recommended target files by area:

- UI gaps: `tests/admin_portal/service_categories/test_service_categories_ui.py`
- Search gaps: `tests/admin_portal/service_categories/test_service_categories_search_filter.py`
- Filter gaps: new `tests/admin_portal/service_categories/test_service_categories_filters.py`
- CRUD gaps: `tests/admin_portal/service_categories/test_service_categories_positive.py` and `test_service_categories_edit.py`
- Validation/security gaps: `tests/admin_portal/service_categories/test_service_categories_validation.py`
- Permission gaps: new `tests/admin_portal/service_categories/test_service_categories_permissions.py`
- Edge/performance gaps: `tests/admin_portal/service_categories/test_service_categories_edge_cases.py`

## 4. Automation Suitability Matrix

| TC ID Range | Recommendation | Priority | Reason |
|---|---|---:|---|
| SC-UI-001 to SC-UI-008 | Must Automate | P1/P2 | Core screen availability and primary controls are smoke/regression candidates. |
| SC-UI-009 to SC-UI-014 | Good Candidate | P2/P3 | Useful visual/regression checks, but lower business impact than CRUD and validation. |
| SC-UI-015 to SC-UI-020 | Must Automate | P1/P2 | Create form usability and navigation are core workflows. |
| SC-SRCH-001 to SC-SRCH-011 | Must Automate | P1/P2 | Search is repeatable, stable, and high-value for regression. |
| SC-FLTR-001 to SC-FLTR-010 | Must Automate | P1/P2 | Current coverage is zero; filtering is a main list feature. |
| SC-CRUD-001 to SC-CRUD-012 | Must Automate | P1 | CRUD regressions directly affect business setup data. |
| SC-VAL-001 to SC-VAL-012 | Must Automate | P1/P2 | Validation/security inputs are repeatable and prevent data defects. |
| SC-PERM-001 to SC-PERM-007 | Must Automate where test users exist | P1/P2 | High risk, but depends on reliable role/session fixtures. |
| SC-EDGE-001 to SC-EDGE-004 | Good Candidate | P2 | Data-volume and empty-state coverage improves list reliability. |
| SC-EDGE-005 to SC-EDGE-006 | Good Candidate / Needs Manual Review | P2 | Requires parallel sessions or API setup; higher maintenance. |
| SC-EDGE-007 to SC-EDGE-014 | Good Candidate | P2/P3 | Useful resilience checks; automate after core gaps. |
| SC-EDGE-015 | Needs Manual Review | P3 | Depends on whether audit history is supported and where it is exposed. |

## 5. Coverage Metrics

| Metric | Count | Percent |
|---|---:|---:|
| Total Manual Test Cases | 87 | 100.0% |
| Fully Automated | 8 | 9.2% |
| Partially Automated | 15 | 17.2% |
| Incorrectly Automated | 1 | 1.1% |
| Not Automated | 63 | 72.4% |
| Automation Coverage, including partial/incorrect | 24 | 27.6% |
| Automation Coverage, excluding incorrect | 23 | 26.4% |
| Effective Coverage, full + 50% partial only | 15.5 | 17.8% |

Module coverage:

| Module Area | Manual Cases | Full | Partial | Incorrect | Not Automated | Effective Coverage |
|---|---:|---:|---:|---:|---:|---:|
| UI | 20 | 1 | 9 | 0 | 10 | 27.5% |
| Search | 11 | 1 | 1 | 1 | 8 | 13.6% |
| Filter | 10 | 0 | 0 | 0 | 10 | 0.0% |
| CRUD | 12 | 3 | 3 | 0 | 6 | 37.5% |
| Validation | 12 | 2 | 2 | 0 | 8 | 25.0% |
| Permissions | 7 | 1 | 0 | 0 | 6 | 14.3% |
| Edge Cases | 15 | 0 | 0 | 0 | 15 | 0.0% |

## 6. Gap Analysis

### Missing Automation

- 64 of 87 manual cases have no executable matching automation.
- The sheet’s manual automation status is materially overstated compared with repository evidence.

### Weak Assertions

- Invalid search only checks that the search string is absent, not that the no-records state is displayed.
- UI checks assert body text instead of specific visible/clickable elements and exact labels.
- Create tests use an idempotent helper, which is useful for setup but weak evidence for fresh create behavior.
- No tests assert success toasts or old-value removal after updates.

### Validation Gaps

- Duplicate category name.
- Spaces-only category name.
- Min/max length business rules.
- Unicode, emoji, XSS, SQL payloads in category-name field.
- Network interruption during save.

### CRUD Gaps

- Inactive category creation.
- Active/inactive status update.
- Cancel create/edit behavior.
- Browser back during create.
- Duplicate save prevention.
- Concurrent edit handling.

### Search Gaps

- Partial search.
- Case-insensitive search.
- Leading/trailing spaces.
- Numeric search.
- Blank search reset.
- Refresh persistence.
- Very long search.

### Filter Gaps

- No filter popup tests.
- No active/inactive filtering tests.
- No apply/reset validations.
- No filter + search or pagination combination.
- No no-records filter case.

### Permission Gaps

- Unauthorized direct URL access.
- Create/edit permission enforcement.
- Read-only role behavior.
- API authorization during create.
- Session timeout during save.

### Edge Case Gaps

- Empty and one-record datasets.
- Large dataset and pagination performance.
- Multi-user create/edit.
- Refresh during create/edit.
- Cache clear/re-login.
- Audit history.

## 7. Automation Improvement Plan

### Phase 1 - Critical Fixes

| TC ID | Priority | Effort | Recommended Test File | POM Changes Required | Assertions Required |
|---|---:|---|---|---|---|
| SC-SRCH-008 | P1 | Small | `test_service_categories_search_filter.py` | Add `get_empty_state_text` or `is_no_records_displayed`. | Assert no-records message and absence of matching row. |
| SC-CRUD-001 | P1 | Small | `test_service_categories_positive.py` | Add unique-name generator or reuse shared utility. | Assert save success, row visible, status visible. |
| SC-CRUD-003 | P1 | Medium | `test_service_categories_positive.py` | Add `ensure_active_switch_off`. | Assert row status `Inactive`. |
| SC-CRUD-007 | P1 | Medium | `test_service_categories_edit.py` | Add status toggle update helper. | Assert status changes after save and persists after reopen. |
| SC-VAL-002 | P1 | Small | `test_service_categories_validation.py` | Add row absence helper if needed. | Assert form remains and no blank/invalid record is created. |
| SC-VAL-007 | P1 | Medium | `test_service_categories_validation.py` | Add duplicate create flow and toast/error accessor. | Assert duplicate validation message and no duplicate row. |
| SC-PERM-002 | P1 | Medium/Large | `test_service_categories_permissions.py` | Role/session fixture required. | Assert redirect/access denied for unauthorized direct URL. |

Expected coverage after Phase 1: about 30 to 34 covered/effectively improved cases, depending on role fixture availability.

### Phase 2 - Coverage Improvements

| TC ID | Priority | Effort | Recommended Test File | POM Changes Required | Assertions Required |
|---|---:|---|---|---|---|
| SC-UI-002, SC-UI-003 | P2 | Small | `test_service_categories_ui.py` | Sidebar active/expanded locators. | Assert Services expanded and Service Categories highlighted. |
| SC-UI-005 to SC-UI-008 | P2 | Small | `test_service_categories_ui.py` | Element-specific getters for search/filter/grid/edit. | Assert exact controls visible/clickable and grid columns present. |
| SC-UI-019, SC-UI-020 | P2 | Small | `test_service_categories_ui.py` | Back icon locator if distinct from browser back. | Assert cancel/back returns to list without saving. |
| SC-SRCH-002 to SC-SRCH-005 | P2 | Small/Medium | `test_service_categories_search_filter.py` | Search clear helper. | Assert partial/case/trimmed searches return expected rows. |
| SC-SRCH-007, SC-SRCH-009, SC-SRCH-011 | P2 | Small | `test_service_categories_search_filter.py` | Search clear and empty-state helpers. | Assert numeric, blank reset, long text behavior. |
| SC-FLTR-001 to SC-FLTR-010 | P2 | Medium | `test_service_categories_filters.py` | Filter panel, active toggle, apply/reset/count helpers. | Assert active/inactive filtering, reset, combined search/filter, empty state. |
| SC-CRUD-008 to SC-CRUD-011 | P2 | Medium | `test_service_categories_positive.py` / `edit.py` | Cancel/back/refresh helpers. | Assert unsaved changes discarded and saved data persists after refresh. |
| SC-VAL-004 to SC-VAL-006 | P2 | Medium | `test_service_categories_validation.py` | Validation message helper. | Assert min/max/spaces behavior per business rules. |
| SC-VAL-008 to SC-VAL-011 | P2 | Medium | `test_service_categories_validation.py` | Parameterized invalid/special payload helpers. | Assert accepted/rejected behavior and no script execution. |

Expected coverage after Phase 2: about 60 to 68 cases covered or partially covered, with most core regression gaps closed.

### Phase 3 - New Automation

| TC ID | Priority | Effort | Recommended Test File | POM Changes Required | Assertions Required |
|---|---:|---|---|---|---|
| SC-PERM-003 to SC-PERM-007 | P2 | Large | `test_service_categories_permissions.py` | Role fixtures, session-timeout helpers, possible API helpers. | Assert button visibility by role, API rejection, timeout redirect. |
| SC-EDGE-001 to SC-EDGE-004 | P2 | Medium/Large | `test_service_categories_edge_cases.py` | Data setup/teardown helpers; pagination helpers. | Assert empty/one/large-data rendering and pagination. |
| SC-EDGE-005 to SC-EDGE-006 | P2 | Large | `test_service_categories_edge_cases.py` | Parallel browser/session support or API setup. | Assert conflict/integrity behavior. |
| SC-EDGE-007 to SC-EDGE-014 | P3 | Medium/Large | `test_service_categories_edge_cases.py` | Refresh, cache, re-login, multilingual data helpers. | Assert no corruption and latest persisted data. |
| SC-EDGE-015 | P3 | Large / Manual Review | New audit-specific test file if supported. | Audit history page/API access required. | Assert create/update audit entries. |

Expected coverage after Phase 3: about 75 to 82 cases if role, data-volume, and audit dependencies are available. Remaining cases may stay manual or needs-review due to environment constraints.

## Immediate Framework Recommendations

- Add `@pytest.mark.smoke`, `@pytest.mark.regression`, `@pytest.mark.validation`, `@pytest.mark.permissions` markers consistently.
- Add Allure feature/story/title annotations to every Service Categories test.
- Replace body-text assertions with element-level assertions where possible.
- Add common helpers for:
  - unique test data generation,
  - toast/error validation,
  - no-records grid validation,
  - row count and pagination validation,
  - sidebar active state validation.
- Keep one browser/session per module run where possible and avoid opening new windows for each case.
- Use setup helpers only for preconditions; do not let idempotent setup replace the actual create test.
