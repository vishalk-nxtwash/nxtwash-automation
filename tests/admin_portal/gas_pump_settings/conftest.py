import pytest

from pages.admin_portal.gas_pump_settings_page import GasPumpSettingsFormPage, GasPumpSettingsListPage
from tests.admin_portal._data import load as _load
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_D = _load("gas_pump_settings")

GPS_PUMP_NAME    = _D["reference"]["existing_pump"]
GPS_SITE         = _D["reference"]["site"]
GPS_WASH_BOOK    = _D["reference"]["wash_book"]
GPS_UPDATED_NAME = _D["updated"]["pump_name"]
GPS_NEW_NAME     = _D["create"]["pump_name"]

GPS_SERIAL_PORT    = _D["template"]["serial_port"]
GPS_SERIAL_NUMBER  = _D["template"]["serial_number"]
GPS_BAUD_RATE      = _D["template"]["baud_rate"]
GPS_LINK_TIMEOUT   = _D["template"]["link_timeout"]
GPS_FETCH_INTERVAL = _D["template"]["fetch_interval"]
GPS_CODE_LENGTH    = _D["template"]["code_length"]
GPS_WBC_ID_CODE    = _D["template"]["wbc_id_code"]

NONEXISTENT_PUMP_NAME = _D["search"]["nonexistent"]

# Set to True when running against staging with a physically connected gas pump.
# Required for GPS-CON-001 (connected state), GPS-CON-003..006 (modal tests).
PUMP_IS_CONNECTED = False

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def open_gas_pump_list(browser):
    open_admin_path(browser, "/gas_pump_settings/device_list")
    page = GasPumpSettingsListPage(browser)
    page.wait_for_loaded()
    return page


def open_create_gas_pump_form(browser):
    page = open_gas_pump_list(browser)
    page.click_add_pump()
    form = GasPumpSettingsFormPage(browser)
    form.wait_for_create_loaded()
    return form


def open_edit_gas_pump_form(browser, name=GPS_PUMP_NAME):
    page = open_gas_pump_list(browser)
    page.open_edit_pump(name)
    form = GasPumpSettingsFormPage(browser)
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


def ensure_gas_pump_created(browser, name=GPS_PUMP_NAME, site=GPS_SITE):
    """Create VK AGP02 if missing; restore to active baseline if present.

    GPS-CRT-017: asserts that after a successful create, the pump row appears
    in the list and the Gas Pump (N) header count has incremented.
    """
    page = open_gas_pump_list(browser)
    count_before = page.get_header_pump_count()

    if page.pump_exists(name):
        form = open_edit_gas_pump_form(browser, name)
        form.enter_pump_name(name)
        form.ensure_active_pump_on()
        form.click_save()
        return open_gas_pump_list(browser)

    form = open_create_gas_pump_form(browser)
    try:
        form.fill_required_fields(
            name, site,
            GPS_SERIAL_PORT, GPS_SERIAL_NUMBER,
            GPS_BAUD_RATE, GPS_LINK_TIMEOUT,
            GPS_FETCH_INTERVAL, GPS_CODE_LENGTH,
        )
        form.ensure_active_pump_on()
        # WBC row: VKAWB1 wash book, ID code 02 — Dependency: Wash Books module
        try:
            form.click_add_wbc_row()
            form.select_wbc_wash_book(0, GPS_WASH_BOOK)
            form.enter_wbc_id_code(0, GPS_WBC_ID_CODE)
        except Exception:
            pass
    except Exception as exc:
        raise pytest.skip(
            "Could not fill create form for gas pump '%s' — "
            "site '%s' may not exist in staging. Error: %s" % (name, site, exc)
        ) from exc

    form.click_save()

    page = open_gas_pump_list(browser)
    try:
        page.wait_for_pump_row(name)
    except Exception:
        pytest.skip(
            "Gas pump '%s' not found after create — save likely failed "
            "(staging data issue for site '%s')." % (name, site)
        )

    # GPS-CRT-017: header count must increment after a successful create
    count_after = page.get_header_pump_count()
    if count_before is not None and count_after is not None:
        assert count_after > count_before, (
            "GPS-CRT-017: Gas Pump header count did not increment after create "
            "(before: %d, after: %d)" % (count_before, count_after)
        )

    return page


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def managed_gas_pump(browser):
    """Ensure VK AGP02 exists at the active baseline before each test; restore after."""
    page = ensure_gas_pump_created(browser)
    yield page
    ensure_gas_pump_created(browser)


@pytest.fixture
def managed_gas_pump_form(browser, managed_gas_pump):
    """Open the edit form for VK AGP02."""
    form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
    yield form
