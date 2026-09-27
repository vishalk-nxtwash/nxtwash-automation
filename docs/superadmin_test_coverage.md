# Superadmin Test Coverage — Full & Smoke

**Status: FROZEN (2026-09-27).** Superadmin automation is stable on every platform and parked
while other modules are worked on. This file is the pick-up point: what is covered, what is
pending, and the next action for each gap.

Status key: ✅ Covered (real check — CI goes red if it breaks) · 🟡 Xfail but passing (works
today but cannot fail the build — promote) · ⚠️ Xfail (not working yet) · ⏭️ Skipped ·
🌱 Seed-only · 🔥 In smoke.

---

## 1. Where things stand

| Platform | Full suite | Smoke (43) |
|---|---|---|
| Local (macOS, headless) | ✅ all CI shards | ✅ 43/43 |
| GitHub-hosted (`ubuntu-latest`, `-n 2`) | ✅ 5/5 shards | ✅ 43/43 (~2 min) |
| AWS self-hosted (EC2, `-n 4`) | ✅ 5/5 shards | ✅ 43/43 (~2.7 min) |

- **CI scope:** 396 tests across 5 shards — `auth`, `companies`, `users`, `user-roles`,
  `third-party`. A further 14 tests in legacy root files run nowhere (see the last section).
- **Real checks:** 215 of 396 (54%). The biggest cheap win is the 84 🟡 tests that already pass
  but are still marked xfail.

### How to run

```bash
# Full suite locally (same as CI shards)
pytest tests/superadmin/test_login.py tests/superadmin/test_login_debug.py tests/superadmin/auth \
       tests/superadmin/companies tests/superadmin/users tests/superadmin/user_roles \
       tests/superadmin/third_party --headless -n 4

# Smoke only
pytest tests/superadmin -m smoke --headless -n 2

# One failing test on CI without running the whole suite (optional test_path input)
gh workflow run suite-superadmin-github.yml --ref <branch> -f test_path="<node id or path>"
gh workflow run suite-superadmin-aws.yml    --ref <branch> -f test_path="<node id or path>"
gh workflow run suite-superadmin-smoke.yml  --ref <branch> -f runner=ubuntu-latest   # or self-hosted
```

Working rule: fix a failure locally (run the test 3×), run **only that test** on CI via
`test_path`, then run the full suite once.

---

## 2. Smoke suite — 43 tests

### Covered

| Module | List loads | Create form opens | Edit form opens | Filter | Save persists | Validation | Export | Other |
|---|---|---|---|---|---|---|---|---|
| **Auth / Login** (7) | – | – | – | – | – | ✅ empty submit | – | ✅ login, ✅ unknown email rejected, ✅ no-session redirect, ✅ session survives refresh, ✅ `/login` while logged in → home, ✅ logout |
| **Companies** (8) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ empty form | ✅ | ✅ row actions, ✅ "Login to" modal |
| **Users** (7) | ✅ + test user shown | ✅ | ✅ | ✅ email | ❌ | ✅ empty email | ✅ | |
| **User Roles** (6) | ✅ + predefined roles | ✅ | ✅ (via save) | ✅ | ✅ rename | ✅ empty name | ❌ | |
| **Webhook Subscribers** (5) | ✅ | ✅ | ✅ | n/a (no filter in app) | ✅ rename | ✅ empty name | n/a | |
| **Webhook Setup** (5) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ empty form | n/a | |
| **Sales Path** (5) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ no company | n/a | |

All 43 are real checks: none are xfail or skipped.

### Pending for smoke

| Gap | Why not yet | Next action |
|---|---|---|
| Save persists — Companies, Users, Webhook Setup, Sales Path | No reliable test; existing persistence tests are xfail (React inputs / unconfirmed locators) | Add one managed record per module (reset-to-baseline, id-based, unique edit names — the pattern used for roles/subscribers), then promote one save test per module into smoke |
| User Roles export | `test_export_icon_opens_modal` passes in the full suite | Add `@pytest.mark.smoke` (cheap) |
| Wrong password for the real superadmin account | All suites share one account; a lockout policy would take down every CI run | Confirm whether superadmin has a failed-login lockout, or get a second account; then add |
| Create happy paths (company, user) | Would add permanent staging records (no delete in product) | Needs disposable data or a backend cleanup API |
| Permission enforcement | Needs a non-superadmin session | Build a non-superadmin user fixture |

---

## 3. Cross-cutting gaps and infrastructure

| Item | Impact | Next action |
|---|---|---|
| **84 🟡 xfail-but-passing tests** | Work today but cannot fail CI | Confirm each passed in 2+ recent runs, then remove the xfail marker. Concentrated in companies create/edit/list, user roles, webhook setup create, users filter |
| **47 ⚠️ tests with unconfirmed locator/behaviour** | Not yet real coverage | Confirm on staging module by module and implement |
| **Non-superadmin session fixture** (7 tests) | Access control and permission enforcement untested | Create a restricted user and a fixture that logs in as it |
| **Downloaded-file verification** (10 tests) | Export file contents (CSV/XLSX) untested | Point Chrome's download dir at the per-job `TMPDIR` and parse the files |
| **Managed records for Companies, Users, Webhook Setup, Sales Path** | No save-persistence coverage in these modules | Apply the reset-to-baseline pattern (see `tests/superadmin/third_party/conftest.py` → `reset_managed_subscriber`) |
| **Per-run staging isolation** | All superadmin runs share one `superadmin-staging` concurrency queue, so runs cannot overlap | Give each run its own records (e.g. `CI-AUTOTEST` vs `AUTOTEST` prefix, as in `tests/admin_portal/_managed.py`) and then split the queue |
| **Failure hook misses app-level errors** | `core/network_capture.py` flags HTTP ≥ 400 only; the app answers some errors as HTTP 200 with `statusCode: 401/499` in the body | Optionally also inspect JSON bodies of `/api/` responses |
| **Canonical test-case sheet cross-check** | Unknown whether doc cases exist with no script at all | Map `SA-*` IDs against the superadmin test-case sheet |

### Product observations (for the product team, not test bugs)

- Logout is client-side only (no API call): the old token presumably stays valid until it expires.
- A failed role save (HTTP 499 "already exists") shows no error in the UI.
- Unauthenticated access to protected pages **is** correctly redirected to `/login`
  (re-verified 2026-09-27; the old "no auth guard" skips were outdated and are removed).

### Staging data the suites rely on

| Record | Id | Managed by |
|---|---|---|
| Role `VK Auto Test Role` | 11 | `user_roles/conftest.py` (session upsert + id-based restore; recovers `… Edited <hex>` leftovers) |
| Subscriber `VK Auto Test Sub` (VT) | 28 | `third_party/conftest.py` → `reset_managed_subscriber` (includes inactive records in lookup) |
| Role `VK carwash role` | 7 | Created only by legacy `test_create_user_role.py`; users seed data depends on it → move into `users/conftest.py` |
| Legacy orphans: roles 9, 10; subscriber 19 | — | Harmless, but should be renamed (e.g. `ZZ-ARCHIVED …`) after a read-only check that nothing references them |

---

## 4. Full suite — summary by module

| Module | Tests | ✅ Covered (must pass) | 🟡 Xfail but passing (promote) | ⚠️ Xfail (not yet working) | ⏭️ Skipped | 🌱 Seed-only | 🔥 In smoke |
|---|---|---|---|---|---|---|---|
| Auth / Login | 14 | 13 | 0 | 0 | 1 | 0 | 7 |
| Companies | 95 | 31 | 35 | 14 | 15 | 0 | 8 |
| Users | 80 | 60 | 10 | 8 | 1 | 1 | 7 |
| User Roles | 76 | 26 | 25 | 16 | 9 | 0 | 6 |
| Third Party — Webhook Subscribers | 34 | 25 | 1 | 5 | 1 | 2 | 5 |
| Third Party — Webhook Setup | 58 | 29 | 11 | 13 | 2 | 3 | 5 |
| Third Party — Sales Path | 39 | 31 | 2 | 4 | 1 | 1 | 5 |
| **Total** | **396** | **215** | **84** | **60** | **30** | **7** | **43** |

## 5. Full suite — details by module

Each module lists what is covered, then every pending test with its reason and the next action. "Xfail but passing" is based on the last full GitHub run; re-check before promoting.

### Auth / Login

<details><summary>✅ Covered — 13 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `auth/test_login_flows.py::test_empty_submit_shows_email_validation` | — | 🔥 |
| `auth/test_login_flows.py::test_enter_key_submits_login` | — |  |
| `auth/test_login_flows.py::test_logged_in_user_visiting_login_is_redirected_home` | — | 🔥 |
| `auth/test_login_flows.py::test_login_page_shows_fields_and_button` | — |  |
| `auth/test_login_flows.py::test_logout_ends_session_and_protects_pages` | — | 🔥 |
| `auth/test_login_flows.py::test_malformed_email_is_blocked_by_field_validation` | — |  |
| `auth/test_login_flows.py::test_password_is_masked` | — |  |
| `auth/test_login_flows.py::test_session_is_shared_across_tabs` | — |  |
| `auth/test_login_flows.py::test_session_persists_after_refresh` | — | 🔥 |
| `auth/test_login_flows.py::test_unauthenticated_root_redirects_to_login` | — | 🔥 |
| `auth/test_login_flows.py::test_unknown_email_is_rejected` | — | 🔥 |
| `auth/test_login_flows.py::test_valid_email_with_empty_password_does_not_authenticate` | — |  |
| `test_login.py::test_superadmin_login` | — | 🔥 |

</details>

