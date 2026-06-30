# NxtWash Automation — Framework & Module Overview

**Audience:** QA engineers new to this codebase  
**Scope:** Project structure, Login module, Service Categories module

---

## 1. Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Language |
| Selenium 4 | Browser automation |
| pytest 9 | Test runner |
| Allure | HTML/visual test reporting |
| pytest-xdist | Parallel test execution |
| pytest-timeout | Per-test 180-second watchdog |
| webdriver-manager | ChromeDriver binary resolution |
| PyYAML + python-dotenv | Config and secret management |

---

## 2. Project Folder Structure

```
nxtwash-automation/
│
├── config/               # Environment YAML files
│   ├── staging.yaml      # URLs for staging environment
│   ├── production.yaml   # URLs for production environment
│   └── users.yaml        # (reference) user role definitions
│
├── core/                 # Framework internals
│   ├── config_manager.py # Reads config/*.yaml + .env for URLs & credentials
│   └── driver_factory.py # Chrome WebDriver factory (headless/normal/CI flags)
│
├── fixtures/
│   └── browser.py        # pytest `browser` fixture — one Chrome per test
│
├── pages/                # Page Object Model (POM) layer
│   ├── common/
│   │   └── base_page.py  # Shared wait/click/enter/React-dropdown helpers
│   ├── admin_portal/     # One file per Admin Portal screen
│   │   ├── login_page.py
│   │   ├── service_categories_page.py
│   │   ├── sidebar.py
│   │   ├── overview_page.py
│   │   └── ... (wash_packages, memberships, discounts, etc.)
│   └── superadmin/       # Super-Admin portal pages
│
├── tests/                # Test files — mirrors pages/ structure
│   ├── admin_portal/
│   │   ├── _managed.py           # Shared "managed data" pattern
│   │   ├── _bugs.py              # Known-bug placeholders
│   │   ├── admin_session.py      # Session helper (login + retry logic)
│   │   ├── login/                # Login test suite
│   │   └── service_categories/   # Service Categories test suite
│   └── superadmin/
│
├── conftest.py           # Root pytest config (env, markers, Allure, screenshots)
├── pytest.ini            # Marker definitions and global addopts
├── requirements.txt      # Python dependencies
├── .env                  # Secrets (not committed — gitignored)
└── .env.example          # Template showing required env var names
```

---

## 3. How Configuration and Secrets Work

### 3.1 Environment selection

The target environment (`staging` or `production`) is selected at runtime:

```
pytest --env staging    # explicit flag
TEST_ENV=staging pytest # or via env variable
# default: staging
```

`conftest.py::pytest_configure` writes the chosen value into `os.environ["TEST_ENV"]` so every process (including xdist workers) picks it up.

### 3.2 ConfigManager (`core/config_manager.py`)

`ConfigManager` is instantiated inside every Page Object that needs URLs or credentials.

```
ConfigManager()
  ↓ reads os.environ["TEST_ENV"]          → "staging"
  ↓ opens config/staging.yaml             → {"admin_portal": {"url": "https://staging.nxtwash.com/"}, ...}
  ↓ reads .env file (via python-dotenv)   → ADMIN_PORTAL_USERNAME, ADMIN_PORTAL_PASSWORD, etc.
```

Key methods:

| Method | Returns |
|---|---|
| `get_url("admin_portal")` | Portal base URL from YAML |
| `get_username("admin_portal")` | Value of `ADMIN_PORTAL_USERNAME` from `.env` |
| `get_password("admin_portal")` | Value of `ADMIN_PORTAL_PASSWORD` from `.env` |

Credentials are **never** in YAML — only in `.env` (local) or GitHub Actions secrets (CI).

### 3.3 Required `.env` variables

```
ADMIN_PORTAL_USERNAME=...
ADMIN_PORTAL_PASSWORD=...
SUPERADMIN_USERNAME=...
SUPERADMIN_PASSWORD=...
```

---

## 4. Browser Fixture (`fixtures/browser.py`)

```
pytest collects a test
  ↓
`browser` fixture is requested
  ↓
DriverFactory.get_driver(headless=...) creates a Chrome instance
  ↓ (pinned ChromeDriver binary or webdriver-manager fallback)
  ↓ headless: adds CI-safe Chrome flags (--headless=new, --no-sandbox, etc.)
  ↓ maximise window (non-headless)
  ↓
driver is yielded to the test
  ↓
test runs
  ↓
teardown: navigate to about:blank → driver.quit()
```

