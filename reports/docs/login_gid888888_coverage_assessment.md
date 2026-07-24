# Login Coverage Assessment - Google Sheet gid=888888

Generated: 2026-06-11

## Executive Summary

- Sheet tab analyzed: `gid=888888`, exported as CSV from Google Sheets.
- Module in sheet: Admin Portal Login.
- Manual test cases extracted: 49.
- Existing and updated automation files reviewed under `tests/admin_portal/login/` and `pages/admin_portal/login_page.py`.
- Impacted suite result after implementation: `42 passed, 3 xfailed`.
- Allure results: `reports/allure-results-login`.
- Allure HTML report: `reports/allure-report-login`.

Limitations:

- CSV export does not expose Google Sheets row metadata such as hidden/grouped/filter state. All exported rows were analyzed.
- Several sheet rows have blank expected-result cells. Coverage was only marked from actual executable assertions; blank expectations were not inferred as covered unless the test behavior is explicit in code.
- Inactive, deleted, locked, and expired-password user tests require dedicated test users or backend setup. No such test data exists in the repository.

## Framework Summary

- Language: Python.
- Automation stack: Selenium WebDriver, Pytest.
- Design pattern: Page Object Model.
- Reporting: Allure via `allure-pytest`.
- Shared fixtures: root `conftest.py`, `fixtures/browser.py`.
- Login page object: `pages/admin_portal/login_page.py`.
- Login tests: `tests/admin_portal/login/`.
- Synchronization: explicit waits through `WebDriverWait` and base page helper methods.
- CI/CD: GitHub Actions workflow exists under `.github/workflows/tests.yml`.

## Files Modified

- `pages/admin_portal/login_page.py`
- `tests/admin_portal/login/test_login_ui.py`
- `tests/admin_portal/login/test_login_positive.py`
- `tests/admin_portal/login/test_login_validation.py`
- `tests/admin_portal/login/test_login_security_smoke.py`
- `tests/admin_portal/login/test_login_password.py`

## New/Updated Page Object Methods

- `get_logo_src()` - validates rendered logo source.
- `email_label_is_visible()` / `password_label_is_visible()` - validates the actual label-based UI.
- `email_field_is_enabled()` / `password_field_is_enabled()` - validates enabled state.
- `focus_email_field()`, `active_element_name()`, `active_element_type()`, `press_tab()` - validates tab order.
- `open_overview_in_new_tab()` - validates same-session multi-tab access.
- Password visibility locator updated to target the visible control container.

## Coverage Metrics

| Metric | Count |
| --- | ---: |
| Total manual test cases | 49 |
| Fully automated | 32 |
| Partially automated | 7 |
| Not automated | 10 |
| Strict expected failures | 3 |

Fully automated coverage: 65.31%.

Effective coverage including partial executable coverage: 79.59%.

## Coverage Matrix

