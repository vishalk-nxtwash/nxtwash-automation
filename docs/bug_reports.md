# Bug reports — surfaced by admin-portal automation (2026-06-15)

Both are discount-filter/search defects found while building coverage against the
`Discounts_Master` spec. File these in the tracker and link the IDs back into the
test sheet and the `xfail`/deferred markers in code.

---

## BUG 1 — Discount partial search returns no results
- **Spec:** DS-RG-002 (Search Partial Discount → "Matching results")
- **Severity:** Medium (search usability)
- **Environment:** staging.nxtwash.com, 2026-06-15

**Steps to reproduce**
1. Admin Portal → Services → Discounts.
2. In the discount search box, type a partial/substring of an existing discount
   name (e.g. first 4 chars of `VK AD02`).

**Expected:** discounts whose name contains the substring are listed.
**Actual:** no records are returned for the partial term (only exact matches work).

**Automation:** `test_discounts_partial_search_blocker` (DS-RG-002) is marked
`xfail(strict=True)` — it will flip to XPASS automatically once fixed.

---

## BUG 2 — Discount filter "Select site" dropdown is empty
- **Spec:** DS-RG-004 (Filter By Site), also blocks DS-FLT-005/006/008 and
  site-based DS-DEP cases
- **Severity:** Medium–High (site filtering and dependency flows unusable)
- **Environment:** staging.nxtwash.com, 2026-06-15

**Steps to reproduce**
1. Admin Portal → Services → Discounts → "Filter by".
2. Click the "Select site" dropdown (optionally type `carwash`).

**Expected:** the site list populates; selecting a site (e.g. `VK Test carwash 2`)
filters the discount grid to that site.
**Actual:** the dropdown shows **"No options"** for any query, incl. the known
site `VK Test carwash 2` — discounts cannot be filtered by site.

**Key comparison (isolates the defect):** the identical "Select site" control in
the **Memberships** filter preloads 11 sites and filters correctly, so the issue
is specific to the Discounts filter, not the site data.

**Automation:** DS-RG-004 is deferred (not xfail, since it's a UI/data-population
defect not a behavioral assertion). `DiscountsPage.select_filter_site()` is ready
and will work once the dropdown populates.