**Pending — 1 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_login_debug` (test_login_debug.py) | — | ⏭️ skip | test_login_debug: Interactive debug test using input() — not suitable for automated or headless execution. | Interactive debug helper — never automated |

Next actions for this module: Interactive debug helper — never automated ×1

### Companies

<details><summary>✅ Covered — 31 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `companies/test_companies_access.py::test_unauthenticated_create_redirects_to_login` | SA-CMP-ACC-002 |  |
| `companies/test_companies_create.py::test_add_company_button_opens_create_form` | SA-CMP-CRT-001 | 🔥 |
| `companies/test_companies_create.py::test_cancel_returns_to_companies_list` | SA-CMP-CRT-033 |  |
| `companies/test_companies_create.py::test_create_form_shows_both_settings_sections` | SA-CMP-CRT-002 |  |
| `companies/test_companies_create.py::test_invalid_email_format_rejected` | SA-CMP-CRT-019 |  |
| `companies/test_companies_create.py::test_save_empty_form_shows_validation` | SA-CMP-CRT-007 | 🔥 |
| `companies/test_companies_edit.py::test_cancel_discards_edit_changes` | SA-CMP-EDT-013 |  |
| `companies/test_companies_edit.py::test_edit_button_opens_edit_form` | SA-CMP-EDT-001 | 🔥 |
| `companies/test_companies_edit.py::test_edit_form_prefills_company_name` | SA-CMP-EDT-002 |  |
| `companies/test_companies_export.py::test_cancel_closes_export_modal` | SA-CMP-EXP-012 |  |
| `companies/test_companies_export.py::test_export_default_format_is_xlsx` | SA-CMP-EXP-005 |  |
| `companies/test_companies_export.py::test_export_icon_is_visible` | SA-CMP-EXP-001 |  |
| `companies/test_companies_export.py::test_export_icon_opens_modal` | SA-CMP-EXP-002 | 🔥 |
| `companies/test_companies_export.py::test_export_modal_default_column_toggles` | SA-CMP-EXP-006 |  |
| `companies/test_companies_export.py::test_export_modal_title_contains_companies` | SA-CMP-EXP-003 |  |
| `companies/test_companies_filter.py::test_active_company_toggle_on_shows_active_only` | SA-CMP-FLT-007 |  |
| `companies/test_companies_filter.py::test_apply_filters_updates_list_and_count` | SA-CMP-FLT-010 |  |
| `companies/test_companies_filter.py::test_close_filter_panel_without_applying` | SA-CMP-FLT-012 |  |
| `companies/test_companies_filter.py::test_combined_name_and_active_filter` | SA-CMP-FLT-009 |  |
| `companies/test_companies_filter.py::test_filter_button_opens_filter_panel` | SA-CMP-FLT-001 |  |
| `companies/test_companies_filter.py::test_filter_by_exact_company_name_returns_match` | SA-CMP-FLT-003 | 🔥 |
| `companies/test_companies_filter.py::test_filter_by_partial_name_returns_matches` | SA-CMP-FLT-004 |  |
| `companies/test_companies_filter.py::test_filter_panel_shows_company_name_field` | SA-CMP-FLT-002 |  |
| `companies/test_companies_filter.py::test_no_match_filter_shows_empty_state` | SA-CMP-FLT-005 |  |
| `companies/test_companies_list.py::test_companies_list_page_loads` | SA-CMP-LST-001 | 🔥 |
| `companies/test_companies_list.py::test_company_row_shows_login_to_and_edit_actions` | SA-CMP-LST-003 | 🔥 |
| `companies/test_companies_list.py::test_no_match_filter_shows_no_error` | SA-CMP-LST-009 |  |
| `companies/test_companies_list.py::test_pagination_records_count_visible` | SA-CMP-LST-004 |  |
| `companies/test_companies_login.py::test_close_dismisses_launcher_without_navigating` | SA-CMP-LGN-008 |  |
| `companies/test_companies_login.py::test_login_to_modal_lists_all_app_options` | SA-CMP-LGN-002 |  |
| `companies/test_companies_login.py::test_login_to_opens_app_selection_modal` | SA-CMP-LGN-001 | 🔥 |

</details>

**Pending — 64 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_non_superadmin_cannot_reach_companies` (test_companies_access.py) | SA-CMP-ACC-001 | ⏭️ skip | Non-Superadmin access to /companies requires a different user role fixture — not available in the current test setup. | Needs non-superadmin session fixture |
| `test_address_2_is_optional` (test_companies_create.py) | SA-CMP-CRT-004 | 🟡 xfail/passing | Verifying Address 2 has no asterisk requires CSS inspection of the label — not reliably done via Selenium. | **Promote** — passed in last full run; remove xfail |
| `test_city_options_depend_on_state` (test_companies_create.py) | SA-CMP-CRT-023 | 🟡 xfail/passing | City depends on state — cascade not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_company_name_max_length` (test_companies_create.py) | SA-CMP-CRT-031 | 🟡 xfail/passing | Maximum name length — value not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_company_name_required` (test_companies_create.py) | SA-CMP-CRT-008 | 🟡 xfail/passing | Per-field company-name validation requires filling all other required dropdowns (Database, country, state, city, timezone) which are Reac… | **Promote** — passed in last full run; remove xfail |
| `test_company_name_whitespace_trimmed` (test_companies_create.py) | SA-CMP-CRT-030 | 🟡 xfail/passing | Leading/trailing whitespace trim — server behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_country_dropdown_loads_states` (test_companies_create.py) | SA-CMP-CRT-021 | ⚠️ xfail | Country→State cascade — React Select interaction and option values not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_create_company_with_all_required_fields` (test_companies_create.py) | SA-CMP-CRT-005 | ⏭️ skip | Core happy-path create — skipped to avoid creating new company records in staging. | Needs disposable/managed data (would add permanent staging records) |
| `test_database_dropdown_lists_options` (test_companies_create.py) | SA-CMP-CRT-020 | ⚠️ xfail | Database dropdown option list — React Select structure not confirmed; option values unknown. | Confirm behaviour/locator on staging, then implement |
| `test_duplicate_company_name_behaviour` (test_companies_create.py) | SA-CMP-CRT-027 | ⏭️ skip | Duplicate company name uniqueness rule — confirming requires creating a company, skipped to avoid new records. | Needs disposable/managed data (would add permanent staging records) |
| `test_email_required` (test_companies_create.py) | SA-CMP-CRT-011 | 🟡 xfail/passing | Email field name ('email') on create form not confirmed via DOM — may differ from the edit form. | **Promote** — passed in last full run; remove xfail |
| `test_new_company_appears_in_list_and_count_increments` (test_companies_create.py) | SA-CMP-CRT-006 | ⏭️ skip | Depends on CRT-005 (actual company creation) — skipped. | Needs disposable/managed data (would add permanent staging records) |
| `test_password_field_is_masked` (test_companies_create.py) | SA-CMP-CRT-028 | 🟡 xfail/passing | Password field masking / visibility toggle — password input type and toggle button presence not confirmed via DOM. | **Promote** — passed in last full run; remove xfail |
| `test_phone_number_validation_rule` (test_companies_create.py) | SA-CMP-CRT-026 | 🟡 xfail/passing | Phone number format/length rule not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_required_fields_are_marked_with_asterisk` (test_companies_create.py) | SA-CMP-CRT-003 | ⚠️ xfail | Checking for a red asterisk on required fields requires CSS pseudo-element or aria-required inspection — not reliably done via Selenium. | Visual/layout — not reliably verifiable via Selenium |
| `test_special_characters_in_company_name` (test_companies_create.py) | SA-CMP-CRT-032 | 🟡 xfail/passing | Special characters / emoji — behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_state_options_depend_on_country` (test_companies_create.py) | SA-CMP-CRT-022 | 🟡 xfail/passing | State depends on country — cascade not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_timezone_dropdown_lists_timezones` (test_companies_create.py) | SA-CMP-CRT-024 | ⚠️ xfail | Timezone dropdown — React Select structure and option values not confirmed via DOM inspection. | Confirm behaviour/locator on staging, then implement |
| `test_whitespace_only_company_name_rejected` (test_companies_create.py) | SA-CMP-CRT-029 | 🟡 xfail/passing | Whitespace-only rejection — server behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_zip_validation_rule` (test_companies_create.py) | SA-CMP-CRT-025 | 🟡 xfail/passing | Zip format/length rule not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_clearing_required_field_rejected_on_save` (test_companies_edit.py) | SA-CMP-EDT-008 | 🟡 xfail/passing | Clearing a required field via the X clear icon — inline clear icon locator not confirmed; save may proceed without blocking. | **Promote** — passed in last full run; remove xfail |
| `test_edit_company_name_persists` (test_companies_edit.py) | SA-CMP-EDT-005 | 🟡 xfail/passing | Company name edit persistence — rich-text or React-controlled input may not accept Selenium send_keys correctly; save behaviour not confi… | **Promote** — passed in last full run; remove xfail |
| `test_edit_country_state_city_cascade` (test_companies_edit.py) | SA-CMP-EDT-010 | 🟡 xfail/passing | Country/State/City cascade on edit — React Select interaction and cascade behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_edit_email_is_prefilled` (test_companies_edit.py) | SA-CMP-EDT-006 | ⚠️ xfail | Email field name on edit form not confirmed — locator (By.NAME, 'email') may not match the actual DOM. | Confirm locator on staging, then implement |
| `test_edit_form_does_not_show_database_or_site_name` (test_companies_edit.py) | SA-CMP-EDT-004 | 🟡 xfail/passing | Field names for Database, Site name, Password on the create form not confirmed — cannot verify absence on the edit form. | **Promote** — passed in last full run; remove xfail |
| `test_edit_form_prefills_location_fields` (test_companies_edit.py) | SA-CMP-EDT-003 | 🟡 xfail/passing | Location field names (country, state, city, address, zip, timezone) on the edit form not confirmed via DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_edit_phone_is_prefilled` (test_companies_edit.py) | SA-CMP-EDT-007 | ⚠️ xfail | Phone field name on edit form not confirmed — locator (By.NAME, 'phoneNumber') may not match the actual DOM. | Confirm locator on staging, then implement |
| `test_editing_partial_data_company_loads_without_error` (test_companies_edit.py) | SA-CMP-EDT-015 | 🟡 xfail/passing | Company with missing data (e.g. crewcarwashtest) — existence of this company in staging not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_invalid_email_on_edit_form_rejected` (test_companies_edit.py) | SA-CMP-EDT-009 | 🟡 xfail/passing | Invalid email on edit form — email field name not confirmed; entering invalid value via send_keys may not work. | **Promote** — passed in last full run; remove xfail |
| `test_nonexistent_company_id_shows_error_or_redirect` (test_companies_edit.py) | SA-CMP-EDT-016 | 🟡 xfail/passing | Non-existent company ID (404 vs redirect) — app behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_save_with_no_modifications_is_safe` (test_companies_edit.py) | SA-CMP-EDT-014 | ⚠️ xfail | Save changes with no modifications — behaviour (silent success, confirmation dialog) not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_upload_logo_image` (test_companies_edit.py) | SA-CMP-EDT-011 | ⏭️ skip | Logo upload requires file-upload tooling — manual test. | Manual test |
| `test_upload_logo_invalid_file_rejected` (test_companies_edit.py) | SA-CMP-EDT-012 | ⏭️ skip | Logo upload rejection (invalid type/size) — manual test. | Manual test |
| `test_all_columns_off_disables_export_or_shows_message` (test_companies_export.py) | SA-CMP-EXP-010 | ⚠️ xfail | Turning every column OFF then exporting — toggle interaction and Export button disabled state not confirmed via DOM. | Confirm behaviour/locator on staging, then implement |
| `test_export_csv_downloads_valid_file` (test_companies_export.py) | SA-CMP-EXP-008 | ⏭️ skip | Download CSV content verification — Automation: Pending in spec; requires download tooling. | Needs downloaded-file verification |
| `test_export_modal_has_xlsx_and_csv_options` (test_companies_export.py) | SA-CMP-EXP-004 | ⚠️ xfail | Export format selector structure (native select vs React Select) not confirmed — DOM inspection required to verify XLSX/CSV options. | Needs downloaded-file verification |
| `test_export_respects_active_filter` (test_companies_export.py) | SA-CMP-EXP-011 | 🟡 xfail/passing | Export respects active filter — filter + export interaction not confirmed; download tooling not available. | **Promote** — passed in last full run; remove xfail |
| `test_export_xlsx_downloads_valid_file` (test_companies_export.py) | SA-CMP-EXP-007 | ⏭️ skip | Download XLSX content verification — Automation: Pending in spec; requires download tooling. | Needs downloaded-file verification |
| `test_exported_rows_match_on_screen_list` (test_companies_export.py) | SA-CMP-EXP-009 | ⏭️ skip | Exported row/value reconciliation against on-screen list — Automation: Pending in spec; requires download tooling. | Needs downloaded-file verification |
| `test_active_toggle_off_shows_all_companies` (test_companies_filter.py) | SA-CMP-FLT-008 | ⚠️ xfail | Testing 'active toggle OFF' requires at least one inactive company in staging — existence not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_applied_filter_persists_until_reset` (test_companies_filter.py) | SA-CMP-FLT-014 | 🟡 xfail/passing | Filter persistence across navigation — whether the server stores filter state after reload is not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_clear_x_icon_empties_company_name_input` (test_companies_filter.py) | SA-CMP-FLT-006 | ⏭️ skip | The Company name filter is a plain <input type='text'> with no built-in clear (X) button — confirmed from DOM inspection. Clearing must b… | Rewrite: app has no clear (X) button — test the manual clear instead |
| `test_name_filter_is_case_insensitive` (test_companies_filter.py) | SA-CMP-FLT-013 | 🟡 xfail/passing | Case-insensitive filter — server may perform case-sensitive matching; behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_reset_filters_restores_full_list` (test_companies_filter.py) | SA-CMP-FLT-011 | ⚠️ xfail | Parallel workers create/delete companies concurrently — row count comparison is inherently flaky under -n 2. | Re-check — xdist grouping may have fixed the race |
| `test_companies_table_has_required_columns` (test_companies_list.py) | SA-CMP-LST-002 | 🟡 xfail/passing | Exact column header labels not confirmed via DOM inspection — table may render headers differently from the spec. | **Promote** — passed in last full run; remove xfail |
| `test_long_address_wraps_within_cell` (test_companies_list.py) | SA-CMP-LST-008 | 🟡 xfail/passing | Address-wrap is a visual/layout assertion — not reliably verifiable via Selenium element properties. | **Promote** — passed in last full run; remove xfail |
| `test_partial_data_company_renders_without_error` (test_companies_list.py) | SA-CMP-LST-007 | 🟡 xfail/passing | Company name 'crewcarwashtest' (partial-data company) has not been confirmed to exist in this staging environment. | **Promote** — passed in last full run; remove xfail |
| `test_previous_page_button_disabled_on_page_1` (test_companies_list.py) | SA-CMP-LST-006 | 🟡 xfail/passing | With a single page of results the Prev/Next buttons may not exist at all — behaviour when disabled state differs per implementation. | **Promote** — passed in last full run; remove xfail |
| `test_records_count_updates_after_edit` (test_companies_list.py) | SA-CMP-LST-010 | 🟡 xfail/passing | Verifying count change after an edit requires modifying data and checking before/after — fragile and dependent on a writable fixture. | **Promote** — passed in last full run; remove xfail |
| `test_results_per_page_options` (test_companies_list.py) | SA-CMP-LST-005 | 🟡 xfail/passing | Results-per-page selector structure (React Select vs native <select>) not confirmed — DOM inspection required. | **Promote** — passed in last full run; remove xfail |
| `test_admin_portal_launches_in_company_context` (test_companies_login.py) | SA-CMP-LGN-003 | ⏭️ skip | 'Admin Portal' impersonation opens a new window/tab and navigates away — side effects on browser state; skipped for automated suite. | Out of scope (opens external app) |
| `test_back_on_domain_step_returns_to_app_selection` (test_companies_login.py) | SA-CMP-LGN-007 | 🟡 xfail/passing | 'Back' button on domain step returns to app selection — Back button locator in the POS domain step not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_login_to_opens_correct_company_context` (test_companies_login.py) | SA-CMP-LGN-010 | 🟡 xfail/passing | Context integrity check — verifying the launched app opens the correct company requires reading the destination page, which involves a ne… | **Promote** — passed in last full run; remove xfail |
| `test_login_to_partial_data_company` (test_companies_login.py) | SA-CMP-LGN-011 | 🟡 xfail/passing | 'Login to' on a company with missing data — company 'crewcarwashtest' existence not confirmed in staging. | **Promote** — passed in last full run; remove xfail |
| `test_pos_app_shows_domain_selection_step` (test_companies_login.py) | SA-CMP-LGN-004 | 🟡 xfail/passing | POS App sub-step (domain selection) — dialog structure not confirmed via DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_pos_production_launches` (test_companies_login.py) | SA-CMP-LGN-005 | ⏭️ skip | POS Production launch — opens external URL; side effects on browser state; skipped for automated suite. | Out of scope (opens external app) |
| `test_pos_staging_launches` (test_companies_login.py) | SA-CMP-LGN-006 | ⏭️ skip | POS Staging launch — opens external URL; side effects on browser state; skipped for automated suite. | Out of scope (opens external app) |
| `test_tunnel_nxtcrm_nxttrack_launch` (test_companies_login.py) | SA-CMP-LGN-009 | ⏭️ skip | Tunnel/NxtCRM/NxtTrack app launch — opens external URLs; side effects on browser state; skipped for automated suite. | Out of scope (opens external app) |
| `test_changing_default_language_persists` (test_companies_public.py) | SA-CMP-PUB-002 | 🟡 xfail/passing | Changing default language and saving — React Select dropdown locator not confirmed; save persistence not verified. | **Promote** — passed in last full run; remove xfail |
| `test_custom_terms_url_toggle_reveals_url_field` (test_companies_public.py) | SA-CMP-PUB-004 | ⚠️ xfail | 'Enable company custom terms and conditions URL' toggle — locator not confirmed via DOM inspection. | Confirm locator on staging, then implement |
| `test_default_language_defaults_to_english` (test_companies_public.py) | SA-CMP-PUB-001 | 🟡 xfail/passing | Default language dropdown locator not confirmed — React Select structure needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_membership_terms_toggle_persists` (test_companies_public.py) | SA-CMP-PUB-005 | ⚠️ xfail | 'Enable membership terms' toggle — locator not confirmed via DOM inspection. | Confirm locator on staging, then implement |
| `test_privacy_policy_is_optional` (test_companies_public.py) | SA-CMP-PUB-006 | ⚠️ xfail | Saving with an empty privacy policy — modifies data; PRIVACY_POLICY_TEXTAREA (By.NAME, 'privacyPolicyText') and save interaction not conf… | Confirm behaviour/locator on staging, then implement |
| `test_terms_condition_required_clearing_blocked` (test_companies_public.py) | SA-CMP-PUB-003 | ⏭️ skip | Terms and conditions required validation — termsCondition is a rich-text editor; content comparison and clearing via Selenium fail due to… | Needs rich-text editor helper (content set/clear) |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×35; Confirm behaviour/locator on staging, then implement ×7; Confirm locator on staging, then implement ×4; Needs downloaded-file verification ×4; Out of scope (opens external app) ×4; Needs disposable/managed data (would add permanent staging records) ×3; Manual test ×2; Needs non-superadmin session fixture ×1; Visual/layout — not reliably verifiable via Selenium ×1; Rewrite: app has no clear (X) button — test the manual clear instead ×1; Re-check — xdist grouping may have fixed the race ×1; Needs rich-text editor helper (content set/clear) ×1

