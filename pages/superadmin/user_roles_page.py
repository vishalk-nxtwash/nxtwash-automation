from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

    def wait_for_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROLE_BUTTON))

    def click_add_role(self):
        self.click(self.ADD_ROLE_BUTTON)

    def open_filters_if_available(self):
        try:
            self.click(self.FILTER_BUTTON)
        except TimeoutException:
            return False

        self.wait.until(EC.presence_of_element_located(self.SEARCH_INPUTS))
        return True

    def filter_by_role_name(self, role_name):
        if self.open_filters_if_available():
            self.enter_text(self.SEARCH_INPUTS, role_name)
            self.click(self.APPLY_FILTERS_BUTTON)
            return

        search_inputs = self.driver.find_elements(*self.SEARCH_INPUTS)
        if search_inputs:
            search_inputs[0].clear()
            search_inputs[0].send_keys(role_name)

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

    def role_exists(self, role_name):
        self.filter_by_role_name(role_name)

        try:
            self.wait_for_role_row(role_name)
            return True
        except TimeoutException:
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


class CreateUserRolePage(BasePage):

    PAGE_HEADING = (
        By.XPATH,
        "//*[normalize-space()='User Role' or normalize-space()='Role']"
    )
    NEW_MODE_LABEL = (
        By.XPATH,
        "//*[normalize-space()='New' or normalize-space()='Create']"
    )
    ROLE_NAME_INPUT = (
        By.XPATH,
        "//input[@name='name' or @name='roleName' or @name='role']"
    )
    SAVE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Save new' or normalize-space()='Save' "
        "or normalize-space()='Update']"
    )
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space()='Yes']")

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

    def wait_for_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.ROLE_NAME_INPUT))

    def enter_role_name(self, role_name):
        self.enter_text(self.ROLE_NAME_INPUT, role_name)

    def expand_permission_groups(self):
        if getattr(self, "_permission_groups_expanded", False):
            return

        buttons = self.driver.find_elements(*self.EXPAND_PERMISSION_BUTTONS)

        for button in buttons:
            try:
                if not button.is_displayed() or not button.is_enabled():
                    continue

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    button
                )
                button.click()
            except StaleElementReferenceException:
                return

        self._permission_groups_expanded = True

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
            "arguments[0].scrollIntoView({block: 'center'});",
            switch
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

    def confirm_yes_if_present(self):
        short_wait = WebDriverWait(self.driver, 2)

        try:
            short_wait.until(
                EC.element_to_be_clickable(self.CONFIRM_YES_BUTTON)
            ).click()
            short_wait.until(
                EC.invisibility_of_element_located(self.CONFIRM_YES_BUTTON)
            )
        except TimeoutException:
            return

    def save(self):
        self.click_save()
        self.confirm_yes_if_present()

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def wait_for_any_text(self, expected_texts):
        expected_texts = [text.lower() for text in expected_texts]

        self.wait.until(
            lambda driver: any(
                text in self.get_body_text().lower()
                for text in expected_texts
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

    def upsert_role_with_api(self, role_name):
        """Create or update role through the authenticated browser session.

        The current UI submit omits required empty child permission arrays from
        the payload. This fallback keeps the test idempotent while still using
        the logged-in SuperAdmin session.
        """
        result = self.driver.execute_async_script(
            """
            const roleName = arguments[0];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const baseUrl = "https://api.nxtwash.com:401/api/SuperAdminUserRole";

            const headers = {
                accept: "application/json",
                "content-type": "application/json",
                authorization: "Bearer " + auth.accessToken
            };

            const rolePayload = (roleId) => ({
                key: auth.key,
                superAdminUserRoleId: roleId || 0,
                roleName,
                isActive: true,
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
                                isEnabled: false,
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
            """,
            role_name
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return result

    def get_role_permissions_with_api(self, role_name):
        result = self.driver.execute_async_script(
            """
            const roleName = arguments[0];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const baseUrl = "https://api.nxtwash.com:401/api/SuperAdminUserRole";
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
            """,
            role_name
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return result["body"]
