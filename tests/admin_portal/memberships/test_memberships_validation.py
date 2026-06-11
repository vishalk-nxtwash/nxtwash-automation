import logging

import allure
import pytest

from tests.admin_portal.memberships.conftest import GLOBAL_COMMISSION
from tests.admin_portal.memberships.conftest import MEMBERSHIP_NAME
from tests.admin_portal.memberships.conftest import create_membership_if_missing
from tests.admin_portal.memberships.conftest import open_memberships_page


LOG = logging.getLogger(__name__)


@allure.epic("Admin Portal")
@allure.feature("Memberships")
@allure.story("Validation")
@allure.title("MEM-VAL-001 Verify Membership Name is mandatory")
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
@allure.title("MEM-VAL-002 Verify Global Price is mandatory")
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
@allure.title("MEM-VAL-004 Verify duplicate Membership Name is rejected")
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
@allure.title("MEM-VAL-007 Verify negative Global Price is rejected")
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
@allure.title("MEM-VAL-010 Verify negative Global Commission is rejected")
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