**Scope:** One Chrome per test function (default). Pass `--single-window` for session-scoped (shared window) — useful for quick local runs.

**Timeout patch:** `fixtures/browser.py` patches `Selenium.Service._terminate_process` to use a 3-second wait instead of the upstream 60-second default, so a frozen Chrome doesn't block the entire run.

---

## 5. Page Object Model — BasePage

`pages/common/base_page.py` is the parent class for every Page Object.

| Method | What it does |
|---|---|
| `click(locator)` | Waits 20 s for element to be clickable, then clicks |
| `enter_text(locator, text)` | Cmd+A → Backspace to clear, then sends text (React-safe) |
| `get_text(locator)` | Waits for visibility, returns `.text` |
| `select_react_dropdown_option(locator, text)` | Opens a React Select, types to filter, JS-clicks the matching option |
| `_find_react_option(text)` | JS scan for `[role="option"]` or CSS-class-based options across portals |

All waits default to **20 seconds** (`WebDriverWait(driver, 20)`).

---

## 6. Login Module

### 6.1 Files involved

```
pages/admin_portal/login_page.py          ← Page Object
tests/admin_portal/login/conftest.py      ← Fixtures
tests/admin_portal/login/test_login_positive.py
tests/admin_portal/login/test_login_negative.py
tests/admin_portal/login/test_login_ui.py
tests/admin_portal/login/test_login_session.py
tests/admin_portal/login/test_login_validation.py
tests/admin_portal/login/test_login_password.py
tests/admin_portal/login/test_login_security_smoke.py
tests/admin_portal/admin_session.py      ← Shared session helper (used by all modules)
```

### 6.2 Page Object: `AdminLoginPage`

Inherits `BasePage`. Adds login-specific locators and methods.

**Key locators:**

| Constant | Element |
|---|---|
| `EMAIL_OR_PHONE_INPUT` | `name="emailOrPhone"` |
| `PASSWORD_INPUT` | `name="password"` |
| `LOGIN_BUTTON` | `type="submit"` |
| `OVERVIEW_TITLE` | The `"Overview"` heading (post-login) |
| `PASSWORD_VISIBILITY_BUTTON` | Eye icon next to password field |

**Key methods and what they do:**

```
open()
  → driver.get( config.get_url("admin_portal") )

wait_for_loaded()
  → Asserts URL contains /login
  → Waits for: title, email input, password input, submit button (30 s)

login()
  → Reads ADMIN_PORTAL_USERNAME / ADMIN_PORTAL_PASSWORD from .env
  → Calls login_with(username, password)

login_with(email, password)
  → enter_email_or_phone(email)
  → enter_password(password)
  → click_login()

wait_for_overview()
  → Waits up to 60 s for URL == base URL and "Overview" heading visible
  → 60 s (not 30 s) because CI runners are CPU-constrained

authenticated_session_is_stored()
  → Reads localStorage["persist:root"]
  → Parses JSON → checks isAuthorized == true && accessToken is set
  → Returns True/False (used as fast-path skip in session helper)

visible_error_text()
  → Reads full body text, lowercases it
  → Returns body text if any of ["invalid","incorrect","unauthorized",...] found
  → Returns "" if no error is present
```

### 6.3 Login Test Fixtures (`tests/admin_portal/login/conftest.py`)

```python
@pytest.fixture
def login_page(browser):
    page = AdminLoginPage(browser)
    page.open()           # navigate to /login
    page.wait_for_loaded()  # block until form is ready
    return page

@pytest.fixture
def login_credentials(login_page):
    return (username, password)   # tuple read from .env via ConfigManager
```

Every login test gets a fresh browser (function scope) and a freshly opened login page.

### 6.4 Login Flow (step by step)

```
Test starts
  ↓
`browser` fixture → new Chrome window
  ↓
`login_page` fixture
  → AdminLoginPage(browser)
  → page.open() → driver.get("https://staging.nxtwash.com/")
     (SPA redirects to /login automatically)
  → page.wait_for_loaded()
     → waits for URL contains /login
     → waits for email field, password field, submit button
  ↓
Test calls page.login() or page.login_with(email, password)
  → enter_email_or_phone(): BasePage.enter_text() → Cmd+A + Backspace + send_keys
  → enter_password():        BasePage.enter_text()
  → click_login():           BasePage.click(LOGIN_BUTTON)
  ↓
SPA submits credentials to backend API
  ↓
On success: SPA redirects to https://staging.nxtwash.com/ (no /login)
  ↓
page.wait_for_overview()
  → Waits for URL == base URL
  → Waits for "Overview" text visible
  ↓
Test assertions run
```

