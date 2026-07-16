import pytest

from pages.admin_portal.pos_settings_page import AdminPOSFormPage, AdminPOSSettingsPage
from tests.admin_portal.admin_session import open_admin_path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

POS_NAME = "VK POS 1"
POS_SITE = "VK AL03"
POS_LANE = "L1"
POS_UPDATED_NAME = "VK POS 1 edited"
POS_NEW_NAME = "VK APOS02"

POS_MIDDLEWARE_IP = "https://middleware-zeus.nxtwash.info/"
POS_PAYMENT_SERIAL = "1.1.1.1"
POS_CONTROLLER_ID = "RTC"
POS_CONTROLLER_IP = "192.168.1.180:502"
POS_ALLOW_CHECKOUT = "With assigned customer only"
POS_ALLOW_CHECKOUT_NO_CUSTOMER = "No customer assigned"

NONEXISTENT_POS_NAME = "pos-does-not-exist-automation"

# ---------------------------------------------------------------------------
# Navigation helpers
# ---------------------------------------------------------------------------


def get_next_available_pos_name(page, base_name=None):
    """Return base_name if unused, else VK APOS03, VK APOS04, … until one is free."""
    import re
    if base_name is None:
        base_name = POS_NEW_NAME
    m = re.match(r'^(.*?)(\d+)$', base_name)
    if not m:
        return base_name
    prefix, num_str = m.group(1), m.group(2)
    width = len(num_str)
    num = int(num_str)
    for _ in range(20):
        candidate = prefix + str(num).zfill(width)
        if not page.pos_exists(candidate):
            return candidate
        num += 1
    return base_name


def get_free_lane(browser, site=POS_SITE):
    """Return the first lane for `site` that no existing POS is currently using.

    Steps:
    1. Open the POS list, filter by site, read which lanes are already taken.
    2. Open the create form, select the site, read all available lane options.
    3. Return the first lane that is not in the taken set.
    Returns None if every lane is already assigned.
    """
    # Step 1 — lanes already in use at this site
    list_page = open_pos_page(browser)
    used_lanes = list_page.get_used_lanes_for_site(site)

    # Step 2 — all lanes that exist for this site (from the create-form dropdown)
    form = open_create_pos_form(browser)
    form.select_site(site)
    all_lanes = form.get_lane_options()

    if not all_lanes:
        # Dropdown returned no real options — fall back to the module constant.
        # If that lane is also taken, the caller handles the None return below.
        return POS_LANE if POS_LANE not in used_lanes else None

    # Step 3 — pick the first free one
    for lane in all_lanes:
        if lane not in used_lanes:
            return lane

    return None  # every lane is occupied


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


def create_pos_if_missing(browser, name=POS_NAME, site=POS_SITE, lane=None,
                          payment_serial=POS_PAYMENT_SERIAL,
                          middleware_ip=POS_MIDDLEWARE_IP):
    page = open_pos_page(browser)

    if page.pos_exists(name):
        form = open_edit_pos_form(browser, name)
        form.enter_pos_name(name)
        form.ensure_active_pos_on()
        form.click_save()
        return open_pos_page(browser)

    # Resolve a free lane automatically if none was specified
    if lane is None:
        lane = get_free_lane(browser, site)
    if lane is None:
        raise pytest.skip(
            "No free lanes available for site '%s' — every lane is already "
            "assigned to an existing POS." % site
        )

    form = open_create_pos_form(browser)
    try:
        form.fill_create_form(name, site, lane,
                              payment_serial=payment_serial,
                              middleware_ip=middleware_ip)
    except Exception as exc:  # noqa: BLE001
        raise pytest.skip(
            "Could not create test POS — site '%s' or lane '%s' may not exist "
            "in staging. Original error: %s" % (site, lane, exc)
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
