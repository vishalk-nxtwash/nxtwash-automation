import pytest

from pages.admin_portal.wash_packages_page import WashPackagesPage
from tests.admin_portal.admin_session import open_admin_path
from tests.admin_portal._data import load as _load

_D = _load("wash_packages")

EXISTING_PACKAGE            = _D["reference"]["existing_package"]
MISSING_PACKAGE             = _D["search"]["nonexistent"]
ASSIGNMENT_SITE             = _D["reference"]["assignment_site"]
SECOND_ASSIGNMENT_SITE      = _D["reference"]["second_assignment_site"]
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
CONTROLLER_CODE             = _D["template"]["controller_code"]
LOCATION_PRICE              = _D["template"]["location_price"]
DESCRIPTION_TEXT            = _D["template"]["description"]
BROKEN_STATE_TEXTS = [
    "Something went wrong",
    "Internal Server Error",
    "Unauthorized",
    "Failed to fetch",
]


def open_wash_packages_page(browser):
    # Reset Redux Persist wash packages filter BEFORE navigation so the page
    # loads with the default filter state.  The UI-based clear_active_filters()
    # handles in-memory Redux state; this reset covers the localStorage
    # rehydration path that survives driver.get() navigation.
    try:
        browser.execute_script("""
            try {
                var root = JSON.parse(localStorage.getItem('persist:root') || '{}');
                var tfr = JSON.parse(root.tableFilterReducer || '{}');
                var tf = tfr.tableFilters || {};
                tf.washPackages = {
                    serviceName: '',
                    isActive: false
                };
                tfr.tableFilters = tf;
                root.tableFilterReducer = JSON.stringify(tfr);
                localStorage.setItem('persist:root', JSON.stringify(root));
            } catch(e) {}
        """)
    except Exception:
        pass

    open_admin_path(browser, "/services/washPackages")

    page = WashPackagesPage(browser)
    page.wait_for_list_loaded()
    page.clear_active_filters()

    return page


def create_wash_package_if_missing(browser, package_name=PACKAGE_NAME):

    page = open_wash_packages_page(browser)

    if page.package_exists(package_name):
        # Package already exists — re-navigate to get a clean list state.
        return open_wash_packages_page(browser)

    # Package not in active list — may be inactive from a prior test run.
    # Reactivate rather than re-creating to avoid barcode/name duplicate errors.
    page = open_wash_packages_page(browser)
    try:
        page.open_filter_panel()
        page.toggle_active_service_filter()
        page.apply_filters()
        if page.package_exists(package_name):
            page.open_edit_package(package_name)
            page.ensure_active_switch_on()
            page.save_and_return_to_list()
            return open_wash_packages_page(browser)
    except Exception:
        pass
    finally:
        try:
            page.clear_active_filters()
        except Exception:
            pass

    page = open_wash_packages_page(browser)
    page.create_package(
        package_name,
        POINTS_AWARDED,
        POINTS_REDEEMED,
        GLOBAL_PRICE,
        GLOBAL_COMMISSION,
        ASSIGNMENT_SITE,
        controller_code=CONTROLLER_CODE,
        location_price=LOCATION_PRICE,
    )
    page = open_wash_packages_page(browser)
    if not page.package_exists(package_name):
        raise RuntimeError(
            "create_wash_package_if_missing: '%s' not in grid after create — "
            "possible duplicate name or barcode conflict on staging" % package_name
        )

    return page


def _restore_package_fields(page):
    """Reset mutable fields to baseline; only touch the Inovua site grid if needed."""
    page.enter_service_name(PACKAGE_NAME)
    page.set_loyalty_points(POINTS_AWARDED, POINTS_REDEEMED)
    page.ensure_active_switch_on()
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    if not page.site_is_assigned(ASSIGNMENT_SITE):
        page.assign_site_with_price_and_commission(
            ASSIGNMENT_SITE,
            LOCATION_PRICE,
            GLOBAL_COMMISSION,
            controller_code=CONTROLLER_CODE,
        )


def _reset_managed_package(browser):
    """Ensure PACKAGE_NAME exists and reset its mutable fields to baseline."""
    page = open_wash_packages_page(browser)
    if page.package_exists(PACKAGE_NAME):
        page = open_wash_packages_page(browser)
        page.open_edit_package(PACKAGE_NAME)
        _restore_package_fields(page)
        page.save_and_return_to_list()
        return page

    # PACKAGE_NAME not found — check whether a prior interrupted run left it
    # renamed to UPDATED_PACKAGE_NAME; rename it back if so.
    page = open_wash_packages_page(browser)
    if page.package_exists(UPDATED_PACKAGE_NAME):
        page = open_wash_packages_page(browser)
        page.open_edit_package(UPDATED_PACKAGE_NAME)
        _restore_package_fields(page)
        page.save_and_return_to_list()
        return page

    # Neither name found in active list — test_deactivate may have left the
    # package inactive.  Show inactive entries and restore if found.
    page = open_wash_packages_page(browser)
    try:
        page.open_filter_panel()
        page.toggle_active_service_filter()
        page.apply_filters()
        for name in (PACKAGE_NAME, UPDATED_PACKAGE_NAME):
            if page.package_exists(name):
                page.open_edit_package(name)
                _restore_package_fields(page)
                page.save_and_return_to_list()
                return page
    except Exception:
        pass
    finally:
        page.clear_active_filters()

    page.create_package(
        PACKAGE_NAME, POINTS_AWARDED, POINTS_REDEEMED,
        GLOBAL_PRICE, GLOBAL_COMMISSION, ASSIGNMENT_SITE,
        barcode=BARCODE_VALUE,
        controller_code=CONTROLLER_CODE,
        location_price=LOCATION_PRICE,
    )
    page = open_wash_packages_page(browser)
    if not page.package_exists(PACKAGE_NAME):
        raise RuntimeError(
            "_reset_managed_package: '%s' not in grid after create — "
            "check BARCODE_VALUE conflict on staging" % PACKAGE_NAME
        )
    return page


def page_has_no_broken_state(page):

    body_text = page.get_body_text()
    return not any(text in body_text for text in BROKEN_STATE_TEXTS)


@pytest.fixture
def managed_package(browser):
    """Ensure PACKAGE_NAME exists at baseline before the test and restore after."""
    page = _reset_managed_package(browser)
    yield page
    try:
        _reset_managed_package(browser)
    except Exception:
        _reset_managed_package(browser)
