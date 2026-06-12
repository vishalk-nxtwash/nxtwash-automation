import allure

from tests.admin_portal.memberships.conftest import MISSING_MEMBERSHIP
from tests.admin_portal.memberships.conftest import open_memberships_page
from tests.admin_portal.memberships.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Memberships"),
    allure.story("Negative"),
]


def test_missing_membership_is_not_returned(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership(MISSING_MEMBERSHIP)

    assert MISSING_MEMBERSHIP not in memberships_page.get_body_text()
    assert page_has_no_broken_state(memberships_page)


def test_memberships_special_character_search_stays_usable(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.search_membership("%%%___###")

    assert page_has_no_broken_state(memberships_page)
    assert memberships_page.driver.find_element(
        *memberships_page.SEARCH_INPUT
    ).is_displayed()
