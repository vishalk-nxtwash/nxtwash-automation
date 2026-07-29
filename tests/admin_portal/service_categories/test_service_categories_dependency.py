import allure
import pytest

from tests.admin_portal.discounts.conftest import open_discounts_page
from tests.admin_portal.discounts.conftest import page_has_no_broken_state
from tests.admin_portal.service_categories.conftest import CATEGORY_NAME
from tests.admin_portal.service_categories.conftest import create_category_if_missing


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Service Categories"),
    allure.story("Dependency"),
]


@allure.title("SC-DEP-001 Created category is selectable in discount creation")
@pytest.mark.regression
@pytest.mark.skip(reason="staging data / intermittent — deferred")
def test_category_available_in_discount_creation(browser):

    create_category_if_missing(browser)

    discounts_page = open_discounts_page(browser)
    discounts_page.open_create_discount()
    discounts_page.open_service_category_dropdown()

    option = discounts_page.find_select_option(CATEGORY_NAME)

    assert option is not None, (
        "Expected service category '%s' to be selectable in the discount "
        "creation form" % CATEGORY_NAME
    )
    assert page_has_no_broken_state(discounts_page)


@allure.title("SC-EC-001 Rename category linked to discount [requires cross-module fixture]")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Needs a stable cross-module fixture that links a specific category to a "
        "discount. Deferred until single-module SC coverage is solid."
    )
)
def test_rename_category_linked_to_discount(browser):
    pass


@allure.title("SC-DEP-002 Deactivate category used by discount [requires cross-module fixture]")
@pytest.mark.regression
@pytest.mark.skip(
    reason=(
        "Needs controlled discount data linked to a specific service category. "
        "Deferred until single-module SC coverage is solid."
    )
)
def test_deactivate_category_used_by_discount(browser):
    pass


@allure.title("SC-DEP-003 Category available when assigning services [requires Services module]")
@pytest.mark.regression
@pytest.mark.skip(reason="Services module not yet automated. Deferred.")
def test_category_available_assigning_services(browser):
    pass


@allure.title("SC-DEP-004 Rename category with assigned services [requires Services module]")
@pytest.mark.regression
@pytest.mark.skip(reason="Services module not yet automated. Deferred.")
def test_rename_category_with_assigned_services(browser):
    pass
