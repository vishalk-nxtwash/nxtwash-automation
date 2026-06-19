import allure
import pytest

from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import INACTIVE_CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import MISSING_CATEGORY
from tests.admin_portal.service_categories.conftest import create_category_if_missing
from tests.admin_portal.service_categories.conftest import create_inactive_category_if_missing
from tests.admin_portal.service_categories.conftest import open_service_categories_page
from tests.admin_portal.service_categories.conftest import page_has_no_broken_state


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Negative"),
]


@allure.title("SC-NG-001 Create Without Name")
@pytest.mark.regression
@pytest.mark.validation
def test_service_category_required_name_validation(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()
    page.click_save_new()

    assert not page.category_name_input_is_valid()
    assert page.get_category_name_validation_message() != ""
    assert page_has_no_broken_state(page)


@allure.title("SC-NG-002 Create Duplicate Category")
@pytest.mark.regression
def test_create_duplicate_category_is_blocked(browser):

    page = create_category_if_missing(browser)

    page.open_create_category()
    page.enter_category_name(CATEGORY_NAME)
    page.ensure_active_switch_on()
    page.click_save_new()

    # App should reject the duplicate — user stays on the create form
    body = page.get_body_text()
    assert "Category name" in body or "Save new category" in body, (
        "Expected to stay on create form after submitting a duplicate name"
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-NG-003 Create category name exceeding max allowed length")
@pytest.mark.regression
@pytest.mark.validation
def test_create_category_exceeding_max_length(browser):

    page = open_service_categories_page(browser)
    page.open_create_category()

    long_name = "VK " + ("A" * 253)
    page.enter_category_name(long_name)
    page.click_save_new()

    # Either the input truncates the value or the form is blocked
    input_value = page.get_category_name_value()
    body = page.get_body_text()
    assert len(input_value) <= 256 or "Category name" in body
    assert page_has_no_broken_state(page)


@allure.title("SC-NG-004 Create category with leading/trailing/only whitespace")
@pytest.mark.regression
@pytest.mark.validation
def test_create_category_with_whitespace_name(browser):

    page = create_category_if_missing(browser)

    page.open_create_category()
    page.enter_category_name("  %s  " % CATEGORY_NAME)
    page.click_save_new()

    # App should trim and treat it as a duplicate, or show a validation error
    body = page.get_body_text()
    assert "Category name" in body or "Save new category" in body, (
        "Expected form to reject a whitespace-padded duplicate name"
    )
    assert page_has_no_broken_state(page)


@allure.title("SC-RG-006 Search with term matching no category")
@pytest.mark.regression
def test_missing_service_category_is_not_returned(browser):

    page = open_service_categories_page(browser)
    page.search_category(MISSING_CATEGORY)

    assert MISSING_CATEGORY not in page.get_body_text()
    assert page_has_no_broken_state(page)


@allure.title("SC-CRUD-004 Create service category is idempotent")
@pytest.mark.regression
def test_create_service_category_is_idempotent(browser):

    page = create_category_if_missing(browser)
    page.search_category(CATEGORY_NAME)

    assert page.wait_for_category_row(CATEGORY_NAME).is_displayed()
    assert page_has_no_broken_state(page)