### Users

<details><summary>✅ Covered — 60 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `users/test_users_access.py::test_unauthenticated_create_user_redirects_to_login` | SA-USR-ACC-002 |  |
| `users/test_users_access.py::test_unauthenticated_users_list_redirects_to_login` | SA-USR-ACC-001 |  |
| `users/test_users_create.py::test_add_user_button_navigates_to_create_form` | SA-USR-CRT-001 | 🔥 |
| `users/test_users_create.py::test_cancel_button_returns_to_users_list` | SA-USR-CRT-004 |  |
| `users/test_users_create.py::test_create_form_accepts_each_role[Company Owner]` | SA-USR-CRT-022 |  |
| `users/test_users_create.py::test_create_form_accepts_each_role[POS Super User1]` | SA-USR-CRT-022 |  |
| `users/test_users_create.py::test_create_form_accepts_each_role[POS User8]` | SA-USR-CRT-022 |  |
| `users/test_users_create.py::test_create_form_accepts_each_role[VK carwash role]` | SA-USR-CRT-022 |  |
| `users/test_users_create.py::test_create_form_has_save_and_cancel_buttons` | SA-USR-CRT-003 |  |
| `users/test_users_create.py::test_create_form_shows_required_fields` | SA-USR-CRT-002 |  |
| `users/test_users_create.py::test_created_user_appears_in_users_list` | SA-USR-CRT-028 |  |
| `users/test_users_create.py::test_direct_url_to_create_loads_form` | SA-USR-CRT-026 |  |
| `users/test_users_create.py::test_duplicate_email_shows_error` | SA-USR-CRT-020 |  |
| `users/test_users_create.py::test_duplicate_phone_shows_error` | SA-USR-CRT-021 |  |
| `users/test_users_create.py::test_first_name_too_short_rejected` | SA-USR-CRT-011 |  |
| `users/test_users_create.py::test_form_new_label_is_present` | SA-USR-CRT-027 |  |
| `users/test_users_create.py::test_invalid_email_format_rejected` | SA-USR-CRT-013 |  |
| `users/test_users_create.py::test_last_name_too_short_rejected` | SA-USR-CRT-012 |  |
| `users/test_users_create.py::test_mismatched_passwords_rejected` | SA-USR-CRT-015 |  |
| `users/test_users_create.py::test_password_too_short_rejected` | SA-USR-CRT-014 |  |
| `users/test_users_create.py::test_role_dropdown_lists_all_active_roles` | SA-USR-CRT-019 |  |
| `users/test_users_create.py::test_save_with_empty_email_rejected` | SA-USR-CRT-007 | 🔥 |
| `users/test_users_create.py::test_save_with_empty_first_name_rejected` | SA-USR-CRT-005 |  |
| `users/test_users_create.py::test_save_with_empty_last_name_rejected` | SA-USR-CRT-006 |  |
| `users/test_users_create.py::test_save_with_empty_password_rejected` | SA-USR-CRT-009 |  |
| `users/test_users_create.py::test_save_with_empty_phone_rejected` | SA-USR-CRT-008 |  |
| `users/test_users_create.py::test_save_with_no_role_rejected` | SA-USR-CRT-010 |  |
| `users/test_users_edit.py::test_cancel_discards_changes` | SA-USR-EDT-009 |  |
| `users/test_users_edit.py::test_direct_url_to_users_edit` | SA-USR-EDT-011 |  |
| `users/test_users_edit.py::test_edit_button_opens_edit_form` | SA-USR-EDT-001 | 🔥 |
| `users/test_users_edit.py::test_edit_form_prefills_email` | SA-USR-EDT-005 |  |
| `users/test_users_edit.py::test_edit_form_prefills_first_name` | SA-USR-EDT-003 |  |
| `users/test_users_edit.py::test_edit_form_prefills_last_name` | SA-USR-EDT-004 |  |
| `users/test_users_edit.py::test_edit_form_prefills_phone` | SA-USR-EDT-006 |  |
| `users/test_users_edit.py::test_edit_form_shows_edit_label` | SA-USR-EDT-002 |  |
| `users/test_users_export.py::test_cancel_button_closes_export_modal` | SA-USR-EXP-010 |  |
| `users/test_users_export.py::test_esc_key_closes_export_modal` | SA-USR-EXP-011 |  |
| `users/test_users_export.py::test_export_button_enabled_by_default` | SA-USR-EXP-009 |  |
| `users/test_users_export.py::test_export_icon_is_visible` | SA-USR-EXP-001 |  |
| `users/test_users_export.py::test_export_icon_opens_modal` | SA-USR-EXP-002 | 🔥 |
| `users/test_users_export.py::test_export_modal_has_users_title` | SA-USR-EXP-003 |  |
| `users/test_users_filter.py::test_apply_filters_updates_list` | SA-USR-FLT-009 |  |
| `users/test_users_filter.py::test_combined_filters_narrow_results` | SA-USR-FLT-012 |  |
| `users/test_users_filter.py::test_filter_button_opens_filter_panel` | SA-USR-FLT-001 |  |
| `users/test_users_filter.py::test_filter_by_exact_email` | SA-USR-FLT-005 | 🔥 |
| `users/test_users_filter.py::test_filter_by_exact_first_name` | SA-USR-FLT-003 |  |
| `users/test_users_filter.py::test_filter_by_exact_last_name` | SA-USR-FLT-004 |  |
| `users/test_users_filter.py::test_filter_by_exact_phone` | SA-USR-FLT-006 |  |
| `users/test_users_filter.py::test_filter_panel_shows_required_fields` | SA-USR-FLT-002 |  |
| `users/test_users_filter.py::test_non_matching_filter_shows_empty_state` | SA-USR-FLT-007 |  |
| `users/test_users_filter.py::test_partial_first_name_filter` | SA-USR-FLT-010 |  |
| `users/test_users_list.py::test_add_user_button_is_present` | SA-USR-LST-008 |  |
| `users/test_users_list.py::test_direct_url_loads_users_list` | SA-USR-LST-009 |  |
| `users/test_users_list.py::test_pagination_info_contains_page_and_of` | SA-USR-LST-005 |  |
| `users/test_users_list.py::test_pagination_info_is_present` | SA-USR-LST-004 |  |
| `users/test_users_list.py::test_previous_page_button_disabled_on_page_1` | SA-USR-LST-006 |  |
| `users/test_users_list.py::test_primary_test_user_appears_in_list` | SA-USR-LST-010 | 🔥 |
| `users/test_users_list.py::test_users_list_page_loads` | SA-USR-LST-001 | 🔥 |
| `users/test_users_list.py::test_users_list_shows_at_least_one_user` | SA-USR-LST-003 |  |
| `users/test_users_list.py::test_users_table_has_required_columns` | SA-USR-LST-002 |  |

