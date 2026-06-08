from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class ServiceCategoriesPage(BasePage):

    FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories')]"
    )
    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories?')]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/serviceCategories/') "
        "and not(contains(@src,'/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Service categories']")
    SEARCH_INPUT = (By.NAME, "categoryName")
    FILTER_BUTTON = (By.XPATH, "//button[normalize-space()='Filter by']")
    ADD_CATEGORY_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new category']"
    )
    SAVE_NEW_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save new category']"
    )
    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CATEGORY_NAME_INPUT = (By.NAME, "categoryName")
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )

    def switch_to_module_frame(self):
        """Switch into the Service Categories iframe."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.FRAME))

    def wait_for_list_loaded(self):
        """Wait until the Service Categories list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_CATEGORY_BUTTON))

    def wait_for_create_loaded(self):
        """Wait until the create category form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_NEW_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit category form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CHANGES_BUTTON))

    def get_body_text(self):
        """Get visible text inside the current frame."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_category_row_locator(self, category_name):
        """Build a locator for a virtual-grid row by category name."""
        return (
            By.XPATH,
            "//*[@data-props-id='categoryName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % category_name
        )

    def wait_for_category_row(self, category_name):
        """Wait until a category row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_category_row_locator(category_name)
            )
        )

    def category_exists(self, category_name):
        """Return whether the category exists in the list."""
        self.wait_for_list_loaded()
        self.search_category(category_name)

        try:
            self.wait_for_category_row(category_name)
            return True
        except TimeoutException:
            return False

    def search_category(self, category_name):
        """Search category by name."""
        self.enter_text(self.SEARCH_INPUT, category_name)
        self.wait.until(
            lambda driver: (
                category_name in self.get_body_text()
                or "Showing 0" in self.get_body_text()
                or "No records" in self.get_body_text()
            )
        )

    def get_category_status(self, category_name):
        """Return visible status for a category row."""
        row = self.wait_for_category_row(category_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def open_create_category(self):
        """Open create category form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_CATEGORY_BUTTON)
        self.wait_for_create_loaded()

    def open_edit_category(self, category_name):
        """Open edit category form."""
        self.wait_for_list_loaded()
        self.search_category(category_name)
        row = self.wait_for_category_row(category_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def enter_category_name(self, category_name):
        """Enter category name."""
        self.enter_text(self.CATEGORY_NAME_INPUT, category_name)

    def get_category_name_validation_message(self):
        """Return native validation message for category name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def category_name_input_is_valid(self):
        """Return native validity state for category name input."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CATEGORY_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def active_switch_is_on(self):
        """Return whether active switch is checked."""
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_SWITCH)
        )
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_switch_on(self):
        """Turn active switch on if needed."""
        switch = self.wait.until(
            EC.element_to_be_clickable(self.ACTIVE_SWITCH)
        )

        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(
                lambda driver: switch.get_attribute("aria-checked") == "true"
            )

    def click_save_new(self):
        """Save new category."""
        self.click(self.SAVE_NEW_BUTTON)

    def click_save_changes(self):
        """Save category changes."""
        self.click(self.SAVE_CHANGES_BUTTON)

    def click_cancel(self):
        """Cancel create/edit category."""
        self.click(self.CANCEL_BUTTON)

    def create_category(self, category_name):
        """Create an active category."""
        self.open_create_category()
        self.enter_category_name(category_name)
        self.ensure_active_switch_on()
        self.click_save_new()
        self.wait_for_list_loaded()

    def update_category_name(self, old_name, new_name):
        """Update category name and return to list."""
        self.open_edit_category(old_name)
        self.enter_category_name(new_name)
        self.ensure_active_switch_on()
        self.click_save_changes()
        self.wait_for_list_loaded()
