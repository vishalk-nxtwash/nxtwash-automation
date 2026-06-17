# NxtWash Automation Framework

UI Automation Framework for:

- SuperAdmin Portal
- Admin Portal
- POS App
- Tunnel App
- Customer Portal

## Tech Stack

- Python (3.10+)
- Selenium
- Pytest
- Allure + pytest-html (reporting)

## Prerequisites

- Python 3.10 or newer
- Google Chrome installed (ChromeDriver is downloaded automatically by `webdriver-manager`)

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS / Linux
   # .\venv\Scripts\activate       # Windows (PowerShell)
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure credentials. Copy the example file and fill in real values:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```
   SUPERADMIN_USERNAME=your_superadmin_email
   SUPERADMIN_PASSWORD=your_superadmin_password
   ADMIN_PORTAL_USERNAME=your_admin_email
   ADMIN_PORTAL_PASSWORD=your_admin_password
   ```

   `.env` is git-ignored and never committed. Tests that only check the
   login/UI screens run without credentials; tests that log in require them.

## Configuration

- Environment URLs live in `config/staging.yaml` and `config/production.yaml`.
- Default environment is **staging**. Switch at runtime with `--env` or the
  `TEST_ENV` environment variable:

  ```bash
  pytest --env production
  TEST_ENV=production pytest
  ```

- Credentials are read from environment variables (loaded from `.env`).

## Running Tests

Run the full suite:

```bash
pytest
```

Run a specific portal, folder, file, or single test:

```bash
pytest tests/admin_portal/
pytest tests/admin_portal/login/
pytest tests/admin_portal/login/test_login_ui.py
pytest tests/admin_portal/login/test_login_ui.py::test_login_page_loads
```

### Markers

Tests are auto-tagged by location, so you can slice the suite without manual
decorators:

| Marker        | Selects                                  |
| ------------- | ---------------------------------------- |
| `admin`       | everything under `tests/admin_portal/`   |
| `superadmin`  | everything under `tests/superadmin/`     |
| `smoke`       | login flows, `*_positive`, `*_smoke`     |

`admin`, `superadmin`, and `smoke` are applied automatically by path. Suites
also tag tests by intent via decorators — `sanity`, `regression`, `validation`,
`export`, `permissions`, `e2e` — so you can target a depth of coverage:

```bash
pytest -m smoke
pytest -m "admin and sanity"
pytest -m regression
pytest -m superadmin
pytest tests/admin_portal/memberships   # target a feature by path
```

Marker hygiene is enforced (`--strict-markers`): unknown markers fail fast.
All markers are registered in `pytest.ini`.

### Browser behavior

| Flag               | Effect                                                        |
| ------------------ | ------------------------------------------------------------- |
| _(default)_        | Visible Chrome that **stays open** after the test (`detach`)  |
| `--close-browser`  | Quit the browser automatically after the run                  |
| `--headless`       | Run headless (no window) — recommended for CI / servers       |
| `--single-window`  | Reuse one browser window across a grouped screen suite        |

Headless can also be toggled with the `HEADLESS=1` environment variable.

```bash
pytest --headless --close-browser
```

### Parallel execution

```bash
pytest -n auto --headless --close-browser
```

### Retrying flaky tests

`pytest-rerunfailures` is available for the inherently flaky nature of UI tests:

```bash
pytest --reruns 2 --reruns-delay 3
```

## Reports

Every run automatically writes Allure results to `allure-results/`
(configured in `pytest.ini`). You can additionally produce a self-contained
HTML report and JUnit XML:

```bash
pytest --headless --close-browser \
       --html=report.html --self-contained-html \
       --junitxml=results.xml
```

- **Allure** (rich, with history/trends) — install the CLI separately
  (`brew install allure`) then:

  ```bash
  allure serve allure-results
  ```

- **pytest-html** — `report.html` is a single shareable file (email / Slack).
- **JUnit XML** — `results.xml` for CI dashboards and test-management tools.

