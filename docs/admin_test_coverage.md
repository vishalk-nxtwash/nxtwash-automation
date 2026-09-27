# Admin Portal Test Coverage — Full & Smoke

**Status: stabilization pass 1 (2026-09-27).** Covered vs pending tests for the
admin full suite and smoke, with the next action for every gap. Companion to
`docs/superadmin_test_coverage.md`.

Status key: ✅ Covered (real check) · 🟡 Xfail but passing (promote) ·
⚠️ Xfail (not working yet) · ⏭️ Skipped · 🔥 In smoke.

---

## 1. Where things stand

**2,146 tests in 30 modules** (was 2,329 — 183 duplicated tests removed).
Latest CI outcome per test (GitHub-hosted, targeted parallel runs):
**1,148 passed · 5 failed · 144 xfail · 91 xpass · 677 skipped** — memberships
not included (its run was cancelled; see pending).

| Group | Modules | Status |
|---|---|---|
| Reports | revenue_overview, performance_metrics, general_sales_report, transactions, cash_report, card_declines, labor_shifts, wash_activity, redemptions | ✅ all green |
| Catalog | wash_books, wash_extras, custom_services, service_categories, discounts, gift_cards, coupon_packages | ✅ all green |
| Catalog | wash_packages | ⚠️ 36 pass / 4 fail (save race, below) |
| Catalog | memberships | ⚠️ create flow blocked (below) |
| People | customers, users, user_roles | ✅ green |
| People | employees | ✅ green (create path = product BUG 4 → xfail) |
| Settings | sites, kiosk_settings, tunnel_settings, pos_settings, bank_drop | ✅ green |
| Settings | gas_pump_settings | ✅ 26/27 (GPS-CRT-013 xfail — data) |
| Auth / overview | login, overview | ✅ green |

### How to run

```bash
# One module / test on CI — each path becomes its own parallel job
gh workflow run suite-admin.yml --ref <branch> \
  -f test_path="tests/admin_portal/cash_report tests/admin_portal/card_declines"

# Full suite on CI (4 waves) / smoke
gh workflow run suite-admin.yml --ref <branch>
gh workflow run suite-admin-smoke.yml --ref <branch>

# Locally
pytest tests/admin_portal/<module> --headless -n 4
pytest tests/admin_portal -m smoke --headless -n 2
```

All admin workflows share one `admin-staging` concurrency queue (runs queue,
never overlap). Working rule: fix locally (3×) → run only that test on CI via
`test_path` → then the module/group.

---

## 2. Smoke — 147 curated tests

4–6 explicit `@pytest.mark.smoke` checks per module (page loads, key data,
filter, create/edit, validation, save, export) across all 30 modules; no xfail
or skipped tests in smoke. 7 balanced shards, ~5–15 min.

Pending in smoke: memberships create/persist (blocked, below); wash-packages
activate/validation (click fixed; re-confirm after the save-race fix).

---

## 3. Pending — known failures and next actions

| Item | Diagnosis | Next action |
|---|---|---|
| **Memberships create / settings persist** | Stacked blockers. Fixed: select-all key; empty required location rows (typed `0`). Still failing after Save — the page runs in a cross-origin legacy iframe, so the failure hook can't see its API calls | Trace the remaining step after Save (success signal / list refresh); consider API seeding of `VK MA5` |
| **Wash packages: barcode, name, global price, managed reset** | Save → navigate race inside the legacy iframe: `save_and_return_to_list()` waits for the Save button to disable/re-enable, else sleeps 5 s, then navigates — sometimes before the save lands. Inconsistent (price passed locally, failed on CI) | Wait for a real "saved" signal (success toast / list value) before navigating; same helper pattern likely affects other legacy forms |
| **Gas pump GPS-CRT-013** | Fixed-name pump `VK AGP04 INA` cannot be deleted and exists as Active (left by an earlier run whose toggle click the staging toast swallowed) | Managed-record redesign (reset-to-baseline) |
| **91 🟡 xfail-but-passing** | Pass today but cannot fail CI (35 in overview) | Confirm across 2+ runs, remove the xfail |
| **141 locator rewrites** | Label/section heuristics no longer match the DOM (settings sections, permission accordions) | Rewrite per module |
| **Legacy Overview iframe** (22) | Loads empty on staging | Product/env question |
| **Network hook blind spot** | Cross-origin legacy iframes run out of process; their API calls are not in the page's performance log | Attach CDP to iframe targets (auto-attach) |

### Product bugs found (see `docs/bug_reports.md`)

- **BUG 4** — Employees: Last Name input is `type="email"` → employees cannot be created.
- **BUG 5** — Customers created before "Exempt tax" existed cannot be edited (silent validation error).
- **BUG 6 (suspected)** — Memberships: unassigned location rows cleared but still required.
- Product changes the tests were updated for: users grid "Status" column removed; gas pump / tunnel headers renamed to "Name".

### Staging data hygiene

- Tests create uniquely-named records each run with no cleanup (e.g. many
  `VK decimal xxxxxx` memberships; new `VK AL0x` sites). Each new site adds a
  required price/commission row to membership forms. Needs managed records or
  a backend purge.

---

## 4. Full suite — summary by module

| Module | Tests | ✅ Covered (must pass) | 🟡 Xfail but passing (promote) | ⚠️ Xfail (not yet working) | ⏭️ Skipped | 🌱 Seed-only | 🔥 In smoke |
|---|---|---|---|---|---|---|---|
| bank_drop | 27 | 20 | 1 | 2 | 4 | 0 | 4 |
| card_declines | 84 | 75 | 3 | 4 | 2 | 0 | 11 |
| cash_report | 56 | 43 | 0 | 0 | 13 | 0 | 4 |
| coupon_packages | 45 | 26 | 0 | 0 | 19 | 0 | 5 |
| custom_services | 58 | 12 | 1 | 2 | 43 | 0 | 3 |
| customers | 93 | 54 | 1 | 0 | 38 | 0 | 6 |
| discounts | 73 | 49 | 0 | 6 | 18 | 0 | 2 |
| employees | 98 | 45 | 0 | 2 | 51 | 0 | 6 |
| gas_pump_settings | 39 | 27 | 0 | 0 | 12 | 0 | 9 |
| general_sales_report | 83 | 71 | 0 | 0 | 12 | 0 | 4 |
| gift_cards | 37 | 29 | 2 | 2 | 4 | 0 | 3 |
| kiosk_settings | 91 | 12 | 0 | 8 | 71 | 0 | 3 |
| labor_shifts | 86 | 83 | 0 | 1 | 2 | 0 | 7 |
| login | 44 | 40 | 0 | 2 | 2 | 0 | 6 |
| memberships | 66 | 59 | 0 | 6 | 1 | 0 | 5 |
| overview | 76 | 18 | 35 | 23 | 0 | 0 | 3 |
| performance_metrics | 86 | 66 | 0 | 18 | 2 | 0 | 4 |
| pos_settings | 68 | 52 | 0 | 3 | 13 | 0 | 6 |
| redemptions | 103 | 74 | 0 | 1 | 28 | 0 | 4 |
| revenue_overview | 100 | 77 | 6 | 9 | 8 | 0 | 4 |
| service_categories | 36 | 15 | 2 | 6 | 13 | 0 | 4 |
| sites | 66 | 40 | 4 | 4 | 18 | 0 | 5 |
| transactions | 121 | 82 | 0 | 11 | 28 | 0 | 4 |
| tunnel_settings | 46 | 26 | 1 | 14 | 5 | 0 | 6 |
| user_roles | 72 | 29 | 1 | 5 | 37 | 0 | 4 |
| users | 68 | 39 | 0 | 1 | 28 | 0 | 4 |
| wash_activity | 83 | 46 | 27 | 5 | 5 | 0 | 9 |
| wash_books | 82 | 64 | 0 | 2 | 16 | 0 | 5 |
| wash_extras | 79 | 56 | 1 | 1 | 21 | 0 | 5 |
| wash_packages | 80 | 41 | 6 | 8 | 25 | 0 | 2 |
| **Total** | **2146** | **1370** | **91** | **146** | **539** | **0** | **147** |

## 5. Full suite — details by module

Each module lists what is covered, then every pending test with its reason and the next action. "Xfail but passing" is based on the last full GitHub run; re-check before promoting.

### bank_drop

<details><summary>✅ Covered — 20 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `bank_drop/test_bank_drop_edge_cases.py::test_download_button_is_visible` | — |  |
| `bank_drop/test_bank_drop_edge_cases.py::test_duplicate_name_documents_behavior` | — |  |
| `bank_drop/test_bank_drop_edge_cases.py::test_duplicate_order_documents_behavior` | — |  |
| `bank_drop/test_bank_drop_edge_cases.py::test_negative_order_documents_behavior` | — |  |
| `bank_drop/test_bank_drop_edge_cases.py::test_zero_order_documents_behavior` | — |  |
| `bank_drop/test_bank_drop_edit.py::test_activate_inactive_bank_drop` | — | 🔥 |
| `bank_drop/test_bank_drop_edit.py::test_cancel_out_of_edit_form` | — |  |
| `bank_drop/test_bank_drop_edit.py::test_edit_bank_drop_order_persists` | — |  |
| `bank_drop/test_bank_drop_edit.py::test_edit_form_prepopulates_existing_values` | — |  |
| `bank_drop/test_bank_drop_edit.py::test_edited_bank_drop_persists_after_reload` | — |  |
| `bank_drop/test_bank_drop_positive.py::test_cancel_out_of_add_form` | — |  |
| `bank_drop/test_bank_drop_positive.py::test_create_active_bank_drop` | — | 🔥 |
| `bank_drop/test_bank_drop_positive.py::test_created_bank_drop_persists_after_reload` | — |  |
| `bank_drop/test_bank_drop_ui.py::test_add_bank_drop_form_loads` | — |  |
| `bank_drop/test_bank_drop_ui.py::test_bank_drop_grid_columns_are_visible` | — |  |
| `bank_drop/test_bank_drop_ui.py::test_bank_drop_page_loads_with_primary_controls` | — | 🔥 |
| `bank_drop/test_bank_drop_ui.py::test_bank_drop_pagination_controls_visible` | — |  |
| `bank_drop/test_bank_drop_validation.py::test_blank_name_is_blocked` | — | 🔥 |
| `bank_drop/test_bank_drop_validation.py::test_blank_order_is_blocked` | — |  |
| `bank_drop/test_bank_drop_validation.py::test_non_numeric_order_rejected` | — |  |

</details>

**Pending — 7 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_changing_order_resequences_list` (test_bank_drop_edge_cases.py) | — | ⏭️ skip | Manual: the admin list sorts by creation time, not order value; order sequencing on the customer portal must be verified manually. | Manual test |
| `test_pagination_footer_shows_record_count` (test_bank_drop_edge_cases.py) | BD-UI-002 | ⚠️ xfail | BD-UI-002: Pagination footer displays '0 of 0' even when records are present. Remove xfail once the count is rendered correctly. | Case-by-case (see reason) |
| `test_save_button_has_human_readable_label` (test_bank_drop_edge_cases.py) | BD-UI-001 | ⚠️ xfail | BD-UI-001: Save button text is the raw i18n key 'saveNewBankDrop' instead of 'Save bank drop'. Remove xfail once the translation is wired… | Case-by-case (see reason) |
| `test_bank_drop_list_sorted_by_order` (test_bank_drop_edit.py) | — | ⏭️ skip | Manual: the admin list sorts by creation time, not order value; the order field controls display sequence on the customer portal, not adm… | Manual test |
| `test_deactivate_active_bank_drop` (test_bank_drop_edit.py) | BD-EDT-004 | 🟡 xfail/passing | BD-EDT-004: staging server saves bank drop as Active regardless of the Inactive toggle on the edit form. Same app bug as WP-TGL-002 / POS… | **Promote** — passed in last full run; remove xfail |
| `test_edit_bank_drop_name_persists` (test_bank_drop_edit.py) | BD-EDT-001 | ⏭️ skip | CI-SKIP BD-EDT-001: managed_edit_bank_drop fixture fails in headless CI. Fix: decouple fixture from form frame switch; add retry on Timeo… | Case-by-case (see reason) |
| `test_create_inactive_bank_drop` (test_bank_drop_positive.py) | BD-EDT-004 | ⏭️ skip | Manual: create-form active toggle saves as Active regardless of state; deactivation behaviour is covered by BD-EDT-004. | Possible product bug — confirm with product |

Next actions for this module: Case-by-case (see reason) ×3; Manual test ×2; **Promote** — passed in last full run; remove xfail ×1; Possible product bug — confirm with product ×1

### card_declines

<details><summary>✅ Covered — 75 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `card_declines/test_card_declines.py::TestCardDeclinesBestWorst::test_best_sites_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesBestWorst::test_bws_section_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesBestWorst::test_worst_sites_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDailySummary::test_daily_summary_has_content` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDailySummary::test_daily_summary_section_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_date_preset_count` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_date_preset_dropdown_options` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-002]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-003]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-004]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-005]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-006]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_preset_populates_date_range[CDL-DTE-007]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesDateFilter::test_selecting_preset_fills_date_range` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_section_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-01]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-02]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-03]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-04]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-05]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-06]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-07]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_term_visible[CDL-GLS-002-08]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesGlossary::test_glossary_visible_for_zero_data` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesHeatmap::test_heatmap_section_visible` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-01]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-02]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-03]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-04]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-05]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-06]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-07]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_card_visible[CDL-KPI-001-08]` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesKPI::test_kpi_zero_data_state` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-01]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-02]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-03]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-04]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-05]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-06]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-07]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-08]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-09]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-10]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-11]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-12]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_column_present[CDL-MTX-002-13]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_pagination_present` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesMatrix::test_matrix_section_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_apply_filters_closes_modal` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_filter_modal_auto_opens` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_filter_values_reflected_in_page_bar` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_modal_contains_all_controls` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_modal_opens_with_all_sites_default` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_page_bar_changes_do_not_reopen_modal` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_page_content_visible_after_apply` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesNav::test_page_loads_at_correct_url` | — | 🔥 |
| `card_declines/test_card_declines.py::TestCardDeclinesReasonDist::test_reason_dist_section_visible` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_all_sites_is_default` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_cdl_site_present_in_dropdown` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_clear_all_sites` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_multi_site_selection_accepted` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_page_bar_site_change_no_modal` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_removing_chip_reduces_site_filter` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_selecting_site_creates_chip` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_single_site_scopes_data` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_widgets_refresh_on_site_change[CDL-BWS-007]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_widgets_refresh_on_site_change[CDL-HMP-005]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_widgets_refresh_on_site_change[CDL-KPI-003]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_widgets_refresh_on_site_change[CDL-MTX-012]` | — |  |
| `card_declines/test_card_declines.py::TestCardDeclinesSiteFilter::test_widgets_refresh_on_site_change[CDL-TDS-005]` | — |  |
| `card_declines/test_card_declines.py::TestSingleDaySync::test_modal_sdm_syncs_to_page_bar` | — |  |
| `card_declines/test_card_declines.py::TestSingleDaySync::test_modal_single_day_changes_date_field` | — |  |
| `card_declines/test_card_declines.py::TestSingleDaySync::test_modal_single_day_checkbox_visible` | — |  |
| `card_declines/test_card_declines.py::TestSingleDaySync::test_page_bar_sdm_uncheck_syncs_to_modal` | — |  |

</details>

**Pending — 9 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestCardDeclinesBestWorst` (test_card_declines.py) | CDL-BWS-004 | 🟡 xfail/passing | Known defect CDL-BWS-004: 'Test Location 1' appears in the Best & Worst Sites widget even when it is explicitly excluded from the site fi… | **Promote** — passed in last full run; remove xfail |
| `TestCardDeclinesGlossary` (test_card_declines.py) | — | ⏭️ skip | Manual - Check later for fixes: 'Important' label may be in styled aside/tooltip, get_body_text() may not capture it; verify DOM via DevT… | Manual test |
| `TestCardDeclinesKPI` (test_card_declines.py) | — | 🟡 xfail/passing | No CC decline data on staging for last month; KPI values are zero. | **Promote** — passed in last full run; remove xfail |
| `TestCardDeclinesMatrix` (test_card_declines.py) | — | 🟡 xfail/passing | No CC decline data on staging for last month; matrix shows no rows. | **Promote** — passed in last full run; remove xfail |
| `TestCardDeclinesMatrix` (test_card_declines.py) | — | ⏭️ skip | Manual - Check later for fixes: cdl_zero_data fixture needs calendar picker for reliable zero-data range | Manual test |
| `TestCardDeclinesSiteFilter` (test_card_declines.py) | CDL-SIT-012 | ⚠️ xfail | Known defect CDL-SIT-012: when a specific site subset is chosen, the line chart title continues to display 'All Sites' rather than updati… | Case-by-case (see reason) |
| `TestCardDeclinesSiteFilter` (test_card_declines.py) | — | ⚠️ xfail | CDL site dropdown indicator click is intermittent in headless Chrome — options sometimes not rendered before JS query runs. | Case-by-case (see reason) |
| `TestCardDeclinesSiteFilter` (test_card_declines.py) | — | ⚠️ xfail | CDL site dropdown indicator click is intermittent in headless Chrome — options sometimes not rendered before JS query runs. | Case-by-case (see reason) |
| `TestCardDeclinesSiteFilter` (test_card_declines.py) | — | ⚠️ xfail | CDL site dropdown indicator click is intermittent in headless Chrome — options sometimes not rendered before JS query runs. | Case-by-case (see reason) |

Next actions for this module: Case-by-case (see reason) ×4; **Promote** — passed in last full run; remove xfail ×3; Manual test ×2

### cash_report

<details><summary>✅ Covered — 43 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `cash_report/test_cash_report.py::TestAnalyticsTab::test_analytics_metrics_not_all_zero` | — |  |
| `cash_report/test_cash_report.py::TestAnalyticsTab::test_analytics_tab_shows_metrics` | — | 🔥 |
| `cash_report/test_cash_report.py::TestAnalyticsTab::test_analytics_zero_data_message` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_date_preset_count` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-002]` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-003]` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-004]` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-005]` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-006]` | — |  |
| `cash_report/test_cash_report.py::TestDateFilter::test_preset_populates_date_range[CSH-DTE-007]` | — |  |
| `cash_report/test_cash_report.py::TestExport::test_export_xlsx_button_visible` | — | 🔥 |
| `cash_report/test_cash_report.py::TestExport::test_export_xlsx_triggers_download` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_apply_filters_closes_modal_and_renders_metrics` | — | 🔥 |
| `cash_report/test_cash_report.py::TestFilterModal::test_date_preset_dropdown_options` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_filter_values_reflected_in_page_bar` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_modal_opens_with_no_default_site` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_page_bar_changes_do_not_reopen_modal` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_selecting_preset_fills_date_range` | — |  |
| `cash_report/test_cash_report.py::TestFilterModal::test_sites_dropdown_lists_active_sites` | — |  |
| `cash_report/test_cash_report.py::TestKioskTab::test_kiosk_balance_summary_pagination` | — |  |
| `cash_report/test_cash_report.py::TestKioskTab::test_kiosk_denomination_pagination` | — |  |
| `cash_report/test_cash_report.py::TestKioskTab::test_kiosk_denomination_visible` | — |  |
| `cash_report/test_cash_report.py::TestKioskTab::test_kiosk_transactions_pagination` | — |  |
| `cash_report/test_cash_report.py::TestKioskTab::test_kiosk_zero_data_state` | — |  |
| `cash_report/test_cash_report.py::TestNavigation::test_filter_modal_auto_opens` | — |  |
| `cash_report/test_cash_report.py::TestNavigation::test_modal_contains_all_controls` | — |  |
| `cash_report/test_cash_report.py::TestNavigation::test_page_loads_at_correct_url` | — | 🔥 |
| `cash_report/test_cash_report.py::TestNavigation::test_page_title_visible_after_apply` | — |  |
| `cash_report/test_cash_report.py::TestNavigation::test_sidebar_highlights_active_item` | — |  |
| `cash_report/test_cash_report.py::TestPOSTab::test_pos_balance_summary_pagination` | — |  |
| `cash_report/test_cash_report.py::TestPOSTab::test_pos_bank_drop_pagination` | — |  |
| `cash_report/test_cash_report.py::TestPOSTab::test_pos_transactions_pagination` | — |  |
| `cash_report/test_cash_report.py::TestPOSTab::test_pos_zero_data_state` | — |  |
| `cash_report/test_cash_report.py::TestSingleDayMode::test_modal_single_day_changes_date_field` | — |  |
| `cash_report/test_cash_report.py::TestSingleDayMode::test_modal_single_day_checkbox_visible` | — |  |
| `cash_report/test_cash_report.py::TestSiteFilter::test_clearing_chip_removes_site_filter` | — |  |
| `cash_report/test_cash_report.py::TestSiteFilter::test_no_all_sites_option` | — |  |
| `cash_report/test_cash_report.py::TestSiteFilter::test_selecting_site_creates_chip` | — |  |
| `cash_report/test_cash_report.py::TestTabNavigation::test_analytics_tab_active_by_default` | — |  |
| `cash_report/test_cash_report.py::TestTabNavigation::test_analytics_tab_restores` | — |  |
| `cash_report/test_cash_report.py::TestTabNavigation::test_kiosk_tab_click` | — |  |
| `cash_report/test_cash_report.py::TestTabNavigation::test_pos_tab_click` | — |  |
| `cash_report/test_cash_report.py::TestTabNavigation::test_three_tabs_visible` | — |  |

</details>

