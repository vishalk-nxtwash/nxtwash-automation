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

---

## BUG 4 — Discount: "all locations" create form does not submit
- **Spec:** DS-HP-003
- **Found:** 2026-06-17 (reproduces headless, non-headless, and CI)
- **Module:** Admin Portal → Services → Discounts → Add new discount

**Steps to reproduce**
1. Add new discount; set name, category, Amount type, amount, start date.
2. Turn on "Allow discount at all locations".
3. Click **Save discount**.

**Expected:** Discount saves and returns to the list.
**Actual:** The form stays on `/services/discounts/new` — it never submits.
Each per-location row shows an empty "Percentage 0%" value while the global
type is Amount, which appears to block validation/submit.

**Automation:** `test_create_discount_assign_all_locations` — marked `xfail`
pending a page-object fix that fills per-location values (Phase 2).

---

## BUG 5 — Membership: re-activate edit form does not submit
- **Spec:** MB-EDT-009
- **Found:** 2026-06-17 (reproduces headless, non-headless, and CI)
- **Module:** Admin Portal → Services → Memberships → Edit

**Steps to reproduce**
1. Deactivate a membership; use the inactive filter to reopen it.
2. Turn the **Active service** toggle on.
3. Click **Save membership**.

**Expected:** Membership saves and returns to the list.
**Actual:** The edit form stays open; the list iframe never reloads
(`wait_for_list_loaded` times out even at 60s).

**Automation:** `test_activate_membership` — marked `xfail` pending investigation
of the save interaction (Phase 2).

---

## Phase 2 — managed-discount reset hardening (test-infra, not a product bug)
`reset_managed_discount` cannot find the managed record when it is left
**inactive** (the product hides inactive discounts from the default grid and
search) or **renamed**. The rename case now self-heals; the **inactive** case
still needs the reset to surface records via the inactive filter before
reactivating, otherwise activate/deactivate discount tests can leave duplicate
or stale state on teardown. Tracked for Phase 2.
