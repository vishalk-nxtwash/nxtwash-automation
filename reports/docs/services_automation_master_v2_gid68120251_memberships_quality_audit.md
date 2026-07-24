# Services Automation Master v2 - Memberships Quality And Coverage Gate Audit

Source: Google Sheet 1DQwP3_sDlKH9MakoNtZAlunMkEFuDz-fDNdSVsp8HHw, tab gid=68120251.

## Coverage Summary

| Metric | Count |
| --- | ---: |
| Total Test Cases | 99 |
| Automatable Test Cases | 0 |
| Incomplete Test Design | 99 |
| Fully Covered | 0 |
| Partially Covered | 0 |
| Not Covered | 0 |
| Framework Non-Compliant | 0 |
| Coverage % | N/A - no automatable test cases in this sheet tab |

All rows were classified as Incomplete Test Design for coverage-calculation purposes because the exported sheet does not provide standalone actionable test steps or measurable expected results. Available columns are TC ID, Module Area, Scenario, Type, Priority, Automation, and Future Dependency.

This does not mean the product behavior is unautomated. It means this manual-test source is not sufficient to prove coverage or generate missing automation without assuming expected behavior.

## Extracted Metadata

| Field | Source Status |
| --- | --- |
| Test Case ID | Present as TC ID |
| Requirement ID | Missing |
| Module | Present as Module Area; all rows are Membership-related |
| Component | Missing |
| Test Type | Present as Type |
| Test File | Missing |
| Priority | Present |
| Marker | Missing |
| Execution Tier | Missing |
| Allure Epic / Feature / Story | Missing |
| Data Strategy | Missing |
| Cleanup Strategy | Missing |
| Dependencies | Partially present as Future Dependency |
| Test Steps | Missing |
| Expected Results | Missing |

## Inventory Distribution

Module Area counts:
- Discount Settings: 14
- Edit: 10
- Export: 3
- Filter: 8
- Integration: 7
- List: 2
- Location Assignment: 15
- Membership Settings: 26
- Redemption: 9
- Search: 5

Type counts:
- Edge: 8
- Negative: 16
- Positive: 75

Priority counts:
- P0: 7
- P1: 59
- P2: 33

## Framework Evidence Reviewed

