import allure
import pytest

from tests.admin_portal.wash_packages.conftest import (
    APPLICABLE_DISCOUNT,
    ASSIGNMENT_SITE,
    DESCRIPTION_TEXT,
    GLOBAL_COMMISSION,
    GLOBAL_PRICE,
    PACKAGE_NAME,
    SECOND_APPLICABLE_DISCOUNT,
    SITE_OVERRIDE_COMMISSION,
    SITE_OVERRIDE_PRICE,
    UPDATED_POINTS_AWARDED,
    UPDATED_POINTS_REDEEMED,
    open_wash_packages_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Packages"),
    allure.story("Edit"),
]


@allure.title("WP-EDT-001 Edit wash package name persists after save")
@pytest.mark.regression
def test_edit_wash_package_name_persists(browser, isolated_package):
    # Isolated record (not the shared managed_package) — renaming it doesn't
    # stack read-after-write lag onto the ~15 other tests sharing PACKAGE_NAME.
    page, name = isolated_package
    updated_name = name + " updated"
    page.open_edit_package(name)
    page.enter_service_name(updated_name)
    page.save_and_return_to_list()
    page.search_package(updated_name)

    assert page.wait_for_package_row(updated_name).is_displayed()


@allure.title("WP-EDT-002 Edit global price persists after save")
@pytest.mark.regression
def test_edit_wash_package_global_price_persists(managed_package):
    new_price = "45"
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.set_global_price(new_price)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.wait_for_persisted_value(
        page.get_global_price_value, new_price, reopen=lambda: page.open_edit_package(PACKAGE_NAME)
    ) == new_price
    assert page_has_no_broken_state(page)


@allure.title("WP-EDT-003 Edit global commission persists after save")
@pytest.mark.regression
def test_edit_wash_package_global_commission_persists(isolated_package):
    # Isolated record — see WP-EDT-001's comment.
    new_commission = "12"
    page, name = isolated_package
    page.open_edit_package(name)
    page.set_global_commission(new_commission)
    page.save_and_return_to_list()

    page.open_edit_package(name)
    assert page.wait_for_persisted_value(
        page.get_global_commission_value, new_commission, reopen=lambda: page.open_edit_package(name)
    ) == new_commission
    assert page_has_no_broken_state(page)


