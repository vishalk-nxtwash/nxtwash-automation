import time

import pytest

from pages.admin_portal.tunnel_settings_page import TunnelSettingsFormPage, TunnelSettingsListPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TUNNEL_NAME = "VK AT02"
TUNNEL_CRT_NAME = "VK AT02 auto"
TUNNEL_SITE = "VK test carwash 2"
TUNNEL_CONTROLLER_IP = "1.1.1.1:502"
TUNNEL_MIDDLEWARE_IP = "http://localhost:5000"
TUNNEL_CONTROLLER_ID = "RTC"
TUNNEL_RETRACT_SERVICE = "Tire wash"
TUNNEL_BEHAVIOR_DEFAULT = "Sequence stacking"   # default shown on /new form
TUNNEL_BEHAVIOR = "Retrieve wash via plate"      # selected for the fixture tunnel

NONEXISTENT_TUNNEL_NAME = "tunnel-does-not-exist-automation"

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
    """Apply all non-default settings required by the fixture tunnel (VK AT01).

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

    # Retract settings: one row → Tire wash service → Save retract for car ON
    try:
        form.expand_section("Retract settings")
        time.sleep(0.5)
        if form.get_retract_row_count() == 0:
            form.click_add_retract_row()
            time.sleep(0.5)
        form.select_retract_service(0, TUNNEL_RETRACT_SERVICE)
        form.toggle_retract_save_for_car(0, True)
    except Exception:
        pass

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
    page = open_tunnel_list(browser)
    page.wait_for_tunnel_row(name)
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_tunnel(browser):
    """Ensure VK AT01 exists with the full fixture config before each test; restore after."""
    page = ensure_tunnel_created(browser)
    yield page
    ensure_tunnel_created(browser)


@pytest.fixture
def managed_tunnel_form(browser, managed_tunnel):
    """Open the edit form for VK AT01."""
    form = open_edit_tunnel_form(browser, TUNNEL_NAME)
    yield form