| Area | Evidence |
| --- | --- |
| Language / runner | Python, Selenium, Pytest |
| Design pattern | POM under pages/admin_portal, especially pages/admin_portal/memberships_page.py |
| Reporting | Allure annotations in tests/admin_portal/memberships/*.py; markers declared in pytest.ini |
| Navigation | tests/admin_portal/admin_session.py provides authenticated navigation helpers; tests should not hardcode URLs |
| Membership fixtures | tests/admin_portal/memberships/conftest.py provides reusable test data and helpers |
| Managed data | tests/admin_portal/memberships/test_memberships_managed.py and tests/admin_portal/_managed.py support managed Membership reset behavior |
| Existing test areas | UI, search/filter shell, download, validation, positive CRUD, edit, edge cases, negative, managed-data checks |

## Useful Existing Automation References

These are evidence references that may map once the manual sheet is expanded with steps and expected results:

| Behavior Area | Existing Evidence |
| --- | --- |
| List shell and primary controls | tests/admin_portal/memberships/test_memberships_ui.py::test_memberships_page_loads_with_primary_controls |
| Grid columns and edit action | tests/admin_portal/memberships/test_memberships_ui.py grid/edit tests |
| Exact/partial/case/trim/missing/clear search | tests/admin_portal/memberships/test_memberships_search_filter.py |
| Filter panel shell | tests/admin_portal/memberships/test_memberships_search_filter.py::test_memberships_filter_panel_shows_controls |
| Download starts and file format | tests/admin_portal/memberships/test_memberships_download.py |
| Name/price/commission validation | tests/admin_portal/memberships/test_memberships_validation.py |
| Recurring/prepaid creation and persisted settings | tests/admin_portal/memberships/test_memberships_positive.py |
| Loyalty points and discount edit | tests/admin_portal/memberships/test_memberships_edit.py::test_edit_membership_loyalty_points_and_discount |
| Membership name edit and restore | tests/admin_portal/memberships/test_memberships_edit.py::test_edit_membership_name_and_restore |

## Traceability Matrix

| Test Case ID | Module Area | Scenario | Priority | Sheet Automation | Status | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| MB-LST-001 | List | Verify membership list loads | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LST-002 | List | Verify membership details displayed | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SRH-001 | Search | Search exact membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SRH-002 | Search | Search partial membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SRH-003 | Search | Search inactive membership | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SRH-004 | Search | Search non-existing membership | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SRH-005 | Search | Clear search restores results | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-001 | Filter | Filter by recurring type | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-002 | Filter | Filter by prepaid type | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-003 | Filter | Filter by site | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-004 | Filter | Filter by barcode | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-005 | Filter | Filter active memberships | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-006 | Filter | Filter inactive memberships | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-007 | Filter | Apply multiple filters together | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-FLT-008 | Filter | Reset filters | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EXP-001 | Export | Export memberships | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EXP-002 | Export | Export filtered memberships | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EXP-003 | Export | Verify export data matches grid | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-NAM-001 | Membership Settings | Valid membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-NAM-002 | Membership Settings | Blank membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-NAM-003 | Membership Settings | Duplicate membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-NAM-004 | Membership Settings | Maximum length membership name | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-NAM-005 | Membership Settings | Leading/trailing spaces in name | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TYP-001 | Membership Settings | Create recurring membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TYP-002 | Membership Settings | Create prepaid membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TYP-003 | Membership Settings | Change membership type during edit | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-PRI-001 | Membership Settings | Valid global price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-PRI-002 | Membership Settings | Blank global price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-PRI-003 | Membership Settings | Zero global price | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-PRI-004 | Membership Settings | Decimal global price | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-PRI-005 | Membership Settings | Negative global price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-COM-001 | Membership Settings | Valid global commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-COM-002 | Membership Settings | Decimal commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-COM-003 | Membership Settings | Negative commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LTY-001 | Membership Settings | Valid loyalty points | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LTY-002 | Membership Settings | Zero loyalty points | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LTY-003 | Membership Settings | Negative loyalty points | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-BAR-001 | Membership Settings | Membership with barcode | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-BAR-002 | Membership Settings | Membership without barcode | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-BAR-003 | Membership Settings | Duplicate barcode | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TGL-001 | Membership Settings | Create active membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TGL-002 | Membership Settings | Create inactive membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TGL-003 | Membership Settings | Show membership on customer portal | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TGL-004 | Membership Settings | Hide membership from customer portal | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SIT-001 | Location Assignment | Assign single location | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SIT-002 | Location Assignment | Assign multiple locations | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SIT-003 | Location Assignment | Assign all locations | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-SIT-004 | Location Assignment | Save without assigned location | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LPR-001 | Location Assignment | Override location price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LPR-002 | Location Assignment | Use global price only | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LPR-003 | Location Assignment | Zero location price | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LPR-004 | Location Assignment | Negative location price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TAX-001 | Location Assignment | Enable tax exemption | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-TAX-002 | Location Assignment | Disable tax exemption | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LCM-001 | Location Assignment | Set location commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LCM-002 | Location Assignment | Override global commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-LCM-003 | Location Assignment | Negative location commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-CPV-001 | Location Assignment | Show location on customer portal | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-CPV-002 | Location Assignment | Hide location on customer portal | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-RED-001 | Redemption | Redeem at single location | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-RED-002 | Redemption | Redeem at multiple locations | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-RED-003 | Redemption | Redeem at all locations | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-RED-004 | Redemption | Save without redemption location | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-WPK-001 | Redemption | Assign wash package | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-WPK-002 | Redemption | Different wash package per location | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-WPK-003 | Redemption | Change assigned wash package | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-WPK-004 | Redemption | Save without wash package | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-WPK-005 | Redemption | Mapped wash package becomes inactive | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-DIS-001 | Discount Settings | Assign single discount | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-DIS-002 | Discount Settings | Assign multiple discounts | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-DIS-003 | Discount Settings | Remove assigned discount | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-DIS-004 | Discount Settings | Save membership without discount | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-DIS-005 | Discount Settings | Only active discounts available | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-001 | Discount Settings | Add multi-month discount profile | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-002 | Discount Settings | Add multiple discount profiles | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-003 | Discount Settings | Remove discount profile | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-004 | Discount Settings | Valid discount selection | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-005 | Discount Settings | Valid month value | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-006 | Discount Settings | Zero month value | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-007 | Discount Settings | Negative month value | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-008 | Discount Settings | From date greater than To date | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-MMD-009 | Discount Settings | Overlapping date ranges | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-001 | Edit | Edit membership name | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-002 | Edit | Edit membership type | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-003 | Edit | Edit global price | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-004 | Edit | Edit global commission | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-005 | Edit | Edit loyalty points | P2 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-006 | Edit | Edit assigned locations | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-007 | Edit | Edit redemption configuration | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-008 | Edit | Edit discount configuration | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-009 | Edit | Activate inactive membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-EDT-010 | Edit | Deactivate active membership | P1 | Yes | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-001 | Integration | Membership maps to configured wash package | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-002 | Integration | Updated wash package reflected in membership | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-003 | Integration | Membership references assigned discounts | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-004 | Integration | Discount updates reflected in membership | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-005 | Integration | Membership visible on customer portal when enabled | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-006 | Integration | Membership hidden on customer portal when disabled | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |
| MB-INT-007 | Integration | Membership description displayed on customer portal | P0 | Future | Incomplete Test Design | Missing standalone test steps and measurable expected results in the sheet tab; automation generation would require assumptions. |

## Gap Analysis

| Gap | Impact | Recommendation |
| --- | --- | --- |
| Missing expected results for all 99 rows | Prevents defensible coverage status and assertion design | Add an Expected Result column with measurable outcomes for each scenario |
| Missing test steps for all 99 rows | Prevents reliable automation workflow generation | Add Given/When/Then or numbered steps for each TC |
| Missing test file, marker, execution tier, and Allure metadata | Prevents metadata-preserving generation | Add automation metadata columns or provide a mapping file |
| Missing data and cleanup strategy | Risk of permanent data creation and flaky tests | Define managed-record/reusable-data expectations per TC |
| Sheet Automation=Yes conflicts with quality gate | Yes cannot be treated as code evidence | Replace with actual automation file/method or leave as target status |

## Recommended Next Step

Update this sheet tab with at least Test Steps, Expected Results, Test File, Marker, Allure Story, Data Strategy, and Cleanup Strategy. After that, rerun the coverage audit and map rows to executable tests with line-level evidence. No production automation was generated in this pass because every row failed the required manual-test quality gate.