| TC ID | Scenario | Status | Evidence |
| --- | --- | --- | --- |
| LOGIN-UI-001 | Login page loads successfully | Fully Automated | `test_login_page_loads`, `test_login_ui.py:6`; asserts login URL state and `Log in`, `test_login_ui.py:10-11` |
| LOGIN-UI-002 | Login page URL is correct | Fully Automated | `test_login_page_url_is_correct`, `test_login_ui.py:14`; asserts exact `/login`, `test_login_ui.py:18-20` |
| LOGIN-UI-003 | Browser title displayed correctly | Fully Automated | `test_login_browser_title`, `test_login_ui.py:69`; asserts `Admin Portal NxtWash`, `test_login_ui.py:73` |
| LOGIN-UI-004 | NxtWash logo visible | Partially Automated | `test_login_logo_is_available`, `test_login_ui.py:23`; asserts logo DOM presence and NxtWash source, `test_login_ui.py:27-28`; Selenium visible check is unreliable in current headless layout |
| LOGIN-UI-005 | Email field visible and enabled | Fully Automated | `test_login_fields_and_button_are_visible`, `test_login_ui.py:31`; asserts visible/enabled, `test_login_ui.py:35-36` |
| LOGIN-UI-006 | Password field visible and enabled | Fully Automated | `test_login_fields_and_button_are_visible`, `test_login_ui.py:31`; asserts visible/enabled, `test_login_ui.py:37-38` |
| LOGIN-UI-007 | Password visibility icon displayed | Fully Automated | `test_password_visibility_icon_is_displayed`, `test_login_ui.py:43`; asserts icon/control exists, `test_login_ui.py:47-50` |
| LOGIN-UI-008 | Login button visible | Fully Automated | `test_login_fields_and_button_are_visible`, `test_login_ui.py:31`; asserts visible, `test_login_ui.py:39` |
| LOGIN-UI-009 | Login button enabled on load | Fully Automated | `test_login_fields_and_button_are_visible`, `test_login_ui.py:31`; asserts enabled, `test_login_ui.py:40` |
| LOGIN-UI-010 | Email placeholder text | Partially Automated | Current DOM has label `Email`, no placeholder attribute. Label coverage: `test_login_field_labels_are_displayed`, `test_login_ui.py:53`; `test_login_ui.py:57` |
| LOGIN-UI-011 | Password placeholder text | Partially Automated | Current DOM has label `Password`, no placeholder attribute. Label coverage: `test_login_field_labels_are_displayed`, `test_login_ui.py:53`; `test_login_ui.py:58` |
| LOGIN-UI-012 | Footer text displayed | Fully Automated | `test_login_footer_is_displayed`, `test_login_ui.py:61`; asserts footer text, `test_login_ui.py:65-66` |
| LOGIN-UI-013 | Layout renders after refresh | Fully Automated | `test_login_layout_renders_after_refresh`, `test_login_ui.py:76`; asserts key controls after refresh, `test_login_ui.py:80-86` |
| LOGIN-UI-014 | Tab order Email -> Password -> Login | Fully Automated | `test_login_tab_order_email_password_login_button`, `test_login_ui.py:89`; asserts active elements, `test_login_ui.py:93-100` |
| LOGIN-POS-001 | Valid credentials | Fully Automated | `test_login_with_valid_credentials`, `test_login_positive.py:7`; asserts URL and Overview, `test_login_positive.py:11-15` |
| LOGIN-POS-002 | Redirect to dashboard | Fully Automated | `test_login_with_valid_credentials`, `test_login_positive.py:7`; URL assertion, `test_login_positive.py:14` |
| LOGIN-POS-003 | Login using Enter key | Fully Automated | `test_login_using_enter_key`, `test_login_positive.py:18`; asserts Overview, `test_login_positive.py:23-26` |
| LOGIN-POS-004 | Session persists after refresh | Fully Automated | `test_session_persists_after_refresh`, `test_login_positive.py:29`; asserts Overview after refresh, `test_login_positive.py:33-38` |
| LOGIN-POS-005 | Authenticated user cannot access login page | Fully Automated | `test_authenticated_user_cannot_access_login_page`, `test_login_positive.py:41`; asserts `/login` absent, `test_login_positive.py:45-50` |
| LOGIN-POS-006 | Dashboard elements visible after login | Fully Automated | `test_login_with_valid_credentials`, `test_login_positive.py:7`; asserts Overview, `test_login_positive.py:15` |
| LOGIN-POS-007 | Session active in new tab | Fully Automated | `test_session_remains_active_in_new_tab`, `test_login_positive.py:90`; asserts Overview in new tab, `test_login_positive.py:94-99` |
| LOGIN-VAL-001 | Both fields empty | Fully Automated | `test_login_validation_both_fields_empty`, `test_login_validation.py:6`; asserts login page, email toast, no Overview, `test_login_validation.py:10-15` |
| LOGIN-VAL-002 | Email empty | Fully Automated | `test_login_validation_email_empty`, `test_login_validation.py:18`; asserts email toast, `test_login_validation.py:22-28` |
| LOGIN-VAL-003 | Password empty | Fully Automated | `test_login_validation_password_empty`, `test_login_validation.py:31`; asserts password toast, `test_login_validation.py:35-41` |
| LOGIN-VAL-004 | Email spaces only | Fully Automated | `test_login_validation_email_spaces_only`, `test_login_validation.py:44`; asserts login blocked, `test_login_validation.py:48-52` |
| LOGIN-VAL-005 | Password spaces only | Fully Automated | `test_login_validation_password_spaces_only`, `test_login_validation.py:55`; asserts login blocked, `test_login_validation.py:59-63` |
| LOGIN-VAL-006 | Invalid email formats | Fully Automated | `test_login_validation_invalid_email_formats`, `test_login_validation.py:66`; covers all listed formats, `test_login_validation.py:68-86` |
| LOGIN-VAL-007 | Leading spaces in email | Incorrectly Automated / Product Gap | `test_login_with_email_leading_space`, `test_login_positive.py:57`; strict xfail because app does not trim leading spaces, `test_login_positive.py:53-65` |
| LOGIN-VAL-008 | Trailing spaces in email | Fully Automated | `test_login_with_email_trailing_space`, `test_login_positive.py:68`; asserts login succeeds, `test_login_positive.py:73-76` |
| LOGIN-VAL-009 | Email case variation | Fully Automated | `test_login_with_email_case_variation`, `test_login_positive.py:79`; asserts login succeeds, `test_login_positive.py:84-87` |
| LOGIN-VAL-010 | Maximum email length | Fully Automated | `test_login_validation_maximum_email_length_does_not_break_ui`, `test_login_validation.py:89`; asserts no UI break/login blocked, `test_login_validation.py:94-101` |
| LOGIN-NEG-001 | Invalid email + valid password | Fully Automated | `test_login_invalid_email_valid_password_does_not_authenticate`, `test_login_negative.py:5`; asserts login page/no Overview |
| LOGIN-NEG-002 | Valid email + invalid password | Fully Automated | `test_login_valid_email_invalid_password_does_not_authenticate`, `test_login_negative.py:17`; asserts login page/no Overview |
| LOGIN-NEG-003 | Invalid email + invalid password | Fully Automated | `test_login_invalid_email_invalid_password_does_not_authenticate`, `test_login_negative.py:29`; asserts login page/no Overview |
| LOGIN-NEG-004 | Inactive user login | Not Automated | No inactive-user credentials/test data found |
| LOGIN-NEG-005 | Deleted user login | Not Automated | No deleted-user credentials/test data found |
| LOGIN-NEG-006 | Locked user login | Not Automated | No locked-user workflow/test data found |
| LOGIN-NEG-007 | Expired password login | Not Automated | No expired-password workflow/test data found |
| LOGIN-NEG-008 | Parametrized invalid tuples | Partially Automated | Negative tuple coverage exists across `test_login_negative.py:5`, `:17`, `:29`; expected error text is not asserted |
| LOGIN-SESSION-001 | Direct dashboard URL without login | Fully Automated | `test_direct_protected_url_without_login_redirects_to_login`, `test_login_session.py:4`; clears storage and asserts login page, `test_login_session.py:7-14` |
| LOGIN-SESSION-002 | Logout successfully | Not Automated | No logout POM method or logout test exists |
| LOGIN-SESSION-003 | Browser back after logout | Not Automated | Depends on logout automation |
| LOGIN-SESSION-004 | Dashboard URL after logout | Not Automated | Depends on logout automation |
| LOGIN-SESSION-005 | Second tab after logout | Not Automated | Depends on logout automation |
| LOGIN-SESSION-006 | Session survives refresh | Fully Automated | `test_session_persists_after_refresh`, `test_login_positive.py:29`; `test_login_positive.py:33-38` |
| LOGIN-SEC-001 | SQL injection in email | Fully Automated | `test_login_security_payloads_do_not_authenticate`, `test_login_security_smoke.py:6`; payload row `test_login_security_smoke.py:9`, assertions `:19-23` |
| LOGIN-SEC-002 | SQL injection in password | Fully Automated | `test_login_security_payloads_do_not_authenticate`, `test_login_security_smoke.py:6`; payload row `test_login_security_smoke.py:10`, assertions `:19-23` |
| LOGIN-SEC-003 | XSS in email | Fully Automated | `test_login_security_payloads_do_not_authenticate`, `test_login_security_smoke.py:6`; payload row `test_login_security_smoke.py:11`, assertions `:19-23` |
| LOGIN-SEC-004 | XSS in password | Fully Automated | `test_login_security_payloads_do_not_authenticate`, `test_login_security_smoke.py:6`; payload row `test_login_security_smoke.py:12`, assertions `:19-23` |

