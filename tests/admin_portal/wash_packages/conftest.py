import pytest

from pages.admin_portal.wash_packages_page import WashPackagesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("wash_packages")

EXISTING_PACKAGE            = _D["reference"]["existing_package"]
MISSING_PACKAGE             = _D["search"]["nonexistent"]
ASSIGNMENT_SITE             = _D["reference"]["assignment_site"]
PACKAGE_NAME                = _D["template"]["package_name"]
UPDATED_PACKAGE_NAME        = _D["updated"]["package_name"]
POINTS_AWARDED              = _D["template"]["points_awarded"]
POINTS_REDEEMED             = _D["template"]["points_redeemed"]
UPDATED_POINTS_AWARDED      = _D["updated"]["points_awarded"]
UPDATED_POINTS_REDEEMED     = _D["updated"]["points_redeemed"]
GLOBAL_PRICE                = _D["template"]["global_price"]
GLOBAL_COMMISSION           = _D["template"]["global_commission"]
VISIBLE_PRICE               = _D["template"]["visible_price"]
SITE_OVERRIDE_PRICE         = _D["updated"]["site_override_price"]
SITE_OVERRIDE_PRICE_HIGH    = _D["updated"]["site_override_price_high"]
SITE_OVERRIDE_COMMISSION    = _D["updated"]["site_override_commission"]
APPLICABLE_DISCOUNT         = _D["reference"]["applicable_discount"]
SECOND_APPLICABLE_DISCOUNT  = _D["reference"]["second_applicable_discount"]
BARCODE_VALUE               = _D["template"]["barcode"]
DESCRIPTION_TEXT            = _D["template"]["description"]
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_wash_packages_page(browser):

    open_admin_path(browser, "/services/washPackages")

    page = WashPackagesPage(browser)
    page.wait_for_list_loaded()

    return page


def create_wash_package_if_missing(browser, package_name=PACKAGE_NAME):

    page = open_wash_packages_page(browser)

    if page.package_exists(package_name):
        # Package already exists — re-navigate to get a clean list state.
        # Do NOT open the edit form here: saving triggers a SPA redirect back
        # to /edit/:id which makes the subsequent open_wash_packages_page hang.
        # Value resets belong to _reset_managed_package / managed_package fixture.
        return open_wash_packages_page(browser)

    page.create_package(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE
    )
    page = open_wash_packages_page(browser)
    page.search_package(package_name)
    page.wait_for_package_row(package_name)

    return page


def _reset_managed_package(browser):
    """Ensure PACKAGE_NAME exists and reset its mutable fields to baseline."""
    page = open_wash_packages_page(browser)
    if page.package_exists(PACKAGE_NAME):
        page = open_wash_packages_page(browser)
        page.open_edit_package(PACKAGE_NAME)
        page.fill_package_form(
            PACKAGE_NAME, POINTS_AWARDED, POINTS_REDEEMED,
            GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE,
        )
        page.save_and_return_to_list()
        return page

    # PACKAGE_NAME not found — check whether a prior interrupted run left it
    # renamed to UPDATED_PACKAGE_NAME; rename it back if so.
    page = open_wash_packages_page(browser)
    if page.package_exists(UPDATED_PACKAGE_NAME):
        page = open_wash_packages_page(browser)
        page.open_edit_package(UPDATED_PACKAGE_NAME)
        page.fill_package_form(
            PACKAGE_NAME, POINTS_AWARDED, POINTS_REDEEMED,
            GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE,
        )
        page.save_and_return_to_list()
        return page

    page.create_package(
        PACKAGE_NAME, POINTS_AWARDED, POINTS_REDEEMED,
        GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE,
        barcode=BARCODE_VALUE,
    )
    return open_wash_packages_page(browser)


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


@pytest.fixture
def managed_package(browser):
    """Ensure PACKAGE_NAME exists at baseline before the test and restore after."""
    page = _reset_managed_package(browser)
    yield page
    _reset_managed_package(browser)
