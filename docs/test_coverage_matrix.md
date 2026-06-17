# Test Coverage Matrix — Admin Portal

Source of truth: **Services_Automation_Master_v2** Google Sheet
(tabs: `ServiceCategories`, `Membership`, `Discounts_Master`).

Status key: ✅ Covered · ⚠️ Partial (under-verifies the expected result) ·
❌ Missing · 🔮 Future (not expected yet).

Mapping note: this is a manual cross-reference of doc TC IDs against the current
automated tests. Script Allure IDs currently do **not** match the doc TC IDs
(see the ID-alignment finding in the review) — the "Automated test" column lists
the actual test function that satisfies each row.

---

## 1. Service Category — 6 / 20 covered (30%)

| Doc TC | Scenario | Status | Automated test |
|--------|----------|--------|----------------|
| SC-HP-001 | Create Active Category | ✅ | `test_create_active_service_category` |
| SC-HP-002 | Create Inactive Category | ❌ | — (page object always forces active) |
| SC-HP-003 | Edit Category | ✅ | `test_edit_service_category_name_and_restore` |
| SC-HP-004 | Activate Category | ❌ | — |
| SC-HP-005 | Deactivate Category | ❌ | — |
| SC-RG-001 | Search Exact Name | ✅ | `test_service_categories_search_variants_and_clear` |
| SC-RG-002 | Search Partial Name | ✅ | `test_service_categories_search_variants_and_clear` |
| SC-RG-003 | Filter Active | ❌ | — |
| SC-RG-004 | Filter Inactive | ❌ | — |
| SC-RG-005 | Export Categories | ❌ | — |
| SC-NG-001 | Create Without Name | ✅ | `test_service_category_required_name_validation` |
| SC-NG-002 | Create Duplicate Category | ❌ | — |
| SC-EC-001 | Rename Category Linked To Discount | ❌ | — (P1, dependency) |
| SC-EC-002 | Search After Rename | ⚠️ | partially via edit test |
| SC-EC-003 | Activate-Deactivate-Activate | ❌ | — |
| SC-EC-004 | Verify After Re-login | ❌ | — |
| SC-EC-005 | Edit Inactive Category | ❌ | — |
| SC-EC-006 | Deactivate Then Search/Filter | ❌ | — |
| SC-DEP-001 | Category Available During Discount Creation | ❌ | — (**P0**) |
| SC-DEP-002 | Deactivate Category Used By Discount | ❌ | — (**P0**) |

**Script-only extras (no doc row):** settings-persist, long-name edge, managed
baseline/rename, special-character search, UI shell/add-form, create-idempotent,
missing-search.

**Biggest gaps:** entire inactive/activate/deactivate lifecycle, filtering,
export, duplicate rule, all edge cases, both P0 dependency cases.

---

## 2. Discount — ~4 covered + 4 partial / 51 (~15%)

