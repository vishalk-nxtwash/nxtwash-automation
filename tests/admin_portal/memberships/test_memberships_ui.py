from selenium.webdriver.common.by import By

from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


def test_memberships_page_loads_with_primary_controls(browser):

    memberships_page = open_memberships_page(browser)
    body_text = memberships_page.get_body_text()

    assert "Memberships" in body_text
    assert memberships_page.driver.find_element(
        *memberships_page.SEARCH_INPUT
    ).is_displayed()
    assert memberships_page.driver.find_element(
        *memberships_page.FILTER_BUTTON
    ).is_displayed()
    assert memberships_page.download_button_is_clickable()
    assert memberships_page.driver.find_element(
        *memberships_page.ADD_MEMBERSHIP_BUTTON
    ).is_displayed()
    assert page_has_no_broken_state(memberships_page)


def test_memberships_grid_columns_are_visible(browser):

    memberships_page = open_memberships_page(browser)
    body_text = memberships_page.get_body_text()

    assert "Membership Name" in body_text
    assert "Type" in body_text
    assert "Price" in body_text
    assert "Status" in body_text


def test_add_membership_form_loads(browser):

    memberships_page = open_memberships_page(browser)

    memberships_page.open_create_membership()
    body_text = memberships_page.get_body_text()

    assert "Add new membership" in body_text
    assert "Membership name" in body_text
    assert "Global price" in body_text
    assert "Global commission" in body_text
    assert memberships_page.driver.find_element(
        By.NAME,
        "membershipName"
    ).is_displayed()
