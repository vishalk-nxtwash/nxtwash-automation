from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.common.base_page import BasePage

# Confirmed from spec (SA-SET-EVT-001)
EVENT_TYPE_NAMES = [
    "Invoice Created Member Ship Data",
    "Invoice Created Retail Visit",
    "Membership Extend",
    "Membership Change",
    "Membership Auto Charge",
    "Membership Cancelled",
    "Membership Declined",
    "Update Customer",
    "Update Customer Opt In",
    "Membership Pending Change",
]


class WebhookSetupPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Webhook Setup']")
    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add Webhook Setup')]")
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")

    # Filter controls — name attributes are best guesses; form ID unconfirmed
    COMPANY_NAME_FILTER = (By.NAME, "companyName")
    # 'Active Third Party Key' toggle — same hidden-checkbox pattern
    ACTIVE_KEY_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active Third Party Key']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active Third Party Key']/..//input[@type='checkbox']"
    )
    APPLY_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Apply filters']")
    RESET_FILTERS_BUTTON = (By.XPATH, "//button[normalize-space()='Reset filters']")
    # Close button confirmed to use aria-label="Close popup" (same pattern as companies)
    FILTER_CLOSE_BUTTON = (
        By.XPATH,
        "//div[@aria-labelledby='popup-title']//button[@aria-label='Close popup']"
    )

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))
        self._reset_filter_state()

    def _reset_filter_state(self):
        """Clear any sticky filter left over from a previous test on this worker."""
        try:
            if not self.filter_panel_is_open():
                btn_els = self.driver.find_elements(*self.FILTER_BUTTON)
                if not btn_els:
                    return
                self.driver.execute_script("arguments[0].click();", btn_els[0])
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located(self.COMPANY_NAME_FILTER)
                )
            reset_els = self.driver.find_elements(*self.RESET_FILTERS_BUTTON)
            if reset_els and reset_els[0].is_displayed():
                self.driver.execute_script("arguments[0].click();", reset_els[0])
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//tbody"))
                )
            close_els = self.driver.find_elements(*self.FILTER_CLOSE_BUTTON)
            if close_els and close_els[0].is_displayed():
                self.driver.execute_script("arguments[0].click();", close_els[0])
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.invisibility_of_element_located(self.COMPANY_NAME_FILTER)
                    )
                except TimeoutException:
                    pass
        except Exception:
            pass

    def click_add_setup(self):
        self.click(self.ADD_BUTTON)

    # ── Filter ────────────────────────────────────────────────────────────────

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.COMPANY_NAME_FILTER)
        return bool(els) and els[0].is_displayed()

    def open_filters(self):
        if not self.filter_panel_is_open():
            self.click(self.FILTER_BUTTON)
            self.wait.until(EC.visibility_of_element_located(self.COMPANY_NAME_FILTER))

    def apply_filters(self):
        self.click(self.APPLY_FILTERS_BUTTON)

    def reset_filters(self):
        self.click(self.RESET_FILTERS_BUTTON)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//tbody")))

    def close_filter_panel(self):
        els = self.driver.find_elements(*self.FILTER_CLOSE_BUTTON)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])
        self.wait.until(EC.invisibility_of_element_located(self.COMPANY_NAME_FILTER))

    def filter_by_company_name(self, name):
        self.open_filters()
        self.enter_text(self.COMPANY_NAME_FILTER, name)
        self.apply_filters()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tbody"))
        )

    def get_third_party_name_options(self):
        """Return list of subscriber names in the Third Party Name dropdown."""
        combobox_loc = (
            By.XPATH,
            "//div[@aria-labelledby='popup-title']//*[@role='combobox']"
        )
        combos = self.driver.find_elements(*combobox_loc)
        if combos:
            try:
                self.driver.execute_script("arguments[0].click();", combos[0])
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@role='option']"))
                )
                opts = self.driver.find_elements(By.XPATH, "//*[@role='option']")
                result = [o.text.strip() for o in opts if o.text.strip()]
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                return result
            except Exception:
                pass
        return []

    def select_third_party_name_filter(self, subscriber_name):
        combobox_loc = (
            By.XPATH,
            "//div[@aria-labelledby='popup-title']//*[@role='combobox']"
        )
        self.select_react_dropdown_option(combobox_loc, subscriber_name)

    # ── Table ─────────────────────────────────────────────────────────────────

    def get_column_headers(self):
        headers = self.driver.find_elements(
            By.XPATH, "//th | //thead//td | //div[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr[td]")
        return len(rows) if rows else len(
            self.driver.find_elements(By.XPATH, "//tbody/tr")
        )

    def get_records_count_text(self):
        els = self.driver.find_elements(
            By.XPATH, "//*[contains(.,'out of') and contains(.,'records')]"
        )
        return els[0].text.strip() if els else ""

    def prev_page_button_is_disabled(self):
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        return els[0].get_attribute("disabled") is not None if els else True

    def get_row_locator(self, company_name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]" % company_name
        )

    def wait_for_row(self, company_name):
        return self.wait.until(
            EC.visibility_of_element_located(self.get_row_locator(company_name))
        )

    def row_exists(self, company_name, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.get_row_locator(company_name))
            )
            return True
        except TimeoutException:
            return False

    def open_edit(self, company_name):
        row = self.wait_for_row(company_name)
        btn = row.find_element(By.XPATH, ".//button[normalize-space()='Edit']")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )
        self.driver.execute_script("arguments[0].click();", btn)