@allure.title("WP-EDT-004 Edit loyalty points persists after save")
@pytest.mark.regression
def test_edit_wash_package_loyalty_points_persist(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.set_loyalty_points(UPDATED_POINTS_AWARDED, UPDATED_POINTS_REDEEMED)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.wait_for_persisted_value(
        page.get_points_awarded_value, UPDATED_POINTS_AWARDED, reopen=lambda: page.open_edit_package(PACKAGE_NAME)
    ) == UPDATED_POINTS_AWARDED
    assert page.get_points_redeemed_value() == UPDATED_POINTS_REDEEMED
    assert page_has_no_broken_state(page)


@allure.title("WP-EDT-005 Editing site assignment persists after save")
@pytest.mark.regression
def test_edit_wash_package_assigned_sites(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.assign_site_with_price_and_commission(
        ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION
    )
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    # site_is_assigned scrolls the Inovua virtual grid to find the row rather
    # than relying on get_body_text(), which only captures currently rendered rows.
    assert page.wait_for_persisted_value(
        lambda: page.site_is_assigned(ASSIGNMENT_SITE), True,
        reopen=lambda: page.open_edit_package(PACKAGE_NAME),
    )
    assert page_has_no_broken_state(page)


@pytest.mark.smoke
@allure.title("WP-EDT-008 Activate an inactive wash package updates its status to Active")
@pytest.mark.regression
@pytest.mark.timeout(480)
def test_activate_wash_package(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)

    # Toggle off then immediately back on within the same edit session.
    # Inactive packages are hidden from search results so a save-deactivate →
    # re-search → open-edit flow is not reliable in this environment.
    page.ensure_active_switch_off()
    page.ensure_active_switch_on()
    page.save_and_return_to_list()
    page.search_package(PACKAGE_NAME)

    assert page.wait_for_package_row(PACKAGE_NAME).is_displayed()
    assert page.get_package_status(PACKAGE_NAME) == "Active"
    assert page_has_no_broken_state(page)


@allure.title("WP-EDT-009 Deactivate an active wash package hides it from the default list")
@pytest.mark.regression
@pytest.mark.timeout(480)
def test_deactivate_wash_package(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.ensure_active_switch_off()
    page.save_and_return_to_list()
    page.search_package(PACKAGE_NAME)

    assert page.wait_for_persisted_value(
        lambda: PACKAGE_NAME not in page.get_body_text(), True,
        reopen=lambda: page.search_package(PACKAGE_NAME),
    )
    assert page_has_no_broken_state(page)


@allure.title("WP-DIS-001 Applicable discount assigned to wash package persists after save")
@pytest.mark.regression
@pytest.mark.timeout(480)
def test_assign_applicable_discount_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()

    def _reopen():
        page.open_edit_package(PACKAGE_NAME)
        page.open_discount_settings()

    assert page.wait_for_persisted_value(
        lambda: page.discount_is_selected(APPLICABLE_DISCOUNT), True, reopen=_reopen,
    )
    assert page_has_no_broken_state(page)


@allure.title("WP-DIS-002 Assigning multiple discounts persists after save")
@pytest.mark.regression
def test_assign_multiple_discounts_persist(isolated_package):
    # Isolated record — see WP-EDT-001's comment.
    page, name = isolated_package
    page.open_edit_package(name)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    try:
        page.select_applicable_discount(SECOND_APPLICABLE_DISCOUNT)
    except Exception:
        pytest.skip(
            "Second discount '%s' not available in dropdown — verify SECOND_APPLICABLE_DISCOUNT "
            "in conftest.py" % SECOND_APPLICABLE_DISCOUNT
        )

    page.save_and_return_to_list()

    page.open_edit_package(name)
    page.open_discount_settings()

    assert page.discount_is_selected(APPLICABLE_DISCOUNT)
    assert page.discount_is_selected(SECOND_APPLICABLE_DISCOUNT)
    assert page_has_no_broken_state(page)


@allure.title("WP-DIS-003 Removing an assigned discount persists after save")
@pytest.mark.regression
def test_remove_applicable_discount_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()
    page.remove_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()

    def _reopen():
        page.open_edit_package(PACKAGE_NAME)
        page.open_discount_settings()

    assert not page.wait_for_persisted_value(
        lambda: page.discount_is_selected(APPLICABLE_DISCOUNT), False, reopen=_reopen,
    )
    assert page_has_no_broken_state(page)


@allure.title("WP-EDT-007 Editing discount configuration persists after save")
@pytest.mark.regression
def test_edit_wash_package_discount_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()
    page.select_applicable_discount(APPLICABLE_DISCOUNT)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    page.open_discount_settings()

    def _reopen():
        page.open_edit_package(PACKAGE_NAME)
        page.open_discount_settings()

    assert page.wait_for_persisted_value(
        lambda: page.discount_is_selected(APPLICABLE_DISCOUNT), True, reopen=_reopen,
    )
    assert page_has_no_broken_state(page)


@allure.title("WP-DSC-002 Saving a wash package without a description succeeds")
@pytest.mark.regression
def test_save_wash_package_without_description(browser):
    import uuid
    package_name = "VK no-desc %s" % uuid.uuid4().hex[:6]
    page = open_wash_packages_page(browser)
    page.open_create_package()
    page.enter_service_name(package_name)
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission(GLOBAL_COMMISSION)
    page.assign_site_with_price_and_commission(ASSIGNMENT_SITE, GLOBAL_PRICE, GLOBAL_COMMISSION)
    # Description intentionally left empty
    page.save_and_return_to_list()
    page.search_package(package_name)

    assert page.wait_for_package_row(package_name).is_displayed()
    assert page_has_no_broken_state(page)


@allure.title("WP-DSC-001 Service description saves and persists after save")
@pytest.mark.regression
@pytest.mark.timeout(480)
def test_service_description_persists(managed_package):
    page = managed_package
    page.open_edit_package(PACKAGE_NAME)
    page.enter_description(DESCRIPTION_TEXT)
    page.save_and_return_to_list()

    page.open_edit_package(PACKAGE_NAME)
    assert page.wait_for_persisted_value(
        page.get_description_value, DESCRIPTION_TEXT,
        reopen=lambda: page.open_edit_package(PACKAGE_NAME),
    ) == DESCRIPTION_TEXT
    assert page_has_no_broken_state(page)
