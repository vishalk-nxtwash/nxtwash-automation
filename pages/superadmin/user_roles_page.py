import json

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class UserRolesPage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='User Roles']")
    ADD_ROLE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Add') and contains(.,'Role')]"
    )
    FILTER_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(),'Filter by')]"
    )
    SEARCH_INPUTS = (
        By.XPATH,
        "//input[@name='name' or @name='roleName' or "
        "@placeholder='Search' or contains(@placeholder,'Role')]"
    )
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters' or normalize-space()='Apply']"
    )
    RESET_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset filters' or normalize-space()='Reset']"
    )
    NO_RECORDS_TEXT = (
        By.XPATH,
        "//*[contains(.,'out of 0 records') or contains(.,'No records')]"
    )
    # React Select — hidden input carries the selected value
    RESULTS_PER_PAGE_SELECT = (
        By.XPATH,
        "//input[@type='hidden' and @name='pageSize']"
    )
    # Hidden checkbox inside label that follows the "Active User Role" div
    ACTIVE_FILTER_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active User Role']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active User Role']/..//input[@type='checkbox']"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    @property
    def api_url(self):
        return self.config.get_url("api").rstrip("/")

    def _api_script(self, body):
        return "const API_BASE = " + json.dumps(self.api_url) + ";\n" + body

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))
        self._reset_filter_state()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.EXPORT_ICON_BUTTON)
            )
        except Exception:
            pass

    def _reset_filter_state(self):
        """Close any open filter panel left by a prior test on this worker."""
        close_btn = (By.XPATH, "//button[.//svg[contains(@class,'lucide-x')]]")
        try:
            if not self.filter_panel_is_open():
                return
            reset_els = self.driver.find_elements(*self.RESET_FILTERS_BUTTON)
            if reset_els and reset_els[0].is_displayed():
                self.driver.execute_script("arguments[0].click();", reset_els[0])
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//tbody"))
                )
            close_els = self.driver.find_elements(*close_btn)
            if close_els and close_els[0].is_displayed():
                self.driver.execute_script("arguments[0].click();", close_els[0])
                try:
                    WebDriverWait(self.driver, 3).until(
                        EC.invisibility_of_element_located(self.SEARCH_INPUTS)
                    )
                except TimeoutException:
                    pass
        except Exception:
            pass

    def click_add_role(self):
        self.click(self.ADD_ROLE_BUTTON)

    def open_filters(self):
        if not self.filter_panel_is_open():
            self.click(self.FILTER_BUTTON)
            self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUTS))

    def open_filters_if_available(self):
        if self.filter_panel_is_open():
            return True
        try:
            self.click(self.FILTER_BUTTON)
        except TimeoutException:
            return False
        self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUTS))
        return True

    def apply_filters(self):
        self.click(self.APPLY_FILTERS_BUTTON)

    def reset_filters(self):
        self.click(self.RESET_FILTERS_BUTTON)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//tbody")))

    def filter_panel_is_open(self):
        els = self.driver.find_elements(*self.SEARCH_INPUTS)
        return bool(els) and els[0].is_displayed()

    def close_filter_panel(self):
        # lucide-x SVG is the close icon — no aria-label on the button
        close_btn = (By.XPATH, "//button[.//svg[contains(@class,'lucide-x')]]")
        els = self.driver.find_elements(*close_btn)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def filter_by_role_name(self, role_name):
        if self.open_filters_if_available():
            self.enter_text(self.SEARCH_INPUTS, role_name)
            self.click(self.APPLY_FILTERS_BUTTON)
            return
        search_inputs = self.driver.find_elements(*self.SEARCH_INPUTS)
        if search_inputs:
            search_inputs[0].clear()
            search_inputs[0].send_keys(role_name)

    def get_column_headers(self):
        headers = self.driver.find_elements(
            By.XPATH, "//th | //thead//td | //div[@role='columnheader']"
        )
        return [h.text.strip() for h in headers if h.text.strip()]

    def get_visible_row_count(self):
        rows = self.driver.find_elements(By.XPATH, "//tbody/tr")
        return len(rows)

    def get_role_row_locator(self, role_name):
        return (
            By.XPATH,
            "//*[normalize-space()='%s']"
            "/ancestor::*[.//button or .//a][1]" % role_name
        )

    def wait_for_role_row(self, role_name):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_role_row_locator(role_name)
            )
        )

    def role_row_is_visible(self, role_name):
        try:
            self.wait_for_role_row(role_name)
            return True
        except TimeoutException:
            return False

    def role_exists(self, role_name):
        self.filter_by_role_name(role_name)
        return self.role_row_is_visible(role_name)

    def get_pagination_text(self):
        locators = [
            (By.XPATH, "//*[contains(.,'Page') and contains(.,' of ')]"),
            (By.XPATH, "//nav[contains(.,'Page')] | //div[contains(@class,'pagination')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                return els[0].text.strip()
        return ""

    def get_records_text(self):
        locators = [
            (By.XPATH, "//*[contains(.,'out of') and contains(.,'records')]"),
            (By.XPATH, "//*[contains(.,'out of') and contains(.,'record')]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                return els[0].text.strip()
        return ""

    def prev_page_button_is_disabled(self):
        # lucide-chevron-left = prev; lucide-chevrons-left = first-page (different icon)
        btn_loc = (
            By.XPATH,
            "//button[.//svg[contains(@class,'lucide-chevron-left') "
            "and not(contains(@class,'lucide-chevrons-left'))]]"
        )
        els = self.driver.find_elements(*btn_loc)
        if els:
            return els[0].get_attribute("disabled") is not None
        return True

    def get_role_type_for_row(self, role_name):
        # Table: td[0]=Role Name, td[1]=Role Type ("Custom" or "Default/Predefined"), td[2]=Edit
        try:
            row = self.wait_for_role_row(role_name)
            cells = row.find_elements(By.XPATH, "./td")
            if len(cells) >= 2:
                return cells[1].text.strip()
        except (TimeoutException, Exception):
            pass
        return None

    def empty_state_is_visible(self):
        locators = [
            (By.XPATH, "//*[contains(.,'No records') or contains(.,'No data')]"),
            (By.XPATH, "//*[contains(.,'out of 0 records')]"),
            (By.XPATH, "//*[contains(.,'0 results') or contains(.,'no results')]"),
        ]
        for loc in locators:
            if self.driver.find_elements(*loc):
                return True
        return False

    def open_role(self, role_name):
        row = self.wait_for_role_row(role_name)
        action_locator = (
            By.XPATH,
            ".//button[normalize-space()='Edit' or contains(.,'Edit')]"
            "|.//a[contains(@href,'user-roles')]"
        )
        actions = row.find_elements(*action_locator)
        if actions:
            actions[0].click()
            return
        row.click()

    # ── Export ────────────────────────────────────────────────────────────────

    EXPORT_ICON_BUTTON = (
        By.XPATH, "//button[.//*[contains(@class,'lucide-download')]]"
    )
    # Export popup has no role="dialog" — anchored on title text
    EXPORT_MODAL = (
        By.XPATH,
        "//div[contains(normalize-space(),'Export User Roles')]"
        "/ancestor::div[contains(@class,'rounded-xl')][1]"
    )
    EXPORT_COLUMN_TOGGLES = (
        By.XPATH,
        "//div[contains(normalize-space(),'Export User Roles')]"
        "/ancestor::div[contains(@class,'rounded-xl')]"
        "//label//input[@type='checkbox']"
    )

    def click_export_icon(self):
        btn = self.wait.until(EC.presence_of_element_located(self.EXPORT_ICON_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def export_modal_is_visible(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.EXPORT_MODAL)
            )
            return True
        except TimeoutException:
            return False

    def get_default_export_format(self):
        try:
            el = self.driver.find_element(
                By.XPATH,
                "//div[contains(normalize-space(),'Export User Roles')]"
                "/ancestor::div[contains(@class,'rounded-xl')]"
                "//div[contains(@class,'singleValue')]"
            )
            return el.text.strip()
        except Exception:
            return ""

    def get_export_format_options(self):
        try:
            indicator = self.driver.find_element(
                By.XPATH,
                "//div[contains(normalize-space(),'Export User Roles')]"
                "/ancestor::div[contains(@class,'rounded-xl')]"
                "//div[contains(@class,'indicatorContainer')]"
            )
            self.driver.execute_script("arguments[0].click();", indicator)
        except Exception:
            pass
        try:
            options = WebDriverWait(self.driver, 5).until(
                lambda d: d.find_elements(By.XPATH, "//div[@role='option']")
            )
            return [o.text.strip() for o in options if o.text.strip()]
        except TimeoutException:
            return []

    def get_export_column_states(self):
        toggles = self.driver.find_elements(*self.EXPORT_COLUMN_TOGGLES)
        states = {}
        for toggle in toggles:
            name = toggle.get_attribute("name") or ""
            states[name] = toggle.is_selected()
        return states

    def export_confirm_button_is_disabled(self):
        els = self.driver.find_elements(
            By.XPATH,
            "//div[contains(normalize-space(),'Export User Roles')]"
            "/ancestor::div[contains(@class,'rounded-xl')]"
            "//button[@type='submit' or normalize-space()='Export']"
        )
        return bool(els) and els[0].get_attribute("disabled") is not None

    def cancel_export(self):
        self.click((
            By.XPATH,
            "//div[contains(normalize-space(),'Export User Roles')]"
            "/ancestor::div[contains(@class,'rounded-xl')]"
            "//button[normalize-space()='Cancel']"
        ))


class CreateUserRolePage(BasePage):

    PAGE_HEADING = (
        By.XPATH,
        "//*[normalize-space()='User Role' or normalize-space()='Role']"
    )
    NEW_MODE_LABEL = (
        By.XPATH,
        "//*[normalize-space()='New' or normalize-space()='Create']"
    )
    ROLE_NAME_INPUT = (By.XPATH, "//input[@name='roleName']")
    SAVE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save new' or normalize-space()='Save' "
        "or normalize-space()='Update']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")
    CONFIRM_NO_BUTTON = (By.XPATH, "//button[normalize-space()='No']")

    PERMISSION_CHECKBOXES = (
        By.XPATH,
        "//input[@type='checkbox' and not(@disabled)]"
    )
    EXPAND_PERMISSION_BUTTONS = (
        By.XPATH,
        "//form//button[normalize-space()='Overview' or "
        "normalize-space()='Users' or normalize-space()='User Roles' or "
        "normalize-space()='Sites' or normalize-space()='Companies']"
    )

    COMPANY_SECTION = (
        By.XPATH,
        "//*[normalize-space()='Companies' or normalize-space()='Company']"
    )
    CREATE_COMPANY_CHECKBOX = (
        By.XPATH,
        "//*[translate(normalize-space(), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')="
        "'create company']"
        "/following-sibling::label[1]//input[@type='checkbox']"
    )

    ROLE_SETTINGS_SECTION = (
        By.XPATH,
        "//div[normalize-space()='User Role Settings']"
    )
    ROLE_PERMISSIONS_SECTION = (
        By.XPATH,
        "//div[normalize-space()='User Role Permissions']"
    )
    # Hidden checkbox inside the label that follows the "Active User Role" div
    ACTIVE_USER_ROLE_TOGGLE = (
        By.XPATH,
        "//div[normalize-space()='Active User Role']"
        "/following-sibling::label//input[@type='checkbox'] | "
        "//div[normalize-space()='Active User Role']/..//input[@type='checkbox']"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    @property
    def api_url(self):
        return self.config.get_url("api").rstrip("/")

    def _api_script(self, body):
        return "const API_BASE = " + json.dumps(self.api_url) + ";\n" + body

    def wait_for_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.ROLE_NAME_INPUT))

    def enter_role_name(self, role_name):
        self.enter_text(self.ROLE_NAME_INPUT, role_name)

    def get_role_name_value(self):
        el = self.driver.find_element(*self.ROLE_NAME_INPUT)
        return el.get_attribute("value") or ""

    def role_settings_section_visible(self):
        return bool(self.driver.find_elements(*self.ROLE_SETTINGS_SECTION))

    def role_permissions_section_visible(self):
        return bool(self.driver.find_elements(*self.ROLE_PERMISSIONS_SECTION))

    def get_active_toggle_state(self):
        els = self.driver.find_elements(*self.ACTIVE_USER_ROLE_TOGGLE)
        if els:
            return els[0].is_selected()
        return None

    def set_active_toggle(self, state):
        current = self.get_active_toggle_state()
        if current is None or current == state:
            return
        # Click the visual span (slider) to toggle
        span_loc = (
            By.XPATH,
            "//div[normalize-space()='Active User Role']"
            "/following-sibling::label//span"
        )
        els = self.driver.find_elements(*span_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def get_permission_checkbox_by_name(self, name):
        self.expand_permission_groups()
        locators = [
            (By.XPATH,
             "//*[normalize-space()='%s']/following-sibling::label[1]//input[@type='checkbox']"
             % name),
            (By.XPATH,
             "//label[contains(normalize-space(),'%s')]//input[@type='checkbox']" % name),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                return els[0]
        return None

    def expand_permission_groups(self):
        if getattr(self, "_permission_groups_expanded", False):
            return
        buttons = self.driver.find_elements(*self.EXPAND_PERMISSION_BUTTONS)
        for button in buttons:
            try:
                if not button.is_displayed() or not button.is_enabled():
                    continue
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", button
                )
                button.click()
            except StaleElementReferenceException:
                return
        self._permission_groups_expanded = True
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(*self.PERMISSION_CHECKBOXES)) > 1
            )
        except TimeoutException:
            pass

    def get_permission_checkboxes(self):
        self.expand_permission_groups()
        return self.wait.until(
            lambda driver: (
                driver.find_elements(*self.PERMISSION_CHECKBOXES)
                if len(driver.find_elements(*self.PERMISSION_CHECKBOXES)) > 1
                else False
            )
        )

    def set_checkbox(self, checkbox, should_be_checked):
        checked = checkbox.is_selected()
        if checked == should_be_checked:
            return
        switch = checkbox.find_element(By.XPATH, "./ancestor::label[1]")
        slider = checkbox.find_element(By.XPATH, "./following-sibling::span[1]")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", switch
        )
        try:
            slider.click()
        except ElementNotInteractableException:
            self.driver.execute_script("arguments[0].click();", switch)
        self.wait.until(lambda driver: checkbox.is_selected() == should_be_checked)

    def select_all_permissions(self):
        for _ in range(3):
            changed = False
            for checkbox in self.get_permission_checkboxes():
                try:
                    if not checkbox.is_selected():
                        self.set_checkbox(checkbox, True)
                        changed = True
                except StaleElementReferenceException:
                    changed = True
                    break
            if not changed:
                return

    def get_create_company_checkbox(self):
        self.expand_permission_groups()
        return self.wait.until(
            EC.presence_of_element_located(self.CREATE_COMPANY_CHECKBOX)
        )

    def deselect_create_company_permission(self):
        self.set_checkbox(self.get_create_company_checkbox(), False)

    def configure_permissions(self):
        self.select_all_permissions()
        self.deselect_create_company_permission()

    def click_save(self):
        self.click(self.SAVE_BUTTON)

    def click_save_new(self):
        self.click(self.SAVE_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def confirm_no(self):
        self.click(self.CONFIRM_NO_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.CONFIRM_NO_BUTTON)
            )
        except TimeoutException:
            pass

    def save(self):
        self.click_save()
        self.confirm_yes_if_present()

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_for_any_text(self, *texts, timeout=15):
        texts_lower = [t.lower() for t in texts]
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                text in d.find_element(By.TAG_NAME, "body").text.lower()
                for text in texts_lower
            )
        )

    def all_permissions_except_create_company_are_selected(self):
        create_company = self.get_create_company_checkbox()
        for checkbox in self.get_permission_checkboxes():
            try:
                if checkbox == create_company:
                    continue
                if not checkbox.is_selected():
                    return False
            except StaleElementReferenceException:
                return self.all_permissions_except_create_company_are_selected()
        return not create_company.is_selected()

    def upsert_role_with_api(self, role_name, is_active=True, include_create_company=False):
        result = self.driver.execute_async_script(
            self._api_script("""
            const roleName = arguments[0];
            const isActive = arguments[1];
            const includeCreateCompany = arguments[2];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const baseUrl = API_BASE + "/api/SuperAdminUserRole";

            const headers = {
                accept: "application/json",
                "content-type": "application/json",
                authorization: "Bearer " + auth.accessToken
            };

            const rolePayload = (roleId) => ({
                key: auth.key,
                superAdminUserRoleId: roleId || 0,
                roleName,
                isActive: isActive,
                userRolesMenuAccess: [
                    {
                        menuId: 1,
                        menuName: "DashboardOverview",
                        isEnabled: true,
                        subMenuAccessList: []
                    },
                    {
                        menuId: 2,
                        menuName: "Companies",
                        isEnabled: true,
                        subMenuAccessList: [
                            {
                                subMenuId: 6,
                                subMenuName: "Create Company",
                                isEnabled: includeCreateCompany,
                                subMenuItemAccessList: []
                            }
                        ]
                    },
                    {
                        menuId: 3,
                        menuName: "Sites",
                        isEnabled: true,
                        subMenuAccessList: []
                    },
                    {
                        menuId: 4,
                        menuName: "User Roles",
                        isEnabled: true,
                        subMenuAccessList: [
                            {
                                subMenuId: 7,
                                subMenuName: "Create Role",
                                isEnabled: true,
                                subMenuItemAccessList: []
                            }
                        ]
                    },
                    {
                        menuId: 5,
                        menuName: "Users",
                        isEnabled: true,
                        subMenuAccessList: []
                    }
                ]
            });

            fetch(baseUrl + "?key=" + encodeURIComponent(auth.key), {
                headers
            })
                .then((response) => response.json())
                .then((listResponse) => {
                    const roles = listResponse.data || [];
                    const existingRole = roles.find(
                        (role) => role.roleName === roleName
                    );
                    const roleId = existingRole
                        ? existingRole.superAdminUserRoleId
                        : 0;
                    const method = existingRole ? "PUT" : "POST";

                    return fetch(baseUrl, {
                        method,
                        headers,
                        body: JSON.stringify(rolePayload(roleId))
                    }).then(async (response) => ({
                        status: response.status,
                        body: await response.text(),
                        method
                    }));
                })
                .then(done)
                .catch((error) => done({ error: String(error) }));
            """),
            role_name,
            is_active,
            include_create_company,
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return result

    def get_role_permissions_with_api(self, role_name):
        result = self.driver.execute_async_script(
            self._api_script("""
            const roleName = arguments[0];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const baseUrl = API_BASE + "/api/SuperAdminUserRole";
            const headers = {
                accept: "application/json",
                authorization: "Bearer " + auth.accessToken
            };

            fetch(baseUrl + "?key=" + encodeURIComponent(auth.key), {
                headers
            })
                .then((response) => response.json())
                .then((listResponse) => {
                    const existingRole = (listResponse.data || []).find(
                        (role) => role.roleName === roleName
                    );

                    if (!existingRole) {
                        return {
                            status: 404,
                            body: "Role not found"
                        };
                    }

                    const params = new URLSearchParams({
                        id: existingRole.superAdminUserRoleId,
                        key: auth.key
                    });

                    return fetch(baseUrl + "?" + params.toString(), {
                        headers
                    }).then(async (response) => ({
                        status: response.status,
                        body: await response.text()
                    }));
                })
                .then(done)
                .catch((error) => done({ error: String(error) }));
            """),
            role_name
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return result["body"]


class EditUserRolePage(CreateUserRolePage):

    SAVE_CHANGES_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save changes' or normalize-space()='Update']"
    )

    def wait_for_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.ROLE_NAME_INPUT))
        self.wait.until(lambda d: "/create" not in d.current_url)
        self.wait.until(
            lambda d: d.find_element(*self.ROLE_NAME_INPUT).get_attribute("value") not in (None, "")
        )

    def get_role_name(self):
        el = self.wait.until(EC.presence_of_element_located(self.ROLE_NAME_INPUT))
        return el.get_attribute("value") or ""

    def set_role_name(self, name):
        self.enter_text(self.ROLE_NAME_INPUT, name)

    def click_save_changes(self):
        self.click(self.SAVE_CHANGES_BUTTON)

    def click_cancel(self):
        self.click(self.CANCEL_BUTTON)

    def confirm_yes_if_present(self, timeout=5):
        short_wait = WebDriverWait(self.driver, timeout)
        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def confirm_no(self):
        self.click(self.CONFIRM_NO_BUTTON)
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(self.CONFIRM_NO_BUTTON)
            )
        except TimeoutException:
            pass

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_for_any_text(self, *texts, timeout=15):
        texts_lower = [t.lower() for t in texts]
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(
                text in d.find_element(By.TAG_NAME, "body").text.lower()
                for text in texts_lower
            )
        )

    def get_active_toggle_state(self):
        els = self.driver.find_elements(*self.ACTIVE_USER_ROLE_TOGGLE)
        if els:
            return els[0].is_selected()
        return None

    def set_active_toggle(self, state):
        current = self.get_active_toggle_state()
        if current is None or current == state:
            return
        # Click the visual span (slider) to toggle
        span_loc = (
            By.XPATH,
            "//div[normalize-space()='Active User Role']"
            "/following-sibling::label//span"
        )
        els = self.driver.find_elements(*span_loc)
        if els:
            self.driver.execute_script("arguments[0].click();", els[0])

    def enabled_permissions_count(self):
        try:
            checkboxes = self.get_permission_checkboxes()
            return sum(1 for cb in checkboxes if cb.is_selected())
        except (TimeoutException, StaleElementReferenceException):
            return 0

    def click_role_name_clear_button(self):
        # Defensive — inline clear X locator needs DOM confirmation
        locators = [
            (By.XPATH,
             "//input[@name='name' or @name='roleName']"
             "/following-sibling::button[1]"),
            (By.XPATH,
             "//input[@name='name' or @name='roleName']"
             "/..//button[@type='button'][1]"),
        ]
        for loc in locators:
            els = self.driver.find_elements(*loc)
            if els:
                els[0].click()
                return