### Failure artifacts

On any failure the framework automatically captures and attaches:

- a **screenshot** → `screenshots/`
- the **page source** (HTML) → `logs/`
- the current **URL** and a log line → `logs/test_run.log`

Screenshots and page source are also attached to the Allure report for each
failed test.

## Continuous Integration

A GitHub Actions workflow is provided at `.github/workflows/tests.yml`. It:

- runs on push / PR and via manual dispatch (choose marker + environment),
- installs Chrome and dependencies, runs tests **headless** with reruns,
- uploads Allure results, `report.html`, `results.xml`, screenshots, and logs
  as build artifacts.

Add credentials as repository secrets: `SUPERADMIN_USERNAME`,
`SUPERADMIN_PASSWORD`, `ADMIN_PORTAL_USERNAME`, `ADMIN_PORTAL_PASSWORD`.

## Project Structure

```
config/        Environment URLs (staging/production) and user mapping
core/          Driver factory and config manager
fixtures/      Pytest fixtures (browser)
pages/         Page Objects (Page Object Model)
  common/      BasePage shared helpers
  admin_portal/
  superadmin/
tests/         Test suites, grouped by portal and feature
conftest.py    Root pytest config (options, markers, failure capture)
pytest.ini     Pytest settings, markers, report defaults
.github/       CI workflow
```

## Test Data Management (managed resources)

Admin Portal catalog entities (memberships, discounts, sites, ...) **cannot be
deleted** through the product, so tests can't create-and-delete throwaway data.
Instead each feature keeps **one dedicated record** and **resets it to a known
baseline before and after** every test that mutates it — no delete needed, no
data accumulation, and parallel-safe as long as each test owns its own record.

- Shared engine: `tests/admin_portal/_managed.py` (`managed_name`,
  `managed_resource`). Records are named with the `AUTOTEST` prefix so they are
  easy to identify and sweep.
- Reference implementation: **Memberships** — see `reset_managed_membership` and
  the `managed_membership` fixture in
  `tests/admin_portal/memberships/conftest.py`, exercised by
  `test_memberships_managed.py`.

### Adding managed data to a new feature (the repeatable part)

1. In the feature's `conftest.py`:
   ```python
   from tests.admin_portal._managed import managed_name, managed_resource

   MANAGED_X = managed_name("Widget")          # -> "AUTOTEST Widget"

   def reset_managed_x(browser):
       page = open_x_page(browser)
       if not page.x_exists(MANAGED_X):
           page.create_x(MANAGED_X, ...)        # create once
       # reset the fields tests mutate back to baseline
       ...
       return page

   managed_widget = managed_resource(reset_managed_x)   # the fixture
   ```
2. Have mutating tests request the `managed_widget` fixture instead of
   `create_*_if_missing`. Teardown is automatic.

Each feature is ~30–50 lines to the same contract — see the rollout checklist
below.

### Rollout status

| Feature            | Managed fixture |
| ------------------ | --------------- |
| memberships        | ✅ done (reference) |
| discounts          | ✅ done |
| service_categories | ✅ done (rename-reset) |
| gift_cards         | ☐ |
| coupon_packages    | ☐ |
| wash_extras        | ☐ (UI delete available) |
| wash_packages      | ☐ |
| wash_books         | ☐ |
| sites              | ⛔ blocked — page object has **no edit and no delete**, so a record can neither be reset nor removed. Needs an `open_edit_site`/`update_site` method (or a backend delete API). Today its tests create incrementing `VK AL0x` sites with no cleanup. |

## Roadmap / Known Limitations

- **Backend purge**: with no product delete, deactivated/managed records persist.
  A backend cleanup API/DB-purge (platform-team dependency) would unlock true
  create-fresh-per-run isolation and reaping of `AUTOTEST` data.
- **Cross-browser**: only Chrome is wired up today.
- **Allure history/trends**: enable by publishing `allure-report` with history
  to GitHub Pages (or an Allure server) from CI.
