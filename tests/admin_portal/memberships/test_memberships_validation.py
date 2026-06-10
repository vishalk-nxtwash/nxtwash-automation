from tests.admin_portal.memberships.conftest import open_memberships_page


def test_membership_required_name_validation(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.click_save_membership()

    assert not memberships_page.membership_name_input_is_valid()
    assert memberships_page.get_membership_name_validation_message() != ""


def test_membership_blank_required_form_stays_on_form(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.click_save_membership()

    assert "Add new membership" in memberships_page.get_body_text()
    assert "Membership name" in memberships_page.get_body_text()


def test_membership_invalid_numeric_values_do_not_break_form(browser):

    memberships_page = open_memberships_page(browser)
    memberships_page.open_create_membership()
    memberships_page.enter_membership_name("invalid-membership-numeric")
    memberships_page.set_global_price("-1")
    memberships_page.set_global_commission("abc")

    assert "Membership name" in memberships_page.get_body_text()
    assert memberships_page.get_membership_name_value() == "invalid-membership-numeric"
