from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from core.config_manager import ConfigManager
from pages.common.base_page import BasePage


class AdminOverviewPage(BasePage):

    PORTAL = "admin_portal"

    OVERVIEW_TITLE = (By.XPATH, "//*[normalize-space()='Overview']")
    PROFILE_ROLE = (
        By.XPATH,
        "//*[contains(normalize-space(),'Admin Portal User')]"
    )
    LEGACY_DASHBOARD_IFRAME = (
        By.XPATH,
        "//iframe[contains(@src,'legacy')]"
    )
    SUPPORT_IFRAME = (
        By.XPATH,
        "//iframe[contains(@title,'widget') or contains(@title,'information')]"
    )

    EXPECTED_NAV_LINKS = {
        "Overview": "/",
        "Sites / Locations": "/sites",
        "Customers": "/customers",
        "Kiosk Settings": "/kiosk_settings/kiosks",
        "Gas Pump Settings": "/gas_pump_settings/device_list",
        "POS Settings": "/pos_settings/pos",
        "Tunnel Settings": "/tunnel_settings/tunnels"
    }
    EXPECTED_NAV_BUTTONS = [
        "Services",
        "Users / Employees",
        "Notifications",
        "Reports"
    ]
    BROKEN_STATE_TEXTS = [
        "Something went wrong",
        "Internal Server Error",
        "404",
        "Unauthorized",
        "Failed to fetch"
    ]
    DASHBOARD_FILTER_LABELS = [
        "Site",
        "Today",
        "Yesterday",
        "This Week",
        "Last Week",
        "This Month",
        "Last Month",
        "Custom",
        "Single Day"
    ]
    DASHBOARD_WIDGET_LABELS = [
        "Cars Washed",
        "Revenue",
        "Average Wash Ticket",
        "Membership",
        "Employees",
        "Gift Cards",
        "Labor"
    ]
    EXPORT_LABELS = ["XLSX", "CSV"]
    FULL_REPORT_LABELS = [
        "Cars Washed Full Report",
        "Revenue Full Report",
        "Employee Full Report",
        "Labor Full Report"
    ]
    EXPORT_DROPDOWN_TRIGGER = (By.XPATH, "//*[normalize-space()='Choose option']")
    CARS_WASHED_FULL_REPORT_LINK = (
        By.XPATH,
        "//*[normalize-space()='Cars Washed']"
        "/following::*[normalize-space()='Full report →'][1]"
    )

    def __init__(self, driver):
        super().__init__(driver)
        self.config = ConfigManager()

    @property
    def base_url(self):
        """Admin Portal base URL for the active environment (no trailing /)."""
        return self.config.get_url(self.PORTAL).rstrip("/")

    def wait_for_loaded(self):
        """Wait until Overview shell is visible and not redirected to login.

        No longer waits for LEGACY_DASHBOARD_IFRAME to mount: confirmed via a
        direct staging check (2026-10-14) that the Overview dashboard was
        migrated to native page content — that iframe no longer exists on
        the page at all, so waiting for it was dead weight (it always timed
        out and was silently swallowed).
        """
        self.wait_visible_with_retry(self.OVERVIEW_TITLE)
        self.wait.until(lambda d: "/login" not in d.current_url)

    def open_relative_path(self, path):
        """Navigate to an Admin Portal path relative to the base URL."""
        self.driver.get(self.base_url + path)


    def get_overview_text(self):
        """Get Overview title text."""
        return self.get_text(self.OVERVIEW_TITLE)

    def has_expected_url(self):
        """Return whether the browser is on the Admin Overview URL."""
        return self.driver.current_url.rstrip("/") == self.base_url

    def is_redirected_to_login(self):
        """Return whether the user was redirected back to login."""
        return "/login" in self.driver.current_url

    def get_nav_link_locator(self, label, href):
        return (
            By.XPATH,
            "//a[@href='%s' and normalize-space()='%s']" % (href, label)
        )

    def nav_link_is_visible(self, label, href):
        """Return whether a direct sidebar link is visible."""
        els = self.driver.find_elements(*self.get_nav_link_locator(label, href))
        return bool(els) and els[0].is_displayed()

    def nav_button_is_visible(self, label):
        """Return whether a sidebar dropdown button is visible."""
        els = self.driver.find_elements(
            By.XPATH, "//button[normalize-space()='%s']" % label
        )
        return bool(els) and els[0].is_displayed()

    def expected_navigation_is_visible(self):
        """Return whether all stable sidebar navigation items are visible."""
        for label, href in self.EXPECTED_NAV_LINKS.items():
            if not self.nav_link_is_visible(label, href):
                return False

        for label in self.EXPECTED_NAV_BUTTONS:
            if not self.nav_button_is_visible(label):
                return False

        return True

    def profile_role_is_visible(self):
        """Return whether the logged-in profile role is visible."""
        return self.driver.find_element(*self.PROFILE_ROLE).is_displayed()

    def has_broken_state_text(self):
        """Return whether a known broken/error state is visible."""
        body_text = self.get_body_text()
        return any(text in body_text for text in self.BROKEN_STATE_TEXTS)

    def legacy_dashboard_iframe_is_present(self):
        """Return whether the legacy Overview iframe is mounted.

        Confirmed via a direct staging check (2026-10-14) that this now
        correctly, permanently returns False — the Overview dashboard was
        migrated from an iframe-embedded legacy app to native page content,
        so the iframe genuinely doesn't exist anymore. Not a bug in this
        method; any caller still asserting this is True is testing a stale
        expectation and needs its own assertion rewritten separately
        against the new native content (not part of this pass).
        """
        return len(self.driver.find_elements(*self.LEGACY_DASHBOARD_IFRAME)) > 0

    def get_legacy_dashboard_text(self):
        """Return visible dashboard text.

        Despite the name (kept so every caller across the test suite didn't
        need touching in this pass), this no longer reads from an iframe:
        confirmed via a direct staging check (2026-10-14) that the Overview
        dashboard was migrated to native page content — the
        //iframe[contains(@src,'legacy')] this used to switch into doesn't
        exist anymore. Reads the main document body directly instead.
        """
        return self.get_body_text()

    def support_button_is_visible(self):
        """Return whether the support widget iframe is visible."""
        for iframe in self.driver.find_elements(*self.SUPPORT_IFRAME):
            try:
                self.driver.switch_to.frame(iframe)
                if "Support" in self.driver.find_element(By.TAG_NAME, "body").text:
                    return True
            finally:
                self.driver.switch_to.default_content()
        return False

    def dashboard_text_contains(self, expected_text):
        """Return whether expected text is visible in the Overview dashboard."""
        return expected_text in self.get_legacy_dashboard_text()

    def dashboard_has_all_texts(self, expected_texts):
        """Return whether all expected dashboard labels are visible."""
        dashboard_text = self.get_legacy_dashboard_text()
        return all(text in dashboard_text for text in expected_texts)

    def dashboard_has_any_text(self, expected_texts):
        """Return whether any expected dashboard label is visible."""
        dashboard_text = self.get_legacy_dashboard_text()
        return any(text in dashboard_text for text in expected_texts)

    def dashboard_has_rendered(self):
        """Return whether the Overview dashboard has rendered, either architecture.

        Accepts either a mounted legacy iframe OR native dashboard widget
        content, rather than assuming one. Staging is confirmed migrated to
        native content (2026-10-14 direct check), but this same check also
        runs against production via the prod_smoke marker
        (test_overview_shell_redirects_and_loads), and production's
        migration state has not been verified — asserting either form is
        present is correct regardless of which architecture a given
        environment is currently running, now or after a future migration.
        """
        return (
            self.legacy_dashboard_iframe_is_present()
            or self.dashboard_has_any_text(self.DASHBOARD_WIDGET_LABELS)
        )

    # ── Filter interaction helpers ────────────────────────────────────────────
    # Previously ran inside the legacy iframe (via _in_iframe()). Confirmed via
    # a direct staging check (2026-10-14) that the Overview dashboard was
    # migrated to native page content, so these now operate on the main
    # document directly. The locator strategies below are unchanged from the
    # iframe era and have NOT yet been verified against the actual new filter
    # widget's DOM (Sites/Locations dropdown, Predefined date range dropdown,
    # Pick custom date range picker) — that verification is separate,
    # follow-up work, not part of this pass.

    def select_site_filter(self, site_name):
        """Select a site by name from the Site filter."""
        # Try <select> first, then React combobox / listbox.
        try:
            sel = self.wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//select[contains(@class,'site') or @id='site' or @name='site']"
                " | //*[normalize-space()='Site']/following::select[1]",
            )))
            from selenium.webdriver.support.ui import Select
            Select(sel).select_by_visible_text(site_name)
        except Exception:  # noqa: BLE001
            # Fallback: click the combobox then click the matching option.
            combo = self.wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//*[normalize-space()='Site']/following::*[@role='combobox' or @role='listbox'][1]",
            )))
            combo.click()
            self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//*[normalize-space()='%s']" % site_name,
            ))).click()

    def select_date_preset(self, preset_label):
        """Click a date-preset button (e.g. 'Last Month')."""
        self.wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//*[normalize-space()='%s' and ("
            "self::button or self::a or contains(@class,'preset') or contains(@class,'tab'))]"
            " | //*[normalize-space()='%s']" % (preset_label, preset_label),
        ))).click()

    def set_custom_date_range(self, from_date, to_date):
        """Select Custom preset and fill start/end date inputs (YYYY-MM-DD format)."""
        # Click "Custom" to reveal the date inputs.
        self.wait.until(EC.element_to_be_clickable((
            By.XPATH, "//*[normalize-space()='Custom']",
        ))).click()
        start = self.wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//*[contains(normalize-space(),'Start') or @placeholder='Start']"
            "/following::input[@type='date' or @type='text'][1]"
            " | //input[@name='startDate' or @name='start_date' or @name='fromDate'][1]",
        )))
        end = self.driver.find_element(
            By.XPATH,
            "//*[contains(normalize-space(),'End') or @placeholder='End']"
            "/following::input[@type='date' or @type='text'][1]"
            " | //input[@name='endDate' or @name='end_date' or @name='toDate'][1]",
        )
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; "
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            start, from_date,
        )
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; "
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            end, to_date,
        )

    def open_overview_in_new_tab(self):
        """Open Overview in a second browser tab."""
        self.driver.execute_script(
            "window.open(arguments[0], '_blank');",
            self.base_url + "/"
        )
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def shell_has_content(self):
        """Return whether the Overview shell has meaningful visible content."""
        body_text = self.get_body_text()
        return (
            "Overview" in body_text
            and "Sites / Locations" in body_text
        )

    def open_export_dropdown(self):
        """Open the Export "Choose option" dropdown.

        The export format options (XLSX, CSV) are not static page text —
        confirmed via a direct staging check (2026-10-15) that they only
        appear in the body once this dropdown is opened.
        """
        self.wait.until(EC.element_to_be_clickable(
            self.EXPORT_DROPDOWN_TRIGGER
        )).click()

    def open_cars_washed_full_report(self):
        """Click the "Cars Washed" card's "Full report" link.

        Confirmed via a direct staging check (2026-10-15) that this is a
        real page navigation (/ -> /wash-activity), not a modal — and that
        a synthetic execute_script click does not trigger it (same
        mousedown-vs-click gap already documented for react-select in
        sites_page.py's _real_click()); a native Selenium click is
        required. There are 7 "Full report" links on the page, one per
        card, so this locator is anchored relative to the "Cars Washed"
        title to reliably hit the right one.
        """
        self.wait.until(EC.element_to_be_clickable(
            self.CARS_WASHED_FULL_REPORT_LINK
        )).click()
        # Wait for the destination page's title, not just the URL change:
        # confirmed via a live run (2026-10-15) that reading body text
        # immediately after the click can race the page's own content
        # rendering — the top summary cards (e.g. "Total Redemptions")
        # appear to render before lower sections like the breakdown
        # table, so a check for the title is a reliable "fully ready"
        # signal regardless of which part of the page a caller reads next.
        self.wait.until(
            lambda d: "Wash Activity Report" in d.find_element(
                By.TAG_NAME, "body"
            ).text
        )
