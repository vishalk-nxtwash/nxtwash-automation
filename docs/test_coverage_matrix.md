# Test Coverage Matrix — Admin Portal

Source of truth: **Services_Automation_Master** Google Sheet
(tabs: `Service Category`, `Membership`, `Discounts_Master`).

Status key: ✅ Covered · ⚠️ Partial (under-verifies the expected result) ·
❌ Missing · 🔮 Future (not expected yet) · 🐞 Blocked by product defect.

**ID alignment (Phase 1 — done 2026-06-17):** automated `@allure.title` IDs have
been realigned to the sheet's TC IDs. The legacy `DIS-*`/`EXP-*` prefixes and the
mis-numbered `DS-RG`/`DS-SRH`/`DS-FLT`/`DS-UPD` search/filter/update/export IDs are
gone; Membership `MB-TGL-*` scenario mismatches are fixed (activate/deactivate now
`MB-EDT-009/010`). Tests with no sheet row keep an `*-EXTRA`-style legacy label and
are listed under "Extras" per module.

> ⚠️ The sheet's **"Automation: Yes"** column is aspirational, not factual, for
> Service Category and Membership — many rows marked "Yes" are **not** automated
> (see gaps below). Do not treat the sheet as sign-off evidence until either the
> tests are built (Phase 2) or those rows are set to No/Partial.

---

## 1. Service Category — ~10 / 30 covered (~33%)

| Suite | Covered | Missing |
|-------|---------|---------|
| Happy Path | SC-HP-001, SC-HP-003 | **SC-HP-002 (create inactive), SC-HP-004 (activate), SC-HP-005 (deactivate)** |
| Search | SC-RG-001, SC-RG-002, SC-RG-006 | — |
| Filter | — | **SC-RG-003 (active), SC-RG-004 (inactive), SC-RG-007 (toggle off)** |
| Export | — | SC-RG-005 |
| Negative | SC-NG-001, SC-NG-003 ⚠️ | SC-NG-002 (duplicate), SC-NG-004 (whitespace), SC-NG-005 (case-insensitive dup), SC-NG-006 (dup inactive) |
| Edge | SC-EC-002 ⚠️ | SC-EC-001, SC-EC-003, SC-EC-004 (re-login), SC-EC-005, SC-EC-006, SC-EC-007/008 (cancel add/edit) |
| Dependency (P0) | SC-DEP-001, SC-DEP-002 (from Discount side) | SC-DEP-003 (service assignment), SC-DEP-004 (rename w/ assigned services) |

- ⚠️ `SC-NG-003` only asserts the form does not break; sheet expects reject/truncate.
- ⚠️ `SC-EC-002` satisfied indirectly by the edit-and-restore test.
- **Extras (no sheet row):** SC-SRCH-002 (special-char search), SC-CRUD-002
  (settings persist), SC-CRUD-004 (idempotent), SC-VAL-002 (blank form stays),
  SC-UI-001/002, SC-MANAGED-001/002 (framework).
- **Biggest gaps:** entire activate/deactivate lifecycle, status filters, export,
  duplicate-rule negatives, cancel flows, re-login persistence, P0 `SC-DEP-003/004`.

---

## 2. Discount — ~67 / 67 automatable covered (100%); 5 `FUT-*` are Future

All sheet rows now have a mapped, ID-aligned test.

| Suite | Status |
|-------|--------|
| Happy Path DS-HP-001..007 | ✅ (plus extra DS-HP-008 idempotent) |
| Combination DS-CMB-001..006 | ✅ |
| Edge DS-EC-001..009 | ✅ |
| Negative DS-NG-001..006 | ✅ |
| Persistence DS-PER-001..004 | ✅ |
| Updates DS-UPD-001..006 | ✅ |
| Search DS-SRH-001..006 | ✅ |
| Filter DS-FLT-001..006 | ✅ |
| Export DS-EXP-001..004 | DS-EXP-001 ⚠️ (button-clickable only; sheet expects "matches grid"), 002/003/004 ✅ |
| Dependency DS-DEP-001..005 (P0) | DS-DEP-001 ✅; **DS-DEP-002..005 xfail** — stubs awaiting Service-Category / Sites page support |
| UI DS-UI-001..003 | ✅ |
| Validation DS-VAL-001..003 | ✅ |
| Framework DS-FRM-001/002 | ✅ (managed baseline/reset) |
| 🔮 FUT-001..005 (POS/Kiosk/Reports/Dashboard) | Future — correctly not automated |