## Gap Analysis

High priority:

- Logout workflow coverage is missing: LOGIN-SESSION-002 through LOGIN-SESSION-005.
- User-state negative coverage is missing: inactive, deleted, locked, expired-password users.

Product/UI gaps detected by automation:

- LOGIN-VAL-007: valid email with leading space is not trimmed; strict xfail.
- Password visibility behavior: icon exists initially, but disappears after typing; strict xfail for show/hide behavior.
- LOGIN-UI-010 and LOGIN-UI-011: sheet expects placeholders, but current UI uses labels and empty placeholder attributes.

Duplicate/overlap:

- LOGIN-NEG-008 overlaps LOGIN-NEG-001 through LOGIN-NEG-003. Recommendation: keep the existing explicit tests and add one parameterized assertion layer only if detailed error-message requirements are finalized.

## Automation Improvement Plan

Phase 1 - Critical Fixes:

| TC ID | Priority | Effort | Recommendation |
| --- | --- | --- | --- |
| LOGIN-SESSION-002 | P1 | Medium | Add logout POM methods and assert login page plus cleared auth state |
| LOGIN-SESSION-003 | P1 | Medium | Reuse logout flow, then browser back and assert dashboard inaccessible |
| LOGIN-SESSION-004 | P1 | Medium | Reuse logout flow, open protected URL, assert redirect |
| LOGIN-SESSION-005 | P1 | Medium | Reuse logout flow, second tab protected access, assert redirect |

