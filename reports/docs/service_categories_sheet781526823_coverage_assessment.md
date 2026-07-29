# Service Categories Coverage Assessment - Sheet gid 781526823

Source sheet: `1DQwP3_sDlKH9MakoNtZAlunMkEFuDz-fDNdSVsp8HHw`, tab `gid=781526823`

## Coverage Summary

| Metric | Count |
| --- | ---: |
| Total test cases reviewed | 20 |
| Automatable test cases | 20 |
| Incomplete Test Design | 0 |
| Fully Covered | 5 |
| Partially Covered | 7 |
| Not Covered | 8 |
| Framework Non-Compliant | 0 |
| Effective coverage | 25.00% |

Coverage calculation excludes incomplete test designs. All 20 rows have a concrete Service Category scenario and measurable expected result, so none were excluded.

Missing sheet metadata: Requirement ID, Component, Test Type, Test File, Marker, Execution Tier, Allure Epic, Allure Feature, Allure Story, Data Strategy, Cleanup Strategy, and Dependencies were not present in the CSV export. Existing repository conventions were used for assessment only; no missing metadata was invented.

## Framework Summary

| Area | Evidence |
| --- | --- |
| Language / framework | Python + Selenium + Pytest |
| Design pattern | Page Object Model: `pages/admin_portal/service_categories_page.py` |
| Reporting | Allure via `pytest.ini`; screenshots, HTML, and current URL are handled by shared framework hooks |
| Navigation | `tests/admin_portal/admin_session.py:77` uses `open_admin_path`; tests do not need hardcoded URLs |
| Markers | `pytest.ini:8` defines `smoke`, `sanity`, `regression`, `validation`, `export`, `permissions`, and others |
| Managed data | `tests/admin_portal/service_categories/conftest.py:54` defines managed category names; `:77` exposes `managed_category` |

## Traceability Matrix

| Test Case ID | Scenario | Status | Evidence | Notes |
| --- | --- | --- | --- | --- |
| SC-HP-001 | Create Active Category | Fully Covered | `test_service_categories_positive.py:15`, method `test_create_active_service_category`; asserts row and Active status at `:22-23`; setup helper at `conftest.py:28-37`; POM create at `service_categories_page.py:336` | Uses active baseline record and verifies visibility/status. |
| SC-HP-002 | Create Inactive Category | Not Covered | No test calls a create workflow with Active switch off. POM only has `ensure_active_switch_on` at `service_categories_page.py:314` and `create_category` always activates at `:336-340`. | Add create-inactive workflow and assert status Inactive. |
| SC-HP-003 | Edit Category | Fully Covered | `test_service_categories_edit.py:16`, method `test_edit_service_category_name_and_restore`; update call at `:23`, row assertion at `:26`, cleanup at `:28-31`; POM update at `service_categories_page.py:344` | Covers edit and persistence in grid. |
| SC-HP-004 | Activate Category | Partially Covered | `test_service_category_settings_persist` asserts Active switch is on at `test_service_categories_positive.py:33-34`; `test_create_active_service_category` asserts status Active at `:22-23`. | Missing inactive-to-active transition. |
| SC-HP-005 | Deactivate Category | Not Covered | No POM method turns Active switch off and no test asserts Inactive status after save. | Add `ensure_active_switch_off` and deactivation test using managed category. |
| SC-RG-001 | Search Exact Name | Fully Covered | `test_service_categories_search_filter.py:22`, method `test_service_categories_search_variants_and_clear`; exact search/assertion at `:32-33`. | Covers expected correct result. |
| SC-RG-002 | Search Partial Name | Fully Covered | Same method; partial search/assertion at `test_service_categories_search_filter.py:35-36`. | Covers matching results. |
| SC-RG-003 | Filter Active | Not Covered | `test_service_categories_ui.py:30` only asserts filter button is clickable. No test applies the Active filter or asserts all rows are active. | Add filter panel methods and active-result assertions. |
| SC-RG-004 | Filter Inactive | Not Covered | Same as SC-RG-003. No inactive filter application or result assertion exists. | Requires inactive data setup first. |
| SC-RG-005 | Export Categories | Partially Covered | `test_service_categories_ui.py:31` asserts download button display/clickability only. | Missing click, downloaded file verification, and exported data vs grid comparison. |
| SC-NG-001 | Create Without Name | Fully Covered | `test_service_categories_validation.py:15`, method `test_service_category_required_name_validation`; save without value at `:19-21`; invalid and validation message assertions at `:23-24`; form remains usable at `:27-36`. | Covers validation shown and blocked save behavior. |
| SC-NG-002 | Create Duplicate Category | Not Covered | `test_service_categories_negative.py:27` verifies idempotent setup, but does not attempt duplicate creation or assert duplicate-rule messaging. | Add duplicate submit test against managed category. |
| SC-EC-001 | Rename Category Linked To Discount | Not Covered | No Service Categories test creates/uses a discount dependency before renaming. | Requires managed Discount integration. |
| SC-EC-002 | Search After Rename | Partially Covered | `test_service_categories_edit.py:23-26` renames and searches edited name in same run. | Missing explicit old-name absence check and post-refresh search. |
| SC-EC-003 | Activate-Deactivate-Activate | Not Covered | No off/on state transition method or test exists. | Add state-cycle test after POM active toggle setter exists. |
| SC-EC-004 | Verify After Re-login | Not Covered | No Service Categories test logs out/re-authenticates and verifies category state. | Reuse auth/session helpers; avoid custom login retry logic. |
| SC-EC-005 | Edit Inactive Category | Not Covered | No inactive category setup exists. | Requires create inactive plus edit test. |
| SC-EC-006 | Deactivate Then Search/Filter | Not Covered | No deactivation or active/inactive filter assertions exist. | Depends on SC-HP-005 and filter POM methods. |
| SC-DEP-001 | Category Available During Discount Creation | Partially Covered | Discount module has managed fixtures, but no test maps Service Category creation to Discount category dropdown selection for this TC. | Cross-module coverage required; suitable for integration/regression. |
| SC-DEP-002 | Deactivate Category Used By Discount | Partially Covered | No direct automation. Business-rule behavior depends on Discount relationship and Service Category status transition. | P0 dependency rule should be automated once managed linked discount data is stable. |

