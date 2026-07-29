from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class GiftCardsPage(BasePage):

    LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/giftCards')"
        " and not(contains(@src,'/services/giftCards/'))]"
    )
    CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/giftCards/new')]"
    )
    EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/giftCards/') "
        "and not(contains(@src,'/services/giftCards/new'))]"
    )
    CUSTOMER_LIST_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customerGiftCards')"
        " and not(contains(@src,'/services/customerGiftCards/'))]"
    )
    CUSTOMER_CREATE_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customerGiftCards/new')]"
    )
    CUSTOMER_EDIT_FRAME = (
        By.XPATH,
        "//iframe[contains(@src,'/services/customerGiftCards/') "
        "and not(contains(@src,'/services/customerGiftCards/new'))]"
    )

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Gift cards']")
    CUSTOMER_PAGE_TITLE = (
        By.XPATH,
        "//*[normalize-space()='Customer gift cards']"
    )
    SEARCH_INPUT = (By.NAME, "giftCardName")
    CUSTOMER_SEARCH_INPUT = (By.NAME, "giftCardNumber")
    FILTER_BUTTON = (By.XPATH, "//button[starts-with(normalize-space(), 'Filter by')]")
    DOWNLOAD_BUTTON = (
        By.XPATH,
        "//button[starts-with(normalize-space(), 'Filter by')]/following-sibling::button[1]"
    )
    ADD_GIFT_CARD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add new gift card']"
    )
    CUSTOMER_GIFT_CARDS_TAB = (
        By.XPATH,
        "//button[normalize-space()='Customer gift cards']"
    )
    ADD_CUSTOMER_GIFT_CARD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='+ Add customer gift card']"
    )
    SAVE_GIFT_CARD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save gift card']"
    )
    SAVE_CUSTOMER_GIFT_CARD_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save customer gift card']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_ALL_BUTTON = (By.XPATH, "//button[normalize-space()='Reset all']")
    FILTER_SITE_INPUT = (
        By.XPATH,
        "//*[normalize-space()='Select site']/following::input[1]"
    )
    ACTIVE_GIFT_CARD_FILTER_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active gift card']"
        "/following::*[@role='switch' or self::input][1]"
    )
    GIFT_CARD_GRID_ROWS = (
        By.XPATH,
        "//*[contains(@class,'InovuaReactDataGrid__row') "
        "and .//*[@data-props-id='giftCardName']]"
    )

    GIFT_CARD_NAME_INPUT = (By.NAME, "giftCardName")
    GIFT_CARD_AMOUNT_INPUT = (By.NAME, "giftCardAmount")
    LANDING_PAGE_CODE_INPUT = (By.NAME, "landingPageCode")
    CUSTOMER_GIFT_CARD_NUMBER_INPUT = (By.NAME, "giftCardNumber")
    CUSTOMER_GIFT_CARD_AMOUNT_INPUT = (By.NAME, "giftCardAmount")

    OPEN_PRICE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Open price']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    WASH_CARD_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Wash card']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    SHOW_ON_CUSTOMER_PORTAL_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Show on customer portal']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    ACTIVE_SERVICE_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active service']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )
    ACTIVE_CUSTOMER_GIFT_CARD_SWITCH = (
        By.XPATH,
        "//*[normalize-space()='Active customer gift card']"
        "/ancestor::*[contains(@class,'flex-toggler')][1]"
        "//button[@role='switch']"
    )

    def wait_for_list_loaded(self):
        """Wait until the Gift Cards list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.LIST_FRAME)
        )
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_GIFT_CARD_BUTTON))
        # Wait for the grid column headers — the inovua grid initialises
        # asynchronously; in headless mode the header can lag behind the add
        # button, causing body-text assertions to see an empty page.
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[normalize-space()='Gift card name']")
            )
        )

    def wait_for_create_loaded(self):
        """Wait until the create gift card form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CREATE_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_GIFT_CARD_BUTTON))

    def wait_for_edit_loaded(self):
        """Wait until the edit gift card form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.EDIT_FRAME))
        self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_NAME_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_GIFT_CARD_BUTTON))
        self.wait.until(lambda driver: self.get_gift_card_name_value() != "")
        self.wait.until(
            lambda driver: driver.find_element(
                *self.GIFT_CARD_AMOUNT_INPUT
            ).get_attribute("value") != ""
        )
        # Wait for the assign-to grid to finish its async render before filling
        # the form — the grid's data load triggers a React re-render that can
        # reset controlled inputs (amount, landing page code) to their server
        # values if we type into them before the grid settles.
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 ".service-sites-table .InovuaReactDataGrid__row")
            )
        )

    def wait_for_customer_list_loaded(self):
        """Wait until the Customer Gift Cards list is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CUSTOMER_LIST_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_PAGE_TITLE)
        )
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_CUSTOMER_GIFT_CARD_BUTTON)
        )

    def wait_for_customer_create_loaded(self):
        """Wait until the create customer gift card form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                self.CUSTOMER_CREATE_FRAME
            )
        )
        self.wait.until(
            EC.visibility_of_element_located(
                self.CUSTOMER_GIFT_CARD_NUMBER_INPUT
            )
        )
        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_CUSTOMER_GIFT_CARD_BUTTON)
        )

    def get_body_text(self):
        """Get visible text inside the current iframe."""
        return self.driver.find_element(By.TAG_NAME, "body").text

    def get_gift_card_row_locator(self, gift_card_name):
        """Build a locator for a gift card row by name."""
        return (
            By.XPATH,
            "//*[@data-props-id='giftCardName']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % gift_card_name
        )

    def wait_for_gift_card_row(self, gift_card_name):
        """Wait until a gift card row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_gift_card_row_locator(gift_card_name)
            )
        )

    def search_gift_card(self, gift_card_name):
        """Search gift card by name."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(gift_card_name)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == gift_card_name
        )

    def clear_gift_card_search(self):
        """Clear the gift card search input."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.SEARCH_INPUT
            ).get_attribute("value") == ""
        )

    def search_customer_gift_card(self, gift_card_number):
        """Search customer gift card by number."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.CUSTOMER_SEARCH_INPUT)
        )
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(gift_card_number)
        self.wait.until(
            lambda driver: driver.find_element(
                *self.CUSTOMER_SEARCH_INPUT
            ).get_attribute("value") == gift_card_number
        )

    def gift_card_exists(self, gift_card_name):
        """Return whether a gift card exists in the list."""
        self.wait_for_list_loaded()
        self.search_gift_card(gift_card_name)

        try:
            self.wait_for_gift_card_row(gift_card_name)
            return True
        except TimeoutException:
            return False

    def get_gift_card_amount(self, gift_card_name):
        """Return visible amount for a gift card row."""
        row = self.wait_for_gift_card_row(gift_card_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='giftCardAmount']"
        ).text.strip()

    def get_gift_card_status(self, gift_card_name):
        """Return visible status for a gift card row."""
        row = self.wait_for_gift_card_row(gift_card_name)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='isActive']"
        ).text.strip()

    def get_customer_gift_card_row_locator(self, gift_card_number):
        """Build a locator for a customer gift card row by number."""
        return (
            By.XPATH,
            "//*[@data-props-id='giftCardNumber']"
            "[.//span[normalize-space()='%s']]"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % gift_card_number
        )

    def wait_for_customer_gift_card_row(self, gift_card_number):
        """Wait until a customer gift card row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_customer_gift_card_row_locator(gift_card_number)
            )
        )

    def customer_gift_card_exists(self, gift_card_number):
        """Return whether a customer gift card exists in the list."""
        self.wait_for_customer_list_loaded()
        self.search_customer_gift_card(gift_card_number)

        try:
            self.wait_for_customer_gift_card_row(gift_card_number)
            return True
        except TimeoutException:
            return False

    def get_customer_gift_card_name(self, gift_card_number):
        """Return visible gift card name for a customer gift card row."""
        row = self.wait_for_customer_gift_card_row(gift_card_number)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='giftCardName']"
        ).text.strip()

    def get_customer_gift_card_amount(self, gift_card_number):
        """Return visible amount for a customer gift card row."""
        row = self.wait_for_customer_gift_card_row(gift_card_number)
        return row.find_element(
            By.XPATH,
            ".//*[@data-props-id='giftCardAmount']"
        ).text.strip()

    def download_button_is_clickable(self):
        """Return whether the download button can be clicked."""
        return self.wait.until(
            EC.element_to_be_clickable(self.DOWNLOAD_BUTTON)
        ).is_displayed()

    def open_create_gift_card(self):
        """Open create gift card form."""
        self.wait_for_list_loaded()
        self.click(self.ADD_GIFT_CARD_BUTTON)
        self.wait_for_create_loaded()

    def open_customer_gift_cards(self):
        """Open Customer gift cards tab."""
        self.wait_for_list_loaded()
        self.click(self.CUSTOMER_GIFT_CARDS_TAB)
        self.wait_for_customer_list_loaded()

    def open_create_customer_gift_card(self):
        """Open create customer gift card form."""
        self.wait_for_customer_list_loaded()
        self.click(self.ADD_CUSTOMER_GIFT_CARD_BUTTON)
        self.wait_for_customer_create_loaded()

    def open_edit_gift_card(self, gift_card_name):
        """Open edit gift card form."""
        self.wait_for_list_loaded()
        self.search_gift_card(gift_card_name)
        row = self.wait_for_gift_card_row(gift_card_name)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        # The inovua load-mask briefly covers the grid while data loads; JS
        # click bypasses the overlay so we don't need a separate mask wait.
        self.driver.execute_script("arguments[0].click();", edit_button)
        self.wait_for_edit_loaded()

    def get_gift_card_name_value(self):
        """Return current gift card name input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_NAME_INPUT)
        )
        return element.get_attribute("value")

    def get_gift_card_name_validation_message(self):
        """Return native validation message for gift card name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def gift_card_name_input_is_valid(self):
        """Return native validity state for gift card name."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_NAME_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def enter_gift_card_name(self, gift_card_name):
        """Enter gift card name."""
        self.enter_text(self.GIFT_CARD_NAME_INPUT, gift_card_name)

    def enter_gift_card_amount(self, amount):
        """Enter gift card amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_AMOUNT_INPUT)
        )
        element.click()
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(str(amount))

    def enter_landing_page_code(self, landing_page_code):
        """Enter landing page code."""
        self.enter_text(self.LANDING_PAGE_CODE_INPUT, landing_page_code)

    def get_select_input_by_label(self, label):
        """Return a React Select input using its visible label."""
        return self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='%s']"
                    "/ancestor::*[contains(@class,'form-select__wrapper')][1]"
                    "//input[@role='combobox']" % label
                )
            )
        )

    def select_option_by_label(self, label, option):
        """Select a React Select option by field label."""
        select_input = self.get_select_input_by_label(label)
        select_input.click()
        select_input.send_keys(option)
        from selenium.webdriver.support.ui import WebDriverWait
        option_element = WebDriverWait(self.driver, 20).until(
            lambda d: self._find_react_option(option)
        )
        self.driver.execute_script("arguments[0].click();", option_element)
        self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[normalize-space()='%s']"
                    "/ancestor::*[contains(@class,'form-select__wrapper')][1]"
                    "//*[normalize-space()='%s']" % (label, option)
                )
            )
        )

    def select_customer_gift_card_site(self, site_name):
        """Select site on customer gift card form."""
        self.select_option_by_label("Select site", site_name)

    def select_customer_gift_card_template(self, gift_card_name):
        """Select gift card on customer gift card form."""
        self.select_option_by_label("Select gift card", gift_card_name)

    def enter_customer_gift_card_number(self, gift_card_number):
        """Enter customer gift card number."""
        self.enter_text(self.CUSTOMER_GIFT_CARD_NUMBER_INPUT, gift_card_number)

    def enter_customer_gift_card_amount(self, amount):
        """Enter customer gift card amount."""
        self.enter_text(self.CUSTOMER_GIFT_CARD_AMOUNT_INPUT, str(amount))

    def customer_gift_card_number_input_is_valid(self):
        """Return native validity state for customer gift card number."""
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.CUSTOMER_GIFT_CARD_NUMBER_INPUT
            )
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def get_customer_gift_card_number_validation_message(self):
        """Return native validation message for customer gift card number."""
        element = self.wait.until(
            EC.visibility_of_element_located(
                self.CUSTOMER_GIFT_CARD_NUMBER_INPUT
            )
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def switch_is_on(self, locator):
        """Return whether a switch is enabled."""
        switch = self.wait.until(EC.presence_of_element_located(locator))
        return switch.get_attribute("aria-checked") == "true"

    def ensure_switch_on(self, locator):
        """Turn a switch on if needed."""
        switch = self.wait.until(EC.presence_of_element_located(locator))

        if switch.get_attribute("aria-checked") != "true":
            # JS click bypasses the settings-page__form-column overlay that
            # intercepts regular clicks when the assignment grid is tall.
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(*locator).get_attribute("aria-checked") == "true"
            )

    def enable_all_main_toggles(self):
        """Enable all gift card-level toggles."""
        self.ensure_switch_on(self.OPEN_PRICE_SWITCH)
        self.ensure_switch_on(self.WASH_CARD_SWITCH)
        self.ensure_switch_on(self.SHOW_ON_CUSTOMER_PORTAL_SWITCH)
        self.ensure_switch_on(self.ACTIVE_SERVICE_SWITCH)

    def ensure_active_customer_gift_card_on(self):
        """Turn active customer gift card on if needed."""
        self.ensure_switch_on(self.ACTIVE_CUSTOMER_GIFT_CARD_SWITCH)

    def main_toggles_are_on(self):
        """Return whether all gift card-level toggles are enabled."""
        return (
            self.switch_is_on(self.OPEN_PRICE_SWITCH)
            and self.switch_is_on(self.WASH_CARD_SWITCH)
            and self.switch_is_on(self.SHOW_ON_CUSTOMER_PORTAL_SWITCH)
            and self.switch_is_on(self.ACTIVE_SERVICE_SWITCH)
        )

    def _checkbox_is_checked(self, checkbox):
        """Return whether an Inovua grid checkbox is checked."""
        classes = checkbox.get_attribute("class")
        return (
            "inovua-react-toolkit-checkbox--checked" in classes
            and "inovua-react-toolkit-checkbox--unchecked" not in classes
        )

    def get_location_row(self, location_name):
        """Return the location assignment row, scrolling the virtual grid as needed.

        InovuaReactDataGrid uses virtual scrolling — only rows near the current
        viewport are rendered in the DOM.  Scroll the grid's own scroller element
        (data-name="scroller" inside .service-sites-table) 300 px per poll until
        the target row becomes visible.
        """
        scroller = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".service-sites-table [data-name='scroller']")
            )
        )
        row_locator = (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
            % location_name
        )

        def _find_or_scroll(driver):
            rows = driver.find_elements(*row_locator)
            if rows and rows[0].is_displayed():
                # Scroll the row to the top of the grid viewport so it clears
                # the settings-page__form-column overlay at the bottom edge.
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'start'});", rows[0]
                )
                refreshed = driver.find_elements(*row_locator)
                return refreshed[0] if refreshed and refreshed[0].is_displayed() else False
            driver.execute_script("arguments[0].scrollTop += 300;", scroller)
            return False

        return self.wait.until(_find_or_scroll)

    def assign_location(self, location_name):
        """Assign a gift card to one location."""
        row = self.get_location_row(location_name)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        if not self._checkbox_is_checked(checkbox):
            checkbox.click()
            # Wait via a fresh locator — virtual grid re-renders the row after
            # the click, making the original stale-element wait unreliable.
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//*[normalize-space()='%s']"
                    "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
                    "//*[contains(@class,'inovua-react-toolkit-checkbox--checked')"
                    " and not(contains(@class,'inovua-react-toolkit-checkbox--unchecked'))]"
                    % location_name
                ))
            )

    def location_is_assigned(self, location_name):
        """Return whether a location is assigned."""
        row = self.get_location_row(location_name)
        checkbox = row.find_element(
            By.XPATH,
            ".//*[contains(@class,'inovua-react-toolkit-checkbox')]"
        )

        return self._checkbox_is_checked(checkbox)

    def enable_location_show_on_cp(self, location_name):
        """Enable Show on CP for one assigned location."""
        row = self.get_location_row(location_name)
        switch = row.find_element(By.XPATH, "(.//button[@role='switch'])[last()]")

        if switch.get_attribute("aria-checked") != "true":
            switch.click()
            # Wait via a fresh locator to avoid stale reference after re-render.
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "(//*[normalize-space()='%s']"
                    "/ancestor::*[contains(@class,'InovuaReactDataGrid__row')][1]"
                    "//button[@role='switch'])[last()][@aria-checked='true']"
                    % location_name
                ))
            )

    def location_show_on_cp_is_on(self, location_name):
        """Return whether Show on CP is enabled for a location."""
        row = self.get_location_row(location_name)
        switch = row.find_element(By.XPATH, "(.//button[@role='switch'])[last()]")

        return switch.get_attribute("aria-checked") == "true"

    def assign_all_locations_and_show_on_cp(self, location_names):
        """Assign all requested locations and enable their Show on CP switches."""
        for location_name in location_names:
            self.assign_location(location_name)
            self.enable_location_show_on_cp(location_name)

    def fill_gift_card_form(
        self,
        gift_card_name,
        amount,
        landing_page_code,
        location_names
    ):
        """Fill gift card form with requested settings."""
        self.enter_gift_card_name(gift_card_name)
        self.enter_landing_page_code(landing_page_code)
        # Assign location checkboxes BEFORE enabling main toggles: toggling the
        # main switches causes a form reflow that pushes grid rows behind the
        # settings-page__form-column overlay, making checkbox clicks unclickable.
        for location_name in location_names:
            self.assign_location(location_name)
        self.enable_all_main_toggles()
        # Enable per-location Show on CP AFTER main toggles: the "Show on customer
        # portal" main switch triggers a grid re-render that resets per-location
        # CP switches to OFF, so they must be set last.
        for location_name in location_names:
            self.enable_location_show_on_cp(location_name)
        # Enter amount last — toggle/checkbox interactions trigger React
        # re-renders that reset the amount field to its server value if set earlier.
        self.enter_gift_card_amount(amount)

    def click_save_gift_card(self):
        """Click save gift card."""
        from selenium.webdriver.support.ui import WebDriverWait
        button = self.wait.until(EC.element_to_be_clickable(self.SAVE_GIFT_CARD_BUTTON))
        button.click()
        # Wait for the button to go stale (SPA navigated away after a
        # successful save).  Without this, an immediately-following driver.get()
        # can cancel the in-flight save XHR before the server persists the
        # change.  Validation failures keep the button in the DOM so we time
        # out silently after 10 s and let the caller inspect the form state.
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(button))
        except TimeoutException:
            pass

    def click_save_customer_gift_card(self):
        """Click save customer gift card."""
        self.click(self.SAVE_CUSTOMER_GIFT_CARD_BUTTON)

    def click_cancel(self):
        """Cancel create/edit gift card."""
        self.click(self.CANCEL_BUTTON)

    def create_gift_card(
        self,
        gift_card_name,
        amount,
        landing_page_code,
        location_names
    ):
        """Create a gift card and return to list."""
        self.open_create_gift_card()
        self.fill_gift_card_form(
            gift_card_name,
            amount,
            landing_page_code,
            location_names
        )
        self.click_save_gift_card()
        # After saving, the outer SPA sometimes redirects to /new instead of
        # the list (same quirk as edit); use the same fallback as edit save.
        self.wait_for_list_after_edit_save()

    def wait_for_list_after_edit_save(self):
        """Wait for the gift card list after an edit save.

        Saving an inactive card can redirect the outer SPA to /new instead of
        the list; falls back to an explicit full-page navigation when that happens.
        """
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            from urllib.parse import urlparse
            self.driver.switch_to.default_content()
            parsed = urlparse(self.driver.current_url)
            self.driver.get(f"{parsed.scheme}://{parsed.netloc}/services/giftCards")
            self.wait_for_list_loaded()

    def update_gift_card_settings(
        self,
        gift_card_name,
        amount,
        landing_page_code,
        location_names
    ):
        """Update an existing gift card to expected settings."""
        self.open_edit_gift_card(gift_card_name)
        self.fill_gift_card_form(
            gift_card_name,
            amount,
            landing_page_code,
            location_names
        )
        self.click_save_gift_card()
        self.wait_for_list_after_edit_save()

    def fill_customer_gift_card_form(
        self,
        site_name,
        gift_card_name,
        gift_card_number,
        amount
    ):
        """Fill customer gift card form with requested details."""
        self.select_customer_gift_card_site(site_name)
        self.select_customer_gift_card_template(gift_card_name)
        self.enter_customer_gift_card_number(gift_card_number)
        self.enter_customer_gift_card_amount(amount)
        self.ensure_active_customer_gift_card_on()

    def create_customer_gift_card(
        self,
        site_name,
        gift_card_name,
        gift_card_number,
        amount
    ):
        """Create a customer gift card and return to list."""
        self.open_create_customer_gift_card()
        self.fill_customer_gift_card_form(
            site_name,
            gift_card_name,
            gift_card_number,
            amount
        )
        self.click_save_customer_gift_card()
        try:
            self.wait_for_customer_list_loaded()
        except TimeoutException:
            error = self.get_visible_error()
            raise RuntimeError(
                "Customer gift card save did not return to list. Page message: %s"
                % (error or "none visible")
            ) from None

    def ensure_switch_off(self, locator):
        """Turn a switch off if needed."""
        switch = self.wait.until(EC.presence_of_element_located(locator))

        if switch.get_attribute("aria-checked") != "false":
            self.driver.execute_script("arguments[0].click();", switch)
            self.wait.until(
                lambda driver: driver.find_element(*locator).get_attribute("aria-checked") == "false"
            )

    def gift_card_amount_input_is_valid(self):
        """Return native validity state for gift card amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_AMOUNT_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def get_gift_card_amount_validation_message(self):
        """Return native validation message for gift card amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.GIFT_CARD_AMOUNT_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def customer_gift_card_amount_input_is_valid(self):
        """Return native validity state for customer gift card amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_GIFT_CARD_AMOUNT_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].checkValidity();",
            element
        )

    def get_customer_gift_card_amount_validation_message(self):
        """Return native validation message for customer gift card amount."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_GIFT_CARD_AMOUNT_INPUT)
        )
        return self.driver.execute_script(
            "return arguments[0].validationMessage;",
            element
        )

    def search_input_is_visible(self):
        """Return whether gift card search input is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_INPUT)
        ).is_displayed()

    def filter_button_is_clickable(self):
        """Return whether the Filter by button is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.FILTER_BUTTON)
        ).is_displayed()

    def add_gift_card_button_is_clickable(self):
        """Return whether the Add new gift card button is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_GIFT_CARD_BUTTON)
        ).is_displayed()

    def customer_search_input_is_visible(self):
        """Return whether customer gift card search input is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_SEARCH_INPUT)
        ).is_displayed()

    def add_customer_gift_card_button_is_clickable(self):
        """Return whether the Add customer gift card button is clickable."""
        return self.wait.until(
            EC.element_to_be_clickable(self.ADD_CUSTOMER_GIFT_CARD_BUTTON)
        ).is_displayed()

    def open_filter_panel(self):
        """Open the gift card filter panel if not already open."""
        # Use the Apply filters button as the open-state indicator: FILTER_SITE_INPUT
        # relies on the "Select site" placeholder which is absent when a site is already
        # selected, so checking it here would always fail after a prior filter.
        apply_visible = [
            el for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
            if el.is_displayed()
        ]
        if apply_visible:
            return

        button = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(EC.visibility_of_element_located(self.APPLY_FILTERS_BUTTON))

    def select_site_filter(self, site_name):
        """Open filter panel and select a site."""
        self.open_filter_panel()
        self.click(self.FILTER_SITE_INPUT)
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[normalize-space()='%s']" % site_name)
            )
        ).click()

    def toggle_active_filter(self):
        """Enable the Active gift card filter to show only active gift cards.

        The list shows active cards by default so the switch may already be ON
        when the panel opens; this method ensures it is ON rather than blindly
        toggling (which would flip it to inactive-only mode).
        """
        switch = self.wait.until(
            EC.presence_of_element_located(self.ACTIVE_GIFT_CARD_FILTER_SWITCH)
        )
        is_on = (
            switch.get_attribute("aria-checked") == "true"
            or switch.get_attribute("checked") == "true"
        )
        if is_on:
            return
        self.driver.execute_script("arguments[0].click();", switch)
        self.wait.until(
            lambda d: (
                d.find_element(*self.ACTIVE_GIFT_CARD_FILTER_SWITCH).get_attribute("aria-checked") == "true"
                or d.find_element(*self.ACTIVE_GIFT_CARD_FILTER_SWITCH).get_attribute("checked") == "true"
            )
        )

    def apply_filters(self):
        """Click Apply filters and wait for the grid to refresh.

        Waits for either the gift card or customer gift card add button so this
        method works from both the gift card list and the customer gift card list.
        """
        button = self.wait.until(
            EC.element_to_be_clickable(self.APPLY_FILTERS_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)
        self.wait.until(
            lambda driver: any(
                el.is_displayed()
                for locator in (
                    self.ADD_GIFT_CARD_BUTTON,
                    self.ADD_CUSTOMER_GIFT_CARD_BUTTON,
                )
                for el in driver.find_elements(*locator)
            )
        )

    def reset_all_filters(self):
        """Click Reset all inside the open filter panel, then resync to the list.

        Fast-returns when the filter button shows no active filter count — avoids
        opening the panel unnecessarily and keeps the common (no-filter) path cheap.
        Reset All may reload the legacy iframe, so we exit to default_content and
        re-enter via wait_for_list_loaded to avoid stale context.
        """
        filter_buttons = self.driver.find_elements(*self.FILTER_BUTTON)
        filter_active = any(
            "(" in (btn.text or "")
            for btn in filter_buttons
            if btn.is_displayed()
        )
        if not filter_active:
            return

        self.open_filter_panel()
        buttons = self.driver.find_elements(*self.RESET_ALL_BUTTON)
        if buttons:
            self.driver.execute_script("arguments[0].click();", buttons[0])
        try:
            self.wait_for_list_loaded()
        except TimeoutException:
            from urllib.parse import urlparse
            self.driver.switch_to.default_content()
            parsed = urlparse(self.driver.current_url)
            self.driver.get(
                "%s://%s/services/giftCards" % (parsed.scheme, parsed.netloc)
            )
            self.wait_for_list_loaded()

        # Close the filter panel if Reset All left it open — the panel div
        # (settings-page__form-column) overlays the main content and would
        # intercept clicks on the search input in subsequent operations.
        apply_open = [
            el for el in self.driver.find_elements(*self.APPLY_FILTERS_BUTTON)
            if el.is_displayed()
        ]
        if apply_open:
            btn = self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
            self.driver.execute_script("arguments[0].click();", btn)
            self.wait.until(
                lambda d: not any(
                    el.is_displayed()
                    for el in d.find_elements(*self.APPLY_FILTERS_BUTTON)
                )
            )

    def get_visible_gift_card_row_count(self):
        """Return count of visible gift card rows in the grid."""
        return len([
            row for row in self.driver.find_elements(*self.GIFT_CARD_GRID_ROWS)
            if row.is_displayed()
        ])

    def wait_for_customer_edit_loaded(self):
        """Wait until the customer gift card edit form is visible."""
        self.driver.switch_to.default_content()
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it(self.CUSTOMER_EDIT_FRAME)
        )
        self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_GIFT_CARD_NUMBER_INPUT)
        )
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CUSTOMER_GIFT_CARD_BUTTON))
        self.wait.until(lambda driver: self.get_customer_gift_card_number_value() != "")

    def get_customer_gift_card_number_value(self):
        """Return current customer gift card number input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_GIFT_CARD_NUMBER_INPUT)
        )
        return element.get_attribute("value")

    def get_customer_gift_card_amount_value(self):
        """Return current customer gift card amount input value."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.CUSTOMER_GIFT_CARD_AMOUNT_INPUT)
        )
        return element.get_attribute("value")

    def open_edit_customer_gift_card(self, gift_card_number):
        """Open the edit form for a customer gift card."""
        self.wait_for_customer_list_loaded()
        self.search_customer_gift_card(gift_card_number)
        row = self.wait_for_customer_gift_card_row(gift_card_number)
        edit_button = row.find_element(
            By.XPATH,
            ".//*[normalize-space()='Edit']/ancestor::a[1]"
        )
        edit_button.click()
        self.wait_for_customer_edit_loaded()

    def gift_card_option_exists_in_dropdown(self, gift_card_name):
        """Return whether a gift card name appears in the Select gift card dropdown."""
        select_input = self.get_select_input_by_label("Select gift card")
        select_input.click()
        select_input.send_keys(gift_card_name)

        try:
            from selenium.webdriver.support.ui import WebDriverWait
            option = WebDriverWait(self.driver, 10).until(
                lambda d: self._find_react_option(gift_card_name)
            )
            return option is not None
        except TimeoutException:
            return False