class CreateSetupPage(BasePage):

    # Placeholder 'selectSubscriber' confirmed from spec
    SUBSCRIBER_CONTROL = (
        By.XPATH,
        "//*[@placeholder='selectSubscriber'] | "
        "//*[contains(@placeholder,'Subscriber')]/ancestor::div[contains(@class,'control')][1]"
    )
    # Master Company React Select
    COMPANY_CONTROL = (
        By.XPATH,
        "//*[@placeholder='selectCompany'] | "
        "//*[contains(@placeholder,'Company')]/ancestor::div[contains(@class,'control')][1] | "
        "//input[@name='masterCompanyId']/preceding-sibling::div[1]"
    )
    # Text inputs — name attributes are best guesses
    URL_INPUT = (By.NAME, "thirdPartyUrl")
    KEY_INPUT = (By.NAME, "thirdPartyKey")

    # Toggles — same hidden-checkbox pattern
    IS_ENABLED_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Is Enabled']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Is Enabled']/..//input[@type='checkbox']"
    )
    ACTIVE_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active Webhook Setup']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active Webhook Setup']/..//input[@type='checkbox']"
    )

    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")

    def wait_for_loaded(self):
        self.wait.until(EC.url_contains("/third-party/setup"))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_NEW_BUTTON))

    def select_subscriber(self, subscriber_name):
        self.select_react_dropdown_option(self.SUBSCRIBER_CONTROL, subscriber_name)

    def select_company(self, company_name):
        self.select_react_dropdown_option(self.COMPANY_CONTROL, company_name)

    def enter_url(self, url):
        self.enter_text(self.URL_INPUT, url)

    def enter_key(self, key):
        self.enter_text(self.KEY_INPUT, key)

    def get_toggle_state(self, locator):
        els = self.driver.find_elements(*locator)
        return els[0].is_selected() if els else None

    def set_toggle(self, locator, label_text, state):
        current = self.get_toggle_state(locator)
        if current is None or current == state:
            return
        label_loc = (
            By.XPATH,
            "//div[normalize-space()='%s']/following-sibling::label[1]" % label_text
        )
        els = self.driver.find_elements(*label_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def set_is_enabled(self, state):
        self.set_toggle(self.IS_ENABLED_TOGGLE, "Is Enabled", state)

    def set_active(self, state):
        self.set_toggle(self.ACTIVE_TOGGLE, "Active Webhook Setup", state)

    def get_event_checkbox(self, event_name):
        # Try progressively broader ancestor traversals until a match is found
        for ancestor in (
            "/following-sibling::label//input[@type='checkbox']",
            "/..//input[@type='checkbox']",
            "/../..//input[@type='checkbox']",
            "/../../..//input[@type='checkbox']",
        ):
            els = self.driver.find_elements(
                By.XPATH,
                "//*[normalize-space()='%s']%s" % (event_name, ancestor)
            )
            if els:
                return els[0]
        return None

    def get_all_event_states(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 5).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        states = {}
        for name in EVENT_TYPE_NAMES:
            cb = self.get_event_checkbox(name)
            states[name] = cb.is_selected() if cb else None
        return states

    def set_event(self, event_name, state):
        cb = self.get_event_checkbox(event_name)
        if cb is None or cb.is_selected() == state:
            return
        label_loc = (
            By.XPATH,
            "//*[normalize-space()='%s']/following-sibling::label[1]" % event_name
        )
        els = self.driver.find_elements(*label_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])
        else:
            self.driver.execute_script("arguments[0].click();", cb)

    def click_save_new(self):
        self.click(self.SAVE_NEW_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_validation_text(self, text):
        return text.lower() in self.get_body_text().lower()


class EditSetupPage(CreateSetupPage):

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes' or normalize-space()='Update']"
    )
    # Inline X clear buttons — locator unconfirmed
    URL_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='thirdPartyUrl']/following-sibling::button[1] | "
        "//input[@name='thirdPartyUrl']/..//button[@type='button'][1]"
    )
    KEY_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='thirdPartyKey']/following-sibling::button[1] | "
        "//input[@name='thirdPartyKey']/..//button[@type='button'][1]"
    )

    def wait_for_loaded(self):
        self.wait.until(EC.url_contains("/third-party/setup/"))
        self.wait.until(lambda d: "/create" not in d.current_url)
        self.wait.until(EC.visibility_of_element_located(self.SAVE_CHANGES_BUTTON))

    def get_url_value(self):
        els = self.driver.find_elements(*self.URL_INPUT)
        return els[0].get_attribute("value") if els else ""

    def get_key_value(self):
        els = self.driver.find_elements(*self.KEY_INPUT)
        return els[0].get_attribute("value") if els else ""

    def set_url(self, value):
        el = self.wait.until(EC.element_to_be_clickable(self.URL_INPUT))
        self.driver.execute_script(
            "arguments[0].value='';"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el
        )
        if value:
            el.send_keys(value)

    def set_key(self, value):
        el = self.wait.until(EC.element_to_be_clickable(self.KEY_INPUT))
        self.driver.execute_script(
            "arguments[0].value='';"
            "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));",
            el
        )
        if value:
            el.send_keys(value)

    def click_url_clear(self):
        els = self.driver.find_elements(*self.URL_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_key_clear(self):
        els = self.driver.find_elements(*self.KEY_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)