</details>

**Pending — 20 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_confirm_no_stays_on_create_form` (test_users_create.py) | SA-USR-CRT-017 | ⚠️ xfail | Confirmation dialog may not appear or may use different button labels in staging — confirmation dialog behaviour not verified. | Confirm on staging whether a confirmation dialog appears, then fix |
| `test_confirm_yes_creates_user_and_navigates_away` (test_users_create.py) | SA-USR-CRT-018 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_save_new_triggers_confirmation_dialog` (test_users_create.py) | SA-USR-CRT-016 | ⚠️ xfail | Confirmation dialog may not appear or may use different button labels in staging — confirmation dialog behaviour not verified. | Confirm on staging whether a confirmation dialog appears, then fix |
| `test_clearing_required_field_rejected_on_save` (test_users_edit.py) | SA-USR-EDT-008 | 🟡 xfail/passing | Clearing a required field and saving — React-controlled inputs may not update state; save may succeed anyway. | **Promote** — passed in last full run; remove xfail |
| `test_edit_phone_persists_after_save` (test_users_edit.py) | SA-USR-EDT-007 | 🟡 xfail/passing | Phone edit persistence — React-controlled input may not update internal state via Selenium send_keys; save behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_nonexistent_user_id_shows_error_or_redirect` (test_users_edit.py) | SA-USR-EDT-012 | ⏭️ skip | Non-existent user ID (404 vs redirect) — behaviour flagged as '[to be confirmed]' in spec. | Confirm expected behaviour with product |
| `test_save_changes_shows_confirmation` (test_users_edit.py) | SA-USR-EDT-010 | ⚠️ xfail | Save changes confirmation dialog — may not appear on staging (direct save without confirmation). | Confirm on staging whether a confirmation dialog appears, then fix |
| `test_clicking_outside_modal_closes_it` (test_users_export.py) | SA-USR-EXP-012 | ⚠️ xfail | Clicking outside the modal to dismiss — modal backdrop click target not confirmed; some React dialogs ignore outside clicks. | Confirm behaviour/locator on staging, then implement |
| `test_export_all_columns_on_by_default` (test_users_export.py) | SA-USR-EXP-007 | ⚠️ xfail | Column toggle default state not confirmed — depends on aria-checked or is_selected() API which varies by implementation. | Confirm behaviour/locator on staging, then implement |
| `test_export_button_disabled_when_no_columns_selected` (test_users_export.py) | SA-USR-EXP-008 | ⚠️ xfail | Toggling off all columns to disable the Export button — toggle interaction not confirmed; Export button disable state may not be reflecte… | Confirm behaviour/locator on staging, then implement |
| `test_export_default_format_is_xlsx` (test_users_export.py) | SA-USR-EXP-005 | 🟡 xfail/passing | Default export format detection depends on whether the selector is a native <select> or React Select — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_export_modal_has_column_toggles` (test_users_export.py) | SA-USR-EXP-006 | 🟡 xfail/passing | Column toggle locator (@role='switch' or checkbox) inside the modal not confirmed — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_export_modal_has_xlsx_and_csv_options` (test_users_export.py) | SA-USR-EXP-004 | ⚠️ xfail | Export format selector structure (native select vs React Select) not confirmed — needs DOM inspection to verify XLSX/CSV options. | Needs downloaded-file verification |
| `test_applied_filter_persists_across_navigation` (test_users_filter.py) | SA-USR-FLT-013 | 🟡 xfail/passing | Filter persistence across navigation — whether the server stores filter state after reload is not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_clear_x_empties_filter_input` (test_users_filter.py) | SA-USR-FLT-014 | 🟡 xfail/passing | Clear input X button locator inside filter panel not confirmed — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_close_filter_panel_without_applying` (test_users_filter.py) | SA-USR-FLT-016 | 🟡 xfail/passing | Filter panel Close button locator not confirmed — needs DOM inspection with DevTools. | **Promote** — passed in last full run; remove xfail |
| `test_email_filter_is_case_insensitive` (test_users_filter.py) | SA-USR-FLT-015 | 🟡 xfail/passing | Case-insensitive filter — server may perform case-sensitive matching; behaviour not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_partial_email_filter` (test_users_filter.py) | SA-USR-FLT-011 | 🟡 xfail/passing | Partial email filter — server may enforce a minimum term length or require an exact match; behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_reset_filters_restores_full_list` (test_users_filter.py) | SA-USR-FLT-008 | 🟡 xfail/passing | Parallel workers create/delete users concurrently — row count comparison is inherently flaky under -n 2. | **Promote** — passed in last full run; remove xfail |
| `test_results_per_page_options` (test_users_list.py) | SA-USR-LST-007 | ⚠️ xfail | Results-per-page selector locator not confirmed — may render as a React Select or native <select>; needs DOM inspection. | Confirm locator on staging, then implement |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×10; Confirm on staging whether a confirmation dialog appears, then fix ×3; Confirm behaviour/locator on staging, then implement ×3; Seed-only by design (run with `--seed`) ×1; Confirm expected behaviour with product ×1; Needs downloaded-file verification ×1; Confirm locator on staging, then implement ×1

### User Roles

<details><summary>✅ Covered — 26 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `user_roles/test_user_roles_access.py::test_unauthenticated_create_redirects_to_login` | SA-UR-ACC-002 |  |
| `user_roles/test_user_roles_create.py::test_add_role_button_navigates_to_create_form` | SA-UR-CRT-001 | 🔥 |
| `user_roles/test_user_roles_create.py::test_cancel_returns_to_list_with_no_new_role` | SA-UR-CRT-016 |  |
| `user_roles/test_user_roles_create.py::test_newly_created_role_appears_in_list_as_custom` | SA-UR-CRT-006 |  |
| `user_roles/test_user_roles_create.py::test_save_without_role_name_is_blocked` | SA-UR-CRT-009 | 🔥 |
| `user_roles/test_user_roles_edit.py::test_cancel_on_edit_discards_changes` | SA-UR-EDT-011 |  |
| `user_roles/test_user_roles_edit.py::test_edit_button_opens_form_at_correct_url` | SA-UR-EDT-001 |  |
| `user_roles/test_user_roles_edit.py::test_edit_form_prefills_role_name` | SA-UR-EDT-001 |  |
| `user_roles/test_user_roles_edit.py::test_edit_role_name_persists_after_save` | SA-UR-EDT-004 | 🔥 |
| `user_roles/test_user_roles_export.py::test_cancel_closes_export_modal` | SA-UR-EXP-011 |  |
| `user_roles/test_user_roles_export.py::test_export_icon_is_visible` | SA-UR-EXP-001 |  |
| `user_roles/test_user_roles_export.py::test_export_icon_opens_modal` | SA-UR-EXP-001 |  |
| `user_roles/test_user_roles_filter.py::test_apply_filters_updates_list_and_record_count` | SA-UR-FLT-008 |  |
| `user_roles/test_user_roles_filter.py::test_filter_by_button_opens_filter_panel` | SA-UR-FLT-001 |  |
| `user_roles/test_user_roles_filter.py::test_filter_by_exact_role_name_returns_match` | SA-UR-FLT-003 | 🔥 |
| `user_roles/test_user_roles_filter.py::test_filter_by_partial_role_name_returns_matches` | SA-UR-FLT-004 |  |
| `user_roles/test_user_roles_filter.py::test_filter_panel_shows_required_controls` | SA-UR-FLT-002 |  |
| `user_roles/test_user_roles_filter.py::test_filter_with_no_match_shows_empty_state` | SA-UR-FLT-005 |  |
| `user_roles/test_user_roles_list.py::test_list_shows_role_name_and_role_type_columns` | SA-UR-LST-002 |  |
| `user_roles/test_user_roles_list.py::test_pagination_controls_disabled_on_single_page` | SA-UR-LST-007 |  |
| `user_roles/test_user_roles_list.py::test_pagination_shows_page_x_of_y_and_record_count` | SA-UR-LST-005 |  |
| `user_roles/test_user_roles_list.py::test_predefined_roles_appear_in_list` | SA-UR-LST-008 | 🔥 |
| `user_roles/test_user_roles_list.py::test_records_count_reflects_existing_roles` | SA-UR-LST-010 |  |
| `user_roles/test_user_roles_list.py::test_user_roles_list_page_loads` | SA-UR-LST-001 | 🔥 |
| `user_roles/test_user_roles_permissions.py::test_enabling_permission_and_saving_persists` | SA-UR-PRM-005 |  |
| `user_roles/test_user_roles_permissions.py::test_permission_groups_are_present_on_create_form` | SA-UR-PRM-001 |  |

</details>

**Pending — 50 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_user_without_roles_permission_cannot_reach_user_roles` (test_user_roles_access.py) | SA-UR-ACC-001 | 🟡 xfail/passing | Requires a separate user account that lacks the User Roles view permission — not available in the current test setup. | **Promote** — passed in last full run; remove xfail |
| `test_active_user_role_toggle_defaults_to_on` (test_user_roles_create.py) | SA-UR-CRT-004 | 🟡 xfail/passing | Active User Role toggle locator on the create form not confirmed — needs DOM inspection to verify default ON state. | **Promote** — passed in last full run; remove xfail |
| `test_create_form_shows_settings_and_permissions_sections` (test_user_roles_create.py) | SA-UR-CRT-002 | 🟡 xfail/passing | 'User Role Settings' and 'User Role Permissions' section header locators not confirmed — may render as different text on staging. | **Promote** — passed in last full run; remove xfail |
| `test_create_role_with_no_permissions_documents_behaviour` (test_user_roles_create.py) | SA-UR-CRT-015 | 🟡 xfail/passing | Saving a role with no permissions enabled — whether this is allowed or blocked is not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_create_role_with_valid_name_saves_and_navigates` (test_user_roles_create.py) | SA-UR-CRT-005 | ⚠️ xfail | VK Auto Test Role is pre-created via conftest API upsert, so creating it again is rejected as a duplicate; kept xfail to avoid adding new… | Needs disposable/managed data (would add permanent staging records) |
| `test_create_with_active_toggle_off_saves_inactive_role` (test_user_roles_create.py) | SA-UR-CRT-008 | ⚠️ xfail | Creating with Active User Role toggle OFF — toggle interaction and inactive-role verification via filter not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_create_with_active_toggle_on_saves_active_role` (test_user_roles_create.py) | SA-UR-CRT-007 | ⚠️ xfail | Creating with Active User Role toggle ON — toggle interaction and active-state verification via filter not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_duplicate_role_name_shows_error` (test_user_roles_create.py) | SA-UR-CRT-011 | ⚠️ xfail | Duplicate Role Name — uniqueness rule not confirmed; the list already contains a blank-named role suggesting names may not be unique. | Confirm behaviour/locator on staging, then implement |
| `test_role_name_at_maximum_length_saves` (test_user_roles_create.py) | SA-UR-CRT-013 | 🟡 xfail/passing | Maximum allowed Role Name length not documented — behaviour at boundary not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_role_name_field_is_marked_required` (test_user_roles_create.py) | SA-UR-CRT-003 | 🟡 xfail/passing | Required marker (red asterisk) locator next to 'Role Name' not confirmed — depends on CSS class used for required indicators. | **Promote** — passed in last full run; remove xfail |
| `test_role_name_with_whitespace_is_trimmed_or_rejected` (test_user_roles_create.py) | SA-UR-CRT-012 | 🟡 xfail/passing | Leading/trailing whitespace handling — whether the server trims or rejects is not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_special_characters_in_role_name_handled_gracefully` (test_user_roles_create.py) | SA-UR-CRT-014 | 🟡 xfail/passing | Special characters / emoji in Role Name — server sanitisation or rejection behaviour not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_whitespace_only_role_name_is_rejected` (test_user_roles_create.py) | SA-UR-CRT-010 | 🟡 xfail/passing | Whitespace-only Role Name rejection — server may trim and treat as empty, or may accept it; behaviour not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_clearing_role_name_via_x_and_saving_is_blocked` (test_user_roles_edit.py) | SA-UR-EDT-006 | 🟡 xfail/passing | Role Name field inline clear (X) button locator not confirmed — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_deactivate_and_reactivate_role_persists` (test_user_roles_edit.py) | SA-UR-EDT-009 | ⚠️ xfail | Active User Role toggle interaction on edit and verification that deactivate/reactivate persists — toggle locator not confirmed. | Confirm locator on staging, then implement |
| `test_deactivating_assigned_role_documents_impact_on_users` (test_user_roles_edit.py) | SA-UR-EDT-010 | ⏭️ skip | Impact of deactivating a role on assigned users — requires the Users module and a user account assigned to the test role. | Needs a user assigned to the test role (managed data) |
| `test_duplicate_role_name_on_edit_is_rejected` (test_user_roles_edit.py) | SA-UR-EDT-008 | 🟡 xfail/passing | Duplicate Role Name on edit — uniqueness rule on staging not confirmed; same caveat as CRT-011. | **Promote** — passed in last full run; remove xfail |
| `test_edit_form_active_toggle_reflects_saved_state` (test_user_roles_edit.py) | SA-UR-EDT-003 | 🟡 xfail/passing | Active User Role toggle state on the edit form — toggle locator not confirmed; aria-checked detection may vary. | **Promote** — passed in last full run; remove xfail |
| `test_edit_form_prefills_permission_toggles` (test_user_roles_edit.py) | SA-UR-EDT-002 | 🟡 xfail/passing | Pre-filled permission toggles — toggle state detection (is_selected / aria-checked) not confirmed for the edit form. | **Promote** — passed in last full run; remove xfail |
| `test_predefined_role_edit_documents_behaviour` (test_user_roles_edit.py) | SA-UR-EDT-007 | ⚠️ xfail | Predefined role edit behaviour — whether Company Owner can be renamed / have permissions changed / deleted is not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_toggling_permission_persists_after_save` (test_user_roles_edit.py) | SA-UR-EDT-005 | ⚠️ xfail | Toggling a permission on/off and verifying persistence — toggle interaction (set_checkbox) not confirmed on the edit form. | Confirm behaviour/locator on staging, then implement |
| `test_export_as_csv_downloads_valid_file` (test_user_roles_export.py) | SA-UR-EXP-008 | ⏭️ skip | CSV download verification requires inspecting the downloaded file; not feasible in headless CI without additional setup. | Needs downloaded-file verification |
| `test_export_as_xlsx_downloads_valid_file` (test_user_roles_export.py) | SA-UR-EXP-007 | ⏭️ skip | XLSX download verification requires inspecting the downloaded file; not feasible in headless CI without additional setup. | Needs downloaded-file verification |
| `test_export_button_disabled_when_no_columns_selected` (test_user_roles_export.py) | SA-UR-EXP-010 | ⚠️ xfail | Toggling every column OFF then verifying the Export button is disabled — toggle interaction and button disabled-state not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_export_default_column_toggles_are_correct` (test_user_roles_export.py) | SA-UR-EXP-004 | 🟡 xfail/passing | Column toggle defaults (Role Name ON, Role Type ON, Status OFF, etc.) depend on toggle locator (@role='switch') not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_export_default_format_is_xlsx` (test_user_roles_export.py) | SA-UR-EXP-002 | 🟡 xfail/passing | Default export format detection depends on whether the selector is a native <select> or React Select — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_export_format_dropdown_lists_xlsx_and_csv` (test_user_roles_export.py) | SA-UR-EXP-003 | ⚠️ xfail | Export format selector type (native select vs React Select) not confirmed — needs DOM inspection. | Confirm behaviour/locator on staging, then implement |
| `test_exported_rows_match_on_screen_list` (test_user_roles_export.py) | SA-UR-EXP-009 | ⏭️ skip | Verifying exported row count against the on-screen list requires reading the downloaded file. | Needs downloaded-file verification |
| `test_toggling_off_column_on_includes_it_in_export` (test_user_roles_export.py) | SA-UR-EXP-006 | ⏭️ skip | Download content verification requires file-system tooling not available in the current headless test environment. | Needs downloaded-file verification |
| `test_toggling_on_column_off_excludes_it_from_export` (test_user_roles_export.py) | SA-UR-EXP-005 | ⏭️ skip | Download content verification requires file-system tooling not available in the current headless test environment. | Needs downloaded-file verification |
| `test_active_user_role_toggle_off_shows_all_roles` (test_user_roles_filter.py) | SA-UR-FLT-007 | 🟡 xfail/passing | Active User Role toggle OFF requires confirming the inactive role appears — toggle locator and inactive role visibility not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_active_user_role_toggle_on_shows_only_active` (test_user_roles_filter.py) | SA-UR-FLT-006 | 🟡 xfail/passing | 'Active User Role' toggle locator inside the filter panel not confirmed — needs DevTools inspection to verify the toggle element. | **Promote** — passed in last full run; remove xfail |
| `test_close_x_dismisses_panel_without_applying` (test_user_roles_filter.py) | SA-UR-FLT-010 | 🟡 xfail/passing | Close (X) button locator inside the filter panel not confirmed — needs DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_reset_filters_clears_input_and_restores_full_list` (test_user_roles_filter.py) | SA-UR-FLT-009 | ⚠️ xfail | Parallel workers create/delete roles concurrently and Reset button may not be clickable if the panel state is transitional. | Re-check — xdist grouping may have fixed the race |
| `test_role_name_filter_is_case_insensitive` (test_user_roles_filter.py) | SA-UR-FLT-011 | 🟡 xfail/passing | Case-insensitive filter — server may perform case-sensitive matching on staging; behaviour not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_blank_role_name_row_renders_without_breaking` (test_user_roles_list.py) | SA-UR-LST-004 | 🟡 xfail/passing | Blank-named role row rendering — the list contains a role with no name; Edit action presence on that row needs DOM verification. | **Promote** — passed in last full run; remove xfail |
| `test_empty_list_shows_empty_state_not_error` (test_user_roles_list.py) | SA-UR-LST-009 | ⚠️ xfail | Cannot create a reliably empty list state in staging — requires deleting all roles which is destructive. | Not automatable on shared staging (would need deleting all roles) |
| `test_results_per_page_changes_rows_shown` (test_user_roles_list.py) | SA-UR-LST-006 | ⚠️ xfail | 'Show 100' results-per-page dropdown locator not confirmed — may render as a React Select or native <select>. | Confirm locator on staging, then implement |
| `test_role_type_column_shows_correct_value_per_role` (test_user_roles_list.py) | SA-UR-LST-003 | ⚠️ xfail | Exact Role Type cell value ('Custom' vs 'Default'/'Predefined') and column index not confirmed — needs DOM inspection. | Confirm behaviour/locator on staging, then implement |
| `test_all_permission_toggles_default_to_off_on_new_form` (test_user_roles_permissions.py) | SA-UR-PRM-004 | ⚠️ xfail | All permission toggles default to OFF on a new role — toggle state detection via is_selected() / aria-checked not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_create_company_permission_relative_to_parent_companies` (test_user_roles_permissions.py) | SA-UR-PRM-008 | 🟡 xfail/passing | Whether enabling 'Create company' auto-enables the parent 'Companies' view permission — parent-child rule not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_create_role_permission_relative_to_parent_user_roles` (test_user_roles_permissions.py) | SA-UR-PRM-007 | 🟡 xfail/passing | Whether enabling 'Create Role' auto-enables the parent 'User Roles' view permission — parent-child rule not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_disabling_all_permissions_persists_empty_set` (test_user_roles_permissions.py) | SA-UR-PRM-010 | ⚠️ xfail | Disabling all permissions and saving an empty set — whether the server allows a zero-permission role is not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_each_permission_toggle_can_be_set_independently` (test_user_roles_permissions.py) | SA-UR-PRM-006 | 🟡 xfail/passing | Each individual permission toggle independently — toggle interaction via set_checkbox not confirmed on staging. | **Promote** — passed in last full run; remove xfail |
| `test_enabling_all_permissions_persists` (test_user_roles_permissions.py) | SA-UR-PRM-009 | 🟡 xfail/passing | Enabling all permissions and verifying they persist — set_checkbox interaction with all toggles not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_permission_groups_expand_and_collapse` (test_user_roles_permissions.py) | SA-UR-PRM-002 | 🟡 xfail/passing | Expand/collapse behaviour via chevron — the expand buttons may toggle visibility differently; collapsed state not confirmed. | **Promote** — passed in last full run; remove xfail |
| `test_permission_items_match_confirmed_tree` (test_user_roles_permissions.py) | SA-UR-PRM-003 | ⚠️ xfail | Permission sub-items not visible after expand — expand button locator doesn't match actual DOM; items may be collapsed by default. | Confirm locator on staging, then implement |
| `test_user_with_role_can_access_only_permitted_modules` (test_user_roles_permissions.py) | SA-UR-PRM-011 | ⏭️ skip | End-to-end permission enforcement requires assigning the test role to a user and logging in as that user — depends on the Users module an… | Needs non-superadmin session fixture |
| `test_user_without_permission_cannot_reach_module` (test_user_roles_permissions.py) | SA-UR-PRM-012 | ⏭️ skip | Negative enforcement check — requires a non-superadmin user account assigned a restricted role, outside current test scope. | Needs non-superadmin session fixture |
| `test_view_permission_on_create_off_user_can_view_not_create` (test_user_roles_permissions.py) | SA-UR-PRM-013 | ⏭️ skip | Create permission off / view permission on — requires a non-superadmin user session, outside current test scope. | Needs non-superadmin session fixture |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×25; Confirm behaviour/locator on staging, then implement ×10; Needs downloaded-file verification ×5; Confirm locator on staging, then implement ×3; Needs non-superadmin session fixture ×3; Needs disposable/managed data (would add permanent staging records) ×1; Needs a user assigned to the test role (managed data) ×1; Re-check — xdist grouping may have fixed the race ×1; Not automatable on shared staging (would need deleting all roles) ×1