Phase 2 - Coverage Improvements:

| TC ID | Priority | Effort | Recommendation |
| --- | --- | --- | --- |
| LOGIN-NEG-004 | P2 | Medium | Add inactive-user test data and assert denied login |
| LOGIN-NEG-005 | P2 | Medium | Add deleted-user test data and assert denied login |
| LOGIN-NEG-006 | P2 | Medium | Add locked-user setup/test data and assert denied login |
| LOGIN-NEG-007 | P2 | Medium | Add expired-password user fixture and assert denied login |

Phase 3 - Product Alignment:

| TC ID | Priority | Effort | Recommendation |
| --- | --- | --- | --- |
| LOGIN-VAL-007 | P2 | Small | Fix app trim behavior or update manual expectation; remove xfail after fix |
| LOGIN-UI-010 | P3 | Small | Either add placeholder attributes or update manual case to validate labels |
| LOGIN-UI-011 | P3 | Small | Either add placeholder attributes or update manual case to validate labels |

## Final Execution

Command:

```bash
venv/bin/pytest tests/admin_portal/login --headless --close-browser --alluredir=reports/allure-results-login --clean-alluredir
```

Result:

```text
42 passed, 3 xfailed in 219.64s
```

Allure report generated:

```bash
PATH="/opt/homebrew/opt/openjdk/bin:$PATH" npx allure-commandline generate reports/allure-results-login -o reports/allure-report-login --clean
```