### 6.5 Login Test Coverage

| File | What it covers |
|---|---|
| `test_login_positive.py` | Valid credentials, Enter-key submit, session refresh, auth redirect guard, email case-insensitivity, trailing space trim, new tab session persistence |
| `test_login_negative.py` | Wrong email, wrong password, both wrong |
| `test_login_ui.py` | Page load, URL, field labels, tab order, footer, browser title, password visibility toggle |
| `test_login_session.py` | Redirect to /login when no auth, auth token stored in localStorage after login |
| `test_login_validation.py` | Empty field submit, field-level browser validation messages |
| `test_login_password.py` | Password masking (type="password"), visibility toggle switches to type="text" |
| `test_login_security_smoke.py` | Session not leaking across cookie-cleared tabs |

### 6.6 Session Helper (`tests/admin_portal/admin_session.py`)

All non-login tests use `open_admin_path(browser, path)` instead of managing login themselves.

```
open_admin_path(browser, "/services/serviceCategories")
  ↓
ensure_admin_logged_in(browser)
  → Check: is host in current URL? If not → navigate to base URL
  → Fast path: already past /login AND localStorage shows authorized → return
  → Retry loop (up to 3 attempts):
      wait_for_loaded() → login() → wait_for_overview()
      If TimeoutException → navigate back to base URL and retry
  ↓
browser.get(base_url + "/services/serviceCategories")
  ↓
Check: did SPA bounce back to /login? (2-second probe)
  → If yes and attempts remain → re-run ensure_admin_logged_in and retry
  → If still bouncing after all attempts → raise
  ↓
Test proceeds
```

This means every module test is **self-healing**: if a session expires mid-run, it re-authenticates automatically.

---

## 7. Service Categories Module

### 7.1 Files involved

```
pages/admin_portal/service_categories_page.py     ← Page Object
tests/admin_portal/service_categories/conftest.py ← Fixtures + helpers
tests/admin_portal/service_categories/test_service_categories_positive.py
tests/admin_portal/service_categories/test_service_categories_negative.py
tests/admin_portal/service_categories/test_service_categories_edit.py
tests/admin_portal/service_categories/test_service_categories_validation.py
tests/admin_portal/service_categories/test_service_categories_ui.py
tests/admin_portal/service_categories/test_service_categories_search_filter.py
tests/admin_portal/service_categories/test_service_categories_filter.py
tests/admin_portal/service_categories/test_service_categories_edge_cases.py
tests/admin_portal/service_categories/test_service_categories_dependency.py
tests/admin_portal/service_categories/test_service_categories_managed.py
```

### 7.2 The iframe Architecture

The Admin Portal embeds feature modules in `<iframe>` elements. Service Categories uses three distinct iframe URLs:

| Frame constant | Matches | Used when |
|---|---|---|
| `LIST_FRAME` | `.../services/serviceCategories` (no trailing path) | List / grid view |
| `CREATE_FRAME` | `.../services/serviceCategories/new` | Create form |
| `EDIT_FRAME` | `.../services/serviceCategories/{id}` (not `/new`) | Edit form |

**Before interacting with any element, the driver must switch into the correct frame:**

```python
def switch_to_module_frame(self):
    self.driver.switch_to.default_content()   # exit any current frame
    self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.FRAME))
```

Every navigation back to the list calls `driver.switch_to.default_content()` first so stale frame references don't cause errors.

### 7.3 Page Object: `ServiceCategoriesPage`

**Key locators:**

| Constant | Element |
|---|---|
| `PAGE_TITLE` | `"Service categories"` heading |
| `SEARCH_INPUT` | `name="categoryName"` search box |
| `FILTER_BUTTON` | `"Filter by"` button |
| `ADD_CATEGORY_BUTTON` | `"+ Add new category"` button |
| `GRID_ROWS` | All `InovuaReactDataGrid__row` elements that contain a `categoryName` cell |
| `GRID_LOAD_MASK` | The loading overlay on the InovaDataGrid |
| `CATEGORY_NAME_INPUT` | `name="categoryName"` on create/edit form |
| `ACTIVE_SWITCH` | Toggle button next to "Active service" label |
| `SAVE_NEW_BUTTON` | `"Save new category"` |
| `SAVE_CHANGES_BUTTON` | Any button containing `"Save"` (edit form) |