### Third Party — Webhook Subscribers

<details><summary>✅ Covered — 25 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `third_party/test_subscribers_create.py::test_active_subscriber_toggle_defaults_on` | SA-SUB-CRT-004 |  |
| `third_party/test_subscribers_create.py::test_add_subscriber_button_opens_create_form` | SA-SUB-CRT-001 | 🔥 |
| `third_party/test_subscribers_create.py::test_cancel_discards_create_form` | SA-SUB-CRT-017 |  |
| `third_party/test_subscribers_create.py::test_create_form_shows_basic_settings` | SA-SUB-CRT-002 |  |
| `third_party/test_subscribers_create.py::test_create_with_active_off` | SA-SUB-CRT-008 |  |
| `third_party/test_subscribers_create.py::test_duplicate_abbreviation_behaviour` | SA-SUB-CRT-012 |  |
| `third_party/test_subscribers_create.py::test_duplicate_subscriber_name_behaviour` | SA-SUB-CRT-011 |  |
| `third_party/test_subscribers_create.py::test_new_subscriber_appears_in_list` | SA-SUB-CRT-006 |  |
| `third_party/test_subscribers_create.py::test_save_without_abbreviation_shows_validation` | SA-SUB-CRT-010 |  |
| `third_party/test_subscribers_create.py::test_save_without_name_shows_validation` | SA-SUB-CRT-009 | 🔥 |
| `third_party/test_subscribers_create.py::test_special_characters_handled_gracefully` | SA-SUB-CRT-016 |  |
| `third_party/test_subscribers_edit.py::test_cancel_on_edit_discards_changes` | SA-SUB-EDT-008 |  |
| `third_party/test_subscribers_edit.py::test_clearing_required_field_blocks_save` | SA-SUB-EDT-005 |  |
| `third_party/test_subscribers_edit.py::test_deactivating_in_use_subscriber_impact` | SA-SUB-EDT-007 |  |
| `third_party/test_subscribers_edit.py::test_edit_abbreviation_persists` | SA-SUB-EDT-004 |  |
| `third_party/test_subscribers_edit.py::test_edit_opens_form_at_correct_url` | SA-SUB-EDT-001 | 🔥 |
| `third_party/test_subscribers_edit.py::test_edit_subscriber_name_persists` | SA-SUB-EDT-003 | 🔥 |
| `third_party/test_subscribers_list.py::test_subscribers_count_updates_after_add` | SA-SUB-LST-008 |  |
| `third_party/test_subscribers_list.py::test_subscribers_empty_state_shows_no_error` | SA-SUB-LST-007 |  |
| `third_party/test_subscribers_list.py::test_subscribers_has_no_filter_or_export` | SA-SUB-LST-003 |  |
| `third_party/test_subscribers_list.py::test_subscribers_list_columns_and_edit_action` | SA-SUB-LST-002 |  |
| `third_party/test_subscribers_list.py::test_subscribers_page_loads` | SA-SUB-LST-001 | 🔥 |
| `third_party/test_subscribers_list.py::test_subscribers_pagination_footer_shows_records_count` | SA-SUB-LST-004 |  |
| `third_party/test_subscribers_list.py::test_subscribers_prev_page_disabled_on_first_page` | SA-SUB-LST-006 |  |
| `third_party/test_subscribers_list.py::test_subscribers_results_per_page_dropdown` | SA-SUB-LST-005 |  |

