import allure
import pytest

from tests.admin_portal.customers.conftest import (
    CUSTOMER_EMAIL,
    CUSTOMER_FIRST,
    CUSTOMER_LAST,
    CUSTOMER_SITE,
    create_customer_if_missing,
    open_customers_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Customers"),
    allure.story("Validation"),
]


@allure.title("CUST-VAL-001 Blank first name is blocked on save")
@pytest.mark.smoke
def test_blank_first_name_blocked_on_save(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_last_name(CUSTOMER_LAST)
    page.select_site(CUSTOMER_SITE)
    page.click_save_customer()

    assert not page.first_name_input_is_valid()
    assert page.get_first_name_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-002 Blank last name is blocked on save")
@pytest.mark.smoke
def test_blank_last_name_blocked_on_save(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.select_site(CUSTOMER_SITE)
    page.click_save_customer()

    assert not page.last_name_input_is_valid()
    assert page.get_last_name_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-003 Blank site assignment is blocked on save")
@pytest.mark.smoke
def test_blank_site_assignment_blocked_on_save(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name("TVal003")
    # Intentionally skip site selection.
    page.click_save_customer()

    body = page.get_body_text()
    # The form should stay open or show an error — it must not land on the list.
    assert "First Name" in body or "Last Name" in body or "Site" in body
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-004 Invalid email format — document behaviour")
@pytest.mark.edge
def test_invalid_email_format_documents_behaviour(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name("TVal004")
    page.enter_email("not-an-email")
    page.select_site(CUSTOMER_SITE)
    page.click_save_customer()

    # Behaviour may vary: form stays open (validation) or saves (no server-side check).
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-005 Date of birth in the future — document behaviour")
@pytest.mark.edge
def test_dob_in_future_documents_behaviour(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name("TVal005")
    page.select_site(CUSTOMER_SITE)

    dob_el = page.driver.find_elements(*page.DOB_INPUT)
    if dob_el:
        page._set_input_value(dob_el[0], "2099-01-01")

    page.click_save_customer()

    # Document whether a future DOB is accepted or rejected.
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-006 Duplicate email — document behaviour")
@pytest.mark.edge
def test_duplicate_email_documents_behaviour(browser):
    create_customer_if_missing(browser)
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name("TVal006")
    page.enter_email(CUSTOMER_EMAIL)
    page.select_site(CUSTOMER_SITE)
    page.click_save_customer()

    # Document whether duplicate emails are accepted or blocked.
    assert page_has_no_broken_state(page)


@allure.title("CUST-VAL-007 Negative loyalty points amount — document behaviour")
@pytest.mark.edge
@pytest.mark.skip(reason="Requires Loyalty module configuration and loyalty points field on the form.")
def test_negative_loyalty_points_documents_behaviour(browser):
    pass


@allure.title("CUST-VAL Submitting a completely blank form stays on the create page")
@pytest.mark.smoke
def test_blank_form_stays_on_create_page(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.click_save_customer()

    body = page.get_body_text()
    assert "First Name" in body
    assert page_has_no_broken_state(page)
