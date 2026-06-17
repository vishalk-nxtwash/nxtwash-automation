# Document sync checklist — Services_Automation_Master_v2

Changes to apply back to the Google Sheet so the spec and the automation stay in
sync. Grouped by action. (Generated 2026-06-15.)

---

## A. ADD new rows — automated coverage with no spec row yet
These tests exist and pass but have no TC in the sheet. Add a row each so coverage
is traceable both ways.

### Service Category (tab: ServiceCategories)
| Suggested ID | Scenario | Expected Result |
|---|---|---|
| SC-PER-001 | Created category settings persist after save | Name + Active state retained |
| SC-EC-007 | Long category name does not break the form | Form stays usable |
| SC-NG-003 | Special-character search stays usable | No broken grid |
| SC-NG-004 | Blank required form stays on create page | Not saved, stays on form |

### Discount (tab: Discounts_Master)
| Suggested ID | Scenario | Expected Result |
|---|---|---|
| DS-NG-006 | Create flow is idempotent (re-run create) | No duplicate / stable |
| DS-EC-009 | Long discount name does not break the form | Form stays usable |
| DS-NG-007 | Missing discount search returns nothing | No records, no error |
| DS-NG-008 | Special-character / payload search stays usable | No broken grid |
| DS-NG-009 | Discount name is mandatory | Validation shown |
| DS-NG-010 | Blank required form stays on create page | Not saved |
| DS-NG-011 | Negative amount does not break the form | Form stays usable |
| DS-UI-001..003 | List primary controls / grid columns / add-form load | Rendered |

### Membership (tab: Membership)
| Suggested ID | Scenario | Expected Result |
|---|---|---|
| MB-SRH-006 | Case-insensitive search | Match found |
| MB-SRH-007 | Search trims surrounding spaces | Match found |
| MB-SRH-008 | Search payloads do not break grid | No broken grid |
| MB-SRH-009 | Very long search string | No broken grid |
| MB-NAM-006 | Alphabetic global price rejected | Save blocked |
| MB-UI-009/014..021 | Edit action, pagination, add-form/redemption/discount tab UI, save/cancel | Rendered |
| MB-NG-001 | Special-character search stays usable | No broken grid (was mis-tagged MB-SRH-004) |
| MB-CRUD-CANCEL | Cancel on create discards membership | Not saved |

> IDs above are suggestions — adjust to your numbering convention.

---

## B. UPDATE status / add defect note
| TC ID | Change |
|---|---|
| DS-RG-002 | Mark **Failing / Known defect**; link **BUG 1** (partial search returns nothing). |
| DS-RG-004 | Mark **Blocked / Known defect**; link **BUG 2** (filter "Select site" empty). Also flag DS-FLT-005/006/008 as blocked by the same bug. |

---

## C. FYI — alignment already done in code (no sheet change needed)
- Automated test Allure IDs were realigned to the sheet's TC IDs
  (`DS-`, `SC-HP/RG/NG`, `MB-`) for all 1:1-mapped tests.
- DS-RG-003 now fully verifies "only active shown" (was panel-open only).
- Duplicate: two tests map to **MB-SRH-004** (one in search_filter, one in
  negative) — collapse to one in the suite; no sheet change.