## Gaps And Prioritized Backlog

| Rank | Test Case ID | Impact | Effort | Recommended File | Required Work |
| ---: | --- | --- | --- | --- | --- |
| 1 | SC-DEP-002 | P0 dependency protection | Large | `tests/admin_portal/service_categories/test_service_categories_dependencies.py` | Managed category linked to managed discount; deactivate attempt; assert rule enforced. |
| 2 | SC-DEP-001 | P0 discount creation dependency | Medium | `tests/admin_portal/service_categories/test_service_categories_dependencies.py` | Verify created/managed category is selectable during discount creation. |
| 3 | SC-HP-005, SC-EC-003, SC-EC-006 | Status state regression | Medium | `tests/admin_portal/service_categories/test_service_categories_state.py` | Add POM method to turn active switch off; test deactivate, reactivate, persistence, and search/filter visibility. |
| 4 | SC-HP-002, SC-EC-005 | Inactive record workflows | Medium | `tests/admin_portal/service_categories/test_service_categories_crud.py` | Create inactive category using managed data; edit inactive record; assert inactive status retained. |
| 5 | SC-RG-003, SC-RG-004 | Search/filter regression | Medium | `tests/admin_portal/service_categories/test_service_categories_search_filter.py` | Add filter drawer methods and assert all visible rows match selected status. |
| 6 | SC-NG-002 | Business-rule validation | Small | `tests/admin_portal/service_categories/test_service_categories_validation.py` | Attempt duplicate category creation and assert validation/toast/message. |
| 7 | SC-RG-005 | Export regression | Medium | `tests/admin_portal/service_categories/test_service_categories_export.py` | Click download, wait for file, parse export, compare visible category data. |
| 8 | SC-EC-004 | Session persistence | Small | `tests/admin_portal/service_categories/test_service_categories_persistence.py` | Verify managed category after browser/session refresh or re-login using existing auth helpers. |

## Automation Generated / Updated In This Pass

| File | Change |
| --- | --- |
| `tests/admin_portal/service_categories/test_service_categories_negative.py` | Added Allure metadata and pytest markers to make existing negative/search tests framework-compliant. |
| `tests/admin_portal/service_categories/test_service_categories_managed.py` | Restored baseline search before reading managed category status, fixing a real sequencing failure. |

No new tests were generated for dependency, inactive-state, filter-result, or export scenarios in this pass because the audit found missing POM operations and/or cross-module managed-data prerequisites. The backlog above identifies the correct files and required framework updates without creating placeholder tests.

## Execution Results

Command:

```bash
venv/bin/pytest tests/admin_portal/service_categories --headless --close-browser --alluredir=reports/allure-results-service-categories-sheet781526823-full --clean-alluredir
```

Result: `14 passed in 182.61s`

Allure report:

```text
reports/allure-report-service-categories-sheet781526823-full
```
