import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.admin_portal.tunnel_settings_page import TunnelSettingsFormPage, TunnelSettingsListPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

from tests.admin_portal._data import load as _load

_D = _load("tunnel_settings")

TUNNEL_NAME             = _D["template"]["tunnel_name"]
TUNNEL_CRT_NAME         = _D["create"]["tunnel_name"]
TUNNEL_SITE             = _D["reference"]["site"]
TUNNEL_CONTROLLER_IP    = _D["template"]["controller_ip"]
TUNNEL_MIDDLEWARE_IP    = _D["template"]["middleware_ip"]
TUNNEL_CONTROLLER_ID    = _D["template"]["controller_id"]
TUNNEL_RETRACT_SERVICE  = _D["reference"]["retract_service"]
TUNNEL_BEHAVIOR_DEFAULT = _D["reference"]["behavior_default"]
TUNNEL_BEHAVIOR         = _D["template"]["behavior"]

NONEXISTENT_TUNNEL_NAME = _D["search"]["nonexistent"]

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_tunnel_list(browser):
    open_admin_path(browser, "/tunnel_settings/tunnels")
    page = TunnelSettingsListPage(browser)
    page.wait_for_loaded()
    return page


def open_create_tunnel_form(browser):
    # Navigate via the list page + button click (direct deep-link is unreliable in this SPA)
    page = open_tunnel_list(browser)
    page.click_add_tunnel()
    form = TunnelSettingsFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_tunnel_form(browser, name=TUNNEL_NAME):
    page = open_tunnel_list(browser)
    page.open_edit_tunnel(name)
    form = TunnelSettingsFormPage(browser)
    form.wait_for_edit_loaded()
    return form


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    broken_signals = [
        "something went wrong",
        "internal server error",
        "application error",
        "cannot read",
        "typeerror",
        "uncaught error",
    ]
    return not any(s in body for s in broken_signals)


# ---------------------------------------------------------------------------
# Fixture tunnel configuration
# ---------------------------------------------------------------------------


def _configure_fixture_tunnel(form):
    """Apply all non-default settings required by the fixture tunnel (VK AT02).

    Called both on create (after core fields are filled) and on update (to
    restore the tunnel to the expected baseline).  Every step is wrapped in
    try/except so a locator miss doesn't blow up the fixture — the xfail
    markers on dependent tests handle individual failures.
    """
    # Middleware IP
    try:
        form.enter_middleware_ip(TUNNEL_MIDDLEWARE_IP)
    except Exception:
        pass

    # Behavior: Retrieve wash via plate
    try:
        form.select_behavior(TUNNEL_BEHAVIOR)
    except Exception:
        pass

    # Active tunnel configuration: ON
    try:
        form.set_toggle("Active tunnel configuration", True)
    except Exception:
        pass

    # Retract settings: one row → Tire wash service → Save retract for car ON.
    # Use a 5-second cap on the service option search so a missing staging service
    # (e.g. "Tire wash" not configured) wastes at most 5s per call instead of the
    # default 20s — avoids ~15 min of total timeout across 44 fixture invocations.
    try:
        form.expand_section("Retract settings")
        time.sleep(0.5)
        if form.get_retract_row_count() == 0:
            form.click_add_retract_row()
            time.sleep(0.5)
        dropdowns = [
            e for e in form.driver.find_elements(*form.RETRACT_SERVICE_DROPDOWNS)
            if e.is_displayed()
        ]
        if dropdowns:
            from selenium.webdriver.common.action_chains import ActionChains as _AC
            form.driver.execute_script("arguments[0].click();", dropdowns[0])
            inner = dropdowns[0].find_elements(By.XPATH, ".//input")
            if inner:
                try:
                    _AC(form.driver).click(inner[0]).perform()
                except Exception:
                    form.driver.execute_script("arguments[0].click();", inner[0])
            try:
                opt = WebDriverWait(form.driver, 5).until(
                    lambda d: form._find_react_option(TUNNEL_RETRACT_SERVICE)
                )
                form.driver.execute_script("arguments[0].click();", opt)
                form.toggle_retract_save_for_car(0, True)
            except Exception:
                # Service not available in staging — remove the empty row so the
                # form doesn't block save with a "service required" validation error.
                form.driver.execute_script("document.body.click();")
                try:
                    form.remove_retract_row(0)
                except Exception:
                    pass
    except Exception:
        pass

    # Dismiss any open dropdown / overlay before saving so the form is in a
    # stable state (a timed-out retract-service dropdown left open blocks submit).
    try:
        form.driver.execute_script("document.body.click();")
    except Exception:
        pass
    try:
        form.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    except Exception:
        pass
    time.sleep(0.3)

    form.click_save()


# ---------------------------------------------------------------------------
# Upsert helper — create VK AT01 if missing, restore to baseline if present
# ---------------------------------------------------------------------------


def ensure_tunnel_created(browser, name=TUNNEL_NAME, site=TUNNEL_SITE,
                           controller_ip=TUNNEL_CONTROLLER_IP):
    page = open_tunnel_list(browser)

    if page.tunnel_exists(name):
        form = open_edit_tunnel_form(browser, name)
        _configure_fixture_tunnel(form)
        return open_tunnel_list(browser)

    form = open_create_tunnel_form(browser)
    try:
        form.enter_tunnel_name(name)
        form.select_site(site)
        form.enter_controller_ip(controller_ip)
    except Exception as exc:
        raise pytest.skip(
            "Could not create test tunnel — site '%s' may not exist in staging. "
            "Verify the Sites & Locations module. Original error: %s" % (site, exc)
        ) from exc

    _configure_fixture_tunnel(form)
    time.sleep(1.5)  # let save network request complete before navigating away
    page = open_tunnel_list(browser)
    try:
        page.wait_for_tunnel_row(name)
    except TimeoutException:
        pytest.skip(
            "Tunnel '%s' not found after create attempt — form save likely failed "
            "(site missing in staging, or form validation error). "
            "Verify staging data for site '%s'." % (name, site)
        )
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_tunnel(browser):
    """Ensure VK AT02 exists with the full fixture config before each test; restore after."""
    page = ensure_tunnel_created(browser)
    yield page
    ensure_tunnel_created(browser)


@pytest.fixture
def managed_tunnel_form(browser, managed_tunnel):
    """Open the edit form for VK AT01."""
    form = open_edit_tunnel_form(browser, TUNNEL_NAME)
    yield form