</details>

**Pending — 9 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_abbreviation_format_constraint` (test_subscribers_create.py) | SA-SUB-CRT-013 | ⚠️ xfail | Abbreviation length/charset constraint not documented — confirmed values are 2 chars (TE, OP); min/max/charset unconfirmed. | Confirm behaviour/locator on staging, then implement |
| `test_create_subscriber_happy_path` (test_subscribers_create.py) | SA-SUB-CRT-005 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_create_with_active_on` (test_subscribers_create.py) | SA-SUB-CRT-007 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_leading_trailing_whitespace_handling` (test_subscribers_create.py) | SA-SUB-CRT-015 | ⚠️ xfail | Leading/trailing whitespace trim behaviour not confirmed. | Confirm behaviour/locator on staging, then implement |
| `test_required_fields_show_asterisk` (test_subscribers_create.py) | SA-SUB-CRT-003 | ⚠️ xfail | Red asterisk required-field marker locator not confirmed. | Confirm locator on staging, then implement |
| `test_whitespace_only_inputs_rejected` (test_subscribers_create.py) | SA-SUB-CRT-014 | ⚠️ xfail | Whitespace-only input rejection not confirmed — server may trim and then fail required-field validation. | Confirm behaviour/locator on staging, then implement |
| `test_deactivate_and_reactivate_subscriber` (test_subscribers_edit.py) | SA-SUB-EDT-006 | ⚠️ xfail | Toggle locator for 'Active Subscriber' not confirmed via DOM inspection. | Confirm locator on staging, then implement |
| `test_edit_form_prefills_saved_data` (test_subscribers_edit.py) | SA-SUB-EDT-002 | 🟡 xfail/passing | Pre-filled field values depend on 'name' and 'abbreviation' input name attributes being correct — unconfirmed via DOM inspection. | **Promote** — passed in last full run; remove xfail |
| `test_non_superadmin_cannot_reach_subscribers` (test_subscribers_edit.py) | SA-SUB-ACC-001 | ⏭️ skip | Access-control test requires a non-Superadmin browser session — no such fixture exists in this suite. | Needs non-superadmin session fixture |

Next actions for this module: Confirm behaviour/locator on staging, then implement ×3; Seed-only by design (run with `--seed`) ×2; Confirm locator on staging, then implement ×2; **Promote** — passed in last full run; remove xfail ×1; Needs non-superadmin session fixture ×1

### Third Party — Webhook Setup

<details><summary>✅ Covered — 29 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `third_party/test_webhook_setup_create.py::test_active_toggle_defaults_on` | SA-SET-CRT-008 |  |
| `third_party/test_webhook_setup_create.py::test_add_setup_button_opens_create_form` | SA-SET-CRT-001 | 🔥 |
| `third_party/test_webhook_setup_create.py::test_all_event_type_checkboxes_default_off` | SA-SET-CRT-010 |  |
| `third_party/test_webhook_setup_create.py::test_cancel_discards_create_form` | SA-SET-CRT-017 |  |
| `third_party/test_webhook_setup_create.py::test_create_with_is_enabled_off` | SA-SET-CRT-018 |  |
| `third_party/test_webhook_setup_create.py::test_is_enabled_toggle_defaults_on` | SA-SET-CRT-007 |  |
| `third_party/test_webhook_setup_create.py::test_key_field_is_present` | SA-SET-CRT-006 |  |
| `third_party/test_webhook_setup_create.py::test_save_without_any_fields_shows_validation` | SA-SET-CRT-011 | 🔥 |
| `third_party/test_webhook_setup_create.py::test_url_field_is_present` | SA-SET-CRT-005 |  |
| `third_party/test_webhook_setup_edit.py::test_cancel_on_edit_discards_changes` | SA-SET-EDT-009 |  |
| `third_party/test_webhook_setup_edit.py::test_edit_opens_form_at_correct_url` | SA-SET-EDT-001 | 🔥 |
| `third_party/test_webhook_setup_event_types.py::test_all_event_checkboxes_default_off` | SA-SET-EVT-004 |  |
| `third_party/test_webhook_setup_event_types.py::test_event_types_section_is_visible` | SA-SET-EVT-001 |  |
| `third_party/test_webhook_setup_filter.py::test_active_key_toggle_off_shows_all` | SA-SET-FLT-008 |  |
| `third_party/test_webhook_setup_filter.py::test_active_key_toggle_on_shows_active_only` | SA-SET-FLT-007 |  |
| `third_party/test_webhook_setup_filter.py::test_apply_filters_updates_list` | SA-SET-FLT-011 |  |
| `third_party/test_webhook_setup_filter.py::test_combined_company_subscriber_active_filter` | SA-SET-FLT-009 |  |
| `third_party/test_webhook_setup_filter.py::test_filter_button_opens_filter_panel` | SA-SET-FLT-001 |  |
| `third_party/test_webhook_setup_filter.py::test_filter_by_partial_company_name` | SA-SET-FLT-004 |  |
| `third_party/test_webhook_setup_filter.py::test_filter_by_third_party_name` | SA-SET-FLT-006 | 🔥 |
| `third_party/test_webhook_setup_filter.py::test_filter_panel_shows_expected_controls` | SA-SET-FLT-002 |  |
| `third_party/test_webhook_setup_filter.py::test_filter_with_no_match_shows_empty_state` | SA-SET-FLT-010 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_count_updates_after_add` | SA-SET-LST-008 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_empty_state` | SA-SET-LST-007 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_list_columns_and_edit_action` | SA-SET-LST-002 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_page_loads` | SA-SET-LST-001 | 🔥 |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_pagination_controls` | SA-SET-LST-005 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_pagination_footer` | SA-SET-LST-003 |  |
| `third_party/test_webhook_setup_list.py::test_webhook_setup_results_per_page_dropdown` | SA-SET-LST-004 |  |

</details>

**Pending — 29 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_all_ten_event_type_checkboxes_present` (test_webhook_setup_create.py) | SA-SET-CRT-009 | 🟡 xfail/passing | Event type checkbox locators not confirmed via DOM. Depends on event name text matching the rendered labels exactly. | **Promote** — passed in last full run; remove xfail |
| `test_company_dropdown_lists_companies` (test_webhook_setup_create.py) | SA-SET-CRT-004 | ⚠️ xfail | Company dropdown options depend on confirmed React Select combobox locator (CRT-002). | Confirm locator on staging, then implement |
| `test_create_form_shows_subscriber_and_company_dropdowns` (test_webhook_setup_create.py) | SA-SET-CRT-002 | 🟡 xfail/passing | Subscriber (placeholder='selectSubscriber') and Company (placeholder='selectCompany') React Select controls not confirmed via DOM inspect… | **Promote** — passed in last full run; remove xfail |
| `test_create_setup_happy_path` (test_webhook_setup_create.py) | SA-SET-CRT-015 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_create_with_active_off` (test_webhook_setup_create.py) | SA-SET-CRT-019 | ⚠️ xfail | 'Active Webhook Setup' toggle locator not confirmed. | Confirm locator on staging, then implement |
| `test_new_setup_appears_in_list` (test_webhook_setup_create.py) | SA-SET-CRT-016 | 🟡 xfail/passing | Depends on CRT-015 running first in the same session. | **Promote** — passed in last full run; remove xfail |
| `test_save_without_company_shows_validation` (test_webhook_setup_create.py) | SA-SET-CRT-012 | 🟡 xfail/passing | Requires filling Subscriber + URL + Key via unconfirmed locators to isolate the missing-Company case. | **Promote** — passed in last full run; remove xfail |
| `test_save_without_key_shows_validation` (test_webhook_setup_create.py) | SA-SET-CRT-014 | 🟡 xfail/passing | Requires confirmed Key input (name='thirdPartyKey') and other locators to fill all other fields. | **Promote** — passed in last full run; remove xfail |
| `test_save_without_url_shows_validation` (test_webhook_setup_create.py) | SA-SET-CRT-013 | 🟡 xfail/passing | Requires confirmed URL input (name='thirdPartyUrl') and other React Select locators to fill all other fields. | **Promote** — passed in last full run; remove xfail |
| `test_subscriber_dropdown_lists_active_subscribers` (test_webhook_setup_create.py) | SA-SET-CRT-003 | ⚠️ xfail | Subscriber dropdown options depend on confirmed React Select combobox locator (CRT-002). | Confirm locator on staging, then implement |
| `test_edit_form_prefills_key` (test_webhook_setup_edit.py) | SA-SET-EDT-004 | ⚠️ xfail | Key field name='thirdPartyKey' not confirmed — get_attribute('value') may return empty if the name is wrong. | Confirm behaviour/locator on staging, then implement |
| `test_edit_form_prefills_subscriber_and_company` (test_webhook_setup_edit.py) | SA-SET-EDT-002 | ⚠️ xfail | Pre-filled Subscriber and Company React Select values depend on confirmed combobox locators — pre-fill reading pattern unconfirmed. | Confirm locator on staging, then implement |
| `test_edit_form_prefills_url` (test_webhook_setup_edit.py) | SA-SET-EDT-003 | ⚠️ xfail | URL field name='thirdPartyUrl' not confirmed — get_attribute('value') may return empty if the name is wrong. | Confirm behaviour/locator on staging, then implement |
| `test_edit_setup_with_auto_no` (test_webhook_setup_edit.py) | SA-SET-EDT-008 | ⏭️ skip | 'Auto=No' / Auto progression OFF cannot be engineered on staging without additional setup — skip for manual verification. | Manual test |
| `test_editing_event_types_persists` (test_webhook_setup_edit.py) | SA-SET-EDT-007 | 🟡 xfail/passing | Editing event type selections depends on confirmed event checkbox locators (SA-SET-EVT-003). | **Promote** — passed in last full run; remove xfail |
| `test_editing_key_persists` (test_webhook_setup_edit.py) | SA-SET-EDT-006 | ⚠️ xfail | Requires confirmed Key input name + save interaction. | Confirm locator on staging, then implement |
| `test_editing_url_persists` (test_webhook_setup_edit.py) | SA-SET-EDT-005 | ⚠️ xfail | Requires confirmed URL input name + Save changes button to reliably edit and verify persistence. | Confirm locator on staging, then implement |
| `test_non_superadmin_cannot_reach_setup` (test_webhook_setup_edit.py) | SA-SET-ACC-001 | ⏭️ skip | Access-control test requires a non-Superadmin browser session — no such fixture exists in this suite. | Needs non-superadmin session fixture |
| `test_all_ten_event_type_names_visible` (test_webhook_setup_event_types.py) | SA-SET-EVT-002 | 🟡 xfail/passing | All 10 event type label texts not confirmed against the DOM — exact casing / spacing may differ from the spec. | **Promote** — passed in last full run; remove xfail |
| `test_each_event_type_has_a_checkbox` (test_webhook_setup_event_types.py) | SA-SET-EVT-003 | 🟡 xfail/passing | Event checkbox locators use ancestor-traversal XPath — exact DOM structure for event type toggles not confirmed against live UI. | **Promote** — passed in last full run; remove xfail |
| `test_event_selection_persists_on_edit` (test_webhook_setup_event_types.py) | SA-SET-EVT-008 | 🟡 xfail/passing | Confirming event selection persists on the edit form requires confirmed event checkbox locators + edit form pre-fill. | **Promote** — passed in last full run; remove xfail |
| `test_save_with_all_events_selected` (test_webhook_setup_event_types.py) | SA-SET-EVT-006 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_saving_with_no_events_selected_is_allowed` (test_webhook_setup_event_types.py) | SA-SET-EVT-007 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_toggle_single_event_on` (test_webhook_setup_event_types.py) | SA-SET-EVT-005 | ⚠️ xfail | Toggling a single event ON depends on confirmed checkbox and label locators (EVT-003). | Confirm locator on staging, then implement |
| `test_close_filter_panel_without_applying` (test_webhook_setup_filter.py) | SA-SET-FLT-013 | ⚠️ xfail | App may live-filter as text is typed — closing the panel without applying might not restore the full list if the filter was auto-applied. | Confirm live-filter behaviour on staging, then fix |
| `test_filter_by_exact_company_name` (test_webhook_setup_filter.py) | SA-SET-FLT-003 | 🟡 xfail/passing | SETUP_COMPANY webhook setup may not exist on staging when this test runs (parallel worker race — edit_setup_page fixture on another worke… | **Promote** — passed in last full run; remove xfail |
| `test_reset_filters_restores_full_list` (test_webhook_setup_filter.py) | SA-SET-FLT-012 | ⚠️ xfail | Parallel workers create/delete setups concurrently — row count comparison is inherently flaky under -n 2. | Re-check — xdist grouping may have fixed the race |
| `test_third_party_name_dropdown_lists_subscribers` (test_webhook_setup_filter.py) | SA-SET-FLT-005 | ⚠️ xfail | Third Party Name React Select structure and combobox locator inside the filter panel not confirmed via DOM inspection. | Confirm locator on staging, then implement |
| `test_webhook_setup_multiple_companies_same_subscriber` (test_webhook_setup_list.py) | SA-SET-LST-006 | ⚠️ xfail | Staging data may change — Optsopt might have fewer than 2 visible mappings on the current page. Promote once staging data is stable. | Needs guaranteed staging data (managed record) |

Next actions for this module: **Promote** — passed in last full run; remove xfail ×11; Confirm locator on staging, then implement ×8; Seed-only by design (run with `--seed`) ×3; Confirm behaviour/locator on staging, then implement ×2; Manual test ×1; Needs non-superadmin session fixture ×1; Confirm live-filter behaviour on staging, then fix ×1; Re-check — xdist grouping may have fixed the race ×1; Needs guaranteed staging data (managed record) ×1

### Third Party — Sales Path

<details><summary>✅ Covered — 31 tests (click to expand)</summary>

| Test | TC | Smoke |
|---|---|---|
| `third_party/test_sales_path_create.py::test_active_toggle_defaults_on` | SA-SLP-CRT-005 |  |
| `third_party/test_sales_path_create.py::test_add_sales_path_button_opens_create_form` | SA-SLP-CRT-001 | 🔥 |
| `third_party/test_sales_path_create.py::test_cancel_discards_create_form` | SA-SLP-CRT-013 |  |
| `third_party/test_sales_path_create.py::test_create_form_shows_company_dropdown` | SA-SLP-CRT-002 |  |
| `third_party/test_sales_path_create.py::test_create_with_is_enabled_off` | SA-SLP-CRT-010 |  |
| `third_party/test_sales_path_create.py::test_duplicate_company_sales_path_behaviour` | SA-SLP-CRT-012 |  |
| `third_party/test_sales_path_create.py::test_is_enabled_toggle_defaults_on` | SA-SLP-CRT-004 |  |
| `third_party/test_sales_path_create.py::test_new_sales_path_appears_in_list` | SA-SLP-CRT-009 |  |
| `third_party/test_sales_path_create.py::test_save_without_company_shows_validation` | SA-SLP-CRT-007 | 🔥 |
| `third_party/test_sales_path_edit.py::test_cancel_on_edit_discards_changes` | SA-SLP-EDT-005 |  |
| `third_party/test_sales_path_edit.py::test_edit_opens_form_at_correct_url` | SA-SLP-EDT-001 | 🔥 |
| `third_party/test_sales_path_filter.py::test_active_toggle_off_shows_all` | SA-SLP-FLT-008 |  |
| `third_party/test_sales_path_filter.py::test_active_toggle_on_shows_active_only` | SA-SLP-FLT-007 |  |
| `third_party/test_sales_path_filter.py::test_close_filter_panel_without_applying` | SA-SLP-FLT-012 |  |
| `third_party/test_sales_path_filter.py::test_combined_company_enabled_active_filter` | SA-SLP-FLT-009 |  |
| `third_party/test_sales_path_filter.py::test_enabled_toggle_off_shows_all` | SA-SLP-FLT-006 |  |
| `third_party/test_sales_path_filter.py::test_enabled_toggle_on_shows_enabled_only` | SA-SLP-FLT-005 |  |
| `third_party/test_sales_path_filter.py::test_filter_button_opens_filter_panel` | SA-SLP-FLT-001 |  |
| `third_party/test_sales_path_filter.py::test_filter_by_exact_company_name` | SA-SLP-FLT-003 | 🔥 |
| `third_party/test_sales_path_filter.py::test_filter_by_partial_company_name` | SA-SLP-FLT-004 |  |
| `third_party/test_sales_path_filter.py::test_filter_panel_shows_expected_controls` | SA-SLP-FLT-002 |  |
| `third_party/test_sales_path_filter.py::test_filter_with_no_match_shows_empty_state` | SA-SLP-FLT-010 |  |
| `third_party/test_sales_path_filter.py::test_reset_filters_restores_full_list` | SA-SLP-FLT-011 |  |
| `third_party/test_sales_path_list.py::test_sales_path_count_updates_after_add` | SA-SLP-LST-008 |  |
| `third_party/test_sales_path_list.py::test_sales_path_empty_state` | SA-SLP-LST-007 |  |
| `third_party/test_sales_path_list.py::test_sales_path_list_has_expected_controls` | SA-SLP-LST-002 |  |
| `third_party/test_sales_path_list.py::test_sales_path_page_loads` | SA-SLP-LST-001 | 🔥 |
| `third_party/test_sales_path_list.py::test_sales_path_pagination_controls` | SA-SLP-LST-005 |  |
| `third_party/test_sales_path_list.py::test_sales_path_pagination_footer` | SA-SLP-LST-003 |  |
| `third_party/test_sales_path_list.py::test_sales_path_prev_page_disabled_on_first_page` | SA-SLP-LST-006 |  |
| `third_party/test_sales_path_list.py::test_sales_path_results_per_page_dropdown` | SA-SLP-LST-004 |  |

</details>

**Pending — 8 tests**

| Test | TC | Status | Reason (from marker) | Next action |
|---|---|---|---|---|
| `test_company_dropdown_lists_companies` (test_sales_path_create.py) | SA-SLP-CRT-003 | ⚠️ xfail | Company dropdown options depend on confirmed React Select combobox locator (CRT-002). | Confirm locator on staging, then implement |
| `test_create_sales_path_happy_path` (test_sales_path_create.py) | SA-SLP-CRT-008 | 🌱 seed | Seed test — staging data already exists. Re-run with --seed to re-initialize. | Seed-only by design (run with `--seed`) |
| `test_create_with_active_off` (test_sales_path_create.py) | SA-SLP-CRT-011 | 🟡 xfail/passing | 'Active Sales Path' toggle locator unconfirmed. | **Promote** — passed in last full run; remove xfail |
| `test_is_enabled_and_active_toggles_are_independent` (test_sales_path_create.py) | SA-SLP-CRT-006 | 🟡 xfail/passing | Verifying that 'Is Enabled' and 'Active' are independent requires confirmed toggle locators for both fields. | **Promote** — passed in last full run; remove xfail |
| `test_edit_form_prefills_company` (test_sales_path_edit.py) | SA-SLP-EDT-002 | ⚠️ xfail | Pre-filled Company React Select value depends on confirmed combobox locator — reading pre-filled value from React Select is not straightf… | Confirm locator on staging, then implement |
| `test_non_superadmin_cannot_reach_sales_path` (test_sales_path_edit.py) | SA-SLP-ACC-001 | ⏭️ skip | Access-control test requires a non-Superadmin browser session — no such fixture exists in this suite. | Needs non-superadmin session fixture |
| `test_toggle_active_persists` (test_sales_path_edit.py) | SA-SLP-EDT-004 | ⚠️ xfail | 'Active Sales Path' toggle locator not confirmed. | Confirm locator on staging, then implement |
| `test_toggle_is_enabled_persists` (test_sales_path_edit.py) | SA-SLP-EDT-003 | ⚠️ xfail | 'Is Enabled' toggle locator not confirmed; also need to confirm toggle state persists after save + re-open. | Confirm locator on staging, then implement |

Next actions for this module: Confirm locator on staging, then implement ×4; **Promote** — passed in last full run; remove xfail ×2; Seed-only by design (run with `--seed`) ×1; Needs non-superadmin session fixture ×1

## 6. Not in any CI job — legacy root files

14 tests in `tests/superadmin/*.py` root files run nowhere automatically. Most duplicate folder tests. Plan: move the `VK carwash role` setup into `users/conftest.py` (users seed data depends on it), port any unique assertion, then delete the files.

| Test |
|---|
| `test_companies.py::test_login_to_vktestcompany_admin_portal_ap_staging` |
| `test_companies.py::test_open_companies` |
| `test_create_company.py::test_open_create_company` |
| `test_create_user.py::test_cancel_create_user_does_not_create_user` |
| `test_create_user.py::test_create_user_and_confirm_in_users_list` |
| `test_create_user.py::test_create_user_invalid_email_validation` |
| `test_create_user.py::test_create_user_password_mismatch_validation` |
| `test_create_user.py::test_create_user_required_field_validation` |
| `test_create_user.py::test_create_vk_role_user_and_confirm_in_users_list` |
| `test_create_user.py::test_duplicate_user_email_validation` |
| `test_create_user_role.py::test_create_vk_carwash_role_with_all_permissions_except_create_company` |
| `test_edit_company.py::test_cancel_discards_terms_condition_changes` |
| `test_edit_company.py::test_open_edit_company_page` |
| `test_edit_company.py::test_update_terms_condition_and_restore_original` |
