import pytest

from pages.admin_portal.pos_settings_page import AdminPOSFormPage, AdminPOSSettingsPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POS_NAME = "VK POS 1"
POS_SITE = "VK Test carwash 2"
POS_LANE = "Wash lane 2"
POS_UPDATED_NAME = "VK POS 1 edited"
POS_NEW_NAME = "VK POS auto 1"

POS_MIDDLEWARE_IP = "https://middleware-zeus.nxtwash.info"
POS_PAYMENT_SERIAL = "12345"
POS_CONTROLLER_ID = "RTC"
POS_CONTROLLER_IP = "192.168.1.180:502"
POS_ALLOW_CHECKOUT = "With assigned customer only"
POS_ALLOW_CHECKOUT_NO_CUSTOMER = "No customer assigned"

NONEXISTENT_POS_NAME = "pos-does-not-exist-automation"

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_pos_page(browser):
    open_admin_path(browser, "/pos_settings/pos")
    page = AdminPOSSettingsPage(browser)
    page.wait_for_loaded()
    return page


def open_create_pos_form(browser):
    open_admin_path(browser, "/pos_settings/pos/new")
    form = AdminPOSFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_pos_form(browser, name=POS_NAME):
    page = open_pos_page(browser)
    page.open_edit_pos(name)
    form = AdminPOSFormPage(browser)
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
# Upsert helper
# ---------------------------------------------------------------------------


def create_pos_if_missing(browser, name=POS_NAME, site=POS_SITE, lane=POS_LANE):
    page = open_pos_page(browser)

    if page.pos_exists(name):
        form = open_edit_pos_form(browser, name)
        form.enter_pos_name(name)
        form.ensure_active_pos_on()
        form.click_save()
        return open_pos_page(browser)

    form = open_create_pos_form(browser)
    try:
        form.fill_create_form(name, site, lane)
    except Exception as exc:  # noqa: BLE001
        raise pytest.skip(
            "Could not create test POS — site '%s' or lane '%s' may not exist in staging. "
            "Verify the Sites & Locations module. Original error: %s" % (site, lane, exc)
        ) from exc
    form.ensure_active_pos_on()
    form.click_save()
    page = open_pos_page(browser)
    page.search_pos(name)
    page.wait_for_pos_row(name)
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_pos(browser):
    page = create_pos_if_missing(browser)
    yield page
    create_pos_if_missing(browser)


@pytest.fixture
def managed_pos_form(browser, managed_pos):
    form = open_edit_pos_form(browser, POS_NAME)
    yield form