### 7.4 Data Flow: Creating a Category

```
test calls: page.create_category("VK ASC1")
  ↓
open_create_category()
  → wait_for_list_loaded()          ← switches to LIST_FRAME, waits for grid
  → click(ADD_CATEGORY_BUTTON)      ← "+ Add new category"
  → wait_for_create_loaded()        ← switches to CREATE_FRAME, waits for form
  ↓
enter_category_name("VK ASC1")
  → _set_input_value(element, value)
     → JS: set value via HTMLInputElement setter
     → JS: dispatch 'input' event (bubbles: true)
     → JS: dispatch 'change' event (bubbles: true)
     (React synthetic events require this — standard send_keys don't trigger React's onChange)
  ↓
ensure_active_switch_on()
  → reads aria-checked on the switch button
  → if not "true" → switch.click() → waits for aria-checked == "true"
  ↓
click_save_new()
  → BasePage.click(SAVE_NEW_BUTTON)
  ↓
wait_for_list_loaded()
  → switch back to LIST_FRAME
  → wait for page title, Add button, grid idle (load mask gone)
  ↓
Category now exists in the grid
```

**Why `_set_input_value` instead of `send_keys`?**  
React manages form state internally. A plain `send_keys` updates the visible text but does not trigger React's internal `onChange`, so React never registers the value. The JavaScript approach uses the native property setter (bypassing React's override) then fires synthetic DOM events that React is listening for.

### 7.5 Data Flow: Editing a Category

```
page.open_edit_category("VK ASC1")
  ↓
wait_for_list_loaded()
search_category("VK ASC1")         ← Ctrl+A + Backspace + send_keys, wait for grid idle
  ↓
wait_for_category_row("VK ASC1")
  → XPath: grid row containing a categoryName cell with span text == "VK ASC1"
  ↓
(if row not found → apply inactive filter and retry)
  ↓
find Edit link inside the row → JS click (avoids scroll issues)
  ↓
wait_for_edit_loaded()
  → switch to EDIT_FRAME
  → wait for category name input visible
  → wait for Save button clickable
  → wait for input value != "" (form hydrated with data)
  ↓
Test interacts: enter_category_name(), ensure_active_switch_on/off()
  ↓
click_save_changes()
  → patches window.confirm = () => true
     (app shows a native confirm dialog when deactivating;
      headless Chrome auto-dismisses dialogs with "false" which cancels the save)
  → sleep 0.5 s → click Save
  ↓
wait_for_list_loaded() → back to grid
```

### 7.6 Search and Filter Flow

**Search:**
```
search_category("VK ASC1")
  → wait for SEARCH_INPUT clickable
  → click → Ctrl+A → Backspace    (clear existing value, React-safe)
  → send_keys("VK ASC1")
  → wait until input.value == "VK ASC1"
  → wait_for_grid_idle()           (load mask disappears)
```

**Filter (Active/Inactive):**
```
open_filter_panel()
  → wait for list loaded
  → JS click "Filter by" button
  → wait for Apply/Reset/Switch to appear (panel open)
  ↓
set_active_category_filter(False)   ← toggle aria-checked to "false"
  ↓
apply_filters()
  → JS click "Apply filters"
  → wait for Apply button to disappear
  → wait for grid idle
  → wait for stale pre-filter rows (DOM re-rendered)
  ↓
Grid now shows inactive categories
```

**Reset:**
```
reset_filters()
  → open_filter_panel()
  → JS click "Reset all"
```

### 7.7 Accessing Inactive Categories

The grid's **default view shows only Active categories**. To reach an inactive one, the page object has a two-step fallback built into `open_edit_category` and `category_exists`:

```
search_category(name)
  → if wait_for_category_row(name) succeeds → proceed
  → if TimeoutException:
      _show_inactive_categories()
        → clear_category_search()   (Filter button is disabled on empty-results grid)
        → open_filter_panel()
        → set_active_category_filter(False)
        → apply_filters()
      search_category(name)
      wait_for_category_row(name)
```

After accessing an inactive record, `_reset_to_default_view()` clears the filter to leave the grid in its default state for the next test.

