import logging
import uuid

import allure
import pytest

from tests.admin_portal.memberships.conftest import GLOBAL_COMMISSION
from tests.admin_portal.memberships.conftest import FIRST_LOCATION_COMMISSION
from tests.admin_portal.memberships.conftest import FIRST_LOCATION_PRICE
from tests.admin_portal.memberships.conftest import MANAGED_MEMBERSHIP
from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import create_membership_if_missing
from tests.admin_portal.memberships.conftest import managed_membership  # noqa: F401
from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-NAM-002 Verify Membership Name is mandatory")
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.validation
def test_membership_required_name_validation(browser):

    LOG.info("Validating required membership name")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.click_save_membership()

    assert not memberships_page.membership_name_input_is_valid()
    assert memberships_page.get_membership_name_validation_message() != ""


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MEM-VAL-003 Verify blank required form is not saved")
@pytest.mark.validation
def test_membership_blank_required_form_stays_on_form(browser):

    LOG.info("Validating blank required membership form stays on create page")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.click_save_membership()

    assert "Add new membership" in memberships_page.get_body_text()
    assert "Membership name" in memberships_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-PRI-002 Verify Global Price is mandatory")
@pytest.mark.regression
@pytest.mark.validation
def test_membership_requires_global_price(browser):

    LOG.info("Validating required global price")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("invalid-membership-missing-price")
    memberships_page.click_save_membership()

    assert not memberships_page.global_price_input_is_valid()
    assert memberships_page.get_global_price_validation_message() != ""
    assert "Add new membership" in memberships_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-NAM-003 Verify duplicate Membership Name is rejected")
@pytest.mark.regression
@pytest.mark.validation
def test_duplicate_membership_name_is_rejected(browser):

    LOG.info("Validating duplicate membership name is rejected")
    memberships_page = create_membership_if_missing(browser)
    memberships_page.open_create_membership()
    memberships_page.fill_membership_form(
        MEMBERSHIP_NAME,
        "15",
        GLOBAL_COMMISSION,
        "20",
        "3"
    )
    memberships_page.click_save_membership()
    memberships_page.wait_for_duplicate_membership_error()

    assert memberships_page.duplicate_membership_error_is_visible()
    assert "Add new membership" in memberships_page.get_body_text()


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-NAM-005 Verify Membership Name with only spaces")
@pytest.mark.validation
def test_spaces_only_membership_name_is_rejected(browser):

    LOG.info("Validating spaces-only membership name is rejected")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("   ")
    memberships_page.set_global_price("15")
    memberships_page.click_save_membership()

    memberships_page.wait_for_form_save_blocked()

    assert "Add new membership" in memberships_page.get_body_text()
    assert memberships_page.get_membership_name_value().strip() == ""


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-PRI-005 Verify negative Global Price is rejected")
@pytest.mark.regression
@pytest.mark.validation
def test_negative_global_price_is_rejected(browser):

    LOG.info("Validating negative global price")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("invalid-membership-negative-price")
    memberships_page.set_global_price("-1")
    memberships_page.click_save_membership()

    memberships_page.wait_for_form_save_blocked()

    assert "Add new membership" in memberships_page.get_body_text()
    assert memberships_page.get_global_price_value() == "-1"
    assert memberships_page.get_membership_name_value() == (
        "invalid-membership-negative-price"
    )


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MEM-VAL-008 Verify alphabetic Global Price is rejected")
@pytest.mark.validation
def test_alphabetic_global_price_is_rejected(browser):

    LOG.info("Validating alphabetic global price")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("invalid-membership-alpha-price")
    memberships_page.set_global_price("abc")
    memberships_page.click_save_membership()

    memberships_page.wait_for_form_save_blocked()

    assert "Add new membership" in memberships_page.get_body_text()
    assert memberships_page.get_global_price_value() == "abc"
    assert memberships_page.get_membership_name_value() == (
        "invalid-membership-alpha-price"
    )


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-COM-003 Verify negative Global Commission is rejected")
@pytest.mark.validation
def test_negative_global_commission_is_rejected(browser):

    LOG.info("Validating negative global commission")
    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("invalid-membership-negative-commission")
    memberships_page.set_global_price("15")
    memberships_page.set_global_commission("-1")
    memberships_page.click_save_membership()

    memberships_page.wait_for_form_save_blocked()

    assert "Add new membership" in memberships_page.get_body_text()
    assert memberships_page.get_global_commission_value() == "-1"
    assert memberships_page.get_membership_name_value() == (
        "invalid-membership-negative-commission"
    )


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-PRI-004 Verify decimal price value")
@pytest.mark.validation
@pytest.mark.skip(reason="MB-PRI-004: StaleElementReferenceException after create_membership — grid row locator goes stale before assertion; needs staleness-safe wait")
def test_decimal_global_price_is_accepted_and_saved(browser):

    membership_name = "VK decimal %s" % uuid.uuid4().hex[:6]
    decimal_price = "15.50"
    LOG.info("Validating decimal global price is accepted: %s", membership_name)
    memberships_page = open_memberships_page(browser)
    memberships_page.create_membership(
        membership_name,
        decimal_price,
        GLOBAL_COMMISSION,
        FIRST_LOCATION_PRICE,
        FIRST_LOCATION_COMMISSION
    )
    memberships_page.search_membership(membership_name)

    assert memberships_page.wait_for_membership_row(membership_name).is_displayed()
    assert memberships_page.get_membership_price(membership_name) == "$15.50"


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MB-BAR-003 Duplicate barcode is rejected on save")
@pytest.mark.regression
@pytest.mark.validation
@pytest.mark.timeout(900)
@pytest.mark.skip(reason="MB-BAR-003: StaleElementReferenceException in wait_for_form_save_blocked after set_barcode — element reference goes stale; needs staleness-safe locator")
def test_duplicate_barcode_is_rejected(managed_membership):

    page = managed_membership
    duplicate_barcode = "AUTO-DUP-BAR-001"
    LOG.info(
        "Validating duplicate barcode '%s' is rejected", duplicate_barcode
    )
    # Assign the barcode to the managed membership and save
    page.open_edit_membership(MANAGED_MEMBERSHIP)
    page.set_barcode(duplicate_barcode)
    page.save_and_return_to_list()

    # Try to set the same barcode on a second membership — expect rejection
    create_membership_if_missing(page.driver)
    page.open_edit_membership(MEMBERSHIP_NAME)
    page.set_barcode(duplicate_barcode)
    page.click_save_membership()
    page.wait_for_form_save_blocked()

    body = page.get_body_text().lower()
    assert (
        "already" in body or "duplicate" in body or "barcode" in body
    ), "Expected a barcode-conflict error but none was visible"
