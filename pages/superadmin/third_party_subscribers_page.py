import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class SubscribersPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Webhook Subscribers']")
    ADD_BUTTON = (By.XPATH, "//button[contains(.,'Add Webhook Subscriber')]")

    def wait_for_loaded(self):
        self.wait_for_any_visible(self.PAGE_TITLE)
        self.wait.until(EC.element_to_be_clickable(self.ADD_BUTTON))

    def click_add_subscriber(self):
        self.click(self.ADD_BUTTON)

    # ── Read-only API helpers (backend truth for managed-record resets) ──────

    def _get_third_party_api(self, query=""):
        result = self.driver.execute_async_script(
            """
            const [base, query] = arguments;
            const done = arguments[arguments.length - 1];
            const auth = JSON.parse(JSON.parse(localStorage.getItem("persist:root")).authSessionReducer);
            const url = base + "/api/ThirdParty/GetThirdParty?" + query
                + (query ? "&" : "") + "key=" + encodeURIComponent(auth.key);
            fetch(url, {headers: {accept: "application/json", authorization: "Bearer " + auth.accessToken}})
                .then(async (r) => done({status: r.status, body: await r.text()}))
                .catch((e) => done({error: String(e)}));
            """,
            ConfigManager().get_url("api").rstrip("/"), query,
        )
        if result.get("error") or result.get("status") != 200:
            raise AssertionError("GetThirdParty failed: %s" % result)
        return json.loads(result["body"]).get("data")

    def list_with_api(self, include_inactive=True):
        """All subscribers. The endpoint returns only active records unless
        asked for inactive ones explicitly, so merge both by default — a
        uniqueness clash with a hidden inactive record is otherwise invisible."""
        records = list(self._get_third_party_api() or [])
        if include_inactive:
            records += self._get_third_party_api("isActive=false") or []
        return records

    def get_by_id_with_api(self, subscriber_id):
        return self._get_third_party_api("id=%s" % subscriber_id) or {}

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

    def has_no_filter_button(self):
        return not bool(self.driver.find_elements(
            By.XPATH, "//button[contains(.,'Filter by')]"
        ))

    def has_no_export_button(self):
        return not bool(self.driver.find_elements(
            By.XPATH, "//button[.//svg[contains(@class,'lucide-download')]]"
        ))

    def prev_page_button_is_disabled(self):
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        return els[0].get_attribute("disabled") is not None if els else True

    def get_row_locator(self, name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]" % name
        )

    def wait_for_row(self, name):
        return self.wait.until(
            EC.visibility_of_element_located(self.get_row_locator(name))
        )

    def row_exists(self, name, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.get_row_locator(name))
            )
            return True
        except TimeoutException:
            return False

    def open_edit(self, name):
        btn_loc = (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button[normalize-space()='Edit']][1]"
            "//button[normalize-space()='Edit']" % name
        )
        self.js_click_fresh(btn_loc)

    def get_row_actions(self, name):
        row = self.wait_for_row(name)
        btns = row.find_elements(By.XPATH, ".//button")
        return [b.text.strip() for b in btns if b.text.strip()]


class CreateSubscriberPage(BasePage):

    # Input name attributes are best guesses; confirmed after DOM inspection
    NAME_INPUT = (By.NAME, "name")
    ABBREVIATION_INPUT = (By.NAME, "abbreviation")
    # Hidden checkbox following the 'Active Subscriber' label — same pattern as other modules
    ACTIVE_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active Subscriber']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active Subscriber']/..//input[@type='checkbox']"
    )
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")

    def wait_for_loaded(self):
        self.wait.until(EC.url_contains("/third-party/subscribers"))
        self.wait.until(EC.visibility_of_element_located(self.SAVE_NEW_BUTTON))

    def enter_name(self, name):
        self.enter_text(self.NAME_INPUT, name)

    def enter_abbreviation(self, abbr):
        self.enter_text(self.ABBREVIATION_INPUT, abbr)

    def get_active_toggle_state(self):
        els = self.driver.find_elements(*self.ACTIVE_TOGGLE)
        return els[0].is_selected() if els else None

    def set_active_toggle(self, state):
        current = self.get_active_toggle_state()
        if current is None or current == state:
            return
        label_loc = (
            By.XPATH,
            "//div[normalize-space()='Active Subscriber']/following-sibling::label[1]"
        )
        els = self.driver.find_elements(*label_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

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


class EditSubscriberPage(CreateSubscriberPage):

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes' or normalize-space()='Update']"
    )
    # Inline X clear buttons confirmed by spec: "Both fields expose an inline clear (X)"
    # Exact locator unconfirmed — best guess using sibling/parent button patterns
    NAME_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='name']/following-sibling::button[1] | "
        "//input[@name='name']/..//button[contains(@class,'clear') or @type='button'][1]"
    )
    ABBREVIATION_CLEAR_BUTTON = (
        By.XPATH,
        "//input[@name='abbreviation']/following-sibling::button[1] | "
        "//input[@name='abbreviation']/..//button[contains(@class,'clear') or @type='button'][1]"
    )

    def wait_for_loaded(self, expected_name=None):
        self.wait.until(EC.url_contains("/third-party/subscribers/"))
        self.wait.until(
            lambda d: "/create" not in d.current_url
        )
        self.wait.until(EC.visibility_of_element_located(self.SAVE_CHANGES_BUTTON))
        if expected_name:
            self.wait.until(
                lambda d: (
                    d.find_elements(*self.NAME_INPUT)
                    and d.find_element(*self.NAME_INPUT).get_attribute("value") == expected_name
                )
            )

    def get_name(self):
        el = self.driver.find_element(*self.NAME_INPUT)
        return el.get_attribute("value") or ""

    def get_abbreviation(self):
        el = self.driver.find_element(*self.ABBREVIATION_INPUT)
        return el.get_attribute("value") or ""

    def set_name(self, value):
        self.enter_text(self.NAME_INPUT, value)

    def set_abbreviation(self, value):
        self.enter_text(self.ABBREVIATION_INPUT, value)

    def click_name_clear(self):
        els = self.driver.find_elements(*self.NAME_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_abbreviation_clear(self):
        els = self.driver.find_elements(*self.ABBREVIATION_CLEAR_BUTTON)
        if els:
            els[0].click()

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)