**Pending — 13 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestKioskTab` (test_cash_report.py) | CSH-KSK-001 | ⏭️ skip | Manual check required — depends on CSH-KSK-001 heading confirmation | Manual test |
| `TestKioskTab` (test_cash_report.py) | CSH-KSK-001 | ⏭️ skip | Manual check required — depends on CSH-KSK-001 heading confirmation | Manual test |
| `TestKioskTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — actual Kiosk Balance Summary heading unconfirmed via DevTools | Manual test |
| `TestKioskTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — Denomination renders as chart/histogram, not HTML table; widget type unconfirmed via DevTools | Manual test |
| `TestKioskTab` (test_cash_report.py) | CSH-KSK-008 | ⏭️ skip | Manual check required — depends on CSH-KSK-008 heading confirmation | Manual test |
| `TestKioskTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — actual Kiosk Transactions heading unconfirmed via DevTools | Manual test |
| `TestPOSTab` (test_cash_report.py) | CSH-POS-001 | ⏭️ skip | Manual check required — depends on CSH-POS-001 heading confirmation | Manual test |
| `TestPOSTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — actual POS Balance Summary heading unconfirmed via DevTools | Manual test |
| `TestPOSTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — actual POS Bank Drop heading unconfirmed via DevTools | Manual test |
| `TestPOSTab` (test_cash_report.py) | — | ⏭️ skip | Manual check required — actual POS Transactions heading unconfirmed via DevTools | Manual test |
| `TestSingleDayMode` (test_cash_report.py) | — | ⏭️ skip | Manual check required — PAGE_BAR_SINGLE_DAY_CHECKBOX locator unconfirmed via DevTools | Manual test |
| `TestSingleDayMode` (test_cash_report.py) | — | ⏭️ skip | Manual check required — PAGE_BAR_SINGLE_DAY_CHECKBOX locator unconfirmed via DevTools | Manual test |
| `TestSiteFilter` (test_cash_report.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |

Next actions for this module: Manual test ×12; Re-check now — deferred as staging data / intermittent ×1

### coupon_packages

<details><summary>✅ Covered — 26 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `coupon_packages/test_coupon_packages_customer_tab.py::test_customer_coupon_packages_grid_columns_visible` | — |  |
| `coupon_packages/test_coupon_packages_customer_tab.py::test_customer_coupon_packages_tab_loads` | — | 🔥 |
| `coupon_packages/test_coupon_packages_edge_cases.py::test_coupon_package_long_name_does_not_break_form` | — |  |
| `coupon_packages/test_coupon_packages_edge_cases.py::test_coupon_package_save_without_giveaway` | — |  |
| `coupon_packages/test_coupon_packages_edge_cases.py::test_coupon_package_valid_expiration_days` | — |  |
| `coupon_packages/test_coupon_packages_edge_cases.py::test_coupon_package_zero_expiration_days` | — |  |
| `coupon_packages/test_coupon_packages_edit.py::test_edit_coupon_package_discount` | — |  |
| `coupon_packages/test_coupon_packages_edit.py::test_edit_coupon_package_expiration_days` | — |  |
| `coupon_packages/test_coupon_packages_edit.py::test_edit_coupon_package_name` | — |  |
| `coupon_packages/test_coupon_packages_negative.py::test_coupon_packages_special_character_search_stays_usable` | — |  |
| `coupon_packages/test_coupon_packages_positive.py::test_create_coupon_package` | — | 🔥 |
| `coupon_packages/test_coupon_packages_search_filter.py::test_active_coupon_package_filter_shows_active_only` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_active_toggle_off_shows_all_packages` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_coupon_packages_clear_search_restores_list` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_coupon_packages_exact_search` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_coupon_packages_missing_search` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_coupon_packages_partial_search` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_coupon_packages_search_payloads_do_not_break_grid` | — |  |
| `coupon_packages/test_coupon_packages_search_filter.py::test_reset_all_restores_unfiltered_list` | — |  |
| `coupon_packages/test_coupon_packages_ui.py::test_add_coupon_package_form_loads` | — |  |
| `coupon_packages/test_coupon_packages_ui.py::test_coupon_packages_grid_columns_are_visible` | — |  |
| `coupon_packages/test_coupon_packages_ui.py::test_coupon_packages_page_loads_with_primary_controls` | — |  |
| `coupon_packages/test_coupon_packages_ui.py::test_customer_coupon_packages_tab_is_accessible` | — | 🔥 |
| `coupon_packages/test_coupon_packages_validation.py::test_coupon_package_blank_discount_is_blocked` | — | 🔥 |
| `coupon_packages/test_coupon_packages_validation.py::test_coupon_package_blank_name_is_blocked` | — | 🔥 |
| `coupon_packages/test_coupon_packages_validation.py::test_coupon_package_whitespace_name_is_rejected` | — |  |

</details>

**Pending — 19 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_customer_coupon_code_is_unique` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS integration — deferred | Deferred — re-check scope |
| `test_customer_coupon_combined_filter` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_exact_search` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_filter_active` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_filter_all` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_filter_not_used` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_filter_used` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_missing_search` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_partial_search` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_customer_coupon_reset_filters` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS-generated coupon code data — deferred until POS dependency is available | Needs POS-generated data (cross-system) |
| `test_expired_coupon_code_is_inactive` (test_coupon_packages_customer_tab.py) | — | ⏭️ skip | Requires POS integration — deferred | Deferred — re-check scope |
| `test_coupon_package_negative_expiration_days_rejected` (test_coupon_packages_edge_cases.py) | — | ⏭️ skip | App bug: negative expiration days accepted without error — pending fix | Case-by-case (see reason) |
| `test_coupon_package_remove_giveaway_service` (test_coupon_packages_edge_cases.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_activate_inactive_coupon_package` (test_coupon_packages_edit.py) | — | ⏭️ skip | Manual: activation of an inactive package does not persist via automation - needs investigation of legacy iframe form submit behaviour | Possible product bug — confirm with product |
| `test_deactivate_active_coupon_package` (test_coupon_packages_edit.py) | — | ⏭️ skip | manual check: FILTER_BUTTON locator exact text match fails when active filter shows 'Filter by (1)' — fix contains() across all page objects | Manual test |
| `test_edit_coupon_package_giveaway_services` (test_coupon_packages_edit.py) | — | ⏭️ skip | manual check: React controlled input send_keys fix applied, pending clean CI verification | Manual test |
| `test_coupon_package_duplicate_name_is_blocked` (test_coupon_packages_negative.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_coupon_package_settings_persist` (test_coupon_packages_positive.py) | — | ⏭️ skip | manual check: parallel isolation — test_edit_coupon_package_name renames same package concurrently, fix requires separate package names p… | Manual test |
| `test_create_inactive_coupon_package` (test_coupon_packages_positive.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |

Next actions for this module: Needs POS-generated data (cross-system) ×9; Re-check now — deferred as staging data / intermittent ×3; Manual test ×3; Deferred — re-check scope ×2; Case-by-case (see reason) ×1; Possible product bug — confirm with product ×1

### custom_services

<details><summary>✅ Covered — 12 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `custom_services/test_custom_services_category.py::test_service_category_dropdown_lists_active_categories_only` | — |  |
| `custom_services/test_custom_services_discount.py::test_discount_settings_tab_is_visible_on_create` | — |  |
| `custom_services/test_custom_services_positive.py::test_cancel_out_of_create_form` | — | 🔥 |
| `custom_services/test_custom_services_positive.py::test_create_form_has_save_and_cancel_buttons` | — |  |
| `custom_services/test_custom_services_positive.py::test_state_city_sales_tax_columns_are_read_only` | — | 🔥 |
| `custom_services/test_custom_services_search_filter.py::test_search_non_existing_service_returns_empty` | — |  |
| `custom_services/test_custom_services_ui.py::test_custom_services_page_loads_with_primary_controls` | — | 🔥 |
| `custom_services/test_custom_services_ui.py::test_pagination_controls_are_visible` | — |  |
| `custom_services/test_custom_services_validation.py::test_long_service_name_documents_behaviour` | — |  |
| `custom_services/test_custom_services_validation.py::test_negative_global_price_documents_behaviour` | — |  |
| `custom_services/test_custom_services_validation.py::test_non_numeric_price_rejected` | — |  |
| `custom_services/test_custom_services_validation.py::test_zero_global_price_documents_behaviour` | — |  |

</details>

**Pending — 46 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_selected_category_persists_after_save` (test_custom_services_category.py) | CS-CAT-002 | ⏭️ skip | CI-SKIP CS-CAT-002: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_service_category_can_be_changed` (test_custom_services_category.py) | CS-CAT-003 | ⏭️ skip | CI-SKIP CS-CAT-003: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_assigned_site_appears_in_site_grid_after_save` (test_custom_services_dependency.py) | CS-DEP-001 | ⏭️ skip | CI-SKIP CS-DEP-001: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_delete_service_removes_from_pos` (test_custom_services_dependency.py) | — | ⏭️ skip | Manual: delete functionality is not exposed in the admin list UI; POS impact must be verified manually against a live terminal. | Manual test |
| `test_export_download_button_triggers_download` (test_custom_services_dependency.py) | — | ⏭️ skip | Manual: automating file download verification in headless Chrome requires download-directory interception which is out of scope for this … | Needs downloaded-file verification |
| `test_inactive_service_hidden_from_pos` (test_custom_services_dependency.py) | — | ⏭️ skip | Manual: verifying POS visibility for inactive services requires a POS device and is not automatable in the current test setup. | Manual test |
| `test_service_appears_in_pos_after_assignment` (test_custom_services_dependency.py) | — | ⏭️ skip | Manual: verifying service visibility on the POS terminal requires a physical or emulated POS device that is not available in the automati… | Manual test |
| `test_applicable_discount_persists_after_save` (test_custom_services_discount.py) | CS-DSC-002 | ⚠️ xfail | CS-DSC-002: staging server does not persist discount assignment on save; same server-side lock behaviour observed in memberships price/co… | Possible product bug — confirm with product |
| `test_discount_combobox_filters_by_typing` (test_custom_services_discount.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_discount_tab_accessible_on_edit_form` (test_custom_services_discount.py) | CS-DSC-005 | ⏭️ skip | CI-SKIP CS-DSC-005: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_multiple_applicable_discounts_can_be_selected` (test_custom_services_discount.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_remove_applicable_discount_persists` (test_custom_services_discount.py) | CS-DSC-004 | ⚠️ xfail | CS-DSC-004: staging server does not persist discount removal on save; same server-side lock behaviour observed in memberships price/commi… | Possible product bug — confirm with product |
| `test_activate_inactive_service` (test_custom_services_edit.py) | — | ⏭️ skip | Manual: React switch aria-checked updates DOM but isActive not reflected in save payload. Needs app-level investigation. | Manual test |
| `test_cancel_out_of_edit_form` (test_custom_services_edit.py) | CS-EDT-007 | ⏭️ skip | CI-SKIP CS-EDT-007: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_created_service_persists_after_reload` (test_custom_services_edit.py) | CS-PER-001 | ⏭️ skip | CI-SKIP CS-PER-001: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_deactivate_active_service` (test_custom_services_edit.py) | CS-EDT-005 | ⏭️ skip | CI-SKIP CS-EDT-005: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_edit_barcode_and_description_persist` (test_custom_services_edit.py) | — | ⏭️ skip | Manual: description textarea not interactable after barcode entry — likely covered by tooltip/overlay. Needs browser inspection. | Manual test |
| `test_edit_form_prepopulates_existing_values` (test_custom_services_edit.py) | CS-EDT-006 | ⏭️ skip | CI-SKIP CS-EDT-006: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_edit_global_price_persists` (test_custom_services_edit.py) | CS-EDT-002 | ⏭️ skip | CI-SKIP CS-EDT-002: managed_service fixture times out in headless CI. Fix: use window.location.origin fallback in wait_for_list_loaded. | Case-by-case (see reason) |
| `test_edit_service_name_persists` (test_custom_services_edit.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_edit_site_price_override_persists` (test_custom_services_edit.py) | CS-EDT-003 | ⏭️ skip | CI-SKIP CS-EDT-003: managed_service fixture times out in headless CI. Fix: same as CS-EDT-002. | Case-by-case (see reason) |
| `test_edited_service_persists_after_reload` (test_custom_services_edit.py) | CS-PER-002 | ⏭️ skip | CI-SKIP CS-PER-002: managed_service fixture times out in headless CI. Fix: same as CS-EDT-002. | Case-by-case (see reason) |
| `test_create_active_custom_service` (test_custom_services_positive.py) | CS-CRT-001 | ⏭️ skip | CI-SKIP CS-CRT-001: wait_for_list_loaded LIST_FRAME switch times out in headless CI. Fix: use window.location.origin for fallback navigat… | Case-by-case (see reason) |
| `test_create_inactive_custom_service_hidden` (test_custom_services_positive.py) | CS-CRT-002 | 🟡 xfail/passing | CS-CRT-002: staging server saves custom service as Active regardless of the Inactive selection on the create form. Same app bug as WP-TGL… | **Promote** — passed in last full run; remove xfail |
| `test_create_service_with_applicable_discount` (test_custom_services_positive.py) | CS-CRT-012 | ⏭️ skip | CI-SKIP CS-CRT-012: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_create_service_with_barcode` (test_custom_services_positive.py) | CS-CRT-006 | ⏭️ skip | CI-SKIP CS-CRT-006: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_create_service_with_description` (test_custom_services_positive.py) | CS-CRT-007 | ⏭️ skip | CI-SKIP CS-CRT-007: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_create_service_with_force_receipt_enabled` (test_custom_services_positive.py) | CS-CRT-008 | ⏭️ skip | CI-SKIP CS-CRT-008: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_create_service_with_open_price_enabled` (test_custom_services_positive.py) | CS-CRT-009 | ⏭️ skip | CI-SKIP CS-CRT-009: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_created_service_persists_after_reload` (test_custom_services_positive.py) | CS-CRT-014 | ⏭️ skip | CI-SKIP CS-CRT-014: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_enable_tax_exemption_per_site` (test_custom_services_positive.py) | CS-CRT-011 | ⏭️ skip | CI-SKIP CS-CRT-011: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_new_service_global_price_visible_in_list` (test_custom_services_positive.py) | CS-CRT-005 | ⏭️ skip | CI-SKIP CS-CRT-005: same root cause as CS-CRT-001 — wait_for_list_loaded times out. | Case-by-case (see reason) |
| `test_site_level_price_override_saved` (test_custom_services_positive.py) | CS-CRT-010 | ⏭️ skip | CI-SKIP CS-CRT-010: same root cause as CS-CRT-001. | Case-by-case (see reason) |
| `test_active_service_filter_off_shows_all` (test_custom_services_search_filter.py) | CS-EDT-004 | ⏭️ skip | Manual: Active service filter toggle updates DOM but React state does not change — same root cause as CS-EDT-004. Needs app-level investi… | Manual test |
| `test_active_service_filter_shows_active_only` (test_custom_services_search_filter.py) | CS-FLT-002 | ⏭️ skip | CI-SKIP CS-FLT-002: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_clear_search_restores_full_list` (test_custom_services_search_filter.py) | CS-SRH-004 | ⏭️ skip | CI-SKIP CS-SRH-004: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_filter_by_site_narrows_results` (test_custom_services_search_filter.py) | CS-FLT-001 | ⏭️ skip | CI-SKIP CS-FLT-001: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_reset_filters_clears_filters` (test_custom_services_search_filter.py) | CS-FLT-005 | ⏭️ skip | CI-SKIP CS-FLT-005: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_search_exact_service_name` (test_custom_services_search_filter.py) | CS-SRH-001 | ⏭️ skip | CI-SKIP CS-SRH-001: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_search_partial_service_name` (test_custom_services_search_filter.py) | CS-SRH-002 | ⏭️ skip | CI-SKIP CS-SRH-002: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_site_and_active_filter_combined` (test_custom_services_search_filter.py) | CS-FLT-004 | ⏭️ skip | CI-SKIP CS-FLT-004: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_grid_displays_expected_columns` (test_custom_services_ui.py) | CS-LST-002 | ⏭️ skip | CI-SKIP CS-LST-002: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_duplicate_service_name_documents_behaviour` (test_custom_services_validation.py) | CS-VAL-006 | ⏭️ skip | CI-SKIP CS-VAL-006: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_submit_without_category_shows_error` (test_custom_services_validation.py) | CS-VAL-002 | ⏭️ skip | CI-SKIP CS-VAL-002: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_submit_without_global_price_shows_error` (test_custom_services_validation.py) | CS-VAL-003 | ⏭️ skip | CI-SKIP CS-VAL-003: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_submit_without_service_name_shows_error` (test_custom_services_validation.py) | CS-VAL-001 | ⏭️ skip | CI-SKIP CS-VAL-001: wait_for_list_loaded times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |

Next actions for this module: Case-by-case (see reason) ×33; Manual test ×6; Re-check now — deferred as staging data / intermittent ×3; Possible product bug — confirm with product ×2; Needs downloaded-file verification ×1; **Promote** — passed in last full run; remove xfail ×1

### customers

<details><summary>✅ Covered — 54 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `customers/test_customers_cars.py::test_add_car_form_shows_license_plate_field` | — |  |
| `customers/test_customers_cars.py::test_add_car_form_shows_rfid_field` | — |  |
| `customers/test_customers_cars.py::test_add_car_form_shows_save_and_cancel_controls` | — |  |
| `customers/test_customers_cars.py::test_add_car_form_shows_vehicle_detail_fields` | — |  |
| `customers/test_customers_cars.py::test_cars_settings_tab_accessible_on_existing_customer` | — | 🔥 |
| `customers/test_customers_cars.py::test_cars_settings_tab_shows_add_car_button` | — | 🔥 |
| `customers/test_customers_dependency.py::test_customer_site_assignment_matches_sites_module` | — |  |
| `customers/test_customers_edit.py::test_activate_inactive_customer` | — | 🔥 |
| `customers/test_customers_edit.py::test_cancel_edit_customer_discards_changes` | — |  |
| `customers/test_customers_edit.py::test_deactivate_active_customer` | — |  |
| `customers/test_customers_edit.py::test_edit_assigned_site_persists` | — |  |
| `customers/test_customers_edit.py::test_edit_customer_name_persists` | — |  |
| `customers/test_customers_edit.py::test_edit_form_prepopulates_existing_values` | — |  |
| `customers/test_customers_edit.py::test_edit_then_refresh_changes_persist` | — |  |
| `customers/test_customers_edit.py::test_toggle_allow_invoicing_persists` | — |  |
| `customers/test_customers_payment.py::test_credit_card_section_is_visible` | — |  |
| `customers/test_customers_payment.py::test_payment_settings_tab_accessible_on_existing_customer` | — |  |
| `customers/test_customers_payment.py::test_save_card_button_is_present` | — |  |
| `customers/test_customers_payment.py::test_transaction_history_filter_controls_are_present` | — |  |
| `customers/test_customers_payment.py::test_transaction_history_section_is_present` | — |  |
| `customers/test_customers_positive.py::test_assign_to_site_dropdown_lists_available_sites` | — |  |
| `customers/test_customers_positive.py::test_cancel_add_customer_returns_to_list` | — |  |
| `customers/test_customers_positive.py::test_cars_and_payment_tabs_disabled_for_new_customer` | — |  |
| `customers/test_customers_positive.py::test_city_dropdown_empty_without_state` | — | 🔥 |
| `customers/test_customers_positive.py::test_create_customer_with_all_optional_fields` | — |  |
| `customers/test_customers_positive.py::test_create_customer_with_required_fields_only` | — | 🔥 |
| `customers/test_customers_positive.py::test_create_inactive_customer` | — |  |
| `customers/test_customers_positive.py::test_create_then_refresh_data_persists` | — |  |
| `customers/test_customers_positive.py::test_date_of_birth_calendar_picker_selects_past_date` | — |  |
| `customers/test_customers_positive.py::test_state_dropdown_populates_cities_on_selection` | — |  |
| `customers/test_customers_search_filter.py::test_active_accounts_toggle_is_on_by_default` | — |  |
| `customers/test_customers_search_filter.py::test_all_boolean_dropdowns_default_to_all` | — |  |
| `customers/test_customers_search_filter.py::test_filter_by_allow_invoicing_yes` | — |  |
| `customers/test_customers_search_filter.py::test_filter_by_card_on_file` | — |  |
| `customers/test_customers_search_filter.py::test_filter_by_declined_yes` | — |  |
| `customers/test_customers_search_filter.py::test_filter_by_signup_date_range` | — |  |
| `customers/test_customers_search_filter.py::test_filter_panel_opens_with_all_fields_visible` | — | 🔥 |
| `customers/test_customers_search_filter.py::test_license_plate_and_phone_searches_are_independent` | — |  |
| `customers/test_customers_search_filter.py::test_nonmatching_search_returns_empty_state` | — |  |
| `customers/test_customers_search_filter.py::test_reset_all_clears_filter_fields` | — |  |
| `customers/test_customers_search_filter.py::test_search_by_exact_license_plate` | — |  |
| `customers/test_customers_search_filter.py::test_search_by_partial_license_plate` | — |  |
| `customers/test_customers_search_filter.py::test_search_by_partial_phone_number` | — |  |
| `customers/test_customers_search_filter.py::test_signup_date_from_after_to_documents_behaviour` | — |  |
| `customers/test_customers_ui.py::test_add_customer_form_loads_with_required_controls` | — |  |
| `customers/test_customers_ui.py::test_customers_page_loads_with_primary_controls` | — |  |
| `customers/test_customers_ui.py::test_pagination_and_results_per_page_visible` | — |  |
| `customers/test_customers_validation.py::test_blank_first_name_blocked_on_save` | — |  |
| `customers/test_customers_validation.py::test_blank_form_stays_on_create_page` | — |  |
| `customers/test_customers_validation.py::test_blank_last_name_blocked_on_save` | — |  |
| `customers/test_customers_validation.py::test_blank_site_assignment_blocked_on_save` | — |  |
| `customers/test_customers_validation.py::test_dob_in_future_documents_behaviour` | — |  |
| `customers/test_customers_validation.py::test_duplicate_email_documents_behaviour` | — |  |
| `customers/test_customers_validation.py::test_invalid_email_format_documents_behaviour` | — |  |

</details>

**Pending — 39 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_add_car_form_shows_assign_membership_button` (test_customers_cars.py) | — | ⏭️ skip | Manual check — Assign membership button visibility depends on membership module state. | Manual test |
| `test_add_car_then_refresh_car_persists` (test_customers_cars.py) | — | ⏭️ skip | Cars CRUD deferred — verifying field presence only in this pass. Unblock after confirming DOM locators from a live run. | Deferred — re-check scope |
| `test_blacklist_a_car` (test_customers_cars.py) | — | ⏭️ skip | Cars CRUD deferred — verifying field presence only in this pass. Unblock after confirming DOM locators from a live run. | Deferred — re-check scope |
| `test_cars_list_shows_membership_details` (test_customers_cars.py) | — | ⏭️ skip | Requires Memberships module fixtures with active member cars. | Case-by-case (see reason) |
| `test_deactivate_a_car` (test_customers_cars.py) | — | ⏭️ skip | Cars CRUD deferred — verifying field presence only in this pass. Unblock after confirming DOM locators from a live run. | Deferred — re-check scope |
| `test_duplicate_license_plate_documents_behaviour` (test_customers_cars.py) | — | ⏭️ skip | Cars CRUD deferred — verifying field presence only in this pass. Unblock after confirming DOM locators from a live run. | Deferred — re-check scope |
| `test_duplicate_rfid_documents_behaviour` (test_customers_cars.py) | — | ⏭️ skip | Deferred — RFID uniqueness requires POS tunnel integration to verify. | Deferred — re-check scope |
| `test_license_plate_field_is_present_and_required` (test_customers_cars.py) | CUST-CAR-001 | ⏭️ skip | Manual - Check later for fixes: depends on tab locator, xfail until CUST-CAR-001 passes | Manual test |
| `test_rfid_field_is_present_and_required` (test_customers_cars.py) | CUST-CAR-001 | ⏭️ skip | Manual - Check later for fixes: depends on tab locator, xfail until CUST-CAR-001 passes | Manual test |
| `test_update_vehicle_token` (test_customers_cars.py) | — | ⏭️ skip | Deferred — requires POS token provisioning setup. | Deferred — re-check scope |
| `test_car_rfid_links_to_pos_tunnel_entry` (test_customers_dependency.py) | — | ⏭️ skip | Requires POS tunnel integration and RFID-linked car. Deferred. | Deferred — re-check scope |
| `test_customer_appears_in_gift_cards_dropdown` (test_customers_dependency.py) | — | ⏭️ skip | Requires Gift Cards module with a customer selector fixture. Deferred. | Deferred — re-check scope |
| `test_customer_membership_status_reflects_memberships_module` (test_customers_dependency.py) | — | ⏭️ skip | Requires Memberships module fixtures and cross-module setup. Deferred. | Needs cross-module fixtures |
| `test_toggle_send_text_and_email_persists` (test_customers_edit.py) | — | ⏭️ skip | Requires Notifications module configuration to verify downstream effect. | Case-by-case (see reason) |
| `test_export_button_triggers_customer_list_download` (test_customers_export.py) | — | ⏭️ skip | Deferred — export verification requires download interception or a file-system check which is not yet set up in the test harness. | Deferred — re-check scope |
| `test_transaction_details_link_navigates_to_invoice` (test_customers_payment.py) | — | ⏭️ skip | Deferred — requires POS transactions and cross-module invoice navigation. | Needs cross-module fixtures |
| `test_transaction_history_export` (test_customers_payment.py) | — | ⏭️ skip | Deferred — requires POS transactions and export verification setup. | Deferred — re-check scope |
| `test_transaction_history_loads_all_time` (test_customers_payment.py) | — | ⏭️ skip | Requires POS test environment with at least one transaction for this customer. | Needs POS-generated data (cross-system) |
| `test_transaction_history_pagination_defaults_to_ten` (test_customers_payment.py) | — | ⏭️ skip | Requires POS test environment with at least one transaction for this customer. | Needs POS-generated data (cross-system) |
| `test_transaction_history_select_range_filter` (test_customers_payment.py) | — | ⏭️ skip | Requires POS test environment with at least one transaction for this customer. | Needs POS-generated data (cross-system) |
| `test_transaction_history_today_filter` (test_customers_payment.py) | — | ⏭️ skip | Requires POS test environment with at least one transaction for this customer. | Needs POS-generated data (cross-system) |
| `test_filter_by_canceled_yes` (test_customers_search_filter.py) | — | ⏭️ skip | Requires Memberships module fixtures with cancelled members. | Case-by-case (see reason) |
| `test_filter_by_cc_number` (test_customers_search_filter.py) | — | ⏭️ skip | Extended — CC number filter requires customers with saved payment methods. | Case-by-case (see reason) |
| `test_filter_by_cc_type` (test_customers_search_filter.py) | — | ⏭️ skip | Extended — CC type filter requires customers with saved payment methods. | Case-by-case (see reason) |
| `test_filter_by_email` (test_customers_search_filter.py) | — | ⏭️ skip | Manual check — email filter behaviour verified manually against staging. | Manual test |
| `test_filter_by_first_name` (test_customers_search_filter.py) | — | ⏭️ skip | Manual check — first-name filter behaviour verified manually against staging. | Manual test |
| `test_filter_by_last_name` (test_customers_search_filter.py) | — | ⏭️ skip | Manual check — last-name filter behaviour verified manually against staging. | Manual test |
| `test_filter_by_membership` (test_customers_search_filter.py) | — | ⏭️ skip | Requires Memberships module fixtures and active member records. | Case-by-case (see reason) |
| `test_filter_by_next_payment_date_range` (test_customers_search_filter.py) | — | ⏭️ skip | Requires Memberships module fixtures with active recurring members. | Case-by-case (see reason) |
| `test_filter_by_number_of_cars_range` (test_customers_search_filter.py) | — | ⏭️ skip | Extended — requires customers with multiple cars in the test environment. | Case-by-case (see reason) |
| `test_filter_by_prepaid_yes` (test_customers_search_filter.py) | — | ⏭️ skip | Requires Memberships module fixtures with prepaid members. | Case-by-case (see reason) |
| `test_filter_by_recurring_yes` (test_customers_search_filter.py) | — | ⏭️ skip | Requires Memberships module fixtures with recurring members. | Case-by-case (see reason) |
| `test_filter_by_rfid` (test_customers_search_filter.py) | — | ⏭️ skip | Manual check — RFID filter behaviour verified manually against staging. | Manual test |
| `test_filter_by_site` (test_customers_search_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: site filter uses hidden React-Select combobox, needs trigger-click | Manual test |
| `test_filter_result_count_updates_before_applying` (test_customers_search_filter.py) | — | ⏭️ skip | Manual check — live-count behaviour verified manually against staging. | Manual test |
| `test_multiple_filters_combined_narrow_results` (test_customers_search_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: includes site filter with hidden React-Select combobox | Manual test |
| `test_search_by_exact_phone_number` (test_customers_search_filter.py) | CUST-SRH-003 | 🟡 xfail/passing | CUST-SRH-003: staging phone search returns the full unfiltered list instead of narrowing to the matched customer. App-level bug on staging. | **Promote** — passed in last full run; remove xfail |
| `test_grid_membership_status_column_visible` (test_customers_ui.py) | — | ⏭️ skip | Requires Memberships module fixtures and active member records. | Case-by-case (see reason) |
| `test_negative_loyalty_points_documents_behaviour` (test_customers_validation.py) | — | ⏭️ skip | Requires Loyalty module configuration and loyalty points field on the form. | Case-by-case (see reason) |

Next actions for this module: Case-by-case (see reason) ×12; Manual test ×10; Deferred — re-check scope ×10; Needs POS-generated data (cross-system) ×4; Needs cross-module fixtures ×2; **Promote** — passed in last full run; remove xfail ×1

### discounts

<details><summary>✅ Covered — 49 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `discounts/test_discounts_combination.py::test_cmb_amount_selected_locations_active` | — |  |
| `discounts/test_discounts_combination.py::test_cmb_percentage_selected_locations_active` | — |  |
| `discounts/test_discounts_dependency.py::test_service_category_available_in_discount_creation` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_add_location_to_existing` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_expiring_today_accepted` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_future_start_date_accepted` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_hundred_percent_accepted` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_long_name_does_not_break_form` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_remove_assigned_location` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_type_change_amount_to_percentage` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_type_change_percentage_to_amount` | — |  |
| `discounts/test_discounts_edge_cases.py::test_discount_zero_percent_accepted` | — |  |
| `discounts/test_discounts_edit.py::test_edit_discount_all_to_selected_locations` | — |  |
| `discounts/test_discounts_edit.py::test_edit_discount_category_assignment_persists` | — |  |
| `discounts/test_discounts_edit.py::test_edit_discount_end_date_persists` | — |  |
| `discounts/test_discounts_edit.py::test_edit_discount_reapplies_expected_settings` | — |  |
| `discounts/test_discounts_edit.py::test_edit_discount_start_date_persists` | — |  |
| `discounts/test_discounts_export.py::test_discounts_export_after_filter` | — |  |
| `discounts/test_discounts_export.py::test_discounts_export_button_clickable` | — |  |
| `discounts/test_discounts_export.py::test_discounts_export_data_matches_grid` | — |  |
| `discounts/test_discounts_export.py::test_discounts_export_record_count_matches_grid` | — |  |
| `discounts/test_discounts_managed.py::test_managed_discount_provided_at_baseline` | — |  |
| `discounts/test_discounts_negative.py::test_create_discount_no_location_blocked` | — |  |
| `discounts/test_discounts_negative.py::test_create_discount_percentage_above_limit_blocked` | — |  |
| `discounts/test_discounts_negative.py::test_create_discount_without_category_blocked` | — |  |
| `discounts/test_discounts_negative.py::test_create_discount_without_value_blocked` | — |  |
| `discounts/test_discounts_negative.py::test_discounts_special_character_search_stays_usable` | — |  |
| `discounts/test_discounts_negative.py::test_missing_discount_is_not_returned` | — |  |
| `discounts/test_discounts_positive.py::test_create_amount_discount` | — | 🔥 |
| `discounts/test_discounts_positive.py::test_create_percentage_discount` | — |  |
| `discounts/test_discounts_positive.py::test_discount_create_is_idempotent` | — |  |
| `discounts/test_discounts_positive.py::test_discount_first_location_settings_persist` | — | 🔥 |
| `discounts/test_discounts_search_filter.py::test_discounts_clear_filters_restores_grid` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_existing_search` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_filter_active_and_site` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_filter_active_shows_only_active` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_filter_by_site` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_filter_inactive_and_site` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_partial_search` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_search_and_filter_together` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_search_finds_updated_name` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_search_inactive_discount` | — |  |
| `discounts/test_discounts_search_filter.py::test_discounts_search_payloads_do_not_break_grid` | — |  |
| `discounts/test_discounts_ui.py::test_add_discount_form_loads` | — |  |
| `discounts/test_discounts_ui.py::test_discounts_grid_columns_are_visible` | — |  |
| `discounts/test_discounts_ui.py::test_discounts_page_loads_with_primary_controls` | — |  |
| `discounts/test_discounts_validation.py::test_discount_blank_required_form_stays_on_form` | — |  |
| `discounts/test_discounts_validation.py::test_discount_invalid_amount_does_not_break_form` | — |  |
| `discounts/test_discounts_validation.py::test_discount_required_name_validation` | — |  |

</details>

**Pending — 24 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_cmb_amount_all_locations_active` (test_discounts_combination.py) | — | ⚠️ xfail | BUG 4 — create form does not submit when all-locations toggle is on. | Known product bug (see docs/bug_reports.md) |
| `test_cmb_amount_with_end_date` (test_discounts_combination.py) | — | ⚠️ xfail | BUG 4 — create form does not submit when all-locations toggle is on. | Known product bug (see docs/bug_reports.md) |
| `test_cmb_percentage_all_locations_active` (test_discounts_combination.py) | — | ⚠️ xfail | BUG 4 — create form does not submit when all-locations toggle is on. | Known product bug (see docs/bug_reports.md) |
| `test_cmb_percentage_future_start_date` (test_discounts_combination.py) | — | ⚠️ xfail | BUG 4 — create form does not submit when all-locations toggle is on. | Known product bug (see docs/bug_reports.md) |
| `test_deactivate_assigned_site_reflects_in_discount` (test_discounts_dependency.py) | — | ⏭️ skip | Product behavior verified manually (2026-06-15): deactivating site 'VK AL01' removed it from linked discount site assignment and from new… | Manual test |
| `test_deactivate_linked_category_blocks_discount` (test_discounts_dependency.py) | — | ⏭️ skip | Product behavior verified manually (2026-06-15): deactivating 'VK wash01' made the category field empty in linked discounts and invisible… | Manual test |
| `test_edit_site_assignment_reflects_in_discount` (test_discounts_dependency.py) | — | ⏭️ skip | Product behavior verified manually (2026-06-15): updating site name from 'test123' to 'test123 updated' reflected correctly across all li… | Manual test |
| `test_rename_linked_category_reflects_in_discount` (test_discounts_dependency.py) | — | ⏭️ skip | Product behavior verified manually (2026-06-15): renaming 'VK wash01' to 'VK wash01 update' correctly updated the category field in linke… | Manual test |
| `test_edit_discount_name_persists` (test_discounts_edit.py) | — | ⏭️ skip | manual check: React controlled input send_keys fix applied, pending clean CI verification | Manual test |
| `test_edit_discount_selected_to_all_locations` (test_discounts_edit.py) | — | ⚠️ xfail | BUG 4 (edit variant) — the all-locations switch toggles on and the form saves without error, but the backend does not persist the all-loc… | Possible product bug — confirm with product |
| `test_future_category_to_service_config` (test_discounts_future.py) | — | ⏭️ skip | Future E2E: requires integration with a system not yet covered by this automation suite. Implement once the relevant page objects are ava… | Future E2E (system not yet covered) |
| `test_future_discount_reflected_in_dashboard` (test_discounts_future.py) | — | ⏭️ skip | Future E2E: requires integration with a system not yet covered by this automation suite. Implement once the relevant page objects are ava… | Future E2E (system not yet covered) |
| `test_future_discount_reflected_in_reports` (test_discounts_future.py) | — | ⏭️ skip | Future E2E: requires integration with a system not yet covered by this automation suite. Implement once the relevant page objects are ava… | Future E2E (system not yet covered) |
| `test_future_discount_visible_in_kiosk` (test_discounts_future.py) | — | ⏭️ skip | Future E2E: requires integration with a system not yet covered by this automation suite. Implement once the relevant page objects are ava… | Future E2E (system not yet covered) |
| `test_future_discount_visible_in_pos` (test_discounts_future.py) | — | ⏭️ skip | Future E2E: requires integration with a system not yet covered by this automation suite. Implement once the relevant page objects are ava… | Future E2E (system not yet covered) |
| `test_managed_discount_mutation_is_reset_on_teardown` (test_discounts_managed.py) | — | ⏭️ skip | manual check: React controlled input send_keys fix applied, pending clean CI verification | Manual test |
| `test_create_discount_start_after_end_blocked` (test_discounts_negative.py) | — | ⏭️ skip | Manual — headless date-picker validation: after setting end=day 10, the product calendar blocks selecting start=day 20, preventing the in… | Manual test |
| `test_discount_deactivation_persists_after_refresh` (test_discounts_persistence.py) | — | ⏭️ skip | Manual — headless: grid search does not resolve within the 10s wait after a save cycle in headless mode. Passes reliably in non-headless … | Manual test |
| `test_discount_edit_persists_after_refresh` (test_discounts_persistence.py) | — | ⏭️ skip | manual check: set_discount_amount React fiber state issue — send_keys fix applied but number input + JS save click not committing value | Manual test |
| `test_discount_persists_after_relogin` (test_discounts_persistence.py) | — | ⏭️ skip | Manual — window.localStorage.clear() invalidates the auth session in headless mode; the 2-second bounce-detection window in open_admin_pa… | Manual test |
| `test_activate_discount` (test_discounts_positive.py) | — | ⏭️ skip | Manual — headless: after two consecutive edit-save cycles the grid search does not resolve within the 10s wait. Passes reliably in non-he… | Manual test |
| `test_create_discount_assign_all_locations` (test_discounts_positive.py) | — | ⚠️ xfail | BUG 4 — create form does not submit when 'Allow discount at all locations' toggle is on. Remove xfail once the product defect is resolved. | Known product bug (see docs/bug_reports.md) |
| `test_deactivate_discount` (test_discounts_positive.py) | — | ⏭️ skip | Manual — headless: after two consecutive edit-save cycles the grid search does not resolve within the 10s wait. Passes reliably in non-he… | Manual test |
| `test_discount_settings_persist` (test_discounts_positive.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |

Next actions for this module: Manual test ×12; Known product bug (see docs/bug_reports.md) ×5; Future E2E (system not yet covered) ×5; Possible product bug — confirm with product ×1; Re-check now — deferred as staging data / intermittent ×1

### employees

<details><summary>✅ Covered — 45 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `employees/test_employees_create.py::test_add_employee_form_opens` | — | 🔥 |
| `employees/test_employees_create.py::test_create_employee_address_fields_optional` | — |  |
| `employees/test_employees_create.py::test_create_employee_cancel_discards_form` | — |  |
| `employees/test_employees_create.py::test_create_employee_code_optional` | — |  |
| `employees/test_employees_create.py::test_create_employee_email_required` | — |  |
| `employees/test_employees_create.py::test_create_employee_first_name_required` | — |  |
| `employees/test_employees_create.py::test_create_employee_hire_date_optional` | — |  |
| `employees/test_employees_create.py::test_create_employee_hourly_wage_decimal` | — |  |
| `employees/test_employees_create.py::test_create_employee_hourly_wage_optional` | — |  |
| `employees/test_employees_create.py::test_create_employee_invalid_email_rejected` | — |  |
| `employees/test_employees_create.py::test_create_employee_last_name_required` | — |  |
| `employees/test_employees_create.py::test_create_employee_multiple_locations` | — |  |
| `employees/test_employees_create.py::test_create_employee_phone_required` | — |  |
| `employees/test_employees_create.py::test_create_employee_single_location_persists` | — |  |
| `employees/test_employees_edge_cases.py::test_employee_data_persists_after_relogin` | — |  |
| `employees/test_employees_edge_cases.py::test_employee_name_with_special_characters` | — |  |
| `employees/test_employees_edit.py::test_deactivate_active_employee` | — | 🔥 |
| `employees/test_employees_edit.py::test_edit_cancel_discards_changes` | — |  |
| `employees/test_employees_edit.py::test_edit_clear_first_name_blocked` | — |  |
| `employees/test_employees_edit.py::test_edit_clear_last_name_blocked` | — |  |
| `employees/test_employees_edit.py::test_edit_first_name_persists` | — |  |
| `employees/test_employees_edit.py::test_edit_form_opens_prepopulated` | — | 🔥 |
| `employees/test_employees_edit.py::test_edit_invalid_email_blocked` | — |  |
| `employees/test_employees_edit.py::test_edit_last_name_persists` | — |  |
| `employees/test_employees_edit.py::test_edit_phone_persists` | — |  |
| `employees/test_employees_filter.py::test_filter_panel_opens` | — | 🔥 |
| `employees/test_employees_list.py::test_clear_search_restores_full_list` | — |  |
| `employees/test_employees_list.py::test_employees_list_displays_correct_columns` | — |  |
| `employees/test_employees_list.py::test_employees_page_loads` | — | 🔥 |
| `employees/test_employees_list.py::test_search_by_exact_last_name` | — |  |
| `employees/test_employees_list.py::test_search_by_partial_last_name` | — |  |
| `employees/test_employees_list.py::test_shift_status_inactive_when_no_active_shift` | — |  |
| `employees/test_employees_list.py::test_status_column_shows_badge` | — |  |
| `employees/test_employees_shift_create.py::test_add_shift_form_opens` | — |  |
| `employees/test_employees_shift_create.py::test_create_shift_cancel_discards_form` | — |  |
| `employees/test_employees_shift_export.py::test_shift_export_button_clickable` | — |  |
| `employees/test_employees_shift_filter.py::test_shift_filter_active_on` | — |  |
| `employees/test_employees_shift_filter.py::test_shift_filter_by_site` | — |  |
| `employees/test_employees_shift_filter.py::test_shift_filter_panel_opens_with_controls` | — |  |
| `employees/test_employees_shift_list.py::test_shift_clear_search_restores_list` | — |  |
| `employees/test_employees_shift_list.py::test_shift_empty_state_when_no_records` | — | 🔥 |
| `employees/test_employees_shift_list.py::test_shift_search_by_exact_last_name` | — |  |
| `employees/test_employees_shift_list.py::test_shift_search_by_partial_last_name` | — |  |
| `employees/test_employees_shift_list.py::test_shift_search_nonexistent_shows_empty` | — |  |
| `employees/test_employees_shift_list.py::test_shift_tab_loads` | — |  |

</details>

**Pending — 53 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_create_active_employee` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: location combobox locator uses label heuristics, verify React Select in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_employee_city_populates_after_state` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: state/city cascade locators use label heuristics, verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_employee_duplicate_code_behavior` (test_employees_create.py) | EMP-CRT-017 | ⏭️ skip | EMP-CRT-017: Whether duplicate employee codes are blocked is a product decision. Confirm expected behaviour with the team before implemen… | Case-by-case (see reason) |
| `test_create_employee_duplicate_email_rejected` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: location combobox locator uses label heuristics, verify React Select in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_employee_future_hire_date` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: hire date calendar picker not modelled, verify input in DevTools | Manual test |
| `test_create_employee_hire_date_persists` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: hire date calendar picker not modelled, verify input in DevTools | Manual test |
| `test_create_employee_locations_required` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: location combobox locator uses label heuristics, verify React Select in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_employee_negative_wage_rejected` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: wage 'min' attribute not verified in DevTools | Manual test |
| `test_create_employee_state_change_clears_city` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: state/city cascade locators use label heuristics, verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_employee_state_dropdown_has_options` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: state combobox locator uses label heuristics, verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_inactive_employee` (test_employees_create.py) | — | ⏭️ skip | Manual - Check later for fixes: location combobox locator uses label heuristics, verify React Select in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_newly_created_employee_appears_immediately` (test_employees_create.py) | EMP-CRT-026 | ⏭️ skip | Manual — EMP-CRT-026: Grid refresh timing is inconsistent in staging; verify manually after creating an employee. | Manual test |
| `test_deactivated_employee_in_inactive_filter` (test_employees_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: inactive filter combobox locator uses label heuristics, verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_locations_required` (test_employees_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: chip remove button uses class heuristics, verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_activate_inactive_employee` (test_employees_edit.py) | — | ⏭️ skip | Manual: after deactivation the employee disappears from the default (Active-only) list view, so the automation cannot re-open the edit fo… | Manual test |
| `test_edit_email_persists` (test_employees_edit.py) | EMP-EDT-005 | ⏭️ skip | EMP-EDT-005: parallel worker teardown races with verify step — deferred | Deferred — re-check scope |
| `test_edit_employee_code_persists` (test_employees_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: employee code locator uses name heuristics, verify @name in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_hire_date_persists` (test_employees_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: hire date picker not modelled, verify date input DOM in DevTools | Manual test |
| `test_edit_hourly_wage_persists` (test_employees_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: wage input name and round-trip not verified in DevTools | Manual test |
| `test_edit_locations_persists` (test_employees_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: location combobox locator uses label heuristics, verify React Select in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_export_button_clickable` (test_employees_export.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_filter_by_active_status` (test_employees_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter panel locators use label heuristics, verify DOM in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_filter_by_inactive_status` (test_employees_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter panel locators use label heuristics, verify DOM in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_filter_result_count_matches_rows` (test_employees_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter panel locators use label heuristics, verify DOM in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_reset_all_clears_filters` (test_employees_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter panel locators use label heuristics, verify DOM in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_employees_pagination_shows_count` (test_employees_list.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_results_per_page_updates_rows` (test_employees_list.py) | — | ⏭️ skip | Manual - Check later for fixes: results-per-page dropdown locator not verified in DevTools | Manual test |
| `test_search_nonexistent_shows_empty_state` (test_employees_list.py) | EMP-SRH-003 | ⏭️ skip | Manual — EMP-SRH-003: Empty-state verification requires manual check of filter panel behaviour. | Manual test |
| `test_create_active_shift` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_inactive_shift` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_datetime_picker_present` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_employee_dropdown_lists_active_employees` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_employee_required` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_end_before_start` (test_employees_shift_create.py) | SH-CRT-010 | ⚠️ xfail | EMP-SH-CRT-010: Whether end-before-start is rejected depends on whether the app supports overnight shifts. Verify expected product behavi… | Case-by-case (see reason) |
| `test_create_shift_midnight_spanning` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_overlapping_shifts` (test_employees_shift_create.py) | SH-CRT-012 | ⚠️ xfail | EMP-SH-CRT-012: Whether overlapping shifts are blocked is a product decision. Verify expected server behaviour before implementing the as… | Case-by-case (see reason) |
| `test_create_shift_site_dropdown_lists_sites` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_site_required` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_shift_time_required` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_newly_created_shift_appears_immediately` (test_employees_shift_create.py) | — | ⏭️ skip | Manual - Check later for fixes: shift form locators use label heuristics, verify DOM and datetime picker in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_edit_activate_inactive_shift` (test_employees_shift_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: edit form locators use label heuristics — verify DOM and shift record existence in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_edit_employee_persists` (test_employees_shift_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: edit form locators use label heuristics — verify DOM and shift record existence in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_edit_form_opens_prepopulated` (test_employees_shift_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: edit form locators use label heuristics — verify DOM and shift record existence in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_edit_site_persists` (test_employees_shift_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: edit form locators use label heuristics — verify DOM and shift record existence in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_edit_time_recalculates_hours` (test_employees_shift_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: edit form locators use label heuristics — verify DOM and shift record existence in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_filter_active_off` (test_employees_shift_filter.py) | SH-FLT-006 | ⏭️ skip | EMP-SH-FLT-006: FILTER_ACTIVE_SHIFT_SWITCH locator fails after apply_filters closes panel — deferred | Deferred — re-check scope |
| `test_shift_filter_by_date_range` (test_employees_shift_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: date inputs use name heuristics — verify exact input names and format in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_filter_by_first_name` (test_employees_shift_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: shift filter locators use name/label heuristics — verify exact DOM structure in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_filter_invalid_date_range` (test_employees_shift_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: invalid date range behavior is unverified — product decision needs DevTools confirmation. | Manual test |
| `test_shift_filter_result_count_matches_rows` (test_employees_shift_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: shift filter locators use name/label heuristics — verify exact DOM structure in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_reset_all_clears_filters` (test_employees_shift_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: shift filter locators use name/label heuristics — verify exact DOM structure in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_list_displays_correct_columns` (test_employees_shift_list.py) | — | ⏭️ skip | Manual - Check later for fixes: shift column header locator uses class heuristics — verify exact header element classes in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_shift_pagination_no_negative_numbers` (test_employees_shift_list.py) | SH-LST-004 | ⏭️ skip | Manual — EMP-SH-LST-004: Pagination label verification requires manual visual check. | Manual test |

Next actions for this module: Rewrite locator (label/section heuristics don't match current DOM) ×35; Manual test ×11; Case-by-case (see reason) ×3; Deferred — re-check scope ×2; Re-check now — deferred as staging data / intermittent ×2

### gas_pump_settings

<details><summary>✅ Covered — 27 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpConnectionCode::test_yellow_triangle_on_unconnected_pump` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_active_toggle_on_create[GPS-CRT-012]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_active_toggle_on_create[GPS-CRT-013]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_add_pump_button_opens_form` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_cancel_discards_form` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_connection_indicator_yellow_on_new_pump` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_create_gas_pump_full_flow` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_numeric_field_defaults_on_create_form[GPS-CRT-011-baud-rate]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_numeric_field_defaults_on_create_form[GPS-CRT-011-code-length]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_numeric_field_defaults_on_create_form[GPS-CRT-011-fetch-interval]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_numeric_field_defaults_on_create_form[GPS-CRT-011-link-timeout]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpCreate::test_site_dropdown_lists_active_sites` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpEdgeCases::test_numeric_fields_reject_non_integer[GPS-EC-002-baud-rate]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpEdgeCases::test_numeric_fields_reject_non_integer[GPS-EC-002-code-length]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpEdgeCases::test_numeric_fields_reject_non_integer[GPS-EC-002-link-timeout]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpEdgeCases::test_numeric_fields_reject_non_integer[GPS-EC-002-serial-number]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpEdgeCases::test_numeric_fields_reject_non_integer[GPS-EC-002-serial-port]` | — |  |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-003]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-004]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-005]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-006]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-007]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-008]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-009]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_settings.py::TestGasPumpValidation::test_required_field_validation[GPS-CRT-010]` | — | 🔥 |
| `gas_pump_settings/test_gas_pump_ui.py::test_gas_pump_settings_grid_columns_are_visible` | — |  |
| `gas_pump_settings/test_gas_pump_ui.py::test_gas_pump_settings_page_loads_with_primary_controls` | — |  |

</details>

**Pending — 12 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpConnectionCode` (test_gas_pump_settings.py) | — | ⏭️ skip | Requires a gas pump physically connected to staging hardware. Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device. | Out of scope: needs gas pump hardware |
| `TestGasPumpWashBookCodeList` (test_gas_pump_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: get_wbc_wash_book_options() times out; option selector not verified in DevTools | Manual test |

Next actions for this module: Out of scope: needs gas pump hardware ×11; Manual test ×1

### general_sales_report

<details><summary>✅ Covered — 71 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `general_sales_report/test_general_sales_report.py::test_all_report_sections_present` | — | 🔥 |
| `general_sales_report/test_general_sales_report.py::test_all_sites_filter` | — |  |
| `general_sales_report/test_general_sales_report.py::test_apply_filters_refreshes_data` | — | 🔥 |
| `general_sales_report/test_general_sales_report.py::test_card_distribution_no_data` | — |  |
| `general_sales_report/test_general_sales_report.py::test_clearing_site_reverts_to_all` | — |  |
| `general_sales_report/test_general_sales_report.py::test_custom_date_range_applies` | — |  |
| `general_sales_report/test_general_sales_report.py::test_custom_date_range_picker_opens` | — |  |
| `general_sales_report/test_general_sales_report.py::test_custom_range_clears_preset` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_dropdown_shows_options` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-007]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-008]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-009]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-010]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-011]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_date_preset_updates_range[GSR-FLT-012]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_default_filter_state` | — |  |
| `general_sales_report/test_general_sales_report.py::test_export_button_present` | — |  |
| `general_sales_report/test_general_sales_report.py::test_four_revenue_cards_displayed` | — | 🔥 |
| `general_sales_report/test_general_sales_report.py::test_gift_card_net_revenue_formula` | — |  |
| `general_sales_report/test_general_sales_report.py::test_gift_card_section_collapsible` | — |  |
| `general_sales_report/test_general_sales_report.py::test_gift_card_three_sub_cards` | — |  |
| `general_sales_report/test_general_sales_report.py::test_gift_cards_redeemed_table` | — |  |
| `general_sales_report/test_general_sales_report.py::test_gift_cards_sold_table` | — |  |
| `general_sales_report/test_general_sales_report.py::test_gsr_page_loads` | — | 🔥 |
| `general_sales_report/test_general_sales_report.py::test_liability_composition_bar` | — |  |
| `general_sales_report/test_general_sales_report.py::test_membership_bar_chart` | — |  |
| `general_sales_report/test_general_sales_report.py::test_memberships_breakdown_columns` | — |  |
| `general_sales_report/test_general_sales_report.py::test_month_boundary_date_range` | — |  |
| `general_sales_report/test_general_sales_report.py::test_multi_site_comparison_visible` | — |  |
| `general_sales_report/test_general_sales_report.py::test_multi_site_filtered_single_site` | — |  |
| `general_sales_report/test_general_sales_report.py::test_multi_site_shows_site_rows` | — |  |
| `general_sales_report/test_general_sales_report.py::test_multiple_sites_filter` | — |  |
| `general_sales_report/test_general_sales_report.py::test_prepaid_liability_columns` | — |  |
| `general_sales_report/test_general_sales_report.py::test_rapid_preset_switching` | — |  |
| `general_sales_report/test_general_sales_report.py::test_reapply_same_filter_identical` | — |  |
| `general_sales_report/test_general_sales_report.py::test_redemptions_full_report_link` | — |  |
| `general_sales_report/test_general_sales_report.py::test_redemptions_link_navigates` | — |  |
| `general_sales_report/test_general_sales_report.py::test_redemptions_overview_displayed` | — |  |
| `general_sales_report/test_general_sales_report.py::test_redemptions_update_on_filter_change` | — |  |
| `general_sales_report/test_general_sales_report.py::test_retail_sales_category_expands` | — |  |
| `general_sales_report/test_general_sales_report.py::test_retail_sales_columns` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_breakdown_payment_channels` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_breakdown_updates` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_card_line_items[GSR-REV-002]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_card_line_items[GSR-REV-003]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_card_line_items[GSR-REV-004]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_card_line_items[GSR-REV-005]` | — |  |
| `general_sales_report/test_general_sales_report.py::test_revenue_cards_update_on_filter_change` | — |  |
| `general_sales_report/test_general_sales_report.py::test_sales_activity_no_data` | — |  |
| `general_sales_report/test_general_sales_report.py::test_sales_activity_updates` | — |  |
| `general_sales_report/test_general_sales_report.py::test_single_day_date_range` | — |  |
| `general_sales_report/test_general_sales_report.py::test_single_site_filter` | — |  |
| `general_sales_report/test_general_sales_report.py::test_site_dropdown_lists_sites` | — |  |
| `general_sales_report/test_general_sales_report.py::test_sites_dropdown_reflects_module` | — |  |
| `general_sales_report/test_general_sales_report.py::test_three_summary_tiles` | — |  |
| `general_sales_report/test_general_sales_report.py::test_total_invoices_count` | — |  |
| `general_sales_report/test_general_sales_report.py::test_transaction_breakdown_updates` | — |  |
| `general_sales_report/test_general_sales_report.py::test_washbook_net_revenue_formula` | — |  |
| `general_sales_report/test_general_sales_report.py::test_washbook_reconciliation_accordion` | — |  |
| `general_sales_report/test_general_sales_report.py::test_washbook_section_collapsible` | — |  |
| `general_sales_report/test_general_sales_report.py::test_washbooks_redeemed_table` | — |  |
| `general_sales_report/test_general_sales_report.py::test_washbooks_sold_table` | — |  |
| `general_sales_report/test_general_sales_report.py::test_zero_data_revenue_cards` | — |  |
| `general_sales_report/test_general_sales_report.py::test_zero_transaction_day_renders` | — |  |
| `general_sales_report/test_general_sales_report.py::test_zero_transaction_renders_cleanly` | — |  |
| `general_sales_report/test_redemption_details.py::test_expand_all_button` | — |  |
| `general_sales_report/test_redemption_details.py::test_filter_panel_auto_opened` | — |  |
| `general_sales_report/test_redemption_details.py::test_five_sections_visible` | — |  |
| `general_sales_report/test_redemption_details.py::test_redemption_details_page_loads` | — |  |
| `general_sales_report/test_redemption_details.py::test_single_day_checkbox_constrains_range` | — |  |
| `general_sales_report/test_redemption_details.py::test_site_filter_works` | — |  |

</details>

**Pending — 12 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_column_headers_sort` (test_general_sales_report.py) | — | ⏭️ skip | Manual - Check later for fixes: sort state relies on aria-sort attribute; verify column header DOM in DevTools | Manual test |
| `test_export_modal_four_options` (test_general_sales_report.py) | — | ⏭️ skip | Manual - Check later for fixes: export modal option count uses class heuristics; verify modal DOM in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_washbook_three_sub_cards` (test_general_sales_report.py) | — | ⏭️ skip | Manual - Check later for fixes: sub-card count uses class heuristic; verify container class names in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_apply_filters_updates_metrics` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004/005 | Manual test |
| `test_custom_option_enables_manual_entry` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: 'Custom' option and date input depend on RDT page UI; verify in DevTools | Manual test |
| `test_date_presets_dropdown` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page component; verify in DevTools | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[last-month]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[last-week]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[this-month]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[this-week]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[today]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |
| `test_each_date_preset_applies[GSR-RDT-005[yesterday]]` (test_redemption_details.py) | — | ⏭️ skip | Manual - Check later for fixes: DATE_PRESET_COMBOBOX locator doesn't match RDT page; same root cause as RDT-004 | Manual test |

Next actions for this module: Manual test ×10; Rewrite locator (label/section heuristics don't match current DOM) ×2

### gift_cards

<details><summary>✅ Covered — 29 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `gift_cards/test_gift_cards_edge_cases.py::test_create_gift_card_helper_is_idempotent` | — |  |
| `gift_cards/test_gift_cards_edge_cases.py::test_gift_cards_page_recovers_after_no_result_search` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_activate_inactive_gift_card` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_deactivate_active_gift_card` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_edit_customer_gift_card_amount` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_edit_gift_card_name` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_edit_gift_card_updates_settings_without_duplicate` | — |  |
| `gift_cards/test_gift_cards_edit.py::test_toggle_active_customer_gift_card` | — |  |
| `gift_cards/test_gift_cards_negative.py::test_missing_customer_gift_card_search_does_not_show_match` | — |  |
| `gift_cards/test_gift_cards_negative.py::test_opening_missing_gift_card_does_not_show_edit_form` | — |  |
| `gift_cards/test_gift_cards_positive.py::test_create_gift_card_with_required_settings` | — | 🔥 |
| `gift_cards/test_gift_cards_positive.py::test_create_inactive_gift_card` | — |  |
| `gift_cards/test_gift_cards_positive.py::test_created_gift_card_settings_persist` | — | 🔥 |
| `gift_cards/test_gift_cards_positive.py::test_customer_gift_card_persists_after_page_reload` | — | 🔥 |
| `gift_cards/test_gift_cards_positive.py::test_gift_card_appears_in_customer_gift_card_dropdown` | — |  |
| `gift_cards/test_gift_cards_search_filter.py::test_customer_gift_card_search_partial_number` | — |  |
| `gift_cards/test_gift_cards_search_filter.py::test_gift_cards_search_accepts_partial_text_without_breaking_grid` | — |  |
| `gift_cards/test_gift_cards_search_filter.py::test_search_exact_gift_card_name_returns_match` | — |  |
| `gift_cards/test_gift_cards_ui.py::test_customer_gift_cards_tab_loads` | — |  |
| `gift_cards/test_gift_cards_ui.py::test_gift_cards_page_loads` | — |  |
| `gift_cards/test_gift_cards_ui.py::test_gift_cards_primary_actions_are_available` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_create_customer_gift_card_requires_amount` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_create_customer_gift_card_requires_gift_card_selection` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_create_customer_gift_card_requires_number` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_create_gift_card_requires_amount` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_create_gift_card_requires_name` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_negative_customer_gift_card_amount_rejected` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_negative_gift_card_amount_rejected` | — |  |
| `gift_cards/test_gift_cards_validation.py::test_non_numeric_customer_gift_card_amount_rejected` | — |  |

</details>

**Pending — 8 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_gift_card_show_on_cp_persists` (test_gift_cards_dependency.py) | GC-PER-002 | ⏭️ skip | GC-PER-002: Per-location Show on CP switch is interactive but the value is not persisted by the save API — the switch resets to OFF on re… | Manual test |
| `test_active_toggle_shows_active_gift_cards_only` (test_gift_cards_filter.py) | — | ⚠️ xfail | search_gift_card() send_keys rejected by Chrome 152 overlay check after apply_filters; verify manually. | Manual test |
| `test_filter_by_site_narrows_customer_gift_card_list` (test_gift_cards_filter.py) | — | 🟡 xfail/passing | apply_filters() race: FILTER_BUTTON toggle re-opens panel mid-close-animation on staging; verify manually. | **Promote** — passed in last full run; remove xfail |
| `test_filter_by_site_narrows_gift_card_list` (test_gift_cards_filter.py) | — | ⚠️ xfail | apply_filters() race: FILTER_BUTTON toggle re-opens panel mid-close-animation on staging; verify manually. | Manual test |
| `test_reset_all_clears_gift_card_filters` (test_gift_cards_filter.py) | — | 🟡 xfail/passing | apply_filters() race: FILTER_BUTTON toggle re-opens panel mid-close-animation on staging; verify manually. | **Promote** — passed in last full run; remove xfail |
| `test_create_customer_gift_card_from_template` (test_gift_cards_positive.py) | CGC-CRT-001 | ⏭️ skip | CI-SKIP CGC-CRT-001: wait_for_customer_list_loaded times out in headless CI. Fix: same as CS-CRT-001 — use window.location.origin fallbac… | Case-by-case (see reason) |
| `test_customer_gift_card_linked_to_correct_template` (test_gift_cards_positive.py) | CGC-DEP-001 | ⏭️ skip | CI-SKIP CGC-DEP-001: same root cause as CGC-CRT-001 — wait_for_customer_list_loaded times out in headless CI. | Case-by-case (see reason) |
| `test_non_numeric_gift_card_amount_rejected` (test_gift_cards_validation.py) | — | ⏭️ skip | Manual: Chrome silently drops non-numeric chars from type=number inputs, leaving the field blank; the legacy iframe then saves/redirects … | Manual test |

Next actions for this module: Manual test ×4; **Promote** — passed in last full run; remove xfail ×2; Case-by-case (see reason) ×2

### kiosk_settings

<details><summary>✅ Covered — 12 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `kiosk_settings/test_kiosk_create.py::test_create_form_configure_panel_visible` | — |  |
| `kiosk_settings/test_kiosk_create.py::test_create_form_sections_collapsed_by_default` | — |  |
| `kiosk_settings/test_kiosk_create.py::test_create_kiosk_cancel_discards_form` | — |  |
| `kiosk_settings/test_kiosk_create.py::test_create_kiosk_name_required` | — | 🔥 |
| `kiosk_settings/test_kiosk_edge_cases.py::test_kiosk_name_whitespace_trimmed` | — |  |
| `kiosk_settings/test_kiosk_filter.py::test_filter_by_site` | — |  |
| `kiosk_settings/test_kiosk_filter.py::test_filter_by_site_count_matches_rows` | — |  |
| `kiosk_settings/test_kiosk_filter.py::test_filter_panel_opens` | — | 🔥 |
| `kiosk_settings/test_kiosk_list.py::test_kiosk_list_displays_columns` | — |  |
| `kiosk_settings/test_kiosk_list.py::test_kiosk_list_results_per_page` | — |  |
| `kiosk_settings/test_kiosk_list.py::test_kiosk_page_loads` | — | 🔥 |
| `kiosk_settings/test_kiosk_search.py::test_search_nonexistent_name` | — |  |

</details>

**Pending — 79 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_active_toggle_off_shows_inactive_in_list` (test_kiosk_active_connection.py) | KSK-ACT-002 | ⏭️ skip | Manual - Check later for fixes: KSK-ACT-002: Active toggle OFF not persisting in list — state pollution from edit tests creates a duplica… | Manual test |
| `test_active_toggle_on_shows_active_in_list` (test_kiosk_active_connection.py) | KSK-ACT-001 | ⏭️ skip | CI-SKIP KSK-ACT-001: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_check_regen_code_button_visible_when_connected` (test_kiosk_active_connection.py) | KSK-ACT-004 | ⏭️ skip | Manual - Check later for fixes: KSK-ACT-004: 'Check or re-generate code' button visibility depends on live connection state — verify butt… | Manual test |
| `test_kiosk_connected_message_displays` (test_kiosk_active_connection.py) | KSK-ACT-003 | ⏭️ skip | Manual - Check later for fixes: KSK-ACT-003: Connection status text locator uses heuristics — verify 'Kiosk connected' text presence in D… | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_add_kiosk_form_opens` (test_kiosk_create.py) | — | ⚠️ xfail | Create kiosk iframe does not open on staging | Case-by-case (see reason) |
| `test_create_kiosk_name_only` (test_kiosk_create.py) | KSK-CRT-002 | ⏭️ skip | Manual - Check later for fixes: KSK-CRT-002: Site is required to save — name-only submission is blocked by form validation; test asserts … | Manual test |
| `test_create_kiosk_with_site_and_lane` (test_kiosk_create.py) | KSK-CRT-004 | ⚠️ xfail | KSK-CRT-004/5: Site and Lane dropdowns depend on Sites & Locations data — verify in staging. | Case-by-case (see reason) |
| `test_generate_connection_code_after_create` (test_kiosk_create.py) | KSK-CRT-010 | ⏭️ skip | Manual - Check later for fixes: KSK-CRT-010: Generate connection code button and modal locators use heuristics — verify class names in De… | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_new_kiosk_appears_immediately` (test_kiosk_create.py) | KSK-CRT-009 | ⚠️ xfail | KSK-CRT-009: Depends on Site and Lane dropdowns — verify KSK_SITE/KSK_LANE exist in staging before removing xfail. | Needs guaranteed staging data (managed record) |
| `test_site_selection_populates_lane_dropdown` (test_kiosk_create.py) | KSK-CRT-004 | ⚠️ xfail | KSK-CRT-004/5: Site and Lane dropdowns depend on Sites & Locations data — verify in staging. | Case-by-case (see reason) |
| `test_lane_dropdown_lists_lanes_for_site` (test_kiosk_dependencies.py) | KSK-DEP-002 | ⚠️ xfail | KSK-DEP-002: Lane options depend on selected site in Sites & Locations module — verify KSK_LANE exists under KSK_SITE in staging before r… | Case-by-case (see reason) |
| `test_site_dropdown_lists_sites` (test_kiosk_dependencies.py) | KSK-DEP-001 | ⚠️ xfail | KSK-DEP-001: Site dropdown options depend on Sites & Locations module data — verify KSK_SITE exists in staging before removing xfail. | Case-by-case (see reason) |
| `test_car_recognition_by_plate_persists` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_car_recognition_by_rfid_persists` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_car_recognition_last_selected_wins` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_cc_entry_methods_saves` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_device_section_expand_collapse` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_enter_payment_serial_saves` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_payment_serial_persists` (test_kiosk_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_extras_dismiss_delay_boundary_values_valid` (test_kiosk_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_kiosk_without_site_lane_appears_in_list` (test_kiosk_edge_cases.py) | KSK-EC-002 | ⏭️ skip | Manual - Check later for fixes: KSK-EC-002: Site is required to save in staging — kiosk without site/lane is blocked by form validation | Manual test |
| `test_receipt_modal_delay_boundary_values_valid` (test_kiosk_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_cancel_discards_changes` (test_kiosk_edit.py) | KSK-EDT-006 | ⏭️ skip | Manual - Check later for fixes: KSK-EDT-006: Assertion checks body text for kiosk name but <input> values do not appear in Selenium body … | Manual test |
| `test_edit_clear_name_blocked` (test_kiosk_edit.py) | KSK-EDT-005 | ⏭️ skip | CI-SKIP KSK-EDT-005: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_edit_form_configure_panel_visible` (test_kiosk_edit.py) | KSK-EDT-007 | ⏭️ skip | Manual - Check later for fixes: KSK-EDT-007: Configure panel and tab locators use heuristics — verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_form_opens_prepopulated` (test_kiosk_edit.py) | KSK-EDT-001 | ⏭️ skip | Manual - Check later for fixes: KSK-EDT-001: Assertion checks body text for kiosk name but <input> values do not appear in Selenium body … | Manual test |
| `test_edit_kiosk_lane_persists` (test_kiosk_edit.py) | KSK-CRT-004 | ⚠️ xfail | KSK-CRT-004/5 / KSK-EDT-003/4: Site and Lane dropdowns depend on Sites & Locations data — verify in staging. | Case-by-case (see reason) |
| `test_edit_kiosk_name_persists` (test_kiosk_edit.py) | KSK-EDT-002 | ⏭️ skip | CI-SKIP KSK-EDT-002: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_edit_kiosk_site_persists` (test_kiosk_edit.py) | KSK-CRT-004 | ⚠️ xfail | KSK-CRT-004/5 / KSK-EDT-003/4: Site and Lane dropdowns depend on Sites & Locations data — verify in staging. | Case-by-case (see reason) |
| `test_filter_by_active_status` (test_kiosk_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: Filter panel locators (status combobox, reset button) use label heuristics — verify exact DOM structure i… | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_filter_reset_restores_list` (test_kiosk_filter.py) | KSK-FLT-005 | ⏭️ skip | Manual - Check later for fixes: KSK-FLT-005: Reset All button locator uses label heuristics — verify in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_fleet_call_attendant_toggle_saves` (test_kiosk_fleet_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_fleet_capabilities_dropdown_saves` (test_kiosk_fleet_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_fleet_manager_url_saves` (test_kiosk_fleet_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_fleet_section_expand_collapse` (test_kiosk_fleet_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_fleet_toggles_save_on_off` (test_kiosk_fleet_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_dedup_timer_saves` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_optspot_text_fields_save` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_optspot_toggles_save` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_remaining_toggles_save` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_remaining_toggles_save_duplicate` (test_kiosk_flow_settings.py) | KSK-FLW-007 | ⏭️ skip | Covered by KSK-FLW-007 — same remaining-toggles block in Flow/Appearance section. | Case-by-case (see reason) |
| `test_flow_section_expand_collapse` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_sign_membership_heading_saves` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_theme_dropdown_saves` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_toggles_save_on_and_off` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_flow_wex_wash_cards_toggle_saves` (test_kiosk_flow_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_gate_operational_toggle_off_persists` (test_kiosk_gate_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_gate_operational_toggle_on_persists` (test_kiosk_gate_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_gate_section_expand_collapse` (test_kiosk_gate_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_kiosk_list_pagination_shows_count` (test_kiosk_list.py) | KSK-LST-004 | ⏭️ skip | CI-SKIP KSK-LST-004: create_kiosk_if_missing times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_kiosk_list_status_column` (test_kiosk_list.py) | KSK-LST-003 | ⏭️ skip | CI-SKIP KSK-LST-003: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_localization_external_translations_toggle_saves` (test_kiosk_localization_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_localization_section_expand_collapse` (test_kiosk_localization_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_localization_translation_url_saves` (test_kiosk_localization_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_enter_middleware_ip_saves` (test_kiosk_middleware_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_middleware_ip_persists` (test_kiosk_middleware_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_middleware_section_expand_collapse` (test_kiosk_middleware_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_clear_search_restores_list` (test_kiosk_search.py) | KSK-SRH-004 | ⏭️ skip | CI-SKIP KSK-SRH-004: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_search_by_exact_name` (test_kiosk_search.py) | KSK-SRH-001 | ⏭️ skip | CI-SKIP KSK-SRH-001: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_search_by_partial_name` (test_kiosk_search.py) | KSK-SRH-002 | ⏭️ skip | CI-SKIP KSK-SRH-002: managed_kiosk fixture fails in headless CI — kiosk create flow times out. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_enable_all_checkboxes_and_upsale` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_recheck_memberships_persists` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_service_section_expand_collapse` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_service_section_shows_checkboxes` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_uncheck_memberships_persists` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_upsale_toggle_off_persists` (test_kiosk_service_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_extras_dismiss_delay_above_max_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_extras_dismiss_delay_below_min_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_extras_dismiss_delay_valid_value` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_receipt_modal_delay_above_max_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_receipt_modal_delay_below_min_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_receipt_modal_delay_valid_value` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_rfid_tag_delay_out_of_range_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_rfid_tag_delay_valid_value` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_timer_field_non_numeric_rejected` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_timer_section_expand_collapse` (test_kiosk_timer_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_tunnel_operational_toggle_off_persists` (test_kiosk_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_tunnel_operational_toggle_on_persists` (test_kiosk_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_tunnel_section_expand_collapse` (test_kiosk_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: Settings section locators use heuristics — verify section header classes in DevTools | Rewrite locator (label/section heuristics don't match current DOM) |

Next actions for this module: Rewrite locator (label/section heuristics don't match current DOM) ×56; Case-by-case (see reason) ×16; Manual test ×6; Needs guaranteed staging data (managed record) ×1

### labor_shifts

<details><summary>✅ Covered — 83 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionCards::test_commission_card_currency_format` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionCards::test_commission_cards_update_on_filter_change` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionCards::test_commission_cards_zero_with_no_data` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionCards::test_commission_reconciliation_chain` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionCards::test_four_commission_cards_visible` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_search_filters_table` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-01]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-02]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-03]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-04]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-05]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-06]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-07]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_column_present[LAB-CTX-001-08]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_empty_state` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_table_has_rows` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsCommissionTransactions::test_ctx_type_column_has_values` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_calendar_opens_on_date_click` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_custom_date_range_updates` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_page_level_preset_matches_modal` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-002]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-003]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-004]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-005]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-006]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_preset_populates_date_range[LAB-DTE-007]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_range_spanning_month_boundary_renders` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_selecting_preset_fills_date_range` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_single_day_custom_range_renders` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_single_day_mode_renders_report` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsDateFilter::test_uncheck_single_day_reverts_to_range` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_search_filters_table` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_search_no_match` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_status_filter[LAB-EMP-006-active]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_status_filter[LAB-EMP-006-all]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_status_filter[LAB-EMP-006-inactive]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-01]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-02]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-03]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-04]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-05]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-06]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-07]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_column_present[LAB-EMP-001-08]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsEmployeeTable::test_employee_table_empty_state` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_all_metrics_zero_with_no_data` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_currency_and_percentage_format` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_employee_count_reconciliation` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_employee_summary_matches_table_count` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_employees_summary_card_content` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_kpi_card_visible[LAB-KPI-001-01]` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_kpi_card_visible[LAB-KPI-001-02]` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_kpi_card_visible[LAB-KPI-001-03]` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_kpi_card_visible[LAB-KPI-001-04]` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_total_hours_format` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_widgets_refresh_on_date_change` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsKPI::test_widgets_refresh_on_site_change` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_apply_filters_closes_modal` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_employee_summary_and_commission_visible` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_filter_modal_auto_opens` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_filter_values_reflected_in_page_bar` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_modal_contains_all_controls` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_modal_opens_with_no_site_default` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_page_level_changes_do_not_reopen_modal` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_page_loads_at_correct_url` | — | 🔥 |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_page_renders_widget_stack` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsNav::test_sidebar_active_state` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsPagination::test_table_pagination_controls_present[LAB-CTX-011]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsPagination::test_table_pagination_controls_present[LAB-EMP-012]` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_chip_x_clear_returns_empty_state` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_deactivated_sites_absent` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_deselecting_site_removes_chip` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_multi_site_aggregation` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_multi_site_shows_chips_with_overflow` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_page_level_site_refresh` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_selected_option_highlighted_in_dropdown` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_single_site_scopes_data` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_site_dropdown_scrollable` | — |  |
| `labor_shifts/test_labor_shifts.py::TestLaborShiftsSiteFilter::test_sites_dropdown_lists_active_sites` | — |  |
| `labor_shifts/test_labor_shifts.py::TestSingleDaySync::test_modal_sdm_syncs_to_page_bar` | — |  |
| `labor_shifts/test_labor_shifts.py::TestSingleDaySync::test_modal_single_day_changes_date_field` | — |  |
| `labor_shifts/test_labor_shifts.py::TestSingleDaySync::test_modal_single_day_checkbox_visible` | — |  |
| `labor_shifts/test_labor_shifts.py::TestSingleDaySync::test_page_bar_sdm_uncheck_syncs_to_modal` | — |  |

</details>

**Pending — 3 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestLaborShiftsDateFilter` (test_labor_shifts.py) | — | ⏭️ skip | Manual - Check later for fixes: date preset dropdown CSS class not confirmed — needs DevTools inspection. | Fix date preset dropdown interaction |
| `TestLaborShiftsEmployeeTable` (test_labor_shifts.py) | — | ⏭️ skip | staging data: no employee shifts recorded for current month — deferred | Deferred — re-check scope |
| `TestLaborShiftsNav` (test_labor_shifts.py) | LAB-NAV-008 | ⚠️ xfail | Known defect LAB-NAV-008: subtitle renders 'Commision Transactions' (missing second 'm'). Expected: 'Commission Transactions'. xfail unti… | Case-by-case (see reason) |

Next actions for this module: Fix date preset dropdown interaction ×1; Deferred — re-check scope ×1; Case-by-case (see reason) ×1

### login

<details><summary>✅ Covered — 40 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `login/test_login.py::test_admin_login` | — |  |
| `login/test_login_negative.py::test_login_invalid_email_invalid_password_does_not_authenticate` | — |  |
| `login/test_login_negative.py::test_login_invalid_email_valid_password_does_not_authenticate` | — |  |
| `login/test_login_negative.py::test_login_valid_email_invalid_password_does_not_authenticate` | — | 🔥 |
| `login/test_login_password.py::test_password_is_masked_by_default` | — |  |
| `login/test_login_password.py::test_password_visibility_toggle_hides_password_again` | — |  |
| `login/test_login_password.py::test_very_long_password_does_not_break_login_ui` | — |  |
| `login/test_login_positive.py::test_authenticated_user_cannot_access_login_page` | — | 🔥 |
| `login/test_login_positive.py::test_login_using_enter_key` | — |  |
| `login/test_login_positive.py::test_login_with_email_case_variation` | — |  |
| `login/test_login_positive.py::test_login_with_email_trailing_space` | — |  |
| `login/test_login_positive.py::test_login_with_valid_credentials` | — | 🔥 |
| `login/test_login_positive.py::test_session_persists_after_refresh` | — | 🔥 |
| `login/test_login_positive.py::test_session_remains_active_in_new_tab` | — |  |
| `login/test_login_security_smoke.py::test_login_security_payloads_do_not_authenticate[' OR 1=1 ---password]` | — |  |
| `login/test_login_security_smoke.py::test_login_security_payloads_do_not_authenticate[<script>alert(1)</script>-password]` | — |  |
| `login/test_login_security_smoke.py::test_login_security_payloads_do_not_authenticate[admin@example.com-' OR 1=1 --]` | — |  |
| `login/test_login_security_smoke.py::test_login_security_payloads_do_not_authenticate[admin@example.com-<script>alert(1)</script>]` | — |  |
| `login/test_login_session.py::test_direct_protected_url_without_login_redirects_to_login` | — | 🔥 |
| `login/test_login_ui.py::test_login_browser_title` | — |  |
| `login/test_login_ui.py::test_login_field_labels_are_displayed` | — |  |
| `login/test_login_ui.py::test_login_fields_and_button_are_visible` | — |  |
| `login/test_login_ui.py::test_login_footer_is_displayed` | — |  |
| `login/test_login_ui.py::test_login_page_loads` | — |  |
| `login/test_login_ui.py::test_login_page_url_is_correct` | — |  |
| `login/test_login_ui.py::test_login_tab_order_email_password_login_button` | — |  |
| `login/test_login_ui.py::test_password_visibility_icon_is_displayed` | — |  |
| `login/test_login_validation.py::test_login_validation_both_fields_empty` | — | 🔥 |
| `login/test_login_validation.py::test_login_validation_email_empty` | — |  |
| `login/test_login_validation.py::test_login_validation_email_spaces_only` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[@gmail.com]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc @gmail.com]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc.gmail.com]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc@@gmail.com]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc@]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc@gmail]` | — |  |
| `login/test_login_validation.py::test_login_validation_invalid_email_formats[abc]` | — |  |
| `login/test_login_validation.py::test_login_validation_maximum_email_length_does_not_break_ui` | — |  |
| `login/test_login_validation.py::test_login_validation_password_empty` | — |  |
| `login/test_login_validation.py::test_login_validation_password_spaces_only` | — |  |

</details>

**Pending — 4 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_password_visibility_toggle_shows_password` (test_login_password.py) | — | ⚠️ xfail | Known product gap: password visibility icon disappears after typing. | Case-by-case (see reason) |
| `test_login_with_email_leading_space` (test_login_positive.py) | — | ⚠️ xfail | Known product gap: valid email with a leading space is not trimmed. | Case-by-case (see reason) |
| `test_login_layout_renders_after_refresh` (test_login_ui.py) | — | ⏭️ skip | needs_inspection: depends on LOGO_IMAGE locator — fix test_login_logo_is_available first | Confirm locator on staging, then implement |
| `test_login_logo_is_available` (test_login_ui.py) | — | ⏭️ skip | needs_inspection: logo img alt attribute changed on staging — update LOGO_IMAGE locator in login_page.py after checking /login HTML | Confirm locator on staging, then implement |

Next actions for this module: Case-by-case (see reason) ×2; Confirm locator on staging, then implement ×2

### memberships

<details><summary>✅ Covered — 59 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `memberships/test_memberships_download.py::test_download_filtered_memberships_starts_file_download` | — |  |
| `memberships/test_memberships_download.py::test_download_memberships_file_format` | — |  |
| `memberships/test_memberships_download.py::test_download_memberships_starts_file_download` | — |  |
| `memberships/test_memberships_edge_cases.py::test_membership_create_is_idempotent` | — |  |
| `memberships/test_memberships_edge_cases.py::test_membership_long_name_does_not_break_form` | — |  |
| `memberships/test_memberships_edge_cases.py::test_membership_only_first_location_is_assigned` | — |  |
| `memberships/test_memberships_edit.py::test_applicable_discount_persists` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_assigns_multiple_locations` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_barcode_persists` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_customer_portal_toggle_off` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_customer_portal_toggle_on` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_global_price_and_commission` | — |  |
| `memberships/test_memberships_edit.py::test_edit_managed_membership_type` | — |  |
| `memberships/test_memberships_edit.py::test_edit_membership_loyalty_points_and_discount` | — |  |
| `memberships/test_memberships_edit.py::test_edit_membership_name_and_restore` | — |  |
| `memberships/test_memberships_edit.py::test_limit_membership_toggle_persists` | — |  |
| `memberships/test_memberships_edit.py::test_membership_description_saves` | — |  |
| `memberships/test_memberships_edit.py::test_remove_applicable_discount_persists` | — |  |
| `memberships/test_memberships_managed.py::test_managed_membership_mutation_is_reset_on_teardown` | — |  |
| `memberships/test_memberships_managed.py::test_managed_membership_provided_at_baseline` | — |  |
| `memberships/test_memberships_negative.py::test_memberships_special_character_search_stays_usable` | — |  |
| `memberships/test_memberships_positive.py::test_activate_membership` | — |  |
| `memberships/test_memberships_positive.py::test_cancel_create_membership_discards_unsaved_changes` | — | 🔥 |
| `memberships/test_memberships_positive.py::test_create_prepaid_membership` | — | 🔥 |
| `memberships/test_memberships_positive.py::test_create_recurring_membership` | — |  |
| `memberships/test_memberships_positive.py::test_membership_settings_persist` | — | 🔥 |
| `memberships/test_memberships_redemption.py::test_redemption_single_location_persists` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_apply_multiple_filters` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_case_insensitive_search` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_combined_type_and_status_filter` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_existing_search` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_filter_active_shows_only_active` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_filter_by_prepaid_type` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_filter_by_recurring_type` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_filter_by_site` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_long_search_text_does_not_break_grid` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_missing_search` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_reset_filters_restores_grid` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_search_inactive_membership` | — |  |
| `memberships/test_memberships_search_filter.py::test_memberships_search_payloads_do_not_break_grid` | — |  |
| `memberships/test_memberships_ui.py::test_add_membership_form_loads` | — |  |
| `memberships/test_memberships_ui.py::test_discount_settings_tab_loads` | — |  |
| `memberships/test_memberships_ui.py::test_memberships_filter_panel_shows_controls` | — |  |
| `memberships/test_memberships_ui.py::test_memberships_grid_columns_are_visible` | — |  |
| `memberships/test_memberships_ui.py::test_memberships_page_loads_with_primary_controls` | — | 🔥 |
| `memberships/test_memberships_ui.py::test_memberships_pagination_results_and_support_controls` | — |  |
| `memberships/test_memberships_ui.py::test_redemption_settings_tab_loads` | — |  |
| `memberships/test_memberships_ui.py::test_save_and_cancel_buttons_are_visible_on_create_form` | — |  |
| `memberships/test_memberships_ui.py::test_visible_membership_rows_have_edit_action` | — |  |
| `memberships/test_memberships_validation.py::test_alphabetic_global_price_is_rejected` | — |  |
| `memberships/test_memberships_validation.py::test_decimal_global_price_is_accepted_and_saved` | — |  |
| `memberships/test_memberships_validation.py::test_duplicate_barcode_is_rejected` | — |  |
| `memberships/test_memberships_validation.py::test_duplicate_membership_name_is_rejected` | — |  |
| `memberships/test_memberships_validation.py::test_membership_blank_required_form_stays_on_form` | — |  |
| `memberships/test_memberships_validation.py::test_membership_required_name_validation` | — | 🔥 |
| `memberships/test_memberships_validation.py::test_membership_requires_global_price` | — |  |
| `memberships/test_memberships_validation.py::test_negative_global_commission_is_rejected` | — |  |
| `memberships/test_memberships_validation.py::test_negative_global_price_is_rejected` | — |  |
| `memberships/test_memberships_validation.py::test_spaces_only_membership_name_is_rejected` | — |  |

</details>

**Pending — 7 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_create_inactive_membership` (test_memberships_positive.py) | MB-TGL-002 | ⚠️ xfail | MB-TGL-002: staging server saves membership as Active regardless of the Inactive selection on the create form. Same app bug as WP-TGL-002… | Possible product bug — confirm with product |
| `test_deactivate_membership` (test_memberships_positive.py) | MB-EDT-010 | ⚠️ xfail | MB-EDT-010: staging server saves membership as Active regardless of the Inactive toggle on the edit form. Same app bug as WP-TGL-002 / PO… | Possible product bug — confirm with product |
| `test_redeem_at_multiple_locations_persists` (test_memberships_redemption.py) | MB-RDM-002 | ⚠️ xfail | MB-RDM-002 test-data issue: the service is only configured at one staging location, so multi-location redemption cannot be exercised. | Case-by-case (see reason) |
| `test_memberships_clear_search_restores_records` (test_memberships_search_filter.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_memberships_filter_inactive_excludes_active` (test_memberships_search_filter.py) | — | ⏭️ skip | App bug: inactive filter still shows Active memberships — pending fix | Case-by-case (see reason) |
| `test_memberships_partial_search` (test_memberships_search_filter.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_memberships_search_with_surrounding_spaces` (test_memberships_search_filter.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |

Next actions for this module: Re-check — save/return-to-list fixes may resolve ×3; Possible product bug — confirm with product ×2; Case-by-case (see reason) ×2

### overview

<details><summary>✅ Covered — 18 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `overview/test_overview_data_validation.py::test_overview_filters_persist_navigating_to_report` | — |  |
| `overview/test_overview_data_validation.py::test_overview_modal_and_inline_filters_return_matching_totals` | — |  |
| `overview/test_overview_data_validation.py::test_overview_revenue_daily_matches_report` | — |  |
| `overview/test_overview_exports.py::test_overview_exports_are_available_and_filter_aware` | — |  |
| `overview/test_overview_known_bugs.py::test_overview_labor_percent_extreme_value_bug` | — |  |
| `overview/test_overview_known_bugs.py::test_overview_labor_percent_no_revenue_shows_placeholder` | — |  |
| `overview/test_overview_navigation.py::test_overview_browser_back_returns_to_overview` | — |  |
| `overview/test_overview_navigation.py::test_overview_opens_in_new_tab` | — |  |
| `overview/test_overview_reports.py::test_overview_cars_washed_report_hourly_chart_legend` | — |  |
| `overview/test_overview_reports.py::test_overview_cars_washed_report_percentages_sum_to_100` | — |  |
| `overview/test_overview_reports.py::test_overview_cars_washed_report_redemption_cards` | — |  |
| `overview/test_overview_reports.py::test_overview_cars_washed_report_rounding_rule` | — |  |
| `overview/test_overview_reports.py::test_overview_cars_washed_report_usage_breakdown_tabs` | — | 🔥 |
| `overview/test_overview_reports.py::test_overview_revenue_report_donut_updates_on_click` | — |  |
| `overview/test_overview_reports.py::test_overview_revenue_report_loads` | — | 🔥 |
| `overview/test_overview_reports.py::test_overview_revenue_report_membership_tab` | — |  |
| `overview/test_overview_reports.py::test_overview_revenue_report_summary_cards_update` | — |  |
| `overview/test_overview_ui.py::test_overview_shell_redirects_and_loads` | — | 🔥 |

</details>

**Pending — 58 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_overview_both_report_pages_accept_same_filter_inputs` (test_overview_data_validation.py) | — | ⚠️ xfail | overview iframe does not render on staging — first-load race | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_cars_washed_total_matches_report` (test_overview_data_validation.py) | — | ⚠️ xfail | overview iframe does not render on staging — first-load race | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_clearing_sites_reverts_to_aggregated` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_custom_date_range_updates_dashboard` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_date_preset_filters_are_available` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_date_range_filters_are_available` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_end_date_before_start_documents_behaviour` (test_overview_filters.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_last_month_preset_updates_dashboard` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_selected_site_shows_as_chip` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_single_day_checkbox_is_available` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_single_day_no_date_documents_behaviour` (test_overview_filters.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_single_day_no_date_no_broken_state` (test_overview_filters.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_single_day_today_matches_today_preset` (test_overview_filters.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_site_filter_dropdown_opens` (test_overview_filters.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_site_filter_updates_dashboard` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_uncheck_single_day_reverts_to_range_mode` (test_overview_filters.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_usage_breakdown_percentages_sum_to_100` (test_overview_known_bugs.py) | — | ⚠️ xfail | overview iframe does not render on staging — first-load race | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_report_navigation_is_available` (test_overview_navigation.py) | — | ⚠️ xfail | Known product/environment gap: legacy Overview iframe is empty; report links are unavailable. | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_employees_empty_state_with_no_shift_data` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_employees_no_records_label_when_no_assignments` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_future_date_range_shows_empty_state` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_network_failure_is_handled` (test_overview_negative.py) | — | ⚠️ xfail | Blocked: no network interception utility exists for Overview filter requests. | Case-by-case (see reason) |
| `test_overview_no_data_states_are_handled` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_rapid_filter_switching_does_not_crash` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_zero_data_visually_distinct_from_loading` (test_overview_negative.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_cars_washed_report_loads` (test_overview_reports.py) | — | ⚠️ xfail | overview iframe does not render on staging — first-load race | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_cars_washed_report_summary_cards_update` (test_overview_reports.py) | — | ⚠️ xfail | overview iframe does not render on staging — first-load race | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_dashboard_filter_controls_visible` (test_overview_ui.py) | — | ⚠️ xfail | Known product/environment gap: legacy Overview iframe is empty. | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_dashboard_widgets_visible` (test_overview_ui.py) | — | ⚠️ xfail | Known product/environment gap: legacy Overview iframe is empty. | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_export_buttons_visible` (test_overview_ui.py) | — | 🟡 xfail/passing | Known product/environment gap: legacy Overview iframe is empty. | **Promote** — passed in last full run; remove xfail |
| `test_overview_support_button_is_visible` (test_overview_ui.py) | — | 🟡 xfail/passing | Third-party support widget does not load in headless mode or on staging. | **Promote** — passed in last full run; remove xfail |
| `test_overview_all_dashboard_cards_render` (test_overview_widgets.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_awt_breakdown_bar_renders` (test_overview_widgets.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_awt_formula_values_match_display` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_awt_info_tooltip_shows_formula` (test_overview_widgets.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_awt_tiles_are_clickable` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_cars_washed_breakdown_legend` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_cars_washed_full_report_link` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_cars_washed_hourly_chart_renders` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_cars_washed_totals_update_with_filters` (test_overview_widgets.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_employees_full_report_link` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_employees_shift_status` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_employees_table_columns` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_gift_cards_totals` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_labor_full_report_link` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_labor_per_car_and_per_hour` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_labor_percent_calculates` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_memberships_active_count` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_memberships_canceled_bars_display` (test_overview_widgets.py) | — | ⚠️ xfail | Legacy dashboard iframe loads empty on staging | Product/env: legacy Overview iframe loads empty on staging |
| `test_overview_memberships_info_tooltip_visible` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_memberships_recurring_prepaid_breakdown` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_memberships_transaction_counts_update` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_revenue_donut_chart_renders` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_revenue_full_report_link` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_revenue_memberships_toggle` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_revenue_memberships_toggle_effect_documented` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_revenue_totals_update_with_filters` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |
| `test_overview_wash_books_totals` (test_overview_widgets.py) | — | 🟡 xfail/passing | Legacy dashboard iframe loads empty on staging | **Promote** — passed in last full run; remove xfail |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×35; Product/env: legacy Overview iframe loads empty on staging ×22; Case-by-case (see reason) ×1

### performance_metrics

<details><summary>✅ Covered — 66 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `performance_metrics/test_performance_metrics.py::TestColumnSettings::test_date_column_always_visible` | — |  |
| `performance_metrics/test_performance_metrics.py::TestColumnSettings::test_master_switch_toggles_all_off` | — |  |
| `performance_metrics/test_performance_metrics.py::TestColumnSettings::test_toggle_off_removes_column` | — |  |
| `performance_metrics/test_performance_metrics.py::TestColumnSettings::test_toggle_on_restores_column` | — |  |
| `performance_metrics/test_performance_metrics.py::test_all_sites_option_present_and_default` | — |  |
| `performance_metrics/test_performance_metrics.py::test_all_toggles_on_by_default` | — |  |
| `performance_metrics/test_performance_metrics.py::test_cancelled_vs_canceled_spelling` | — |  |
| `performance_metrics/test_performance_metrics.py::test_checkbox_state_reflects_selection` | — |  |
| `performance_metrics/test_performance_metrics.py::test_clear_all_removes_all_sites` | — |  |
| `performance_metrics/test_performance_metrics.py::test_color_coded_semantics` | — |  |
| `performance_metrics/test_performance_metrics.py::test_conversion_rate_chart_renders` | — |  |
| `performance_metrics/test_performance_metrics.py::test_custom_range_calendar_picker_opens` | — |  |
| `performance_metrics/test_performance_metrics.py::test_custom_range_updates_and_refreshes` | — |  |
| `performance_metrics/test_performance_metrics.py::test_cvr_legend_shows_series_name` | — |  |
| `performance_metrics/test_performance_metrics.py::test_cvr_rerenders_on_filter_change` | — |  |
| `performance_metrics/test_performance_metrics.py::test_cvr_y_axis_percentage_range` | — |  |
| `performance_metrics/test_performance_metrics.py::test_date_cells_with_weekday_and_color` | — |  |
| `performance_metrics/test_performance_metrics.py::test_deactivated_sites_excluded` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Cancelled]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Current day declines count]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Current day recharges]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Date]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Declined & Canceled]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Declined]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Net movement]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[New Prepaid]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[New Recurring]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[New]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Prepaid]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Prev. day recharge]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Previous day declines count]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Recharges]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Recurring]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Resignup]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Site Name]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_default_column_headers[Total]` | — |  |
| `performance_metrics/test_performance_metrics.py::test_dropdown_scrolls_with_many_options` | — |  |
| `performance_metrics/test_performance_metrics.py::test_filter_modal_auto_opens` | — |  |
| `performance_metrics/test_performance_metrics.py::test_filter_modal_contains_four_controls` | — |  |
| `performance_metrics/test_performance_metrics.py::test_filter_values_reflected_in_page_bar` | — |  |
| `performance_metrics/test_performance_metrics.py::test_future_dates_not_selectable` | — |  |
| `performance_metrics/test_performance_metrics.py::test_horizontal_scrollbar_visible` | — |  |
| `performance_metrics/test_performance_metrics.py::test_membership_history_table_renders` | — | 🔥 |
| `performance_metrics/test_performance_metrics.py::test_metrics_shell_renders_behind_modal` | — |  |
| `performance_metrics/test_performance_metrics.py::test_mht_updates_on_filter_change` | — |  |
| `performance_metrics/test_performance_metrics.py::test_modal_does_not_reopen_from_page_bar` | — |  |
| `performance_metrics/test_performance_metrics.py::test_modal_lists_17_column_toggles` | — |  |
| `performance_metrics/test_performance_metrics.py::test_modal_opens_with_default_state` | — |  |
| `performance_metrics/test_performance_metrics.py::test_month_boundary_spanning_range` | — |  |
| `performance_metrics/test_performance_metrics.py::test_multi_year_range_no_error` | — |  |
| `performance_metrics/test_performance_metrics.py::test_no_data_message_when_empty` | — |  |
| `performance_metrics/test_performance_metrics.py::test_page_level_preset_dropdown_has_six_options` | — |  |
| `performance_metrics/test_performance_metrics.py::test_page_level_site_change_auto_applies` | — |  |
| `performance_metrics/test_performance_metrics.py::test_page_loads_at_correct_url` | — | 🔥 |
| `performance_metrics/test_performance_metrics.py::test_page_renders_two_widgets` | — | 🔥 |
| `performance_metrics/test_performance_metrics.py::test_preset_change_in_page_bar_auto_applies` | — |  |
| `performance_metrics/test_performance_metrics.py::test_resignup_label_mismatch` | — |  |
| `performance_metrics/test_performance_metrics.py::test_rows_sorted_descending_by_date` | — |  |
| `performance_metrics/test_performance_metrics.py::test_selected_sites_render_as_chips` | — |  |
| `performance_metrics/test_performance_metrics.py::test_settings_icon_opens_modal` | — |  |
| `performance_metrics/test_performance_metrics.py::test_single_site_scopes_both_widgets` | — | 🔥 |
| `performance_metrics/test_performance_metrics.py::test_sites_dropdown_lists_all_active_sites` | — |  |
| `performance_metrics/test_performance_metrics.py::test_sites_dropdown_uses_checkboxes` | — |  |
| `performance_metrics/test_performance_metrics.py::test_today_highlighted_in_calendar` | — |  |
| `performance_metrics/test_performance_metrics.py::test_unchecking_removes_site` | — |  |
| `performance_metrics/test_performance_metrics.py::test_zero_values_render_as_zero` | — |  |

</details>

**Pending — 20 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_all_sites_aggregates_data` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_apply_closes_modal_and_renders_widgets` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_clear_date_range_button` (test_performance_metrics.py) | PFM-DTE-015 | ⚠️ xfail | Known gap PFM-DTE-015: no clear/X button found for the date range field in the current build — direct JS click on all buttons in the inpu… | Fix date preset dropdown interaction |
| `test_clicking_header_toggles_sort` (test_performance_metrics.py) | PFM-MHT-008 | ⚠️ xfail | Known gap PFM-MHT-008: MHT table does not re-sort on header click — sort interaction is not yet implemented in the current build | Case-by-case (see reason) |
| `test_column_headers_have_sort_controls` (test_performance_metrics.py) | PFM-MHT-007 | ⚠️ xfail | Known gap PFM-MHT-007: MHT column headers do not expose aria-sort or sort-class icons in the current build — sort UI is not yet implemented | Case-by-case (see reason) |
| `test_cvr_week_range_boundary[CVR-002-CVR-003-short_range]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_cvr_week_range_boundary[CVR-004-gte_7days]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_dropdown_lists_six_options` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not rendering options on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[Last month]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[Last week]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[This month]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[This week]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[Today]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_date_preset_sets_correct_range[Yesterday]` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_membership_history_site_name_scoped` (test_performance_metrics.py) | PFM-SIT-006 | ⚠️ xfail | Known defect PFM-SIT-006: Membership history SITE NAME shows 'All Sites' even when a subset of sites is selected | Case-by-case (see reason) |
| `test_mht_includes_most_recent_rows` (test_performance_metrics.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_multiple_sites_aggregate_data` (test_performance_metrics.py) | PFM-SIT-005 | ⚠️ xfail | Known gap PFM-SIT-005: second site (VK AL02) does not appear as a chip after selection — was masked by a SITE_CHIPS locator bug that doub… | Confirm locator on staging, then implement |
| `test_preset_auto_updates_date_range` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |
| `test_sidebar_highlights_active_item` (test_performance_metrics.py) | — | ⏭️ skip | Manual - Check later for fixes: sidebar active state class not detectable; needs DevTools inspection | Manual test |
| `test_single_day_range_shows_cvr_constraint` (test_performance_metrics.py) | — | ⚠️ xfail | PFM date preset dropdown not responding on staging | Fix date preset dropdown interaction |

Next actions for this module: Fix date preset dropdown interaction ×14; Case-by-case (see reason) ×3; Re-check now — deferred as staging data / intermittent ×1; Confirm locator on staging, then implement ×1; Manual test ×1

### pos_settings

<details><summary>✅ Covered — 52 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `pos_settings/test_pos_active.py::test_active_pos_toggle_on_saves` | — | 🔥 |
| `pos_settings/test_pos_create.py::test_add_pos_button_opens_form` | — | 🔥 |
| `pos_settings/test_pos_create.py::test_allow_checkout_default` | — |  |
| `pos_settings/test_pos_create.py::test_cancel_discards_form` | — |  |
| `pos_settings/test_pos_create.py::test_card_checked_by_default` | — |  |
| `pos_settings/test_pos_create.py::test_cash_checked_by_default` | — |  |
| `pos_settings/test_pos_create.py::test_create_pos_lane_required` | — |  |
| `pos_settings/test_pos_create.py::test_create_pos_name_required` | — |  |
| `pos_settings/test_pos_create.py::test_create_pos_site_required` | — |  |
| `pos_settings/test_pos_create.py::test_lane_dropdown_populates_on_site_selection` | — |  |
| `pos_settings/test_pos_create.py::test_new_pos_appears_immediately` | — |  |
| `pos_settings/test_pos_create.py::test_settings_accordions_collapsed` | — |  |
| `pos_settings/test_pos_create.py::test_uncheck_card_persists` | — |  |
| `pos_settings/test_pos_create.py::test_uncheck_cash_persists` | — |  |
| `pos_settings/test_pos_dependencies.py::test_lane_dropdown_from_site_lanes` | — |  |
| `pos_settings/test_pos_device_settings.py::test_device_serial_accepts_valid_input` | — |  |
| `pos_settings/test_pos_device_settings.py::test_device_serial_persists` | — |  |
| `pos_settings/test_pos_device_settings.py::test_device_serial_required` | — |  |
| `pos_settings/test_pos_edge_cases.py::test_pos_name_whitespace_trimmed` | — |  |
| `pos_settings/test_pos_edit.py::test_cancel_discards_changes` | — |  |
| `pos_settings/test_pos_edit.py::test_changing_site_clears_lane` | — |  |
| `pos_settings/test_pos_edit.py::test_edit_blank_name_blocked` | — |  |
| `pos_settings/test_pos_edit.py::test_edit_form_opens_prepopulated` | — | 🔥 |
| `pos_settings/test_pos_edit.py::test_edit_payment_methods_persists` | — |  |
| `pos_settings/test_pos_edit.py::test_edit_pos_name_persists` | — |  |
| `pos_settings/test_pos_edit.py::test_edit_site_persists` | — |  |
| `pos_settings/test_pos_edit.py::test_main_and_service_tabs_visible` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_active_pos_off` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_active_pos_on` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_by_site` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_panel_opens` | — | 🔥 |
| `pos_settings/test_pos_filter.py::test_filter_reset_all` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_result_count_matches_rows` | — |  |
| `pos_settings/test_pos_filter.py::test_filter_site_and_active_combined` | — |  |
| `pos_settings/test_pos_list.py::test_pos_list_displays_columns` | — |  |
| `pos_settings/test_pos_list.py::test_pos_list_pagination_shows_count` | — |  |
| `pos_settings/test_pos_list.py::test_pos_list_results_per_page` | — |  |
| `pos_settings/test_pos_list.py::test_pos_list_status_column` | — |  |
| `pos_settings/test_pos_list.py::test_pos_page_loads` | — | 🔥 |
| `pos_settings/test_pos_middleware_settings.py::test_middleware_ip_accepts_valid_url` | — |  |
| `pos_settings/test_pos_middleware_settings.py::test_middleware_ip_persists` | — |  |
| `pos_settings/test_pos_middleware_settings.py::test_middleware_ip_required` | — |  |
| `pos_settings/test_pos_search.py::test_search_by_exact_name` | — |  |
| `pos_settings/test_pos_search.py::test_search_by_partial_name` | — |  |
| `pos_settings/test_pos_search.py::test_search_clear_restores_list` | — |  |
| `pos_settings/test_pos_search.py::test_search_nonmatching_shows_empty` | — |  |
| `pos_settings/test_pos_service_settings.py::test_restore_default_settings` | — |  |
| `pos_settings/test_pos_service_settings.py::test_service_tab_switches_view` | — | 🔥 |
| `pos_settings/test_pos_tunnel_settings.py::test_car_roller_output_required` | — |  |
| `pos_settings/test_pos_tunnel_settings.py::test_controller_id_required` | — |  |
| `pos_settings/test_pos_tunnel_settings.py::test_send_invoice_toggle_saves` | — |  |
| `pos_settings/test_pos_tunnel_settings.py::test_tunnel_operational_toggle_saves` | — |  |

</details>

**Pending — 16 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_active_pos_toggle_off_saves` (test_pos_active.py) | — | ⏭️ skip | Manual - Check later for fixes: active POS toggle uses role='switch' heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_allow_checkout_no_customer` (test_pos_create.py) | — | ⏭️ skip | Manual - Check later for fixes: allow checkout combobox locator uses label heuristics — verify exact React Select element in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_active_pos_saves` (test_pos_create.py) | — | ⚠️ xfail | Site and Lane dropdowns depend on Sites & Locations data — verify POS_SITE and POS_LANE exist in staging before removing xfail. | Needs guaranteed staging data (managed record) |
| `test_create_inactive_pos` (test_pos_create.py) | POS-CRT-007 | ⚠️ xfail | POS-CRT-007: staging server saves POS as Active regardless of the Inactive selection on the create form. Same app bug as WP-CRT inactive. | Possible product bug — confirm with product |
| `test_site_dropdown_from_sites_locations` (test_pos_dependencies.py) | — | ⏭️ skip | Manual - Check later for fixes: site combobox locator uses positional heuristics — verify exact React Select element in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_device_section_expand_collapse` (test_pos_device_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: device settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_activate_inactive_pos` (test_pos_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: after deactivating, re-opening edit form requires inactive POS to be visible — verify default filter beha… | Manual test |
| `test_deactivate_active_pos` (test_pos_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: active toggle locator uses heuristics — verify aria-checked in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_allow_checkout_persists` (test_pos_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: allow checkout combobox locator uses label heuristics — verify exact React Select element in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_edit_lane_persists` (test_pos_edit.py) | — | ⚠️ xfail | Site and Lane dropdowns depend on Sites & Locations data — verify POS_SITE and POS_LANE exist in staging. | Needs guaranteed staging data (managed record) |
| `test_middleware_section_expand_collapse` (test_pos_middleware_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: middleware settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_car_roller_output_persists` (test_pos_tunnel_settings.py) | POS-TUN-010 | ⏭️ skip | POS-TUN-010: Car/roller output dropdown options are unknown — inspect DevTools for valid option text before removing xfail. | Case-by-case (see reason) |
| `test_controller_id_saves_persists` (test_pos_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: tunnel settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_controller_ip_valid_format_saves` (test_pos_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: tunnel settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_tunnel_controller_ip_required` (test_pos_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: tunnel settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_tunnel_section_expand_collapse` (test_pos_tunnel_settings.py) | — | ⏭️ skip | Manual - Check later for fixes: tunnel settings section locators use heuristics; needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |

Next actions for this module: Rewrite locator (label/section heuristics don't match current DOM) ×11; Needs guaranteed staging data (managed record) ×2; Possible product bug — confirm with product ×1; Manual test ×1; Case-by-case (see reason) ×1

### redemptions

<details><summary>✅ Covered — 74 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_all_sections_refresh_on_filter_change[RDM-SUM-003-date]` | RDM-SUM-003 |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_all_sections_refresh_on_filter_change[RDM-SUM-003-site]` | RDM-SUM-003 |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_header_visible[sec-comp-washes]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_header_visible[sec-gift-cards]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_header_visible[sec-loyalty-points]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_header_visible[sec-memberships]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_header_visible[sec-wash-books]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_name_in_header[sec-comp-washes]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_name_in_header[sec-gift-cards]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_name_in_header[sec-loyalty-points]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_name_in_header[sec-memberships]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_name_in_header[sec-wash-books]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_pagination_present[sec-comp-washes]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_pagination_present[sec-gift-cards]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_pagination_present[sec-loyalty-points]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_pagination_present[sec-memberships]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_pagination_present[sec-wash-books]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_zero_data_state[sec-comp-washes]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_zero_data_state[sec-gift-cards]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_zero_data_state[sec-loyalty-points]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_zero_data_state[sec-memberships]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsAccordionShared::test_section_zero_data_state[sec-wash-books]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsCompWashes::test_comp_washes_summary_cards` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_calendar_date_range_sets_field` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_date_preset_count` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_date_preset_dropdown_options` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_date_range_field_shows_dates` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_future_dates_disabled_in_calendar` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_clears_custom_date_range` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-002]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-003]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-004]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-005]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-006]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_preset_populates_date_range[RDM-DTE-007]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_selecting_preset_fills_date_range` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_single_day_checkbox_visible` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_single_day_mode_changes_date_field` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsDateFilter::test_zero_data_date_range_state` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsExpandCollapse::test_collapse_all_hides_all_sections` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsExpandCollapse::test_summary_cards_visible_without_expanding` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsGiftCards::test_gift_cards_summary_cards` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsLoyalty::test_loyalty_summary_cards` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsMemberships::test_memberships_summary_cards` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_filter_modal_auto_opens` | — | 🔥 |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_filter_values_reflected_in_page_bar` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_modal_contains_all_controls` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_modal_opens_with_no_default_site` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_page_bar_changes_do_not_navigate_away` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_page_content_visible_after_apply` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsNav::test_page_loads_at_correct_url` | — | 🔥 |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_clear_all_sites` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_multi_site_selection_accepted` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_no_default_site_selected` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_page_bar_site_change_does_not_reopen_modal` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_page_bar_site_change_no_modal` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_rdm_site_present_in_dropdown` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_removing_chip_reduces_site_filter` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_selecting_site_creates_chip` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_single_site_scopes_data` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_site_dropdown_lists_multiple_sites` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_site_dropdown_uses_multiselect` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSiteFilter::test_sites_dropdown_lists_active_sites` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSummaryCards::test_all_summary_cards_visible` | — | 🔥 |
| `redemptions/test_redemptions.py::TestRedemptionsSummaryCards::test_summary_card_currency_format[RDM-SUM-004-01]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSummaryCards::test_summary_card_currency_format[RDM-SUM-004-02]` | — |  |
| `redemptions/test_redemptions.py::TestRedemptionsSummaryCards::test_total_redemptions_card_visible` | — | 🔥 |
| `redemptions/test_redemptions.py::TestRedemptionsWashBooks::test_wash_books_summary_cards` | — |  |
| `redemptions/test_redemptions.py::TestSingleDaySync::test_modal_sdm_syncs_to_page_bar` | — |  |
| `redemptions/test_redemptions.py::TestSingleDaySync::test_modal_single_day_changes_date_field` | — |  |
| `redemptions/test_redemptions.py::TestSingleDaySync::test_modal_single_day_checkbox_visible` | — |  |
| `redemptions/test_redemptions.py::TestSingleDaySync::test_page_bar_sdm_uncheck_syncs_to_modal` | — |  |
| `redemptions/test_redemptions_ui.py::test_redemptions_filter_modal_has_site_and_date_controls` | — |  |
| `redemptions/test_redemptions_ui.py::test_redemptions_page_loads_and_modal_opens` | — |  |

</details>

**Pending — 29 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsAccordionShared` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsCompWashes` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: _find_table_by_heading() blocked by accordion DOM structure gap — needs DevTools inspection of table head… | Manual test |
| `TestRedemptionsCompWashes` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection of ex… | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsExpandCollapse` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsGiftCards` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: _find_table_by_heading() blocked by accordion DOM structure gap — needs DevTools inspection of table head… | Manual test |
| `TestRedemptionsGiftCards` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsLoyalty` (test_redemptions.py) | RDM-LOY-002 | ⚠️ xfail | Copy defect RDM-LOY-002: breakdown titled 'Redemptions by Wash Package' but columns are Points Range / Count / Percentage — title does no… | Case-by-case (see reason) |
| `TestRedemptionsLoyalty` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: _find_table_by_heading() blocked by accordion DOM structure gap — needs DevTools inspection of table head… | Manual test |
| `TestRedemptionsMemberships` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: _find_table_by_heading() blocked by accordion DOM structure gap — needs DevTools inspection of table head… | Manual test |
| `TestRedemptionsMemberships` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |
| `TestRedemptionsNav` (test_redemptions.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `TestRedemptionsWashBooks` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: _find_table_by_heading() blocked by accordion DOM structure gap — needs DevTools inspection of table head… | Manual test |
| `TestRedemptionsWashBooks` (test_redemptions.py) | — | ⏭️ skip | Manual - Check later for fixes: section_body_visible() heuristic doesn't match actual RDM accordion DOM — needs DevTools inspection. | Rewrite locator (label/section heuristics don't match current DOM) |

Next actions for this module: Rewrite locator (label/section heuristics don't match current DOM) ×22; Manual test ×5; Case-by-case (see reason) ×1; Re-check now — deferred as staging data / intermittent ×1

### revenue_overview

<details><summary>✅ Covered — 77 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `revenue_overview/test_revenue_overview.py::TestSingleDayMode::test_select_date_in_single_day_mode` | — |  |
| `revenue_overview/test_revenue_overview.py::TestSingleDayMode::test_single_day_changes_label_and_field` | — |  |
| `revenue_overview/test_revenue_overview.py::TestSingleDayMode::test_uncheck_single_day_reverts_to_range` | — |  |
| `revenue_overview/test_revenue_overview.py::test_all_membership_subtabs_clickable` | — |  |
| `revenue_overview/test_revenue_overview.py::test_changing_preset_auto_updates_date_range` | — |  |
| `revenue_overview/test_revenue_overview.py::test_chart_renders_when_data_exists` | — | 🔥 |
| `revenue_overview/test_revenue_overview.py::test_chart_rerenders_on_filter_change` | — |  |
| `revenue_overview/test_revenue_overview.py::test_chart_shows_no_info_when_no_data` | — |  |
| `revenue_overview/test_revenue_overview.py::test_clearing_sites_shows_empty_state` | — |  |
| `revenue_overview/test_revenue_overview.py::test_custom_range_same_start_end` | — |  |
| `revenue_overview/test_revenue_overview.py::test_custom_range_switches_preset_to_custom` | — |  |
| `revenue_overview/test_revenue_overview.py::test_date_preset_auto_applies_on_metrics_screen` | — |  |
| `revenue_overview/test_revenue_overview.py::test_date_range_field_opens_calendar_picker` | — |  |
| `revenue_overview/test_revenue_overview.py::test_deactivated_sites_not_in_dropdown` | — |  |
| `revenue_overview/test_revenue_overview.py::test_deselecting_option_removes_it` | — |  |
| `revenue_overview/test_revenue_overview.py::test_direct_url_opens_filter_modal` | — |  |
| `revenue_overview/test_revenue_overview.py::test_each_row_shows_four_data_points` | — |  |
| `revenue_overview/test_revenue_overview.py::test_export_button_present` | — |  |
| `revenue_overview/test_revenue_overview.py::test_export_triggers_download` | — |  |
| `revenue_overview/test_revenue_overview.py::test_filter_modal_auto_opens` | — |  |
| `revenue_overview/test_revenue_overview.py::test_filter_values_reflected_in_page_level_bar` | — |  |
| `revenue_overview/test_revenue_overview.py::test_five_kpi_cards_render` | — | 🔥 |
| `revenue_overview/test_revenue_overview.py::test_hover_segment_shows_tooltip` | — |  |
| `revenue_overview/test_revenue_overview.py::test_hover_updates_centre_label` | — |  |
| `revenue_overview/test_revenue_overview.py::test_info_icon_tooltip_text` | — |  |
| `revenue_overview/test_revenue_overview.py::test_kpi_cards_show_zero_when_no_data` | — |  |
| `revenue_overview/test_revenue_overview.py::test_kpi_values_currency_format` | — |  |
| `revenue_overview/test_revenue_overview.py::test_kpi_values_update_on_date_change` | — |  |
| `revenue_overview/test_revenue_overview.py::test_legend_lists_all_series` | — |  |
| `revenue_overview/test_revenue_overview.py::test_list_refreshes_on_filter_change` | — |  |
| `revenue_overview/test_revenue_overview.py::test_long_names_truncate_without_breaking` | — |  |
| `revenue_overview/test_revenue_overview.py::test_membership_count_invariant` | — |  |
| `revenue_overview/test_revenue_overview.py::test_membership_plan_names_match_module` | — |  |
| `revenue_overview/test_revenue_overview.py::test_membership_tab_displayed_with_count` | — |  |
| `revenue_overview/test_revenue_overview.py::test_membership_tab_selected_by_default` | — |  |
| `revenue_overview/test_revenue_overview.py::test_membership_tab_shows_three_subtabs` | — |  |
| `revenue_overview/test_revenue_overview.py::test_metrics_shell_renders_behind_modal` | — |  |
| `revenue_overview/test_revenue_overview.py::test_modal_contains_all_controls` | — |  |
| `revenue_overview/test_revenue_overview.py::test_modal_does_not_reopen_from_page_level_bar` | — |  |
| `revenue_overview/test_revenue_overview.py::test_modal_opens_with_default_state` | — |  |
| `revenue_overview/test_revenue_overview.py::test_month_boundary_date_range` | — |  |
| `revenue_overview/test_revenue_overview.py::test_new_sales_subtab_lists_plans` | — |  |
| `revenue_overview/test_revenue_overview.py::test_overflow_counter_chip_shown_for_many_sites` | — |  |
| `revenue_overview/test_revenue_overview.py::test_page_level_preset_lists_seven_options` | — |  |
| `revenue_overview/test_revenue_overview.py::test_page_loads_at_correct_url` | — | 🔥 |
| `revenue_overview/test_revenue_overview.py::test_page_title_and_info_icon_render` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-002]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-003]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-004]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-005]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-006]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-007]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_preset_updates_range_and_data[RVO-DTE-008]` | — |  |
| `revenue_overview/test_revenue_overview.py::test_rapid_preset_switching_no_stale_data` | — |  |
| `revenue_overview/test_revenue_overview.py::test_rapid_site_toggle_no_stale_data` | — |  |
| `revenue_overview/test_revenue_overview.py::test_recharges_subtab_zero_count_renders_cleanly` | — |  |
| `revenue_overview/test_revenue_overview.py::test_resignups_subtab_lists_rows` | — |  |
| `revenue_overview/test_revenue_overview.py::test_retail_only_site_renders_cleanly` | — |  |
| `revenue_overview/test_revenue_overview.py::test_retail_tab_displayed_with_count` | — |  |
| `revenue_overview/test_revenue_overview.py::test_retail_tab_empty_list_when_count_zero` | — |  |
| `revenue_overview/test_revenue_overview.py::test_segment_colours_are_stable` | — |  |
| `revenue_overview/test_revenue_overview.py::test_selected_sites_render_as_chips` | — |  |
| `revenue_overview/test_revenue_overview.py::test_selecting_multiple_sites_aggregates_revenue` | — |  |
| `revenue_overview/test_revenue_overview.py::test_selecting_single_site_scopes_all_sections` | — | 🔥 |
| `revenue_overview/test_revenue_overview.py::test_sidebar_highlights_active_item` | — |  |
| `revenue_overview/test_revenue_overview.py::test_single_day_checkbox_switches_to_single_date` | — |  |
| `revenue_overview/test_revenue_overview.py::test_single_item_count_grammar` | — |  |
| `revenue_overview/test_revenue_overview.py::test_site_change_auto_applies_no_apply_button` | — |  |
| `revenue_overview/test_revenue_overview.py::test_sites_dropdown_reflects_sites_module` | — |  |
| `revenue_overview/test_revenue_overview.py::test_switching_subtabs_does_not_change_kpi_or_chart` | — |  |
| `revenue_overview/test_revenue_overview.py::test_switching_tabs_preserves_kpi_and_chart` | — |  |
| `revenue_overview/test_revenue_overview.py::test_today_with_no_transactions_renders_cleanly` | — |  |
| `revenue_overview/test_revenue_overview.py::test_tooltip_content_is_static` | — |  |
| `revenue_overview/test_revenue_overview.py::test_tooltip_dismisses_on_click_away` | — |  |
| `revenue_overview/test_revenue_overview.py::test_zero_amount_shows_zero_percent` | — |  |
| `revenue_overview/test_revenue_overview.py::test_zero_revenue_series_in_legend_no_arc` | — |  |
| `revenue_overview/test_revenue_overview.py::test_zero_transaction_site_renders_cleanly` | — |  |

</details>

**Pending — 23 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestSingleDayMode` (test_revenue_overview.py) | RVO-DTE-014 | ⚠️ xfail | RVO-DTE-014: Page does not auto-switch preset to 'Custom' when Single day is checked; preset retains its previous value (e.g. 'Today') | Case-by-case (see reason) |
| `test_apply_filters_closes_modal_and_renders_metrics` (test_revenue_overview.py) | — | 🟡 xfail/passing | ElementNotInteractableException in select_site; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `test_centre_label_not_recalculated_after_legend_toggle` (test_revenue_overview.py) | RVO-CHT-010 | ⚠️ xfail | RVO-CHT-010: Known product behaviour — centre label does not update after legend toggle. Remove xfail when product fixes this. | Case-by-case (see reason) |
| `test_centre_label_resets_on_pointer_leave` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: centre label reset on pointer-leave is chart-library specific — verify in DevTools. | Manual test |
| `test_clear_control_removes_all_chips` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: clear-all button locator uses class heuristics (overview__site-select__clear-indicator) — verify in DevTo… | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_date_preset_dropdown_lists_seven_options` (test_revenue_overview.py) | RVO-FMD-002 | 🟡 xfail/passing | RVO-FMD-002: Date preset dropdown intermittently returns no options; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `test_future_dates_disabled_in_calendar` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: disabled future-date detection relies on aria-disabled/class heuristics — verify calendar day button DOM … | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_hiding_all_legend_series_no_error` (test_revenue_overview.py) | RVO-CHT-012 | ⚠️ xfail | RVO-CHT-012: StaleElementReferenceException intermittently when clicking legend items in sequence on staging. | Case-by-case (see reason) |
| `test_kpi_values_update_on_site_change` (test_revenue_overview.py) | — | 🟡 xfail/passing | Staging data: membership tab count inconsistent with new-sales tab count | **Promote** — passed in last full run; remove xfail |
| `test_legend_toggle_hides_segment` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: legend toggle effect on canvas is not DOM-observable — verify aria-pressed/class attribute in DevTools. | Manual test |
| `test_overview_full_report_link_navigates_here` (test_revenue_overview.py) | RVO-DEP-001 | ⚠️ xfail | RVO-DEP-001: Overview page content is inside an iframe; 'Full report' link not findable from outer frame context | Case-by-case (see reason) |
| `test_page_level_sites_dropdown_lists_all_sites` (test_revenue_overview.py) | RVO-SIT-001 | 🟡 xfail/passing | RVO-SIT-001: Page-level site dropdown returns only pre-selected site; same timing race as modal site dropdown (options not fully populate… | **Promote** — passed in last full run; remove xfail |
| `test_retail_count_invariant` (test_revenue_overview.py) | — | 🟡 xfail/passing | Retail count invariant fails when staging has uncategorized retail items not mapped to Wash Package or Wash Extra. | **Promote** — passed in last full run; remove xfail |
| `test_retail_tab_shows_two_subtabs` (test_revenue_overview.py) | RVO-RET-002 | ⚠️ xfail | RVO-RET-002: Retail section uses a flat product list ('Wash Prepaid'); 'Wash Package'/'Wash Extra' subtabs not present on current page | Case-by-case (see reason) |
| `test_selected_options_highlighted_in_dropdown` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: selected-state highlight uses class heuristics (overview__site-select__option--is-selected) — verify in D… | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_site_dropdown_scrolls_for_many_sites` (test_revenue_overview.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_sites_dropdown_lists_all_active_sites` (test_revenue_overview.py) | — | 🟡 xfail/passing | Site dropdown intermittently returns empty on staging; timing race during modal open. | **Promote** — passed in last full run; remove xfail |
| `test_subtab_row_count_equals_badge` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: row count depends on breakdown list DOM structure — verify list-item locator in DevTools. | Manual test |
| `test_wash_extra_names_match_module` (test_revenue_overview.py) | — | ⚠️ xfail | Wash Extra sub-tab not clickable when no Wash Extra retail data exists in staging for the selected date range. | Case-by-case (see reason) |
| `test_wash_extra_subtab_lists_extras` (test_revenue_overview.py) | — | ⚠️ xfail | Wash Extra sub-tab not clickable when no Wash Extra retail data exists in staging for the selected date range. | Case-by-case (see reason) |
| `test_wash_package_names_match_module` (test_revenue_overview.py) | — | ⚠️ xfail | Wash Package sub-tab not clickable when no Wash Package retail data exists in staging for the selected date range. | Case-by-case (see reason) |
| `test_wash_package_subtab_lists_packages` (test_revenue_overview.py) | — | ⚠️ xfail | Wash Package sub-tab not clickable when no Wash Package retail data exists in staging for the selected date range. | Case-by-case (see reason) |
| `test_year_selector_visible_in_calendar` (test_revenue_overview.py) | — | ⏭️ skip | Manual - Check later for fixes: year selector detection uses class/role heuristics — verify calendar year control DOM in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |

Next actions for this module: Case-by-case (see reason) ×9; **Promote** — passed in last full run; remove xfail ×6; Rewrite locator (label/section heuristics don't match current DOM) ×4; Manual test ×3; Re-check now — deferred as staging data / intermittent ×1

### service_categories

<details><summary>✅ Covered — 15 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `service_categories/test_service_categories_edge_cases.py::test_cancel_add_new_does_not_create_category` | — |  |
| `service_categories/test_service_categories_edge_cases.py::test_service_category_long_name_does_not_break_form` | — |  |
| `service_categories/test_service_categories_filter.py::test_export_button_is_clickable` | — |  |
| `service_categories/test_service_categories_filter.py::test_filter_active_categories_shows_active` | — | 🔥 |
| `service_categories/test_service_categories_filter.py::test_reset_active_filter_restores_full_grid` | — |  |
| `service_categories/test_service_categories_negative.py::test_create_category_exceeding_max_length` | — |  |
| `service_categories/test_service_categories_negative.py::test_create_category_with_whitespace_name` | — |  |
| `service_categories/test_service_categories_negative.py::test_create_duplicate_category_is_blocked` | — |  |
| `service_categories/test_service_categories_negative.py::test_missing_service_category_is_not_returned` | — |  |
| `service_categories/test_service_categories_negative.py::test_service_category_required_name_validation` | — |  |
| `service_categories/test_service_categories_search_filter.py::test_service_categories_special_character_search_stays_usable` | — |  |
| `service_categories/test_service_categories_ui.py::test_add_service_category_form_controls` | — | 🔥 |
| `service_categories/test_service_categories_ui.py::test_service_categories_list_shell_controls_and_grid` | — | 🔥 |
| `service_categories/test_service_categories_validation.py::test_service_category_blank_required_form_stays_on_form` | — |  |
| `service_categories/test_service_categories_validation.py::test_service_category_required_name_validation` | — | 🔥 |

</details>

**Pending — 21 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_category_available_assigning_services` (test_service_categories_dependency.py) | — | ⏭️ skip | Services module not yet automated. Deferred. | Deferred — re-check scope |
| `test_category_available_in_discount_creation` (test_service_categories_dependency.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_deactivate_category_used_by_discount` (test_service_categories_dependency.py) | — | ⏭️ skip | Needs controlled discount data linked to a specific service category. Deferred until single-module SC coverage is solid. | Deferred — re-check scope |
| `test_rename_category_linked_to_discount` (test_service_categories_dependency.py) | — | ⏭️ skip | Needs a stable cross-module fixture that links a specific category to a discount. Deferred until single-module SC coverage is solid. | Needs cross-module fixtures |
| `test_rename_category_with_assigned_services` (test_service_categories_dependency.py) | — | ⏭️ skip | Services module not yet automated. Deferred. | Deferred — re-check scope |
| `test_activate_deactivate_activate_cycle` (test_service_categories_edge_cases.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_cancel_edit_does_not_save_changes` (test_service_categories_edge_cases.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_deactivated_category_findable_via_filter` (test_service_categories_edge_cases.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_edit_inactive_category_saves_changes` (test_service_categories_edge_cases.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_edit_service_category_name_and_restore` (test_service_categories_edit.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_filter_inactive_categories_shows_inactive` (test_service_categories_filter.py) | — | 🟡 xfail/passing | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | **Promote** — passed in last full run; remove xfail |
| `test_managed_category_provided_at_baseline` (test_service_categories_managed.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_managed_category_rename_is_reset_on_teardown` (test_service_categories_managed.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_create_service_category_is_idempotent` (test_service_categories_negative.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_activate_service_category` (test_service_categories_positive.py) | — | ⏭️ skip | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_create_active_service_category` (test_service_categories_positive.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_create_inactive_service_category` (test_service_categories_positive.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_deactivate_service_category` (test_service_categories_positive.py) | — | ⏭️ skip | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_edit_service_category_name` (test_service_categories_positive.py) | — | ⏭️ skip | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_service_category_settings_persist` (test_service_categories_positive.py) | — | 🟡 xfail/passing | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | **Promote** — passed in last full run; remove xfail |
| `test_service_categories_search_variants_and_clear` (test_service_categories_search_filter.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |

Next actions for this module: Re-check — save/return-to-list fixes may resolve ×9; Re-check now — deferred as staging data / intermittent ×6; Deferred — re-check scope ×3; **Promote** — passed in last full run; remove xfail ×2; Needs cross-module fixtures ×1

### sites

<details><summary>✅ Covered — 40 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `sites/test_sites_edge_cases.py::test_create_site_form_handles_random_address_value` | — |  |
| `sites/test_sites_edge_cases.py::test_create_site_long_site_name_does_not_break_ui` | — |  |
| `sites/test_sites_edge_cases.py::test_sites_list_handles_refresh` | — |  |
| `sites/test_sites_edit.py::test_cancel_edit_does_not_save` | — |  |
| `sites/test_sites_edit.py::test_edit_site_cc_input_fields_are_displayed` | — |  |
| `sites/test_sites_edit.py::test_edit_site_cc_processor_labels_visible` | — |  |
| `sites/test_sites_edit.py::test_edit_site_contact_email_persists_after_refresh` | — |  |
| `sites/test_sites_edit.py::test_edit_site_credit_card_tab_accessible` | — | 🔥 |
| `sites/test_sites_edit.py::test_edit_site_customer_portal_tab_accessible` | — |  |
| `sites/test_sites_edit.py::test_edit_site_form_prepopulates` | — |  |
| `sites/test_sites_edit.py::test_edit_site_lanes_settings_tab_accessible` | — | 🔥 |
| `sites/test_sites_edit.py::test_edit_site_tax_settings_persist` | — |  |
| `sites/test_sites_export.py::test_sites_export_button_clickable` | — |  |
| `sites/test_sites_negative.py::test_create_site_cancel_does_not_save_record` | — |  |
| `sites/test_sites_negative.py::test_create_site_duplicate_site_name_or_code_is_rejected` | — |  |
| `sites/test_sites_positive.py::test_create_inactive_site_hidden_from_list` | — |  |
| `sites/test_sites_positive.py::test_create_new_site_with_required_general_settings` | — | 🔥 |
| `sites/test_sites_positive.py::test_create_site_with_zero_tax_rates` | — |  |
| `sites/test_sites_positive.py::test_created_site_persists_after_refresh` | — |  |
| `sites/test_sites_search_filter.py::test_sites_filter_active_toggle_off_shows_all` | — |  |
| `sites/test_sites_search_filter.py::test_sites_filter_active_toggle_on_shows_active_only` | — |  |
| `sites/test_sites_search_filter.py::test_sites_filter_by_existing_site_name` | — |  |
| `sites/test_sites_search_filter.py::test_sites_filter_by_missing_site_name_shows_no_match` | — |  |
| `sites/test_sites_search_filter.py::test_sites_filter_by_name_and_active_combined` | — |  |
| `sites/test_sites_search_filter.py::test_sites_reset_filter_restores_list` | — |  |
| `sites/test_sites_ui.py::test_create_site_cancel_returns_to_list` | — |  |
| `sites/test_sites_ui.py::test_create_site_general_settings_ui_elements` | — |  |
| `sites/test_sites_ui.py::test_sites_filter_panel_ui_elements` | — | 🔥 |
| `sites/test_sites_ui.py::test_sites_locations_page_ui_elements` | — | 🔥 |
| `sites/test_sites_validation.py::test_create_site_blank_name_with_complete_form_blocks_save` | — |  |
| `sites/test_sites_validation.py::test_create_site_missing_address_blocks_save` | — |  |
| `sites/test_sites_validation.py::test_create_site_special_chars_in_name_do_not_break_form` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_blocks_empty_required_fields` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[city_sales_tax--1]` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[city_sales_tax-101]` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[city_sales_tax-abc]` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[state_sales_tax--1]` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[state_sales_tax-101]` | — |  |
| `sites/test_sites_validation.py::test_create_site_validation_invalid_tax_values[state_sales_tax-abc]` | — |  |
| `sites/test_sites_validation.py::test_create_site_very_long_name_does_not_crash_form` | — |  |

</details>

**Pending — 26 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_active_site_in_customers_assign_dropdown` (test_sites_dependency.py) | — | ⏭️ skip | Requires cross-module navigation fixtures (Services / Customers). Deferred until module-level fixtures are available. | Needs cross-module fixtures |
| `test_active_site_in_services_dropdowns` (test_sites_dependency.py) | — | ⏭️ skip | Requires cross-module navigation fixtures (Services / Customers). Deferred until module-level fixtures are available. | Needs cross-module fixtures |
| `test_customer_portal_toggle_controls_ecommerce_listing` (test_sites_dependency.py) | — | ⏭️ skip | Requires cross-module navigation fixtures (Services / Customers). Deferred until module-level fixtures are available. | Needs cross-module fixtures |
| `test_deactivated_site_removed_from_dropdowns` (test_sites_dependency.py) | — | ⏭️ skip | Requires deactivating the test site and verifying dropdown removal across multiple modules. Deferred to avoid leaving the shared fixture … | Deferred — re-check scope |
| `test_lane_count_in_list_matches_saved_lanes` (test_sites_dependency.py) | — | ⏭️ skip | Requires lane creation via EditSitePage Lanes tab. Deferred. | Deferred — re-check scope |
| `test_pay_api_token_gates_card_saving` (test_sites_dependency.py) | — | ⏭️ skip | Requires cross-module navigation fixtures (Services / Customers). Deferred until module-level fixtures are available. | Needs cross-module fixtures |
| `test_site_tax_rates_visible_in_service_assignment` (test_sites_dependency.py) | — | ⏭️ skip | Requires cross-module navigation fixtures (Services / Customers). Deferred until module-level fixtures are available. | Needs cross-module fixtures |
| `test_activate_site_shows_in_list` (test_sites_edit.py) | — | ⚠️ xfail | Intermittent TimeoutException opening edit form; verify manually. | Manual test |
| `test_add_lane_creates_visible_row` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: lane row locator needs DOM verification | Manual test |
| `test_add_lane_persists` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: lane locator needs DOM verification against Lanes settings tab | Manual test |
| `test_add_multiple_lanes_succeeds` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: lane row locator needs DOM verification | Manual test |
| `test_deactivate_site_hides_from_list` (test_sites_edit.py) | — | ⚠️ xfail | Intermittent TimeoutException opening edit form; verify manually. | Manual test |
| `test_edit_site_customer_portal_gift_cards_toggle` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: CP toggle locator needs exact checkbox DOM verification | Manual test |
| `test_edit_site_customer_portal_memberships_toggle` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: CP toggle locator needs exact checkbox DOM verification | Manual test |
| `test_edit_site_customer_portal_settings_persist` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: depends on CP toggle locators not yet verified | Manual test |
| `test_edit_site_customer_portal_show_toggle` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: CP toggle locator needs exact checkbox DOM verification | Manual test |
| `test_edit_site_customer_portal_washbooks_toggle` (test_sites_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: CP toggle locator needs exact checkbox DOM verification | Manual test |
| `test_edit_site_name_persists` (test_sites_edit.py) | — | ⏭️ skip | Manual check required — the site name field in the edit form does not respond reliably to automated input (React-controlled input require… | Manual test |
| `test_remove_lane_persists` (test_sites_edit.py) | — | ⏭️ skip | Requires a lane-row delete locator (e.g. a remove/trash button per lane row). Implement once the Lanes settings DOM is inspected. | Confirm locator on staging, then implement |
| `test_sites_export_file_content` (test_sites_export.py) | — | ⏭️ skip | Manual - Check later for fixes: needs download-dir config and CSV parser to validate export | Needs downloaded-file verification |
| `test_created_site_shows_state_and_city_in_list` (test_sites_positive.py) | — | ⚠️ xfail | Managed site created via API lacks UI-sourced state/city; filter also returns 0 on staging. Verify manually. | Manual test |
| `test_site_count_increments_after_create` (test_sites_positive.py) | — | 🟡 xfail/passing | Count stays cached in same sites_page object after creation; page needs re-navigation to reflect new count. Verify manually. | **Promote** — passed in last full run; remove xfail |
| `test_sites_filter_by_partial_site_name` (test_sites_search_filter.py) | — | ⚠️ xfail | Partial name filter returns 0 results on staging; verify manually. | Manual test |
| `test_create_site_validation_invalid_email_formats[abc@]` (test_sites_validation.py) | — | 🟡 xfail/passing | Site create form appears to accept invalid email formats (abc@, abc, abc@yopmail). Investigate product-side email validation before un-xf… | **Promote** — passed in last full run; remove xfail |
| `test_create_site_validation_invalid_email_formats[abc@yopmail]` (test_sites_validation.py) | — | 🟡 xfail/passing | Site create form appears to accept invalid email formats (abc@, abc, abc@yopmail). Investigate product-side email validation before un-xf… | **Promote** — passed in last full run; remove xfail |
| `test_create_site_validation_invalid_email_formats[abc]` (test_sites_validation.py) | — | 🟡 xfail/passing | Site create form appears to accept invalid email formats (abc@, abc, abc@yopmail). Investigate product-side email validation before un-xf… | **Promote** — passed in last full run; remove xfail |

Next actions for this module: Manual test ×13; Needs cross-module fixtures ×5; **Promote** — passed in last full run; remove xfail ×4; Deferred — re-check scope ×2; Confirm locator on staging, then implement ×1; Needs downloaded-file verification ×1

### transactions

<details><summary>✅ Covered — 82 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_custom_date_range_input_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_date_location_tab_opens` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_date_preset_option_present[TRN-DLC-002-This month]` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_date_preset_option_present[TRN-DLC-002-This week]` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_date_preset_option_present[TRN-DLC-002-Today]` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_lane_filter_state[TRN-DLC-008]` | TRN-DLC-008 |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_lane_filter_state[TRN-DLC-009]` | TRN-DLC-008 |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_multi_site_shows_overflow_chip` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_selecting_site_scopes_data` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_site_multiselect_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsDateLocation::test_this_week_starts_on_monday` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_action_buttons_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_back_navigation_from_detail` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_car_details_panel_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_customer_name_matches` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_customer_panel_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_detail_page_loads` | — | 🔥 |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_invoice_number_matches` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_service_table_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsDetailPage::test_transaction_details_panel_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsExport::test_export_button_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsExport::test_export_format_selector` | — |  |
| `transactions/test_transactions.py::TestTransactionsExport::test_export_modal_opens` | — | 🔥 |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_apply_filters_button_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_apply_filters_closes_panel_and_updates` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_panel_can_be_reopened` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_panel_opens` | — | 🔥 |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_panel_structure` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Customer]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Date & Location]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Gift cards]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Invoice]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Membership]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Payment]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Promotions]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Staff]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Transaction]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_filter_tab_present[TRN-FLT-003-Washbook]` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_live_results_count_updates` | — |  |
| `transactions/test_transactions.py::TestTransactionsFilterPanel::test_x_button_closes_panel_without_applying` | — |  |
| `transactions/test_transactions.py::TestTransactionsNav::test_export_icon_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsNav::test_filter_by_button_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsNav::test_page_loads_at_expected_url` | — | 🔥 |
| `transactions/test_transactions.py::TestTransactionsNav::test_page_title_visible` | — |  |
| `transactions/test_transactions.py::TestTransactionsPaymentFilter::test_cc_type_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsPaymentFilter::test_payment_method_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsPaymentFilter::test_payment_status_multiselect_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsPaymentFilter::test_payment_tab_opens` | — |  |
| `transactions/test_transactions.py::TestTransactionsQuickFilters::test_quick_filter_updates_state[TRN-QCK-001]` | TRN-QCK-001 |  |
| `transactions/test_transactions.py::TestTransactionsQuickFilters::test_quick_filter_updates_state[TRN-QCK-002]` | TRN-QCK-001 |  |
| `transactions/test_transactions.py::TestTransactionsQuickFilters::test_quick_filter_updates_state[TRN-QCK-003]` | TRN-QCK-001 |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-CC type]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Customer name]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Discount]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Invoice number]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-License plate]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-PIF]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Payment mode]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Payment status]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-RFID]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Sale Type]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Service]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Site name]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Surcharge]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Tax]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Total amount]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Transaction date/time]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Transaction source0]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_column_header_present[TRN-TBL-001-Transaction source1]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_default_date_preset_is_today` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_pagination_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_record_count_displayed` | — |  |
| `transactions/test_transactions.py::TestTransactionsTable::test_table_has_horizontal_scroll` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_category_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_sale_type_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_sale_type_option_present[TRN-TXN-006-Gift Card Sale]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_sale_type_option_present[TRN-TXN-006-Membership Sale]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_sale_type_option_present[TRN-TXN-006-Retail / Single Wash]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_sale_type_option_present[TRN-TXN-006-Washbook Sale]` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_services_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_transaction_source_dropdown_present` | — |  |
| `transactions/test_transactions.py::TestTransactionsTransactionFilter::test_transaction_tab_opens` | — |  |

</details>

**Pending — 39 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestTransactionsDateLocation` (test_transactions.py) | — | ⚠️ xfail | Known product gap: quick date preset not present in filter panel (only Today, This week, This month are available). | Fix date preset dropdown interaction |
| `TestTransactionsDateLocation` (test_transactions.py) | — | ⚠️ xfail | Known product gap: quick date preset not present in filter panel (only Today, This week, This month are available). | Fix date preset dropdown interaction |
| `TestTransactionsDateLocation` (test_transactions.py) | — | ⚠️ xfail | Known product gap: quick date preset not present in filter panel (only Today, This week, This month are available). | Fix date preset dropdown interaction |
| `TestTransactionsDateLocation` (test_transactions.py) | — | ⚠️ xfail | Known product gap: quick date preset not present in filter panel (only Today, This week, This month are available). | Fix date preset dropdown interaction |
| `TestTransactionsDetailPage` (test_transactions.py) | — | ⚠️ xfail | Known defect: payment type field displays 'CreditCard **** null' instead of the actual card details.  Passes once defect is fixed in back… | Case-by-case (see reason) |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: depends on export column toggle locator (same blocker as EXP-003). Verify manually: open Export modal → confirm Lane name, Image … | Manual test |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: export column toggles use a custom React component whose DOM structure is unresolved — get_export_column_toggle_labels() returns … | Needs helper for custom React toggle component |
| `TestTransactionsExport` (test_transactions.py) | — | ⏭️ skip | Manual: depends on export column toggle locator (same blocker as EXP-003). Verify manually: open Export modal → confirm 'Site name' appea… | Manual test |
| `TestTransactionsFilterPanel` (test_transactions.py) | TRN-FLT-007 | ⚠️ xfail | TRN-FLT-007: reset_panel_filters locator or quick-filter label detection unverified in CI. Deferred. | Deferred — re-check scope |
| `TestTransactionsRowInteraction` (test_transactions.py) | TRN-SEL-002 | ⚠️ xfail | TRN-SEL-002/TRN-TBL-008: cascades from empty table (TRN-TBL-002). Deferred. | Deferred — re-check scope |
| `TestTransactionsRowInteraction` (test_transactions.py) | TRN-SEL-002 | ⚠️ xfail | TRN-SEL-002/TRN-TBL-008: cascades from empty table (TRN-TBL-002). Deferred. | Deferred — re-check scope |
| `TestTransactionsRowInteraction` (test_transactions.py) | — | ⏭️ skip | Not a product feature: row highlight is not implemented. Navigation to detail is via the invoice number (opens new tab). | Case-by-case (see reason) |
| `TestTransactionsTable` (test_transactions.py) | TRN-TBL-007 | ⚠️ xfail | TRN-TBL-007: cascades from empty table (TRN-TBL-002). Deferred. | Deferred — re-check scope |
| `TestTransactionsTable` (test_transactions.py) | TRN-TBL-006 | ⚠️ xfail | TRN-TBL-006: cascades from empty table (TRN-TBL-002). Deferred. | Deferred — re-check scope |
| `TestTransactionsTable` (test_transactions.py) | TRN-TBL-002 | ⚠️ xfail | TRN-TBL-002: 'Last month' preset returns 0 rows on staging — date preset locator or staging data gap. Deferred. | Fix date preset dropdown interaction |

Next actions for this module: Needs helper for custom React toggle component ×25; Fix date preset dropdown interaction ×5; Deferred — re-check scope ×5; Case-by-case (see reason) ×2; Manual test ×2

### tunnel_settings

<details><summary>✅ Covered — 26 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `tunnel_settings/test_tunnel_active.py::test_active_configuration_toggle_saves[TUN-ACT-001]` | — | 🔥 |
| `tunnel_settings/test_tunnel_active.py::test_status_badge_color_reflects_state` | — |  |
| `tunnel_settings/test_tunnel_behavior.py::test_behavior_default_sequence_stacking` | — |  |
| `tunnel_settings/test_tunnel_behavior.py::test_behavior_radio_mutual_exclusivity` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_add_tunnel_button_opens_form` | — | 🔥 |
| `tunnel_settings/test_tunnel_create.py::test_behavior_defaults_to_sequence_stacking` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_create_tunnel_full_save` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_create_tunnel_required_fields_only` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_new_tunnel_appears_immediately` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_required_field_validation[TUN-VAL-001]` | — | 🔥 |
| `tunnel_settings/test_tunnel_create.py::test_required_field_validation[TUN-VAL-002]` | — | 🔥 |
| `tunnel_settings/test_tunnel_create.py::test_required_field_validation[TUN-VAL-003]` | — | 🔥 |
| `tunnel_settings/test_tunnel_create.py::test_required_fields_marked_with_asterisk` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_site_dropdown_lists_active_sites` | — |  |
| `tunnel_settings/test_tunnel_create.py::test_three_sections_present_on_create_form` | — |  |
| `tunnel_settings/test_tunnel_retract_settings.py::test_multiple_retract_rows_added` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Active-tunnel-configuration]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Auto-send]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Automatic-Car-Selection]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[MOXA-auto-send]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Prompt-RFID-entry]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Show-car-count]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Skip-prompt-on-send-car]` | — |  |
| `tunnel_settings/test_tunnel_toggles.py::test_toggle_defaults_on_create_form[Skip-retract-confirmation-dialog]` | — |  |
| `tunnel_settings/test_tunnel_ui.py::test_tunnel_settings_grid_columns_are_visible` | — |  |
| `tunnel_settings/test_tunnel_ui.py::test_tunnel_settings_page_loads_with_primary_controls` | — |  |

</details>

**Pending — 20 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_active_configuration_toggle_saves[TUN-ACT-002]` (test_tunnel_active.py) | TUN-ACT-002 | ⚠️ xfail | TUN-ACT-002: setting Active=False appears to hide the tunnel from the list (list may filter to active tunnels only); wait_for_tunnel_row … | Case-by-case (see reason) |
| `test_behavior_radio_persists` (test_tunnel_behavior.py) | TUN-BHV-004 | ⚠️ xfail | TUN-BHV-004: staging app does not persist the non-default behavior radio selection; re-opening the form always shows the default value. | Possible product bug — confirm with product |
| `test_cancel_discards_form_returns_to_list` (test_tunnel_create.py) | TUN-CRT-008 | 🟡 xfail/passing | TUN-CRT-008 fails in full suite runs (47+ min) when the staging session expires mid-run. Passes in isolation. Fix: increase session TTL o… | **Promote** — passed in last full run; remove xfail |
| `test_retract_row_lifecycle` (test_tunnel_retract_settings.py) | TUN-RTR-004 | ⚠️ xfail | TUN-RTR-004: select_retract_service JS-clicks the React Select option which does not fire onChange — service value is not registered in f… | Case-by-case (see reason) |
| `test_retract_row_numbering_reflects_order` (test_tunnel_retract_settings.py) | TUN-RTR-012 | ⏭️ skip | TUN-RTR-012: managed_tunnel fixture leaves filter state that blocks tunnel row lookup at setup — deferred | Deferred — re-check scope |
| `test_controller_id_dropdown_lists_options` (test_tunnel_settings_section.py) | TUN-TSN-004 | ⚠️ xfail | TUN-TSN-004: Controller ID dropdown is absent from the form. Actual form body text shows no Controller ID field in any section. CONTROLLE… | Confirm locator on staging, then implement |
| `test_controller_id_label_spelled_correctly` (test_tunnel_settings_section.py) | TUN-TSN-006 | ⚠️ xfail | Copy defect TUN-TSN-006: label reads 'Select controler ID' and placeholder reads 'Tunnel controler ID' — missing second l in controller | Case-by-case (see reason) |
| `test_controller_id_selection_persists` (test_tunnel_settings_section.py) | TUN-TSN-005 | ⚠️ xfail | TUN-TSN-005: Controller ID dropdown is absent from the form — same root cause as TUN-TSN-004. select_controller_id() will time out. Pendi… | Case-by-case (see reason) |
| `test_tunnel_operational_toggle_persists[TUN-TSN-002]` (test_tunnel_settings_section.py) | TUN-TSN-002 | ⚠️ xfail | TUN-TSN-002/003: 'Tunnel operational' toggle is absent from the form. Actual form structure (confirmed from body text) shows the 'Tunnel … | Confirm locator on staging, then implement |
| `test_tunnel_operational_toggle_persists[TUN-TSN-003]` (test_tunnel_settings_section.py) | TUN-TSN-002 | ⚠️ xfail | TUN-TSN-002/003: 'Tunnel operational' toggle is absent from the form. Actual form structure (confirmed from body text) shows the 'Tunnel … | Confirm locator on staging, then implement |
| `test_tunnel_settings_section_expand_collapse` (test_tunnel_settings_section.py) | — | ⏭️ skip | Manual - Check later for fixes: section_is_expanded proxy uses missing locator, needs DevTools verification | Manual test |
| `test_toggle_saves_and_persists[TUN-TGL-001]` (test_tunnel_toggles.py) | — | ⚠️ xfail | Staging app does not persist the OFF state for this toggle; the value resets to True on save. Needs product investigation. | Possible product bug — confirm with product |
| `test_toggle_saves_and_persists[TUN-TGL-002]` (test_tunnel_toggles.py) | — | ⚠️ xfail | Staging app does not persist the OFF state for this toggle; the value resets to True on save. Needs product investigation. | Possible product bug — confirm with product |
| `test_toggle_saves_and_persists[TUN-TGL-003]` (test_tunnel_toggles.py) | — | ⚠️ xfail | Staging app does not persist the OFF state for this toggle; the value resets to True on save. Needs product investigation. | Possible product bug — confirm with product |
| `test_toggle_saves_and_persists[TUN-TGL-004]` (test_tunnel_toggles.py) | — | ⏭️ skip | CI-SKIP: managed_tunnel_form fixture fails in headless CI. Fix: decouple frame switch from form fixture setup. | Case-by-case (see reason) |
| `test_toggle_saves_and_persists[TUN-TGL-005]` (test_tunnel_toggles.py) | — | ⏭️ skip | CI-SKIP: managed_tunnel_form fixture fails in headless CI. Fix: decouple frame switch from form fixture setup. | Case-by-case (see reason) |
| `test_toggle_saves_and_persists[TUN-TGL-006]` (test_tunnel_toggles.py) | — | ⚠️ xfail | Staging app does not persist the OFF state for this toggle; the value resets to True on save. Needs product investigation. | Possible product bug — confirm with product |
| `test_toggle_saves_and_persists[TUN-TGL-007]` (test_tunnel_toggles.py) | — | ⏭️ skip | CI-SKIP: managed_tunnel_form fixture fails in headless CI. Fix: decouple frame switch from form fixture setup. | Case-by-case (see reason) |
| `test_toggle_saves_and_persists[TUN-TGL-008]` (test_tunnel_toggles.py) | TUN-TGL-008 | ⚠️ xfail | TUN-TGL-008: setting Active=False hides the tunnel from the list (list filters to active tunnels only); open_edit_tunnel_form cannot navi… | Case-by-case (see reason) |
| `test_toggle_states_reflected_on_reopen` (test_tunnel_toggles.py) | TUN-TGL-010 | ⚠️ xfail | TUN-TGL-010: staging app does not persist toggle OFF states; re-open shows values reset to True regardless of saved state. | Possible product bug — confirm with product |

Next actions for this module: Case-by-case (see reason) ×8; Possible product bug — confirm with product ×6; Confirm locator on staging, then implement ×3; **Promote** — passed in last full run; remove xfail ×1; Deferred — re-check scope ×1; Manual test ×1

### user_roles

<details><summary>✅ Covered — 29 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `user_roles/test_user_roles_create.py::test_create_active_user_role` | — |  |
| `user_roles/test_user_roles_create.py::test_create_duplicate_role_rejected` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_cancel_discards` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_name_max_length_saves` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_name_required` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_name_whitespace_trimmed_or_rejected` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_priority_integers_only` | — |  |
| `user_roles/test_user_roles_create.py::test_create_role_priority_required` | — |  |
| `user_roles/test_user_roles_create.py::test_create_vk_company_user_role` | — |  |
| `user_roles/test_user_roles_create.py::test_newly_created_role_appears_immediately` | — |  |
| `user_roles/test_user_roles_create.py::test_user_roles_add_form_opens` | — | 🔥 |
| `user_roles/test_user_roles_edge_cases.py::test_case_sensitivity_duplicate` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_data_persists_after_logout_relogin` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_duplicate_name_vs_inactive_role` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_duplicate_priority_documents_behavior` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_predefined_name_edit_guard` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_predefined_role_fields_editable` | — |  |
| `user_roles/test_user_roles_edge_cases.py::test_priority_zero_documents_behavior` | — |  |
| `user_roles/test_user_roles_filter.py::test_user_roles_filter_by_site` | — |  |
| `user_roles/test_user_roles_filter.py::test_user_roles_filter_count_matches_rows` | — |  |
| `user_roles/test_user_roles_filter.py::test_user_roles_filter_panel_opens` | — | 🔥 |
| `user_roles/test_user_roles_list.py::test_user_roles_default_roles_present` | — | 🔥 |
| `user_roles/test_user_roles_list.py::test_user_roles_list_page_loads` | — | 🔥 |
| `user_roles/test_user_roles_list.py::test_user_roles_list_required_columns` | — |  |
| `user_roles/test_user_roles_list.py::test_user_roles_pagination_count` | — |  |
| `user_roles/test_user_roles_search.py::test_user_roles_clear_search_restores_list` | — |  |
| `user_roles/test_user_roles_search.py::test_user_roles_search_nonexistent_shows_empty` | — |  |
| `user_roles/test_user_roles_ui.py::test_user_roles_grid_columns_are_visible` | — |  |
| `user_roles/test_user_roles_ui.py::test_user_roles_page_loads_with_primary_controls` | — |  |

</details>

**Pending — 43 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_create_inactive_user_role` (test_user_roles_create.py) | UR-CRT-003 | 🟡 xfail/passing | UR-CRT-003: staging server saves user role as Active regardless of the Inactive selection on the create form. Same app bug as WP-TGL-002 … | **Promote** — passed in last full run; remove xfail |
| `test_deactivate_assigned_role_documents_behavior` (test_user_roles_edge_cases.py) | — | ⚠️ xfail | Filter state instability leaves 0 rows on staging | Re-check with data-arrival waits |
| `test_deactivate_label_correct_terminology` (test_user_roles_edge_cases.py) | — | ⚠️ xfail | Filter state instability leaves 0 rows on staging | Re-check with data-arrival waits |
| `test_activate_inactive_role` (test_user_roles_edit.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_deactivate_active_role` (test_user_roles_edit.py) | UR-EDT-005 | ⏭️ skip | CI-SKIP UR-EDT-005: managed_role fixture fails in headless CI. Fix: same as WP-FRM-001. | Case-by-case (see reason) |
| `test_edit_role_cancel_discards` (test_user_roles_edit.py) | — | ⚠️ xfail | Filter state instability leaves 0 rows on staging | Re-check with data-arrival waits |
| `test_edit_role_name_persists` (test_user_roles_edit.py) | — | ⏭️ skip | manual check: React controlled input send_keys fix applied, pending clean CI verification | Manual test |
| `test_edit_role_name_required` (test_user_roles_edit.py) | — | ⚠️ xfail | Filter state instability leaves 0 rows on staging | Re-check with data-arrival waits |
| `test_edit_role_priority_persists` (test_user_roles_edit.py) | — | ⏭️ skip | manual check: React controlled input send_keys fix applied, pending clean CI verification | Manual test |
| `test_user_roles_edit_form_opens` (test_user_roles_edit.py) | UR-EDT-001 | ⏭️ skip | CI-SKIP UR-EDT-001: managed_role fixture fails in headless CI. Fix: same as WP-FRM-001 — decouple fixture from Inovua grid interaction. | Case-by-case (see reason) |
| `test_user_roles_export_button_clickable` (test_user_roles_export.py) | — | ⏭️ skip | Manual - Check later for fixes: export button locator label needs DevTools verification | Manual test |
| `test_user_roles_filter_active_shows_active_only` (test_user_roles_filter.py) | UR-FLT-002 | ⏭️ skip | CI-SKIP UR-FLT-002: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_user_roles_filter_combined_site_and_active` (test_user_roles_filter.py) | UR-FLT-006 | ⏭️ skip | CI-SKIP UR-FLT-006: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_user_roles_filter_off_shows_all` (test_user_roles_filter.py) | UR-FLT-003 | ⏭️ skip | CI-SKIP UR-FLT-003: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_user_roles_reset_all_clears_filters` (test_user_roles_filter.py) | — | ⚠️ xfail | Manual check: StaleElementReferenceException on Reset All — native click races React re-render | Manual test |
| `test_user_roles_site_filter_alphabetical` (test_user_roles_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: option locator may capture other dropdowns, needs DevTools verification | Manual test |
| `test_user_roles_rows_per_page_changes_display` (test_user_roles_list.py) | — | ⏭️ skip | Manual - Check later for fixes: rows-per-page control locator needs DevTools verification | Manual test |
| `test_assign_multiple_locations_persist` (test_user_roles_locations.py) | UR-LOC-002 | ⏭️ skip | CI-SKIP UR-LOC-002: Location checkbox locator has not been verified against the live DOM. Re-enable once _location_checkbox() locator is … | Confirm locator on staging, then implement |
| `test_assign_single_location_persists` (test_user_roles_locations.py) | UR-LOC-001 | ⏭️ skip | CI-SKIP UR-LOC-001: Location checkbox locator uses a speculative ancestor walk that has not been verified against the live DOM. Re-enable… | Rewrite locator (speculative JS anchors) |
| `test_location_list_includes_configured_sites` (test_user_roles_locations.py) | UR-LOC-004 | ⏭️ skip | CI-SKIP UR-LOC-004: get_location_names() uses a broad ancestor-walk that has not been verified against the live DOM. Re-enable once locat… | Confirm locator on staging, then implement |
| `test_remove_location_persists` (test_user_roles_locations.py) | UR-LOC-003 | ⏭️ skip | CI-SKIP UR-LOC-003: Location checkbox locator has not been verified against the live DOM. Re-enable once _location_checkbox() locator is … | Confirm locator on staging, then implement |
| `test_all_permissions_off_saves_ok` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_child_toggle_independent` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_expand_permission_section_reveals_toggles` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_parent_toggle_off_disables_all_children` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_parent_toggle_on_enables_all_children` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_permission_sections_collapsed_by_default` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_permissions_persist_after_save` (test_user_roles_permissions.py) | — | ⏭️ skip | CI-SKIP UR-PRM: Permission accordion locators use a speculative JS ancestor-walk that has not been verified against the live DOM. Re-enab… | Rewrite locator (speculative JS anchors) |
| `test_user_roles_search_exact_name` (test_user_roles_search.py) | UR-SRH-001 | ⏭️ skip | CI-SKIP UR-SRH-001: create_role_if_missing times out in headless CI. Fix: same as CS-CRT-001. | Case-by-case (see reason) |
| `test_user_roles_search_partial_name` (test_user_roles_search.py) | — | ⏭️ skip | Manual - Check later for fixes: create_role_if_missing cannot reliably activate inactive role | Manual test |
| `test_section_permissions_persist_after_save[Customers]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Employees]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Gas_Pump_Settings]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Kiosk_App]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Kiosk_Settings]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[POS_App]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[POS_Settings]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Reports]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Services]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Sites]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Tunnel_Settings]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[User_Roles]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |
| `test_section_permissions_persist_after_save[Users]` (test_user_roles_section_permissions.py) | UR-PRM-008 | ⏭️ skip | CI-SKIP UR-PRM-008..023: Section permission locators use a speculative JS ancestor-walk that has not been verified against the live DOM. … | Rewrite locator (speculative JS anchors) |

Next actions for this module: Rewrite locator (speculative JS anchors) ×21; Manual test ×7; Case-by-case (see reason) ×6; Re-check with data-arrival waits ×4; Confirm locator on staging, then implement ×3; **Promote** — passed in last full run; remove xfail ×1; Re-check now — deferred as staging data / intermittent ×1

### users

<details><summary>✅ Covered — 39 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `users/test_users_create.py::test_create_user_cancel_discards_form` | — |  |
| `users/test_users_create.py::test_create_user_duplicate_email_rejected` | — |  |
| `users/test_users_create.py::test_create_user_employee_required` | — |  |
| `users/test_users_create.py::test_create_user_invalid_email_rejected` | — |  |
| `users/test_users_create.py::test_users_add_form_opens` | — | 🔥 |
| `users/test_users_edge_cases.py::test_email_whitespace_trimmed_or_rejected` | — |  |
| `users/test_users_edge_cases.py::test_filter_panel_accessible_for_name_email_lookup` | — |  |
| `users/test_users_edge_cases.py::test_long_email_at_boundary` | — |  |
| `users/test_users_edge_cases.py::test_user_data_persists_after_relogin` | — |  |
| `users/test_users_edit.py::test_edit_user_cancel_discards_changes` | — |  |
| `users/test_users_edit.py::test_edit_user_email_persists` | — |  |
| `users/test_users_edit.py::test_edit_user_email_required` | — |  |
| `users/test_users_edit.py::test_edit_user_invalid_email_blocked` | — |  |
| `users/test_users_edit.py::test_edit_user_phone_persists` | — |  |
| `users/test_users_edit.py::test_edit_user_phone_required` | — |  |
| `users/test_users_edit.py::test_edit_user_role_persists` | — |  |
| `users/test_users_edit.py::test_users_edit_form_opens` | — | 🔥 |
| `users/test_users_export.py::test_users_export_button_clickable` | — |  |
| `users/test_users_filter.py::test_users_filter_active_off_shows_all` | — |  |
| `users/test_users_filter.py::test_users_filter_active_only` | — |  |
| `users/test_users_filter.py::test_users_filter_by_email` | — |  |
| `users/test_users_filter.py::test_users_filter_by_site` | — |  |
| `users/test_users_filter.py::test_users_filter_combined_name_and_site` | — |  |
| `users/test_users_filter.py::test_users_filter_panel_opens` | — | 🔥 |
| `users/test_users_filter.py::test_users_filter_partial_name_matches` | — |  |
| `users/test_users_filter.py::test_users_filter_reset_all` | — |  |
| `users/test_users_filter.py::test_users_filter_result_count_matches_rows` | — |  |
| `users/test_users_list.py::test_users_list_page_loads` | — | 🔥 |
| `users/test_users_list.py::test_users_list_pagination_count` | — |  |
| `users/test_users_list.py::test_users_list_required_columns` | — |  |
| `users/test_users_list.py::test_users_list_rows_per_page` | — |  |
| `users/test_users_password.py::test_change_password_button_opens_flow` | — |  |
| `users/test_users_password.py::test_change_password_matching_passwords_save` | — |  |
| `users/test_users_search.py::test_users_search_clear_restores_list` | — |  |
| `users/test_users_search.py::test_users_search_exact_phone` | — |  |
| `users/test_users_search.py::test_users_search_nonexistent_phone_shows_empty` | — |  |
| `users/test_users_search.py::test_users_search_partial_phone` | — |  |
| `users/test_users_ui.py::test_users_grid_columns_are_visible` | — |  |
| `users/test_users_ui.py::test_users_page_loads_with_primary_controls` | — |  |

</details>

**Pending — 29 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_create_active_user` (test_users_create.py) | USR-CRT-002 | ⏭️ skip | Manual — USR-CRT-002: Create active user flow verified manually in staging. | Manual test |
| `test_create_inactive_user` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_confirm_password_required` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_confirm_password_visibility_toggle` (test_users_create.py) | — | ⏭️ skip | Manual - Check later for fixes: confirm eye-icon locator uses class heuristics, needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_user_email_required` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_employee_dropdown_lists_employees` (test_users_create.py) | — | ⏭️ skip | Manual - Check later for fixes: employee combobox locator uses label heuristics, needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_user_password_mismatch` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_password_required` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_password_visibility_toggle` (test_users_create.py) | — | ⏭️ skip | Manual - Check later for fixes: eye-icon locator uses class heuristics, needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_user_phone_required` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_create_user_role_dropdown_lists_roles` (test_users_create.py) | — | ⏭️ skip | Manual - Check later for fixes: role combobox locator uses label heuristics, needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_create_user_role_required` (test_users_create.py) | — | ⏭️ skip | staging data: employee 'test user 3' not seeded — deferred | Seed staging data (managed record) |
| `test_new_user_appears_immediately` (test_users_create.py) | USR-CRT-020 | ⏭️ skip | Manual — USR-CRT-020: New user visibility in list verified manually in staging. | Manual test |
| `test_employee_dropdown_reflects_employees_module` (test_users_dependency.py) | — | ⏭️ skip | Manual - Check later for fixes: employee combobox locator uses label heuristics, needs DevTools verification | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_filter_sites_match_sites_and_locations_module` (test_users_dependency.py) | — | ⏭️ skip | Manual - Check later for fixes: option locator may capture other dropdowns, needs verification | Manual test |
| `test_new_role_appears_in_users_dropdown` (test_users_dependency.py) | — | ⏭️ skip | Manual - Check later for fixes: role combobox locator needs DevTools verification | Manual test |
| `test_only_active_employees_in_dropdown` (test_users_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: employee combobox locator needs DevTools verification | Manual test |
| `test_only_active_roles_in_dropdown` (test_users_edge_cases.py) | — | ⏭️ skip | Manual - Check later for fixes: role combobox locator needs DevTools verification | Manual test |
| `test_activate_inactive_user` (test_users_edit.py) | USR-EDT-006 | ⏭️ skip | Manual — USR-EDT-006: Activate/deactivate toggle flow verified manually in staging. | Manual test |
| `test_deactivate_active_user` (test_users_edit.py) | USR-EDT-007 | ⚠️ xfail | USR-EDT-007: staging server saves user as Active regardless of the Inactive toggle on the edit form. Same app bug as WP-TGL-002 / POS-CRT… | Possible product bug — confirm with product |
| `test_edit_user_employee_persists` (test_users_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: combobox locator and second employee availability need DevTools verification. | Manual test |
| `test_edit_user_no_password_fields` (test_users_edit.py) | — | ⏭️ skip | Manual - Check later for fixes: password_fields_absent() uses name-based heuristics — verify exact form structure in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_users_filter_by_employee_code` (test_users_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter field locators use name/label heuristics — verify exact field names in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_users_filter_by_first_name` (test_users_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter field locators use name/label heuristics — verify exact field names in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_users_filter_by_last_name` (test_users_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: filter field locators use name/label heuristics — verify exact field names in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_users_filter_site_dropdown_lists_sites` (test_users_filter.py) | — | ⏭️ skip | Manual - Check later for fixes: site option locator may capture other dropdown options — verify in DevTools. | Manual test |
| `test_change_password_blank_blocked` (test_users_password.py) | — | ⏭️ skip | Manual - Check later for fixes: password change flow locators use name heuristics — verify DOM in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_change_password_mismatch_rejected` (test_users_password.py) | — | ⏭️ skip | Manual - Check later for fixes: password change flow locators use name heuristics — verify DOM in DevTools. | Rewrite locator (label/section heuristics don't match current DOM) |
| `test_change_password_visibility_toggles` (test_users_password.py) | — | ⏭️ skip | Manual - Check later for fixes: visibility toggle locators need DOM verification. | Manual test |

Next actions for this module: Rewrite locator (label/section heuristics don't match current DOM) ×11; Manual test ×10; Seed staging data (managed record) ×7; Possible product bug — confirm with product ×1

### wash_activity

<details><summary>✅ Covered — 46 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `wash_activity/test_wash_activity.py::TestSingleDaySync::test_modal_sdm_syncs_to_page_bar` | — |  |
| `wash_activity/test_wash_activity.py::TestSingleDaySync::test_modal_single_day_changes_date_field` | — |  |
| `wash_activity/test_wash_activity.py::TestSingleDaySync::test_modal_single_day_checkbox_visible` | — |  |
| `wash_activity/test_wash_activity.py::TestSingleDaySync::test_page_bar_sdm_uncheck_syncs_to_modal` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityChart::test_chart_empty_state_for_zero_data` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityChart::test_chart_legend_toggle_off` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityChart::test_chart_section_visible` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityCompWashes::test_comp_washes_breakdown_cards_present` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityCompWashes::test_comp_washes_empty_state` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityCompWashes::test_comp_washes_tab_matches_kpi` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityDateFilter::test_selecting_preset_fills_date_range` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityDateFilter::test_single_day_checkbox_in_modal` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityDateFilter::test_single_day_field_narrows_to_one_date` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityDateFilter::test_zero_data_state` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_sublabels[WAC-KPI-008]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_sublabels[WAC-KPI-009]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_sublabels[WAC-KPI-010]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-01]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-02]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-03]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-04]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-05]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_card_visible[WAC-KPI-001-06]` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_total_cars_equals_sum` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_values_non_zero` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityKPI::test_kpi_zero_data_state` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityMemberships::test_memberships_breakdown_cards_present` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityMemberships::test_memberships_empty_state` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityMemberships::test_memberships_tab_matches_total_redemptions_kpi` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityNav::test_filter_modal_auto_opens` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityNav::test_filter_values_reflected_in_page_bar` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityNav::test_modal_contains_all_controls` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityNav::test_page_bar_changes_do_not_reopen_modal` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityNav::test_page_loads_at_correct_url` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivitySiteFilter::test_chip_x_and_clear_returns_empty_state` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivitySiteFilter::test_clear_all_sites` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivitySiteFilter::test_removing_chip_reduces_site_filter` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivitySiteFilter::test_selecting_site_creates_chip` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivitySiteFilter::test_site_filter_empty_by_default` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_all_three_tabs_visible` | — | 🔥 |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_default_active_tab_is_memberships` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_empty_tab_clean_state[WAC-TAB-007-cmp]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_empty_tab_clean_state[WAC-TAB-007-mem]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_tab_switching[WAC-TAB-004-cmp]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_tab_switching[WAC-TAB-004-mem]` | — |  |
| `wash_activity/test_wash_activity.py::TestWashActivityTabs::test_tab_switching[WAC-TAB-004-pws]` | — |  |

</details>

**Pending — 37 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `TestWashActivityChart` (test_wash_activity.py) | — | ⏭️ skip | MANUAL CHECK: SVG bar element selector needs DevTools verification against live DOM | Manual test |
| `TestWashActivityChart` (test_wash_activity.py) | — | ⚠️ xfail | StaleElementReferenceException in legend toggle methods on staging. | Case-by-case (see reason) |
| `TestWashActivityChart` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException intermittently in chart section methods on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-008 | 🟡 xfail/passing | WAC-DTE-008: Date preset dropdown intermittently returns empty options; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | Date preset dropdown intermittently returns empty on staging; timing race during modal open. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-012 | ⚠️ xfail | WAC-DTE-012: Date range input may not populate within wait window; staging date preset rendering is intermittently slow. | Fix date preset dropdown interaction |
| `TestWashActivityDateFilter` (test_wash_activity.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | WAC-DTE-005 | 🟡 xfail/passing | WAC-DTE-005/007 TimeoutException intermittently; date range field slow to populate on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | ElementNotInteractableException for kpi widget intermittently after date preset change on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | ElementNotInteractableException for kpi widget intermittently after date preset change on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityDateFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | ElementNotInteractableException for kpi widget intermittently after date preset change on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityExport` (test_wash_activity.py) | — | 🟡 xfail/passing | TimeoutException: export button not found within wait on slow staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityExport` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException in click_export_xlsx() intermittently on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityKPI` (test_wash_activity.py) | WAC-KPI-006 | ⚠️ xfail | WAC-KPI-006: Daily Average KPI returns 0 even when Total Cars > 0 — product defect | Case-by-case (see reason) |
| `TestWashActivityKPI` (test_wash_activity.py) | WAC-KPI-007 | ⚠️ xfail | Defect WAC-KPI-007: Hourly Average displays 0 despite Total Cars=9 — formula not computing. See also WAC-KPI-005, WAC-KPI-011. | Case-by-case (see reason) |
| `TestWashActivityKPI` (test_wash_activity.py) | WAC-KPI-011 | 🟡 xfail/passing | Defect WAC-KPI-011: Total Paid KPI=9 vs Paid Washes tab=11 — count mismatch. Same root cause as WAC-KPI-005, WAC-PWS-006. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityNav` (test_wash_activity.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `TestWashActivityNav` (test_wash_activity.py) | WAC-NAV-004 | 🟡 xfail/passing | WAC-NAV-004: wac_page fixture intermittently raises StaleElementReferenceException during filter application on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityPaidWashes` (test_wash_activity.py) | — | ⏭️ skip | MANUAL CHECK: Breakdown card package names and DOM structure need DevTools verification | Manual test |
| `TestWashActivityPaidWashes` (test_wash_activity.py) | — | ⚠️ xfail | TimeoutException in click_tab/get_tab_count intermittently on staging. | Case-by-case (see reason) |
| `TestWashActivityPaidWashes` (test_wash_activity.py) | WAC-PWS-006 | 🟡 xfail/passing | Defect WAC-PWS-006: Paid Washes tab=11 vs Total Paid KPI=9 — count mismatch with same root cause as WAC-KPI-011. See also WAC-KPI-005. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | WAC-SIT-004 | 🟡 xfail/passing | WAC-SIT-004b: Site selection loop intermittently fails; select_site timing race when iterating all options on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | WAC-SIT-011 | 🟡 xfail/passing | WAC-SIT-011: StaleElementReferenceException intermittently in select_site() when called from the page-bar on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | WAC-SIT-005 | 🟡 xfail/passing | WAC-SIT-005: wac_page fixture intermittently raises StaleElementReferenceException during filter application on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | WAC-SIT-012 | 🟡 xfail/passing | WAC-SIT-012: Site dropdown intermittently returns only one option; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | WAC-SIT-001 | 🟡 xfail/passing | WAC-SIT-001: Site dropdown intermittently returns empty; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | Site dropdown intermittently returns empty; timing race during modal open on staging. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException intermittently when calling select_site() in test body after wac_page fixture. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException intermittently when calling select_site() in test body after wac_page fixture. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivitySiteFilter` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException intermittently when calling select_site() in test body after wac_page fixture. | **Promote** — passed in last full run; remove xfail |
| `TestWashActivityTabs` (test_wash_activity.py) | — | 🟡 xfail/passing | StaleElementReferenceException in usage_breakdown_visible() intermittently on staging. | **Promote** — passed in last full run; remove xfail |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×27; Case-by-case (see reason) ×4; Re-check now — deferred as staging data / intermittent ×3; Manual test ×2; Fix date preset dropdown interaction ×1

### wash_books

<details><summary>✅ Covered — 64 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `wash_books/test_customer_wash_books_dependency.py::test_cwb_washes_reflect_template_wash_book` | — |  |
| `wash_books/test_customer_wash_books_dependency.py::test_only_active_wash_books_in_cwb_dropdown` | — |  |
| `wash_books/test_customer_wash_books_edge_cases.py::test_cwb_customer_search_requires_two_characters` | — |  |
| `wash_books/test_customer_wash_books_edit.py::test_activate_customer_wash_book` | — |  |
| `wash_books/test_customer_wash_books_edit.py::test_deactivate_customer_wash_book` | — |  |
| `wash_books/test_customer_wash_books_edit.py::test_edit_cwb_number_of_washes_persists` | — |  |
| `wash_books/test_customer_wash_books_negative.py::test_create_cwb_blank_number_of_washes_blocked` | — |  |
| `wash_books/test_customer_wash_books_negative.py::test_create_cwb_blank_wash_book_number_blocked` | — |  |
| `wash_books/test_customer_wash_books_negative.py::test_create_cwb_blank_wash_book_selection_blocked` | — | 🔥 |
| `wash_books/test_customer_wash_books_negative.py::test_create_cwb_duplicate_number_rejected` | — |  |
| `wash_books/test_customer_wash_books_positive.py::test_create_customer_wash_book` | — |  |
| `wash_books/test_customer_wash_books_search_filter.py::test_cwb_filter_by_site_narrows_results` | — |  |
| `wash_books/test_customer_wash_books_search_filter.py::test_cwb_filter_reset_all_restores_list` | — |  |
| `wash_books/test_customer_wash_books_search_filter.py::test_cwb_search_by_exact_number` | — |  |
| `wash_books/test_customer_wash_books_search_filter.py::test_cwb_search_by_partial_number` | — |  |
| `wash_books/test_customer_wash_books_search_filter.py::test_cwb_search_non_existing_number_shows_empty_state` | — |  |
| `wash_books/test_customer_wash_books_ui.py::test_customer_wash_books_grid_columns_are_visible` | — |  |
| `wash_books/test_customer_wash_books_ui.py::test_customer_wash_books_tab_loads_with_controls` | — | 🔥 |
| `wash_books/test_wash_books_edge_cases.py::test_wash_book_long_description_does_not_break_form` | — |  |
| `wash_books/test_wash_books_edit.py::test_activate_wash_book` | — | 🔥 |
| `wash_books/test_wash_books_edit.py::test_deactivate_wash_book` | — |  |
| `wash_books/test_wash_books_edit.py::test_edit_wash_book_description` | — |  |
| `wash_books/test_wash_books_edit.py::test_edit_wash_book_global_commission_persists` | — |  |
| `wash_books/test_wash_books_edit.py::test_edit_wash_book_global_price_persists` | — |  |
| `wash_books/test_wash_books_edit.py::test_edit_wash_book_name_persists` | — |  |
| `wash_books/test_wash_books_edit.py::test_edit_wash_book_number_of_washes_persists` | — |  |
| `wash_books/test_wash_books_negative.py::test_duplicate_wash_book_name_is_blocked` | — |  |
| `wash_books/test_wash_books_negative.py::test_negative_global_commission_is_rejected` | — |  |
| `wash_books/test_wash_books_negative.py::test_negative_global_price_is_rejected` | — |  |
| `wash_books/test_wash_books_negative.py::test_negative_number_of_washes_is_rejected` | — |  |
| `wash_books/test_wash_books_negative.py::test_wash_books_special_character_search_stays_usable` | — |  |
| `wash_books/test_wash_books_negative.py::test_whitespace_only_wash_book_name_is_rejected` | — |  |
| `wash_books/test_wash_books_positive.py::test_create_inactive_wash_book` | — |  |
| `wash_books/test_wash_books_positive.py::test_create_wash_book` | — |  |
| `wash_books/test_wash_books_positive.py::test_customer_portal_switch_is_off_by_default` | — |  |
| `wash_books/test_wash_books_positive.py::test_wash_book_decimal_price_accepted` | — | 🔥 |
| `wash_books/test_wash_books_positive.py::test_wash_book_save_without_loyalty_points_succeeds` | — |  |
| `wash_books/test_wash_books_positive.py::test_wash_book_zero_loyalty_points_accepted` | — |  |
| `wash_books/test_wash_books_redemption.py::test_redemption_at_site_with_wash_package_persists` | — |  |
| `wash_books/test_wash_books_redemption.py::test_redemption_site_without_wash_package_behaviour` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_clear_search_restores_list` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_existing_search` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_filter_by_site_narrows_results` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_filter_panel_shows_controls` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_filter_reset_all_restores_list` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_missing_search` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_partial_search_returns_matches` | — |  |
| `wash_books/test_wash_books_search_filter.py::test_wash_books_search_payloads_do_not_break_grid` | — |  |
| `wash_books/test_wash_books_site_assignment.py::test_location_price_override_persists` | — |  |
| `wash_books/test_wash_books_site_assignment.py::test_save_wash_book_with_no_site_assigned` | — |  |
| `wash_books/test_wash_books_ui.py::test_add_wash_book_form_loads` | — |  |
| `wash_books/test_wash_books_ui.py::test_customer_wash_books_tab_is_accessible` | — |  |
| `wash_books/test_wash_books_ui.py::test_wash_books_grid_columns_are_visible` | — |  |
| `wash_books/test_wash_books_ui.py::test_wash_books_page_loads_with_primary_controls` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_blank_global_price_is_blocked` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_blank_required_form_stays_on_form` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_invalid_numeric_values_do_not_break_form` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_max_length_name_handled` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_required_name_validation` | — | 🔥 |
| `wash_books/test_wash_books_validation.py::test_wash_book_save_without_commission_succeeds` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_valid_commission_saves` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_valid_number_of_washes_saves` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_zero_price_boundary_behaviour` | — |  |
| `wash_books/test_wash_books_validation.py::test_wash_book_zero_washes_boundary_behaviour` | — |  |

</details>

**Pending — 18 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_cwb_past_expiration_date_behaviour` (test_customer_wash_books_edge_cases.py) | CWB-VAL-005 | ⏭️ skip | CWB-VAL-005: Date-time picker interaction and past-date validation require additional page object support. Deferred. | Deferred — re-check scope |
| `test_edit_cwb_expiration_date_persists` (test_customer_wash_books_edit.py) | CWB-EDT-002 | ⏭️ skip | CWB-EDT-002: Date-time picker interaction requires additional page object support. Deferred. | Deferred — re-check scope |
| `test_create_cwb_is_active_by_default` (test_customer_wash_books_positive.py) | — | ⏭️ skip | needs_inspection: data-props-id='isActive' no longer exists on CWB grid — check Customer Wash Books grid HTML for the Active/status colum… | Case-by-case (see reason) |
| `test_create_cwb_with_expiration_date` (test_customer_wash_books_positive.py) | CWB-CRT-005 | ⏭️ skip | CWB-CRT-005: Date-time picker interaction requires additional page object support. Deferred. | Deferred — re-check scope |
| `test_create_cwb_with_site_selection` (test_customer_wash_books_positive.py) | CWB-CRT-002 | ⏭️ skip | CWB-CRT-002: Requires a Select site dropdown that is bound to real site data. Deferred until site fixtures for CWB form are established. | Deferred — re-check scope |
| `test_customer_wash_books_export_file_validation` (test_customer_wash_books_ui.py) | — | ⏭️ skip | Manual - Check later for fixes: file content validation requires download-directory config and CSV/XLS parser. | Needs downloaded-file verification |
| `test_active_wash_book_available_for_cwb_creation` (test_wash_books_dependency.py) | — | ⏭️ skip | WB-DEP: Requires Customers module integration to verify wash book appears in the Select wash book dropdown during customer wash book crea… | Deferred — re-check scope |
| `test_customer_portal_enabled_wash_book_visible` (test_wash_books_dependency.py) | WB-CPT-001 | ⏭️ skip | WB-CPT-001: Requires Customer Portal integration to verify portal visibility. Deferred. | Deferred — re-check scope |
| `test_deactivated_wash_book_not_available_for_cwb_creation` (test_wash_books_dependency.py) | — | ⏭️ skip | WB-DEP: Requires Customers module integration to verify wash book appears in the Select wash book dropdown during customer wash book crea… | Deferred — re-check scope |
| `test_description_shows_on_customer_portal` (test_wash_books_dependency.py) | WB-DSC-001 | ⏭️ skip | WB-DSC-001: Requires Customer Portal integration to verify description display. Deferred. | Deferred — re-check scope |
| `test_duplicate_barcode_rejected` (test_wash_books_dependency.py) | WB-BAR-003 | ⏭️ skip | WB-BAR-003: Requires a known barcode already assigned to another wash book. Deferred until barcode fixtures are established. | Deferred — re-check scope |
| `test_valid_points_awarded_saves` (test_wash_books_dependency.py) | WB-LTY-001 | ⏭️ skip | WB-LTY-001: Verification that points are awarded requires Loyalty module integration. Deferred. | Deferred — re-check scope |
| `test_edit_wash_book_site_assignment_persists` (test_wash_books_edit.py) | WB-EDT-004 | ⏭️ skip | CI-SKIP WB-EDT-004: Inovua site-assignment grid times out in headless Chrome. Fix: decouple site-grid interaction from fixture reset; add… | Case-by-case (see reason) |
| `test_wash_book_settings_persist` (test_wash_books_positive.py) | — | ⚠️ xfail | Manual check: dirty staging data + substring match in open_edit_wash_book opens wrong record | Manual test |
| `test_assign_multiple_sites_persists` (test_wash_books_site_assignment.py) | WB-SIT-002 | ⏭️ skip | CI-SKIP WB-SIT-002: Inovua site-assignment grid times out in headless Chrome. Fix: same as WB-EDT-004 — retry on StaleElementReferenceExc… | Case-by-case (see reason) |
| `test_assign_single_site_persists` (test_wash_books_site_assignment.py) | WB-SIT-001 | ⚠️ xfail | WB-SIT-001: EDIT_FRAME iframe not found on second open_edit_wash_book after saving with location assignment. Needs DevTools inspection of… | Case-by-case (see reason) |
| `test_per_site_customer_portal_toggle_persists` (test_wash_books_site_assignment.py) | WB-SIT-005 | ⏭️ skip | WB-SIT-005: Per-site Show on customer portal requires Customer Portal integration to verify visibility. Deferred. | Deferred — re-check scope |
| `test_wash_books_export_file_validation` (test_wash_books_ui.py) | — | ⏭️ skip | Manual - Check later for fixes: file content validation requires download-directory config and CSV/XLS parser. | Needs downloaded-file verification |

Next actions for this module: Deferred — re-check scope ×11; Case-by-case (see reason) ×4; Needs downloaded-file verification ×2; Manual test ×1

### wash_extras

<details><summary>✅ Covered — 56 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `wash_extras/test_wash_extras_discount.py::test_only_active_discounts_appear_in_dropdown` | — |  |
| `wash_extras/test_wash_extras_discount.py::test_remove_assigned_discount_persists` | — |  |
| `wash_extras/test_wash_extras_discount.py::test_save_wash_extra_without_discount` | — |  |
| `wash_extras/test_wash_extras_edge_cases.py::test_info_tooltip_visible_for_points_awarded` | — |  |
| `wash_extras/test_wash_extras_edge_cases.py::test_info_tooltip_visible_for_points_to_redeem` | — |  |
| `wash_extras/test_wash_extras_edge_cases.py::test_wash_extra_create_is_idempotent` | — |  |
| `wash_extras/test_wash_extras_edge_cases.py::test_wash_extra_long_name_does_not_break_form` | — |  |
| `wash_extras/test_wash_extras_edge_cases.py::test_zero_loyalty_points_accepted` | — |  |
| `wash_extras/test_wash_extras_edit.py::test_activate_wash_extra` | — | 🔥 |
| `wash_extras/test_wash_extras_edit.py::test_deactivate_wash_extra` | — |  |
| `wash_extras/test_wash_extras_edit.py::test_edit_wash_extra_assigned_sites_persist` | — |  |
| `wash_extras/test_wash_extras_edit.py::test_edit_wash_extra_global_commission_persists` | — |  |
| `wash_extras/test_wash_extras_edit.py::test_edit_wash_extra_updates_name_prices_and_discount` | — |  |
| `wash_extras/test_wash_extras_loyalty.py::test_info_tooltip_visible_for_points_awarded` | — |  |
| `wash_extras/test_wash_extras_loyalty.py::test_info_tooltip_visible_for_points_to_redeem` | — |  |
| `wash_extras/test_wash_extras_loyalty.py::test_negative_loyalty_points_rejected` | — |  |
| `wash_extras/test_wash_extras_loyalty.py::test_save_without_loyalty_points` | — |  |
| `wash_extras/test_wash_extras_loyalty.py::test_zero_points_awarded_accepted` | — |  |
| `wash_extras/test_wash_extras_negative.py::test_duplicate_wash_extra_name_is_blocked` | — |  |
| `wash_extras/test_wash_extras_negative.py::test_negative_global_commission_is_rejected` | — |  |
| `wash_extras/test_wash_extras_negative.py::test_negative_global_price_is_rejected` | — |  |
| `wash_extras/test_wash_extras_negative.py::test_wash_extras_search_payloads_do_not_break_grid` | — |  |
| `wash_extras/test_wash_extras_negative.py::test_whitespace_only_service_name_is_rejected` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_create_inactive_wash_extra` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_create_wash_extra` | — | 🔥 |
| `wash_extras/test_wash_extras_positive.py::test_open_price_toggle_is_off_by_default` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_decimal_price_accepted` | — | 🔥 |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_save_without_barcode_succeeds` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_save_without_commission_succeeds` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_save_without_description_succeeds` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_settings_persist` | — |  |
| `wash_extras/test_wash_extras_positive.py::test_wash_extra_valid_commission_saves` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_clear_search_restores_list` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_existing_search` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_filter_active_returns_active_only` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_filter_active_toggle_off_shows_all` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_filter_by_site_narrows_results` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_filter_reset_all_restores_list` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_filter_site_and_active_combined` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_missing_search` | — |  |
| `wash_extras/test_wash_extras_search_filter.py::test_wash_extras_partial_search_returns_matches` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_assign_all_sites_via_header_checkbox` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_assign_single_site_persists` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_negative_location_commission_is_rejected` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_negative_location_price_is_rejected` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_save_wash_extra_with_no_site_assigned` | — |  |
| `wash_extras/test_wash_extras_site_assignment.py::test_state_city_tax_fields_are_read_only` | — |  |
| `wash_extras/test_wash_extras_ui.py::test_add_wash_extra_form_loads` | — |  |
| `wash_extras/test_wash_extras_ui.py::test_wash_extras_filter_panel_shows_controls` | — |  |
| `wash_extras/test_wash_extras_ui.py::test_wash_extras_grid_columns_are_visible` | — |  |
| `wash_extras/test_wash_extras_ui.py::test_wash_extras_page_loads_with_primary_controls` | — | 🔥 |
| `wash_extras/test_wash_extras_validation.py::test_wash_extra_blank_global_price_is_blocked` | — |  |
| `wash_extras/test_wash_extras_validation.py::test_wash_extra_invalid_numeric_values_do_not_break_form` | — |  |
| `wash_extras/test_wash_extras_validation.py::test_wash_extra_max_length_name_handled` | — |  |
| `wash_extras/test_wash_extras_validation.py::test_wash_extra_required_service_name_validation` | — | 🔥 |
| `wash_extras/test_wash_extras_validation.py::test_wash_extra_zero_price_boundary_behaviour` | — |  |

</details>

**Pending — 23 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_active_wash_extra_visible_at_pos` (test_wash_extras_dependency.py) | — | ⏭️ skip | Requires POS module integration to verify wash extra visibility. Deferred. | Deferred — re-check scope |
| `test_controller_code_saves` (test_wash_extras_dependency.py) | WE-CTR-001 | ⏭️ skip | WE-CTR-001: Requires POS integration to verify controller code behaviour. Deferred. | Deferred — re-check scope |
| `test_deactivated_discount_not_applied_on_wash_extra` (test_wash_extras_dependency.py) | — | ⏭️ skip | Requires Discounts module integration to verify discount deactivation behaviour. Deferred. | Deferred — re-check scope |
| `test_deactivated_wash_extra_removed_from_pos` (test_wash_extras_dependency.py) | — | ⏭️ skip | Requires POS module integration to verify wash extra visibility. Deferred. | Deferred — re-check scope |
| `test_description_shows_on_ecommerce_site` (test_wash_extras_dependency.py) | WE-DSC-001 | ⏭️ skip | WE-DSC-001: Requires Customer Portal integration to verify description display. Deferred. | Deferred — re-check scope |
| `test_duplicate_controller_code_rejected` (test_wash_extras_dependency.py) | WE-CTR-002 | ⏭️ skip | WE-CTR-002: Requires POS integration to verify duplicate controller code rejection. Deferred. | Deferred — re-check scope |
| `test_open_price_toggle_enabled_saves` (test_wash_extras_dependency.py) | WE-OPR-001 | ⏭️ skip | WE-OPR-001: Verification that price is editable at POS during a sale requires POS integration. Deferred. | Deferred — re-check scope |
| `test_assign_multiple_discounts_persist` (test_wash_extras_discount.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_assign_single_discount_persists` (test_wash_extras_discount.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_edit_wash_extra_discount_configuration_persists` (test_wash_extras_edit.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_edit_wash_extra_loyalty_points_persist` (test_wash_extras_edit.py) | WE-EDT-004 | ⏭️ skip | WE-EDT-004: Verification that updated loyalty points are correctly awarded requires Loyalty module integration. Deferred. | Deferred — re-check scope |
| `test_edit_wash_extra_values_persist` (test_wash_extras_edit.py) | WE-EDT-002 | ⚠️ xfail | WE-EDT-002: Blocked — multi-step edit flaky due to React field update timing. | Use real typing / React-safe input (see memberships fix) |
| `test_valid_points_awarded_saves` (test_wash_extras_loyalty.py) | — | ⏭️ skip | Requires Loyalty module integration to verify points are awarded/redeemed. Deferred. | Deferred — re-check scope |
| `test_valid_points_to_redeem_saves` (test_wash_extras_loyalty.py) | — | ⏭️ skip | Requires Loyalty module integration to verify points are awarded/redeemed. Deferred. | Deferred — re-check scope |
| `test_duplicate_barcode_is_rejected` (test_wash_extras_negative.py) | WE-BAR-003 | ⏭️ skip | WE-BAR-003: Requires a known barcode already assigned to another wash extra. Deferred until barcode fixtures are established. | Deferred — re-check scope |
| `test_assign_multiple_sites_persists` (test_wash_extras_site_assignment.py) | — | ⏭️ skip | staging data / intermittent — deferred | Re-check now — deferred as staging data / intermittent |
| `test_deselect_previously_assigned_site` (test_wash_extras_site_assignment.py) | WE-SIT-005 | ⏭️ skip | WE-SIT-005: Unchecking an already-saved site and verifying removal requires per-row unchecking support. Deferred. | Deferred — re-check scope |
| `test_disable_tax_exemption_for_site_persists` (test_wash_extras_site_assignment.py) | WE-TAX-002 | ⏭️ skip | WE-TAX-002: Exempt tax toggle per site requires per-row toggle selector verification against the actual DOM. Deferred. | Deferred — re-check scope |
| `test_enable_tax_exemption_for_site_persists` (test_wash_extras_site_assignment.py) | WE-TAX-001 | ⏭️ skip | WE-TAX-001: Exempt tax toggle per site requires per-row toggle selector verification against the actual DOM. Deferred. | Deferred — re-check scope |
| `test_global_price_reflected_at_site_level` (test_wash_extras_site_assignment.py) | — | 🟡 xfail/passing | Staging data: location price field returns empty string | **Promote** — passed in last full run; remove xfail |
| `test_location_commission_override_persists` (test_wash_extras_site_assignment.py) | WE-LCM-001 | ⏭️ skip | WE-LCM-001: Blocked — JS value setter not persisting, React controlled-component state not updated. | Use real typing / React-safe input (see memberships fix) |
| `test_location_price_override_persists` (test_wash_extras_site_assignment.py) | WE-PRC-002 | ⏭️ skip | WE-PRC-002: Blocked — JS value setter not persisting on save, React state not updated. | Use real typing / React-safe input (see memberships fix) |
| `test_wash_extras_export_file_validation` (test_wash_extras_ui.py) | — | ⏭️ skip | Manual - Check later for fixes: file content validation requires download-directory config and CSV/XLS parser. | Needs downloaded-file verification |

Next actions for this module: Deferred — re-check scope ×14; Re-check now — deferred as staging data / intermittent ×4; Use real typing / React-safe input (see memberships fix) ×3; **Promote** — passed in last full run; remove xfail ×1; Needs downloaded-file verification ×1

### wash_packages

<details><summary>✅ Covered — 41 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `wash_packages/test_wash_packages_barcode.py::test_wash_package_barcode_persists` | — |  |
| `wash_packages/test_wash_packages_coverage_gap.py::test_add_wash_package_form_service_discount_save_cancel_controls` | — |  |
| `wash_packages/test_wash_packages_coverage_gap.py::test_wash_package_global_price_is_required` | — |  |
| `wash_packages/test_wash_packages_coverage_gap.py::test_wash_packages_filter_panel_site_option_and_reset` | — |  |
| `wash_packages/test_wash_packages_coverage_gap.py::test_wash_packages_list_shell_controls_and_grid` | — |  |
| `wash_packages/test_wash_packages_edge_cases.py::test_wash_package_existing_search_is_repeatable` | — |  |
| `wash_packages/test_wash_packages_edge_cases.py::test_wash_package_long_name_does_not_break_form` | — |  |
| `wash_packages/test_wash_packages_edge_cases.py::test_wash_package_whitespace_name_is_rejected` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_activate_wash_package` | — | 🔥 |
| `wash_packages/test_wash_packages_edit.py::test_assign_applicable_discount_persists` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_assign_multiple_discounts_persist` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_assigned_sites` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_discount_persists` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_global_commission_persists` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_global_price_persists` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_loyalty_points_persist` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_edit_wash_package_name_persists` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_save_wash_package_without_description` | — |  |
| `wash_packages/test_wash_packages_edit.py::test_service_description_persists` | — |  |
| `wash_packages/test_wash_packages_export.py::test_wash_packages_export_button_clickable` | — |  |
| `wash_packages/test_wash_packages_loyalty.py::test_points_awarded_info_tooltip_is_visible` | — |  |
| `wash_packages/test_wash_packages_loyalty.py::test_points_redeemed_info_tooltip_is_visible` | — |  |
| `wash_packages/test_wash_packages_managed.py::test_managed_package_mutation_is_reset_on_teardown` | — |  |
| `wash_packages/test_wash_packages_negative.py::test_wash_package_required_name_validation` | — |  |
| `wash_packages/test_wash_packages_negative.py::test_wash_package_required_price_validation` | — |  |
| `wash_packages/test_wash_packages_negative.py::test_wash_packages_special_character_search_stays_usable` | — |  |
| `wash_packages/test_wash_packages_search_filter.py::test_wash_packages_clear_search_restores_list` | — |  |
| `wash_packages/test_wash_packages_search_filter.py::test_wash_packages_existing_search` | — |  |
| `wash_packages/test_wash_packages_search_filter.py::test_wash_packages_missing_search` | — |  |
| `wash_packages/test_wash_packages_search_filter.py::test_wash_packages_search_payloads_do_not_break_grid` | — |  |
| `wash_packages/test_wash_packages_site_assignment.py::test_location_commission_override_persists` | — |  |
| `wash_packages/test_wash_packages_site_assignment.py::test_save_wash_package_without_site_selection` | — |  |
| `wash_packages/test_wash_packages_ui.py::test_add_wash_package_form_loads` | — |  |
| `wash_packages/test_wash_packages_ui.py::test_wash_packages_filter_panel_shows_controls` | — |  |
| `wash_packages/test_wash_packages_ui.py::test_wash_packages_grid_columns_are_visible` | — |  |
| `wash_packages/test_wash_packages_ui.py::test_wash_packages_page_loads_with_primary_controls` | — |  |
| `wash_packages/test_wash_packages_ui.py::test_wash_packages_pagination_controls_are_visible` | — |  |
| `wash_packages/test_wash_packages_validation.py::test_wash_package_blank_required_form_stays_on_form` | — | 🔥 |
| `wash_packages/test_wash_packages_validation.py::test_wash_package_decimal_commission_is_accepted` | — |  |
| `wash_packages/test_wash_packages_validation.py::test_wash_package_decimal_price_is_accepted` | — |  |
| `wash_packages/test_wash_packages_validation.py::test_wash_package_invalid_numeric_values_do_not_break_form` | — |  |

</details>

**Pending — 39 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_duplicate_barcode_behaviour` (test_wash_packages_barcode.py) | — | 🟡 xfail/passing | Staging shows 'Something went wrong' server error for duplicate barcode (product defect). | **Promote** — passed in last full run; remove xfail |
| `test_wash_packages_advanced_edge_case_harness_blocker` (test_wash_packages_coverage_gap.py) | — | ⏭️ skip | Manual - Check later for fixes: concurrency/network/audit-log coverage needs multi-session, network interception, and environment restart… | Manual test |
| `test_wash_packages_download_file_validation_blocker` (test_wash_packages_coverage_gap.py) | — | ⏭️ skip | Manual - Check later for fixes: download file/content validation needs browser download-directory config and CSV/XLS parser utilities. | Needs downloaded-file verification |
| `test_wash_packages_permission_matrix_blocker` (test_wash_packages_coverage_gap.py) | — | ⏭️ skip | Manual - Check later for fixes: permission cases require non-admin role fixtures and credentials. | Manual test |
| `test_wash_packages_search_variants_and_clear` (test_wash_packages_coverage_gap.py) | — | ⏭️ skip | Intermittent: filter panel appears unexpectedly after create_wash_package_if_missing on staging. | Case-by-case (see reason) |
| `test_deactivate_wash_package_mapped_to_membership` (test_wash_packages_dependency.py) | — | ⏭️ skip | Requires Memberships module fixtures and cross-module setup. Deferred. | Needs cross-module fixtures |
| `test_deactivated_discount_removed_from_wash_package` (test_wash_packages_dependency.py) | — | ⏭️ skip | Requires active Discount mapped to this package. Deferred. | Deferred — re-check scope |
| `test_rename_wash_package_mapped_to_membership` (test_wash_packages_dependency.py) | — | ⏭️ skip | Requires Memberships module fixtures and cross-module setup. Deferred. | Needs cross-module fixtures |
| `test_site_unassignment_does_not_affect_other_redemption_sites` (test_wash_packages_dependency.py) | — | ⏭️ skip | Requires Memberships module fixtures and cross-module setup. Deferred. | Needs cross-module fixtures |
| `test_wash_package_available_for_membership_redemption` (test_wash_packages_dependency.py) | — | ⏭️ skip | Requires Memberships module fixtures and cross-module setup. Deferred. | Needs cross-module fixtures |
| `test_deactivate_wash_package` (test_wash_packages_edit.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_remove_applicable_discount_persists` (test_wash_packages_edit.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_wash_packages_export_after_filter` (test_wash_packages_export.py) | — | 🟡 xfail/passing | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | **Promote** — passed in last full run; remove xfail |
| `test_loyalty_points_awarded_persists` (test_wash_packages_loyalty.py) | WP-LTY-001 | ⏭️ skip | CI-SKIP WP-LTY-001: managed_package fixture times out in headless CI. Fix: decouple site-assignment from fixture reset path. | Case-by-case (see reason) |
| `test_loyalty_points_redeemed_persists` (test_wash_packages_loyalty.py) | WP-LTY-002 | ⏭️ skip | CI-SKIP WP-LTY-002: managed_package fixture times out in headless CI. Fix: same as WP-LTY-001. | Case-by-case (see reason) |
| `test_managed_package_provided_at_baseline` (test_wash_packages_managed.py) | WP-FRM-001 | ⏭️ skip | CI-SKIP WP-FRM-001: managed_package fixture itself times out in headless CI — Inovua site-grid in reset path. This is the root fixture; f… | Case-by-case (see reason) |
| `test_create_duplicate_wash_package_is_blocked` (test_wash_packages_negative.py) | — | 🟡 xfail/passing | Staging shows 'Something went wrong' server error for duplicate package name; same product defect as duplicate barcode. | **Promote** — passed in last full run; remove xfail |
| `test_negative_global_commission_is_rejected` (test_wash_packages_negative.py) | WP-COM-003 | ⚠️ xfail | WP-COM-003: Commission input has no min=0 HTML5 constraint — negative values pass checkValidity(). Product should enforce min=0. Remove x… | Possible product gap — confirm expected validation |
| `test_negative_global_price_is_rejected` (test_wash_packages_negative.py) | WP-PRI-005 | ⚠️ xfail | WP-PRI-005: Price input has no min=0 HTML5 constraint — negative values pass checkValidity(). Product should enforce min=0. Remove xfail … | Possible product gap — confirm expected validation |
| `test_create_active_wash_package` (test_wash_packages_positive.py) | WP-TGL-001 | ⏭️ skip | CI-SKIP WP-TGL-001: Staging data contamination — package exists at wrong price ($45 vs $14) from prior failed teardown. Fix: fix managed … | Case-by-case (see reason) |
| `test_create_inactive_wash_package` (test_wash_packages_positive.py) | WP-TGL-002 | 🟡 xfail/passing | WP-TGL-002: staging server saves wash package as Active regardless of the Inactive selection on the create form. Same app bug as POS-CRT-… | **Promote** — passed in last full run; remove xfail |
| `test_create_wash_package_without_barcode` (test_wash_packages_positive.py) | WP-BAR-002 | ⏭️ skip | CI-SKIP WP-BAR-002: Inovua site-assignment grid times out in headless Chrome during create flow. Fix: decouple site-assignment from manag… | Case-by-case (see reason) |
| `test_create_wash_package_without_discount` (test_wash_packages_positive.py) | WP-DIS-004 | ⏭️ skip | CI-SKIP WP-DIS-004: Inovua site-assignment grid times out in headless Chrome during create flow. Fix: same as WP-BAR-002. | Case-by-case (see reason) |
| `test_create_wash_package_without_loyalty_points` (test_wash_packages_positive.py) | WP-LTY-006 | ⏭️ skip | CI-SKIP WP-LTY-006: Inovua site-assignment grid times out in headless Chrome during create flow. Fix: same as WP-BAR-002. | Case-by-case (see reason) |
| `test_wash_package_settings_persist` (test_wash_packages_positive.py) | WP-NAM-001 | ⏭️ skip | CI-SKIP WP-NAM-001: Staging data contamination — price reads $45 instead of $14 from prior failed teardown. Fix: same as WP-TGL-001. | Case-by-case (see reason) |
| `test_filter_active_shows_active_packages` (test_wash_packages_search_filter.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_filter_by_site_narrows_results` (test_wash_packages_search_filter.py) | WP-FLT-001 | ⏭️ skip | CI-SKIP WP-FLT-001: Filter panel site-dropdown times out in headless CI. Fix: use window.location.origin-based navigation fallback in wai… | Case-by-case (see reason) |
| `test_filter_site_and_active_combined` (test_wash_packages_search_filter.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_reset_filters_restores_grid` (test_wash_packages_search_filter.py) | — | 🟡 xfail/passing | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | **Promote** — passed in last full run; remove xfail |
| `test_search_inactive_wash_package_returns_it` (test_wash_packages_search_filter.py) | — | ⚠️ xfail | Post-save grid reload exceeds wait timeout on staging (grid/iframe re-render race). Verify inactive-package search behaviour manually. | Manual test |
| `test_wash_packages_partial_search` (test_wash_packages_search_filter.py) | — | 🟡 xfail/passing | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | **Promote** — passed in last full run; remove xfail |
| `test_assign_multiple_sites_persists` (test_wash_packages_site_assignment.py) | WP-SIT-002 | ⏭️ skip | CI-SKIP WP-SIT-002: managed_package fixture times out in headless CI. Fix: decouple site-assignment from fixture reset path. | Case-by-case (see reason) |
| `test_global_price_reflected_at_site` (test_wash_packages_site_assignment.py) | WP-PRC-001 | ⏭️ skip | CI-SKIP WP-PRC-001: managed_package fixture times out in headless CI. Fix: same as WP-SIT-002. | Case-by-case (see reason) |
| `test_location_commission_higher_than_global_persists` (test_wash_packages_site_assignment.py) | WP-PRC-006 | ⏭️ skip | CI-SKIP WP-PRC-006: managed_package fixture times out in headless CI. Fix: same as WP-SIT-002. | Case-by-case (see reason) |
| `test_location_price_override_higher_than_global_persists` (test_wash_packages_site_assignment.py) | WP-PRC-003 | ⏭️ skip | CI-SKIP WP-PRC-003: managed_package fixture times out in headless CI. Fix: same as WP-SIT-002. | Case-by-case (see reason) |
| `test_location_price_override_lower_than_global_persists` (test_wash_packages_site_assignment.py) | WP-PRC-004 | ⏭️ skip | CI-SKIP WP-PRC-004: managed_package fixture times out in headless CI. Fix: same as WP-SIT-002. | Case-by-case (see reason) |
| `test_location_price_override_persists` (test_wash_packages_site_assignment.py) | — | ⚠️ xfail | Headless post-save/navigation timeout (grid/iframe re-render race); reproduces locally. Pending individual fix — see docs/admin_test_burn… | Re-check — save/return-to-list fixes may resolve |
| `test_select_all_sites_via_header_checkbox` (test_wash_packages_site_assignment.py) | WP-SIT-003 | ⏭️ skip | CI-SKIP WP-SIT-003: managed_package fixture times out in headless CI. Fix: same as WP-SIT-002. | Case-by-case (see reason) |
| `test_discount_settings_tab_loads` (test_wash_packages_ui.py) | — | ⏭️ skip | CI-SKIP WP-UI: Form tab navigation times out in headless CI. Fix: use window.location.origin fallback in wait_for_list_loaded; add explic… | Case-by-case (see reason) |

Next actions for this module: Case-by-case (see reason) ×17; **Promote** — passed in last full run; remove xfail ×6; Re-check — save/return-to-list fixes may resolve ×5; Needs cross-module fixtures ×4; Manual test ×3; Possible product gap — confirm expected validation ×2; Needs downloaded-file verification ×1; Deferred — re-check scope ×1
