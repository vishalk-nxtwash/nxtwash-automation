# Bug reports — admin-portal automation (2026-06-15)

---

## ~~BUG 1 — Discount partial search returns no results~~ CLOSED — Not a product bug
- **Spec:** DS-RG-002
- **Closed:** 2026-06-15
- **Resolution:** Verified manually — partial search works correctly. The automation
  was asserting too quickly before the grid refreshed (debounce/timing issue).
  Fix: `test_discounts_partial_search` now uses `wait_for_discount_row` which
  waits for the result row to appear. `xfail` marker removed.

---

## ~~BUG 2 — Discount filter "Select site" dropdown is empty~~ CLOSED — Not a product bug
- **Spec:** DS-RG-004, DS-FLT-005, DS-FLT-006
- **Closed:** 2026-06-15
- **Resolution:** Verified manually — site dropdown populates correctly; selecting
  a site and clicking "Apply filters" returns the correct filtered results.
  Fix: `skip` markers removed from DS-RG-004, DS-FLT-005, DS-FLT-006.

---

## BUG 3 — Sites: Cannot re-enable inactive sites via filter
- **Found during:** DS-DEP-004 manual verification (2026-06-15)
- **Module:** Admin Portal → Sites / Locations
- **Severity:** Medium

**Steps to reproduce**
1. Admin Portal → Sites/Locations.
2. Apply the "Inactive" filter to find inactive sites.
3. Try to re-enable (activate) an inactive site from the filtered list.

**Expected:** Inactive sites appear in the filtered list; user can select and
re-enable them.
**Actual:** After applying the inactive filter, the list does not populate —
no inactive sites are shown, so they cannot be re-enabled through the UI.

**Impact:** Once a site is deactivated it cannot be reactivated via the filter.
Blocks reverting test data (e.g. `VK AL01`) used in DS-DEP-004.

**Automation:** No automation currently covers the Sites module.
Noted in `test_deactivate_assigned_site_reflects_in_discount` skip reason.
