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

## BUG 4 — Employees: "Last Name" input is type="email", so employees cannot be created
- **Found during:** admin suite stabilization (2026-09-27)
- **Module:** Admin Portal → Users / Employees → Add employee
- **Severity:** High

**Steps to reproduce**
1. Admin Portal → Users / Employees → Employees → + Add employee.
2. Fill First Name, Last Name (e.g. `user 4`), Email, Phone, and click Save employee.

**Expected:** The employee is created.
**Actual:** Nothing happens. The Last Name input is rendered as
`<input name="lastName" type="email">`, so the browser's validation rejects any
normal surname ("Please include an '@' in the email address") and the form is
never submitted. No error is shown on the page.

**Impact:** Employees cannot be created through the UI on staging.

**Automation:** `create_employee_if_missing` detects this and marks dependent
employee tests as xfail with this reference; they run normally once fixed.

## BUG 5 — Customers: legacy customers without "Exempt tax" cannot be edited
- **Found during:** admin suite stabilization (2026-09-27)
- **Module:** Admin Portal → Customers → Edit customer
- **Severity:** High

**Steps to reproduce**
1. Open a customer created before the "Exempt tax" field existed (e.g. `auto customer1`).
2. Change any field and click Save changes.

**Expected:** The change is saved.
**Actual:** Nothing happens and no error is shown. The browser console logs
`onValidationError {"exemptTax": "Invalid input: expected boolean, received undefined"}`
— the form schema requires a boolean the record does not have.

**Impact:** Such customers cannot be edited in the UI at all, silently.

**Automation:** `CustomersPage.ensure_boolean_fields_defined()` toggles the
checkbox on and off (sets its displayed value) before saving, as a workaround.

## BUG 6 (suspected) — Memberships: unassigned location rows are cleared but still required
- **Found during:** admin suite stabilization (2026-09-27)
- **Module:** Admin Portal → Services → Memberships → Add / Edit membership
- **Severity:** Medium (needs product confirmation)

**Observed:** After unassigning locations on the membership form, their price /
commission inputs are emptied but keep `required`, so the browser's validation
silently blocks Save ("Please fill in this field"). Every new staging site adds
another such row.

**Automation:** `MembershipsPage.fill_all_empty_location_inputs()` types `0`
into every empty row before saving. Even with every row filled, create still
does nothing — see BUG 7.

## BUG 7 — Memberships: "Save membership" on the Add form does nothing
- **Found during:** admin suite stabilization (2026-09-28)
- **Module:** Admin Portal → Services → Memberships → + Add new membership
- **Severity:** High

**Steps to reproduce**
1. Services → Memberships → + Add new membership.
2. Fill name, type (Prepaid), global price/commission, assign the first location,
   fill every location price/commission (no HTML5 `:invalid` fields remain).
3. Click **Save membership**.

**Expected:** The membership is created and the app returns to the list.
**Actual:** Nothing happens. No network request is sent (verified by wrapping
`fetch`/`XMLHttpRequest` inside the iframe), no console error, no validation
message on any tab, no error styling, and the record is never created.
**Editing** an existing membership saves normally (redirects to the list).

**Impact:** New memberships cannot be created through the UI on staging.

**Automation:** The managed-membership fixture adopts a leftover
`VK decimal …` membership and renames it via the edit form, so dependent tests
run. `test_create_new_membership_saves` is an xfail canary that reports XPASS
once create works.
