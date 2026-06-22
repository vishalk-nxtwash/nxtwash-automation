import allure
import pytest

from tests.admin_portal.wash_extras.conftest import (
    EXISTING_EXTRA,
    GLOBAL_PRICE,
    MISSING_EXTRA,
    open_wash_extras_page,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Wash Extras"),
    allure.story("Negative"),
]


@allure.title("WE-SRH-003 Searching a non-existing wash extra shows empty state without error")
@pytest.mark.extended
def test_missing_wash_extra_is_not_returned(browser):

    page = open_wash_extras_page(browser)
    page.search_extra(MISSING_EXTRA)

    assert MISSING_EXTRA not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WE-SRH injection payloads in search do not produce a broken page state")
@pytest.mark.regression
def test_wash_extras_search_payloads_do_not_break_grid(browser):

    page = open_wash_extras_page(browser)

    for payload in ("' OR 1=1 --", "<script>alert(1)</script>"):
        page.search_extra(payload)
        assert page_has_no_broken_state(page)


@allure.title("WE-NAM-003 Duplicate wash extra name is blocked on save")
@pytest.mark.regression
def test_duplicate_wash_extra_name_is_blocked(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name(EXISTING_EXTRA)
    page.set_global_price(GLOBAL_PRICE)
    page.click_save_extra()

    body_text = page.get_body_text()
    error_shown = any(
        phrase in body_text.lower()
        for phrase in ("already exists", "duplicate", "exist")
    )
    still_on_form = "Add new wash extra" in body_text or "Service name" in body_text
    assert error_shown or still_on_form
    assert page_has_no_broken_state(page)


@allure.title("WE-NAM-005 A whitespace-only service name is rejected on save")
@pytest.mark.extended
def test_whitespace_only_service_name_is_rejected(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("   ")
    page.set_global_price(GLOBAL_PRICE)
    page.click_save_extra()

    assert (
        not page.service_name_input_is_valid()
        or "Add new wash extra" in page.get_body_text()
    )
    assert page_has_no_broken_state(page)


@allure.title("WE-PRI-005 Negative global price is rejected on save")
@pytest.mark.regression
def test_negative_global_price_is_rejected(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-neg-price-test")
    page.set_global_price("-10")
    page.click_save_extra()

    assert (
        "Add new wash extra" in page.get_body_text()
        or not page.global_price_input_is_valid()
    )
    assert page_has_no_broken_state(page)


@allure.title("WE-COM-002 Negative global commission is rejected on save")
@pytest.mark.extended
def test_negative_global_commission_is_rejected(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-neg-commission-test")
    page.set_global_price(GLOBAL_PRICE)
    page.set_global_commission("-2")
    page.click_save_extra()

    assert "Add new wash extra" in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("WE-BAR-003 Duplicate barcode is rejected on save")
@pytest.mark.regression
@pytest.mark.skip(
    reason="WE-BAR-003: Requires a known barcode already assigned to another wash extra. "
    "Deferred until barcode fixtures are established."
)
def test_duplicate_barcode_is_rejected(browser):
    pass


@allure.title("WE-LTY-004 Negative loyalty points is rejected on save")
@pytest.mark.extended
def test_negative_loyalty_points_is_rejected(browser):

    page = open_wash_extras_page(browser)
    page.open_create_extra()
    page.enter_service_name("VK EWA2-neg-points-test")
    page.set_points_awarded("-1")

    assert page_has_no_broken_state(page)
