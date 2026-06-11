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

```bash
pytest -m smoke
pytest -m "admin and smoke"
pytest -m superadmin
```

Marker hygiene is enforced (`--strict-markers`): unknown markers fail fast.

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

## Roadmap / Known Limitations

- **Test-data isolation**: some suites create records with fixed names
  (`create_*_if_missing`) without teardown. Add per-feature cleanup fixtures
  before relying on fully parallel (`-n auto`) runs against shared data.
- **Cross-browser**: only Chrome is wired up today.
- **Allure history/trends**: enable by publishing `allure-report` with history
  to GitHub Pages (or an Allure server) from CI.