| Doc TC | Scenario | Status | Automated test |
|--------|----------|--------|----------------|
| DS-HP-001 | Create Amount Discount | ✅ | `test_create_amount_discount` |
| DS-HP-002 | Create Percentage Discount | ❌ | — (page object only does amount) |
| DS-HP-003 | Assign All Locations | ❌ | — |
| DS-HP-004 | Assign Specific Locations | ✅ | `test_discount_first_location_settings_persist` |
| DS-HP-005 | Edit Discount Value | ✅ | `test_edit_discount_reapplies_expected_settings` |
| DS-HP-006 | Activate Discount | ❌ | — |
| DS-HP-007 | Deactivate Discount | ❌ | — |
| DS-CMB-001 | Amount + All Locations + Active | ❌ | — |
| DS-CMB-002 | Amount + Selected Locations + Active | ❌ | — |
| DS-CMB-003 | Percentage + All Locations + Active | ❌ | — |
| DS-CMB-004 | Percentage + Selected Locations + Active | ❌ | — |
| DS-CMB-005 | Percentage + Future Start Date | ❌ | — |
| DS-CMB-006 | Amount + End Date | ❌ | — |
| DS-RG-001 | Search Exact Discount | ✅ | `test_discounts_existing_search` |
| DS-RG-002 | Search Partial Discount | ⚠️ | `test_discounts_partial_search_blocker` (xfail — **product defect**, doc expects matching results) |
| DS-RG-003 | Filter Active | ✅ | `test_discounts_filter_active_shows_only_active` (applies filter, asserts every visible row is Active; `@visual`) |
| DS-RG-004 | Filter By Site | ⚠️🐞 | **blocked by suspected product defect** — the discount filter "Select site" returns "No options" for any query, incl. the known site `VK Test carwash 2`. The same select preloads 11 sites in the membership filter, so it's discount-specific. Automation (`select_filter_site()`) is ready once the dropdown populates. |
| DS-RG-005 | Export Discounts | ❌ | — |
| DS-NG-001 | Create Without Category | ❌ | — |
| DS-NG-002 | Create Without Value | ❌ | — |
| DS-NG-003 | Start Date After End Date | ❌ | — |
| DS-NG-004 | Percentage Above Limit | ❌ | — |
| DS-NG-005 | No Location When Required | ❌ | — |
| DS-EC-001 | 0 Percent Discount | ❌ | — |
| DS-EC-002 | 100 Percent Discount | ❌ | — |
| DS-EC-003 | Future Start Date | ❌ | — |
| DS-EC-004 | Discount Expiring Today | ❌ | — |
| DS-EC-005 | Amount To Percentage | ❌ | — |
| DS-EC-006 | Percentage To Amount | ❌ | — |
| DS-EC-007 | Remove Assigned Location | ❌ | — |
| DS-EC-008 | Add Location To Existing Discount | ❌ | — |
| DS-UPD-006 | Change Discount Name | ❌ | — |
| DS-UPD-007 | Change Start Date | ❌ | — |
| DS-UPD-008 | Change End Date | ❌ | — |
| DS-UPD-009 | Change Category Assignment | ❌ | — |
| DS-UPD-010 | Selected Locations To All Locations | ❌ | — |
| DS-UPD-011 | All Locations To Selected Locations | ❌ | — |
| DS-PER-001 | Create Then Refresh | ⚠️ | `test_discount_settings_persist` (re-opens edit, not a true refresh) |
| DS-PER-002 | Create Then Re-login | ❌ | — |
| DS-PER-003 | Edit Then Refresh | ❌ | — |
| DS-PER-004 | Deactivate Then Refresh | ❌ | — |
| DS-SRH-004 | Search Inactive Discount | ❌ | — |
| DS-SRH-005 | Search After Edit | ❌ | — |
| DS-FLT-005 | Filter Active + Site | ❌ | — |
| DS-FLT-006 | Filter Inactive + Site | ❌ | — |
| DS-FLT-007 | Clear Filters | ⚠️ | `test_discounts_exact_search_clear_restores_records` (clears search box, not filter panel) |
| DS-FLT-008 | Search + Filter Together | ❌ | — |
| DS-DEP-001 | Category To Discount Flow | ❌ | — (**P0**) |
| DS-DEP-002 | Rename Linked Category | ❌ | — (**P0**) |
| DS-DEP-003 | Deactivate Linked Category | ❌ | — (**P0**) |
| DS-DEP-004 | Deactivate Assigned Site | ❌ | — (**P0**) |
| DS-DEP-005 | Edit Site Assignment | ❌ | — (**P0**) |

**Script-only extras (no doc row):** create-idempotent, long-name edge,
missing-search, special-character/payload search, discount-name-mandatory
validation, blank-form, negative-amount, managed baseline/mutation.

**Biggest gaps:** percentage discounts entirely (incl. 0%/100% boundaries),
all 6 combinations, activate/deactivate, all date/value negatives, all edit-flow
specifics, all 5 P0 dependency cases, export, site filters.

---

## 3. Membership — ~35 / 93 automatable covered (~37%)

(7 `MB-INT-*` integration rows are marked **Future** in the doc — correctly not
automated yet.)

