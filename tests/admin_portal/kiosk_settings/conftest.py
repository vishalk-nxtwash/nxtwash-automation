import pytest

from pages.admin_portal.kiosk_settings_page import AdminKioskFormPage, AdminKioskSettingsPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KSK_NAME = "VK kiosk1"
KSK_SITE = "VK Test carwash2"
KSK_LANE = "Wash lane 2"
KSK_MIDDLEWARE_IP = "https://middleware-zeus.nxtwash.info"
KSK_PAYMENT_SERIAL = "1640146298"
KSK_CAR_RECOGNITION_TYPE = "By License Plate"
KSK_CAR_RECOGNITION_ALT = "By RFID tag"
KSK_UPDATED_NAME = "VK kiosk1 edited"
KSK_NEW_NAME = "VK kiosk auto 1"
NONEXISTENT_KSK_NAME = "kiosk-does-not-exist-automation"

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_kiosk_page(browser):
    open_admin_path(browser, "/kiosk_settings/kiosks")
    page = AdminKioskSettingsPage(browser)
    page.wait_for_loaded()
    return page


def open_create_kiosk_form(browser):
    open_admin_path(browser, "/kiosk_settings/kiosks/new")
    form = AdminKioskFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_kiosk_form(browser, name=KSK_NAME):
    page = open_kiosk_page(browser)
    page.open_edit_kiosk(name)
    form = AdminKioskFormPage(browser)
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


def create_kiosk_if_missing(browser, name=KSK_NAME, site=KSK_SITE, lane=KSK_LANE):
    page = open_kiosk_page(browser)

    if page.kiosk_exists(name):
        form = open_edit_kiosk_form(browser, name)
        form.enter_kiosk_name(name)
        form.ensure_active_kiosk_on()
        form.click_save()
        return open_kiosk_page(browser)

    form = open_create_kiosk_form(browser)
    form.enter_kiosk_name(name)
    form.select_site(site)
    form.select_lane(lane)
    form.click_save()
    page = open_kiosk_page(browser)
    page.search_kiosk(name)
    page.wait_for_kiosk_row(name)
    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_kiosk(browser):
    page = create_kiosk_if_missing(browser)
    yield page
    create_kiosk_if_missing(browser)


@pytest.fixture
def managed_kiosk_form(browser, managed_kiosk):
    form = open_edit_kiosk_form(browser, KSK_NAME)
    yield form
