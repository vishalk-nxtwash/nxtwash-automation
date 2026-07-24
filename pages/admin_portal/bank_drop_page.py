from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class BankDropPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/bankDrop') "
        "and not(contains(@src,'/services/bankDrop/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/bankDrop/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/bankDrop/') "
        "and not(contains(@src,'/services/bankDrop/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Bank drop']")
    ADD_BUTTON = (By.XPATH, "//button[normalize-space()='+ Add bank drop']")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[@data-type='item-bordered'][.//img]"
    )
    SAVE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='saveNewBankDrop' "
        "or normalize-space()='Save bank drop' "
        "or normalize-space()='Save new bank drop']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    NAME_INPUT = (
        By.XPATH,
        "//input[@name='name' or @name='bankDropName' "
        "or @name='bankDropCategoryName' or @placeholder='addBankDropName']"
    )
    ORDER_INPUT = (
        By.XPATH,
        "//input[@name='order' or @name='sortOrder' or @placeholder='Order']"
    )
    ACTIVE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active bank drop']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    GRID_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row')]"
    )
    GRID_LOAD_MASK = (
        By.CSS_SELECTOR,
        ".inovua-react-toolkit-load-mask__background-layer"
    )

    def wait_for_list_loaded(self):
        """Wait until the Bank Drop list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))
        self.wait_for_grid_idle()

    def wait_for_grid_idle(self):
        """Wait until the React grid load mask is not blocking interactions."""
        self.wait.until(
            lambda driver: not any(
                mask.is_displayed()
                for mask in driver.find_elements(*self.GRID_LOAD_MASK)
            )
        )

    def wait_for_create_loaded(self):
        """Wait until create Bank Drop form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until edit Bank Drop form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        self.wait.until(lambda driver: self.get_name_value() != "")

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_bank_drop_row_locator(self, name):
        """Build a locator for a Bank Drop row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='bankDropCategoryName']"
            "[.//span[normalize-space()='%s'] or normalize-space()='%s']"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row ')][1]"
            % (name, name)
        )

    def wait_for_bank_drop_row(self, name):
        """Wait until a Bank Drop row is present; scroll it into view if needed."""
        row = self.wait.until(
            EC.presence_of_element_located(self.get_bank_drop_row_locator(name))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", row)
        return row

    def bank_drop_exists(self, name):
        """Return whether a Bank Drop exists in the list.

        Uses find_elements (no wait) after the grid is idle so the call returns
        immediately for items already in the DOM.  Falls back to body-text scan
        for rows the virtual grid has rendered but scrolled out of the viewport.
        """
        self.wait_for_list_loaded()
        if self.driver.find_elements(*self.get_bank_drop_row_locator(name)):
            return True
        return name in self.get_body_text()

    def get_bank_drop_order(self, name):
        """Return visible order for a Bank Drop row."""
        row = self.wait_for_bank_drop_row(name)
        return row.find_element(By.XPATH, ".//*[@data-props-id='sortOrder']").text.strip()

    def get_bank_drop_status(self, name):
        """Return visible status for a Bank Drop row."""
        row = self.wait_for_bank_drop_row(name)
        return row.find_element(By.XPATH, ".//*[@data-props-id='isActive']").text.strip()

    def every_visible_row_has_edit_action(self):
        """Return whether the grid has loaded rows with an Edit action."""
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[contains(@class,'InovuaReactDataGrid__row')"
                    " and .//*[normalize-space()='Edit']]"
                ))
            )
            return True
        except TimeoutException:
            return False

    def pagination_controls_are_visible(self):
        """Return whether pagination controls are visible."""
        text = self.get_body_text()
        return "Page" in text and "Results per page" in text

    def download_button_is_visible(self):
        """Return whether the download button is visible."""
        button = self.wait.until(EC.presence_of_element_located(self.DOWNLOAD_BUTTON))
        return button.is_displayed()

    def add_button_is_clickable(self):
        """Return whether the Add bank drop button is clickable."""
        return self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON)).is_displayed()

    def get_visible_row_orders(self):
        """Return order integer values from visible grid rows, in DOM order."""
        orders = []
        rows = [r for r in self.driver.find_elements(*self.GRID_ROWS) if r.is_displayed()]
        for row in rows:
            try:
                cells = row.find_elements(By.XPATH, ".//*[@data-props-id='sortOrder']")
                if cells:
                    val = cells[0].text.strip()
                    if val:
                        orders.append(int(val))
            except Exception:  # noqa: BLE001
                continue
        return orders

    def open_create(self):
        """Open create Bank Drop form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_BUTTON)
        self.wait_for_create_loaded()

    def open_edit(self, name):
        """Open edit Bank Drop form."""
        self.wait_for_list_loaded()
        row = self.wait_for_bank_drop_row(name)
        edit_button = row.find_element(
            By.XPATH, ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_edit_loaded()

    def get_name_value(self):
        """Return current Bank Drop name input value."""
        element = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        return element.get_attribute("value")

    def get_order_value(self):
        """Return current Bank Drop order input value."""
        element = self.wait.until(EC.visibility_of_element_located(self.ORDER_INPUT))
        return element.get_attribute("value")

    def enter_name(self, name):
        """Enter Bank Drop name."""
        self.enter_text(self.NAME_INPUT, name)

    def enter_order(self, order):
        """Enter Bank Drop order."""
        self.enter_text(self.ORDER_INPUT, order)

    def active_bank_drop_is_on(self):
        """Return whether Active bank drop is enabled."""
        switch = self.wait.until(EC.presence_of_element_located(self.ACTIVE_SWITCH))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_active_on(self):
        """Turn active Bank Drop on if needed."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            self.wait.until(lambda driver: switch.get_attribute("aria-checked") == "true")

    def ensure_active_off(self):
        """Turn active Bank Drop off if needed."""
        switch = self.wait.until(EC.element_to_be_clickable(self.ACTIVE_SWITCH))
        if switch.get_attribute("aria-checked") != "false":
            switch.click()
            self.wait.until(lambda driver: switch.get_attribute("aria-checked") == "false")

    def fill_form(self, name, order):
        """Fill Bank Drop form with requested settings."""
        self.enter_name(name)
        self.enter_order(order)
        self.ensure_active_on()

    def click_save(self):
        """Click save Bank Drop."""
        self.click(self.SAVE_BUTTON)

    def click_cancel(self):
        """Cancel create/edit Bank Drop."""
        self.click(self.CANCEL_BUTTON)

    def bank_drop_name_input_is_valid(self):
        """Return native validity state for Bank Drop name."""
        element = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        return self.driver.execute_script("return arguments[0].checkValidity();", element)

    def bank_drop_order_input_is_valid(self):
        """Return native validity state for Bank Drop order."""
        element = self.wait.until(EC.visibility_of_element_located(self.ORDER_INPUT))
        return self.driver.execute_script("return arguments[0].checkValidity();", element)

    def get_bank_drop_name_validation_message(self):
        """Return native validation message for Bank Drop name."""
        element = self.wait.until(EC.visibility_of_element_located(self.NAME_INPUT))
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def get_bank_drop_order_validation_message(self):
        """Return native validation message for Bank Drop order."""
        element = self.wait.until(EC.visibility_of_element_located(self.ORDER_INPUT))
        return self.driver.execute_script("return arguments[0].validationMessage;", element)

    def deactivate_bank_drop(self, name):
        """Open edit for name, set active off, save, and return to the list."""
        self.open_edit(name)
        self.ensure_active_off()
        self.click_save()
        self.wait_for_list_loaded()

    def create_bank_drop(self, name, order):
        """Create an active Bank Drop and return to the list.

        Returns True when the save succeeded and the list re-loaded.
        Returns False when the server rejected the save (e.g. duplicate name)
        and the list did not reload — the driver is left at default_content.
        """
        self.open_create()
        self.fill_form(name, order)
        self.click_save()
        try:
            self.wait_for_list_loaded()
            return True
        except TimeoutException:
            self.driver.switch_to.default_content()
            return False