### Covered (representative)
List: MB-LST-001/002 · Search: MB-SRH-001/002/004/005 · Name: MB-NAM-001..005 ·
Type: MB-TYP-001/002/003 · Price: MB-PRI-001/002/004/005 · Commission: MB-COM-003 ·
Barcode: MB-BAR-001/002 · Toggle: MB-TGL-001/002/004 · Location: MB-SIT-001/002 ·
Edit: MB-EDT-001..006/008 · Export: MB-EXP-001 (download only) · Filter:
MB-FLT-001 (panel) + MB-FLT-002/003/005/006/008 (type/site/active/inactive/reset,
result-verified).

### Missing (by module)
| Module | Missing doc TCs |
|--------|-----------------|
| Search | MB-SRH-003 (inactive) |
| Filter | MB-FLT-004 (barcode), MB-FLT-007 (multiple filters) — **002/003/005/006/008 now covered with result assertions + screenshots** |
| Export | MB-EXP-002 (filtered), MB-EXP-003 (matches grid) |
| Price/Commission | MB-PRI-003 (zero), MB-COM-001 (valid), MB-COM-002 (decimal) |
| Loyalty | MB-LTY-001/002/003 |
| Barcode | MB-BAR-003 (duplicate) |
| Portal | MB-TGL-003 (show on portal), MB-CPV-001/002 |
| Location | MB-SIT-003 (all), MB-SIT-004 (save w/o location), MB-LPR-002/003/004, MB-TAX-001/002, MB-LCM-001/002/003 |
| Redemption | MB-RED-002/003/004 (RED-001 partial) |
| Wash package | MB-WPK-001/002/003/004/005 (entire module) |
| Discount settings | MB-DIS-002/003/004/005 |
| Multi-month discount | MB-MMD-001..009 (entire module) |
| Edit | MB-EDT-007 (redemption config), MB-EDT-009 (activate), MB-EDT-010 (deactivate) |
| Integration | MB-INT-001..007 🔮 Future |

**Biggest gaps:** wash-package and multi-month-discount modules (entirely),
most filter variants, loyalty, tax exemption, location commission/portal,
redemption multi-location.

---

## Cross-feature themes
1. **ID alignment (done for mapped tests)** — tests that map 1:1 to a doc TC have
   been retitled to the doc IDs (`DS-`, `SC-HP/RG`, `MB-`). Tests that are extra
   coverage with no doc row keep their old `DIS-`/`MEM-`/`SC-*` labels and are
   listed under "Extras to add to the sheet" below.
2. **Filters only assert the panel opens** — they don't verify the filtered subset,
   so several "filter" rows are ⚠️ rather than ✅.
3. **P0 dependency cases are uniformly missing** across Service Category and
   Discount (cross-module reference behavior).
4. **Discount partial search (DS-RG-002)** is a confirmed product defect vs. the
   documented expected result — needs a bug, not just an xfail.
5. **Discount filter "Select site" is empty (suspected defect)** — returns
   "No options" for any query on staging, while the identical control in the
   membership filter preloads sites. Blocks DS-RG-004, DS-FLT-005/006/008, and
   the site-based discount dependency tests until fixed. Verified 2026-06-15.

---

## Extras to add to the sheet (automated, but no doc row yet)
These tests provide real coverage beyond the doc. Add rows so the doc and
automation converge:

- **Service Category:** settings-persist, long-name boundary, special-character
  search, blank-form-stays, create-idempotent, managed baseline/reset (framework).
- **Discount:** create-idempotent, long-name boundary, missing-search,
  special-character/payload search, discount-name-mandatory, blank-form-stays,
  negative-amount, list/grid/add-form UI (`DIS-UI-*`), managed baseline/reset.
- **Membership:** case-insensitive search, trim-spaces search, payload search,
  long-string search, settings-persistence (`MEM-CRUD-003/…`), cancel-on-create,
  download file-format, edit-action-present, pagination, add-form/redemption/
  discount-tab UI, save/cancel buttons, alphabetic-price, special-character search,
  managed baseline/reset (framework).

## Known redundancies / fixes still open
- Membership "search non-existing" is duplicated: both
  `test_memberships_missing_search` (search_filter) and
  `test_missing_membership_is_not_returned` (negative) map to **MB-SRH-004** —
  collapse to one.
- Membership special-character search was mis-tagged `MB-SRH-004`; now untitled as
  an extra (needs its own doc row).