- **Extras (no sheet row):** DIS-SRCH-002 (clear search box restores), DS-HP-008
  (create idempotent), DS-SRH-NEG-001 (duplicates DS-SRH-005 — collapse in Phase 2).
- **Open item:** strengthen DS-EXP-001 to compare export content vs grid; wire up
  DS-DEP-002..005 once cross-module page support lands.

---

## 3. Membership — ~46 / 93 automatable covered (~49%); 7 `MB-INT-*` are Future

### Covered (by module)
List MB-LST-001/002 · Search MB-SRH-001..005 · Filter MB-FLT-001/002/003/005/006/007/008 ·
Export MB-EXP-001/002 · Name MB-NAM-002..005 · Type MB-TYP-001/002/003 ·
Price MB-PRI-002/004/005 · Commission MB-COM-003 · Barcode MB-BAR-001/002 ·
Toggle MB-TGL-002/004 · Location MB-SIT-001/002 ·
Edit MB-EDT-001/003/004/005/006/008/009/010.

### Missing (sheet says "Yes", not automated)
| Module | Missing doc TCs |
|--------|-----------------|
| Loyalty | **MB-LTY-001/002/003 (entire module)** |
| Location price | **MB-LPR-001..004 (entire module)** |
| Tax exemption | **MB-TAX-001/002** |
| Location commission | **MB-LCM-001/002/003** |
| Customer-portal location | **MB-CPV-001/002** |
| Redemption | **MB-RED-001..004** (only the Redemption tab UI is checked) |
| Wash package | **MB-WPK-001..005 (entire module)** |
| Multi-month discount | **MB-MMD-001..009 (entire module)** |
| Discount assignment | **MB-DIS-001..005** (only edit-discount-config MB-EDT-008 exists) |
| Filter | MB-FLT-004 (barcode) |
| Export | MB-EXP-003 (matches grid) |
| Price/Commission | MB-PRI-003 (zero), MB-COM-001/002 (valid/decimal) |
| Barcode | MB-BAR-003 (duplicate) |
| Toggle/Portal | MB-TGL-003 (show on portal) |
| Location | MB-SIT-003 (all), MB-SIT-004 (save w/o location) |
| Search | MB-SRH-003 covered ✅ |
| Edit | MB-EDT-007 (redemption config) |
| Integration | 🔮 MB-INT-001..007 (Future) |

- MB-HP create-active (MB-TGL-001) and MB-NAM-001 / MB-PRI-001 / MB-COM-001 "valid"
  rows are exercised implicitly by the creation tests.
- **Extras (no sheet row):** MEM-CRUD-003/004/005/011/012/013/015/016/018
  (persistence), MEM-CRUD-008 (cancel), MEM-DL-002 (file format),
  MEM-SRCH-003/004/005/007 (case/payload/trim/long), MEM-UI-009/014..022,
  MEM-VAL-003/008, MEM-MANAGED-001/002, MEM-FLT-007b (multi-filter variant),
  special-character search (negative).
- **Biggest gaps:** wash-package, multi-month-discount, loyalty, redemption,
  tax, location price/commission, customer-portal-location, discount-assignment —
  all entire modules.

---

## Cross-feature themes
1. **ID alignment — done.** Automated IDs now match the sheet (Phase 1). Extras
   keep distinct legacy labels and are listed per module above.
2. **Sheet "Automation: Yes" overstates reality** for Service Category (~33% real)
   and Membership (~49% real). Discount is genuinely complete (minus Future rows).
3. **P0 dependency cases** are the highest-value gap: SC-DEP-003/004 and the
   xfail DS-DEP-002..005 (cross-module reference behavior).
4. **Known redundancy:** DS-SRH-NEG-001 duplicates DS-SRH-005 — collapse.

## Phase 2 (build missing tests, after staging login is fixed & CI re-enabled)
Priority order: **Service Category lifecycle** (HP-002/004/005, EC-003) →
SC filters/negatives → Membership wash-package & multi-month-discount →
remaining Membership modules. Each needs new page-object methods and must be
verified against staging as written.