### 7.8 Managed Test Data Pattern

Service Categories (like most Admin entities) **cannot be deleted** through the product UI. To avoid data accumulation:

- Each feature maintains a **single dedicated "managed" record** per test that needs mutation.
- The record is named `"AUTOTEST Category"` (via `managed_name("Category")`).
- A `managed_resource(reset_fn)` factory wraps the reset function in a pytest fixture that runs it **both before and after** the test.

```python
# conftest.py
MANAGED_CATEGORY = "AUTOTEST Category"

def reset_managed_category(browser):
    page = open_service_categories_page(browser)
    # Case 1: was renamed → rename back
    # Case 2: does not exist → create it
    # Case 3: was deactivated → re-activate
    return page

managed_category = managed_resource(reset_managed_category)

# test file
def test_deactivate_service_category(managed_category):
    page = managed_category        # fixture: reset ran → known baseline
    page.open_edit_category(MANAGED_CATEGORY)
    page.ensure_active_switch_off()
    page.click_save_changes()
    ...
    # fixture teardown: reset runs again → baseline restored
```

This guarantees every test starts and ends with a predictable data state.

### 7.9 Service Categories Test Coverage

| File | What it covers |
|---|---|
| `test_service_categories_positive.py` | Create active/inactive, edit name, activate/deactivate, settings persist |
| `test_service_categories_edit.py` | Rename and restore baseline (CRUD round-trip) |
| `test_service_categories_negative.py` | Duplicate name, invalid inputs |
| `test_service_categories_validation.py` | Required name field, blank form stays on page |
| `test_service_categories_ui.py` | Page title, search input, filter/download buttons, grid columns, pagination |
| `test_service_categories_search_filter.py` | Partial search, case-insensitivity, clear search restores grid |
| `test_service_categories_filter.py` | Active filter shows only active, inactive filter shows inactive |
| `test_service_categories_edge_cases.py` | Activate→deactivate→activate cycle, inactive findable via filter |
| `test_service_categories_managed.py` | Managed record baseline and rename/restore via managed fixture |
| `test_service_categories_dependency.py` | Category linked to services — dependency validation |

---

## 8. Allure Reporting

Every test file declares its place in the Allure hierarchy:

```python
pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Happy Path"),
]
```

Individual tests add `@allure.title("SC-HP-001 Create Active Category")` for a readable test ID in the report.

**Run with Allure:**
```bash
pytest tests/admin_portal/service_categories/ \
    --alluredir=allure-results
allure serve allure-results
```

**Failure artifacts** are captured automatically by `conftest.py::pytest_runtest_makereport`:
- Screenshot (PNG) → saved to `screenshots/` + attached to Allure
- Page source (HTML) → saved to `logs/` + attached to Allure
- Failing URL → attached as text

---

## 9. Quarantine / Known Failures

Tests that are intermittently failing due to a known product-side timing issue are marked `xfail(strict=False)` automatically by `conftest.py::pytest_collection_modifyitems`.

```python
_QUARANTINE_TIMING = (
    "test_service_categories_positive.py::test_activate_service_category",
    ...
)
```

`strict=False` means:
- If the test fails → reported as `xfail` (expected, suite stays green)
- If the test passes → reported as `xpass` (a pleasant surprise, not a failure)

The root-cause notes and fix backlog live in `docs/admin_test_burndown.md`.

---

## 10. How to Run Tests

```bash
# All tests (staging, headed Chrome)
pytest tests/

# Login suite only
pytest tests/admin_portal/login/

# Service Categories only
pytest tests/admin_portal/service_categories/

# Smoke tests only
pytest -m smoke

# Headless (CI mode)
pytest --headless tests/

# Against production (read-only prod_smoke tests)
pytest -m prod_smoke --env production

# Parallel (4 workers)
pytest -n 4 tests/

# With Allure report
pytest --alluredir=allure-results tests/
allure serve allure-results
```

---

## 11. Data Ownership Summary

| Record name prefix | Owner | Purpose |
|---|---|---|
| `AUTOTEST *` | Framework (managed fixture) | Single mutable record per feature, reset before/after each test |
| `VK ASC1` / `VK ASC2` | Test setup helpers | Disposable records created if missing; never deleted |
| `category-does-not-exist-automation` | Constant | Sentinel value used in negative/search tests |

Records prefixed `AUTOTEST` are safe to identify as automation-owned data in the product UI.
