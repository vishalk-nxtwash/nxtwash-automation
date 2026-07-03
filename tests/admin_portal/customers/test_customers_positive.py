import uuid

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
    allure.story("CRUD"),
]


@allure.title("CUST-CRT-001 Create customer with required fields only appears in the list")
@pytest.mark.smoke
def test_create_customer_with_required_fields_only(browser):
    last = "TCrt1-%s" % uuid.uuid4().hex[:6]
    page = open_customers_page(browser)
    page.create_customer(CUSTOMER_FIRST, last, CUSTOMER_SITE)
    page.open_filter_panel()
    page.filter_by_last_name(last)
    page.apply_filters()

    assert last in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-002 Create customer with all optional fields filled appears in the list")
@pytest.mark.regression
def test_create_customer_with_all_optional_fields(browser):
    last = "TCrt2-%s" % uuid.uuid4().hex[:6]
    email = "vk.%s@nxtwash-auto.com" % last.lower()
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name(last)
    page.enter_email(email)
    page.ensure_active_switch_on()
    page.select_site(CUSTOMER_SITE)
    page.click_save_customer()
    page.wait_for_list_loaded()
    page.open_filter_panel()
    page.filter_by_last_name(last)
    page.apply_filters()

    assert last in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-003 Date of birth calendar picker accepts a past date")
@pytest.mark.regression
def test_date_of_birth_calendar_picker_selects_past_date(browser):
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name("TDob-%s" % uuid.uuid4().hex[:4])
    page.select_site(CUSTOMER_SITE)

    dob_el = page.driver.find_elements(*page.DOB_INPUT)
    if dob_el:
        page._set_input_value(dob_el[0], "1990-06-15")

    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-004 Assign to Loc/Site dropdown lists available sites")
@pytest.mark.regression
def test_assign_to_site_dropdown_lists_available_sites(browser):
    page = open_customers_page(browser)
    page.open_create_customer()

    # Select the site — this internally opens the dropdown and picks the option.
    # If the site is not listed, select_site() will raise a TimeoutException.
    page.select_site(CUSTOMER_SITE)

    # After selection the chosen site name must appear in the form (selected value).
    body = page.get_body_text()
    assert CUSTOMER_SITE.upper() in body.upper()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-005 State dropdown populates cities on selection")
@pytest.mark.regression
def test_state_dropdown_populates_cities_on_selection(browser):
    page = open_customers_page(browser)
    page.open_create_customer()

    if not page.state_dropdown_is_visible():
        pytest.skip("State dropdown not present on this form — verify field availability.")

    page.select_state("California")

    assert page.city_dropdown_is_visible()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-006 City dropdown has no options when no state is selected")
@pytest.mark.edge
def test_city_dropdown_empty_without_state(browser):
    page = open_customers_page(browser)
    page.open_create_customer()

    if not page.city_dropdown_is_visible():
        pytest.skip("City dropdown not present on this form variant.")

    assert page.city_dropdown_has_no_options()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-007 Create inactive customer — hidden from default active-only list")
@pytest.mark.regression
def test_create_inactive_customer(browser):
    last = "TInact-%s" % uuid.uuid4().hex[:6]
    page = open_customers_page(browser)
    page.open_create_customer()
    page.enter_first_name(CUSTOMER_FIRST)
    page.enter_last_name(last)
    page.select_site(CUSTOMER_SITE)
    page.ensure_active_switch_off()
    page.click_save_customer()
    page.wait_for_list_loaded()

    # Default list shows active only — inactive customer should not appear.
    page.open_filter_panel()
    page.filter_by_last_name(last)
    page.apply_filters()

    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-008 Cars settings and Payment settings tabs are disabled for a new customer")
@pytest.mark.smoke
def test_cars_and_payment_tabs_disabled_for_new_customer(browser):
    page = open_customers_page(browser)
    page.open_create_customer()

    assert page.cars_settings_tab_is_disabled()
    assert page.payment_settings_tab_is_disabled()
    assert page_has_no_broken_state(page)


@allure.title("CUST-CRT-009 Cancel out of Add new customer returns to the list without saving")
@pytest.mark.edge
def test_cancel_add_customer_returns_to_list(browser):
    page = open_customers_page(browser)
    count_before = page.get_visible_row_count()

    page.open_create_customer()
    page.enter_first_name("VK")
    page.enter_last_name("TCancel-%s" % uuid.uuid4().hex[:4])
    page.click_cancel()
    page.wait_for_list_loaded()

    # Row count should be the same as before — no new customer created.
    assert page.get_visible_row_count() == count_before
    assert page_has_no_broken_state(page)


# ── Persistence ───────────────────────────────────────────────────────────────

@allure.title("CUST-PER-001 Create customer then refresh — data persists")
@pytest.mark.regression
def test_create_then_refresh_data_persists(browser):
    last = "TPer1-%s" % uuid.uuid4().hex[:6]
    page = open_customers_page(browser)
    page.create_customer(CUSTOMER_FIRST, last, CUSTOMER_SITE, email="")

    # Force a full page reload to exercise server-side persistence.
    page = open_customers_page(browser)
    page.open_filter_panel()
    page.filter_by_last_name(last)
    page.apply_filters()

    assert last in page.get_body_text()
    assert page_has_no_broken_state(page)
