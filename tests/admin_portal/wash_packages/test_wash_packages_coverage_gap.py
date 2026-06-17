import logging

import allure
import pytest

from tests.admin_portal.wash_packages.conftest import ASSIGNMENT_SITE
from tests.admin_portal.wash_packages.conftest import EXISTING_PACKAGE
from tests.admin_portal.wash_packages.conftest import MISSING_PACKAGE
from tests.admin_portal.wash_packages.conftest import open_wash_packages_page
from tests.admin_portal.wash_packages.conftest import page_has_no_broken_state


LOG = logging.getLogger("nxtwash")


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("UI and List")
@allure.title("WP-UI list shell, controls, grid, pagination, and edit actions")
@pytest.mark.sanity
def test_wash_packages_list_shell_controls_and_grid(browser):
    LOG.info("Verifying Wash Packages list shell and primary controls")
    page = open_wash_packages_page(browser)
    body_text = page.get_body_text()

    assert "Wash packages" in body_text
    assert "Wash package name" in body_text
    assert "Price" in body_text
    assert "Status" in body_text
    assert page.search_input_is_visible()
    assert page.filter_button_is_clickable()
    assert page.download_button_is_clickable()
    assert page.add_package_button_is_clickable()
    assert page.every_visible_row_has_edit_action()
    assert page.pagination_controls_are_visible()
    assert page.results_per_page_control_is_visible()
    assert page_has_no_broken_state(page)


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Search")
@allure.title("WP-SRCH exact, partial, case-insensitive, trim, long, missing, and clear")
@pytest.mark.regression
def test_wash_packages_search_variants_and_clear(browser):
    LOG.info("Verifying Wash Packages search variants")
    page = open_wash_packages_page(browser)
    original_count = len(page.get_visible_package_names())

    page.search_package(EXISTING_PACKAGE)
    assert page.wait_for_package_row(EXISTING_PACKAGE).is_displayed()

    page.search_package(EXISTING_PACKAGE[:4])
    assert EXISTING_PACKAGE in page.get_body_text()

    page.search_package(EXISTING_PACKAGE.upper())
    assert EXISTING_PACKAGE.lower() in page.get_body_text().lower()

    page.search_package("  %s  " % EXISTING_PACKAGE)
    assert EXISTING_PACKAGE.lower() in page.get_body_text().lower()

    page.search_package("x" * 128)
    assert page_has_no_broken_state(page)

    page.search_package(MISSING_PACKAGE)
    assert MISSING_PACKAGE not in page.get_body_text()

    page.clear_package_search()
    assert len(page.get_visible_package_names()) >= min(original_count, 1)


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Filter")
@allure.title("WP-FLTR filter panel controls, site dropdown option, and reset")
@pytest.mark.regression
def test_wash_packages_filter_panel_site_option_and_reset(browser):
    LOG.info("Verifying Wash Packages filter panel controls and reset")
    page = open_wash_packages_page(browser)

    assert page.filter_panel_controls_are_visible()
    assert page.filter_site_option_is_visible(ASSIGNMENT_SITE)
    page.reset_filters()

    assert page_has_no_broken_state(page)


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Create UI")
@allure.title("WP-UI add wash package form service and discount settings")
@pytest.mark.sanity
def test_add_wash_package_form_service_discount_save_cancel_controls(browser):
    LOG.info("Verifying Add Wash Package form controls")
    page = open_wash_packages_page(browser)
    page.open_create_package()
    body_text = page.get_body_text()

    assert "Service settings" in body_text
    assert "Service name" in body_text
    assert "Global price" in body_text
    assert "Global commission" in body_text
    assert page.active_switch_is_on()
    assert page.save_package_button_is_clickable()
    assert page.cancel_button_is_visible()

    page.open_discount_settings()
    assert "Applicable discounts" in page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Validation")
@allure.title("WP-VAL-002 Global Price is mandatory")
@pytest.mark.validation
def test_wash_package_global_price_is_required(browser):
    LOG.info("Verifying global price mandatory validation")
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name("invalid-package-missing-price")
    page.click_save_package()

    assert not page.global_price_input_is_valid()
    assert page.get_global_price_validation_message() != ""
    assert "Service name" in page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Download")
@allure.title("WP-DL file export validation requires download-directory support")
@pytest.mark.export
@pytest.mark.xfail(
    reason=(
        "Download file/content validation needs browser download-directory "
        "configuration and CSV/XLS parser utilities."
    ),
    strict=True,
)
def test_wash_packages_download_file_validation_blocker(browser):
    page = open_wash_packages_page(browser)
    assert page.download_button_is_clickable()
    raise AssertionError("Download file/content validation is not implemented.")


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Permissions")
@allure.title("WP-PERM role-specific permission coverage requires role fixtures")
@pytest.mark.permissions
@pytest.mark.xfail(
    reason="Permission cases require non-admin role fixtures and credentials.",
    strict=True,
)
def test_wash_packages_permission_matrix_blocker(browser):
    page = open_wash_packages_page(browser)
    assert "Wash packages" in page.get_body_text()
    raise AssertionError("Role-specific permission coverage is not implemented.")


@allure.epic("Admin Portal")
@allure.feature("Wash Packages")
@allure.story("Advanced Edge Cases")
@allure.title("WP-EDGE advanced infrastructure scenarios require special harnesses")
@pytest.mark.regression
@pytest.mark.xfail(
    reason=(
        "Concurrency, slow network, audit-log, and server-restart coverage "
        "need multi-session, network interception, audit API, and environment "
        "restart harnesses."
    ),
    strict=True,
)
def test_wash_packages_advanced_edge_case_harness_blocker(browser):
    page = open_wash_packages_page(browser)
    assert "Wash packages" in page.get_body_text()
    raise AssertionError("Advanced edge-case harnesses are not implemented.")
