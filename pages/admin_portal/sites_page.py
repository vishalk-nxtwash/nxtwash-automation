import json

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.common.base_page import BasePage


class SitesPage(BasePage):

    PAGE_TITLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Sites/Locations')]"
    )
    FILTER_BUTTON = (By.XPATH, "//button[contains(.,'Filter by')]")
    ADD_SITE_BUTTON = (
        By.XPATH,
        "//button[contains(normalize-space(), 'Add site')]"
    )
    SITE_NAME_FILTER = (By.NAME, "siteName")
    APPLY_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Apply filters']"
    )
    RESET_FILTERS_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Reset filters']"
    )

    def wait_for_loaded(self):
        """Wait until Sites / Locations is visible."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.element_to_be_clickable(self.FILTER_BUTTON))
        self.wait.until(EC.element_to_be_clickable(self.ADD_SITE_BUTTON))

    def open_filters(self):
        """Open site filters."""
        self.click(self.FILTER_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.SITE_NAME_FILTER))

    def filter_by_site_name(self, site_name):
        """Filter sites by site name."""
        self.open_filters()
        self.enter_text(self.SITE_NAME_FILTER, site_name)
        self.click(self.APPLY_FILTERS_BUTTON)

    def get_site_row_locator(self, site_name):
        """Build a locator for a site row by exact visible site name."""
        return (
            By.XPATH,
            "//*[normalize-space()='%s']/ancestor::tr[1]" % site_name
        )

    def wait_for_site_row(self, site_name):
        """Wait until a site row is visible."""
        return self.wait.until(
            EC.visibility_of_element_located(
                self.get_site_row_locator(site_name)
            )
        )

    def site_exists_in_ui(self, site_name):
        """Return whether a site exists in the filtered UI list."""
        self.filter_by_site_name(site_name)

        try:
            self.wait_for_site_row(site_name)
            return True
        except TimeoutException:
            return False

    def click_add_site(self):
        """Open the create site page."""
        self.click(self.ADD_SITE_BUTTON)

    def get_site_summary_with_api(self, site_name):
        """Return a site summary by exact name from the authenticated session."""
        result = self.driver.execute_async_script(
            """
            const siteName = arguments[0];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const params = new URLSearchParams({
                key: auth.key,
                pageSize: "500",
                pageNumber: "1"
            });

            fetch("https://api.nxtwash.com:401/api/sites?" + params, {
                headers: {
                    accept: "application/json",
                    authorization: "Bearer " + auth.accessToken
                }
            })
                .then((response) => response.json())
                .then((body) => {
                    const sites = body.data || [];
                    const site = sites.find(
                        (item) => item.siteName === siteName
                    );
                    done(site || null);
                })
                .catch((error) => done({ error: String(error) }));
            """,
            site_name
        )

        if isinstance(result, dict) and result.get("error"):
            raise AssertionError(result["error"])

        return result

    def get_site_details_with_api(self, site_name):
        """Return full site details by exact name."""
        summary = self.get_site_summary_with_api(site_name)

        if not summary:
            return None

        result = self.driver.execute_async_script(
            """
            const siteId = arguments[0];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);
            const params = new URLSearchParams({
                key: auth.key,
                id: siteId
            });

            fetch("https://api.nxtwash.com:401/api/sites?" + params, {
                headers: {
                    accept: "application/json",
                    authorization: "Bearer " + auth.accessToken
                }
            })
                .then(async (response) => done({
                    status: response.status,
                    body: await response.text()
                }))
                .catch((error) => done({ error: String(error) }));
            """,
            summary["siteId"]
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") != 200:
            raise AssertionError(result)

        return json.loads(result["body"])["data"]

    def get_site_details_by_name_and_code_with_api(self, site_name, site_code):
        """Return full site details matching both site name and site code."""
        original_timeout = self.driver.timeouts.script
        self.driver.set_script_timeout(120)

        try:
            result = self.driver.execute_async_script(
                """
                const siteName = arguments[0];
                const siteCode = arguments[1];
                const done = arguments[arguments.length - 1];
                const root = JSON.parse(localStorage.getItem("persist:root"));
                const auth = JSON.parse(root.authSessionReducer);
                const headers = {
                    accept: "application/json",
                    authorization: "Bearer " + auth.accessToken
                };
                const baseUrl = "https://api.nxtwash.com:401/api/sites";
                const listParams = new URLSearchParams({
                    key: auth.key,
                    pageSize: "500",
                    pageNumber: "1"
                });

                fetch(baseUrl + "?" + listParams.toString(), { headers })
                    .then((response) => response.json())
                    .then(async (body) => {
                        const sites = body.data || [];
                        const matches = [];

                        for (let index = 0; index < sites.length; index += 15) {
                            const chunk = sites.slice(index, index + 15);
                            const details = await Promise.all(
                                chunk.map(async (site) => {
                                    const params = new URLSearchParams({
                                        key: auth.key,
                                        id: site.siteId
                                    });
                                    const response = await fetch(
                                        baseUrl + "?" + params.toString(),
                                        { headers }
                                    );
                                    return (await response.json()).data;
                                })
                            );

                            for (const detail of details) {
                                if (
                                    detail &&
                                    detail.siteName === siteName &&
                                    detail.siteCode === siteCode
                                ) {
                                    matches.push(detail);
                                }
                            }
                        }

                        done(matches[0] || null);
                    })
                    .catch((error) => done({ error: String(error) }));
                """,
                site_name,
                site_code
            )
        finally:
            self.driver.set_script_timeout(original_timeout)

        if isinstance(result, dict) and result.get("error"):
            raise AssertionError(result["error"])

        return result

    def create_site_from_reference_with_api(self, site_name, reference_site):
        """Create a site by copying a reference site's saved settings."""
        result = self.driver.execute_async_script(
            """
            const siteName = arguments[0];
            const referenceSite = arguments[1];
            const done = arguments[arguments.length - 1];
            const root = JSON.parse(localStorage.getItem("persist:root"));
            const auth = JSON.parse(root.authSessionReducer);

            const payload = JSON.parse(JSON.stringify(referenceSite));
            payload.key = auth.key;
            payload.siteId = 0;
            payload.siteName = siteName;
            payload.siteCode = siteName;
            payload.emailId = siteName + "@yopmail.com";
            payload.createdDate = null;

            if (payload.siteSetting) {
                payload.siteSetting.contactEmailId = payload.emailId;
            }

            if (Array.isArray(payload.siteLaneList)) {
                payload.siteLaneList = payload.siteLaneList.map((lane, index) => ({
                    ...lane,
                    siteLaneId: 0,
                    laneName: lane.laneName || "Lane " + (index + 1)
                }));
            }

            fetch("https://api.nxtwash.com:401/api/sites", {
                method: "POST",
                headers: {
                    accept: "application/json",
                    "content-type": "application/json",
                    authorization: "Bearer " + auth.accessToken
                },
                body: JSON.stringify(payload)
            })
                .then(async (response) => done({
                    status: response.status,
                    body: await response.text()
                }))
                .catch((error) => done({ error: String(error) }));
            """,
            site_name,
            reference_site
        )

        if result.get("error"):
            raise AssertionError(result["error"])

        if result.get("status") not in [200, 201]:
            raise AssertionError(result)

        return json.loads(result["body"])


class CreateSitePage(BasePage):

    PAGE_TITLE = (By.XPATH, "//*[normalize-space()='Sites/Locations']")
    NEW_MODE_LABEL = (By.XPATH, "//*[normalize-space()='New']")
    SAVE_NEW_BUTTON = (By.XPATH, "//button[normalize-space()='Save new']")
    CANCEL_BUTTON = (By.XPATH, "//button[normalize-space()='Cancel']")

    SITE_NAME_INPUT = (By.NAME, "siteName")
    SITE_CODE_INPUT = (By.NAME, "siteCode")
    EMAIL_INPUT = (By.NAME, "emailId")
    PHONE_INPUT = (By.NAME, "phone")

    def wait_for_loaded(self):
        """Wait until the create site form is visible."""
        self.wait.until(EC.visibility_of_element_located(self.PAGE_TITLE))
        self.wait.until(EC.visibility_of_element_located(self.NEW_MODE_LABEL))
        self.wait.until(EC.visibility_of_element_located(self.SITE_NAME_INPUT))

    def get_body_text(self):
        """Get visible page text."""
        return self.driver.find_element(By.TAG_NAME, "body").text
