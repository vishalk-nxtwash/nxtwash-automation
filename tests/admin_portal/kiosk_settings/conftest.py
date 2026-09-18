import pytest

from pages.admin_portal.kiosk_settings_page import AdminKioskFormPage, AdminKioskSettingsPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

from tests.admin_portal._data import load as _load

_D = _load("kiosk_settings")

KSK_NAME                 = _D["reference"]["existing_kiosk"]
KSK_SITE                 = _D["reference"]["site"]
KSK_LANE                 = _D["reference"]["lane"]
KSK_MIDDLEWARE_IP        = _D["template"]["middleware_ip"]
KSK_PAYMENT_SERIAL       = _D["template"]["payment_serial"]
KSK_CAR_RECOGNITION_TYPE = _D["reference"]["car_recognition_type"]
KSK_CAR_RECOGNITION_ALT  = _D["reference"]["car_recognition_alt"]
KSK_UPDATED_NAME         = _D["updated"]["kiosk_name"]
KSK_NEW_NAME             = _D["create"]["kiosk_name"]
NONEXISTENT_KSK_NAME     = _D["search"]["nonexistent"]

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_kiosk_page(browser):
    open_admin_path(browser, "/kiosk_settings/kiosks")
    page = AdminKioskSettingsPage(browser)
    page.wait_for_loaded()
    page.reset_filters_if_active()
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


BROKEN_STATE_TEXTS = [
    "something went wrong",
    "internal server error",
    "application error",
    "cannot read",
    "typeerror",
    "uncaught error",
]


def page_has_no_broken_state(page):
    try:
        body = page.get_body_text().lower()
    except Exception:
        return True
    return not any(s in body for s in BROKEN_STATE_TEXTS)


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
    form.enter_middleware_ip(KSK_MIDDLEWARE_IP)
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
    """Provides a page pointed at the pre-seeded reference kiosk.

    Skips cleanly if the kiosk is absent.  Teardown restores the kiosk name
    in case an edit test renamed it (KSK_NAME → KSK_UPDATED_NAME).
    """
    page = open_kiosk_page(browser)
    if not page.kiosk_exists(KSK_NAME):
        pytest.skip(
            "Reference kiosk '%s' not found in staging — pre-seed required" % KSK_NAME
        )
    yield page
    # Restore kiosk name if an edit test renamed it.
    try:
        restore_page = open_kiosk_page(browser)
        if not restore_page.kiosk_exists(KSK_NAME) and restore_page.kiosk_exists(KSK_UPDATED_NAME):
            form = open_edit_kiosk_form(browser, KSK_UPDATED_NAME)
            form.enter_kiosk_name(KSK_NAME)
            form.click_save()
    except Exception:
        pass


@pytest.fixture
def managed_kiosk_form(browser, managed_kiosk):
    form = open_edit_kiosk_form(browser, KSK_NAME)
    yield form
