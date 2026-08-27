import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 45)

    def _dismiss_page_banner(self):
        """Remove the staging 'dev-environment-unstable' Toastify banner.

        The banner is position:fixed and can appear over iframe content,
        causing ElementClickInterceptedException on any click whose viewport
        coordinates map to the banner's bounding box.  We try both the current
        document and the parent document (same-origin iframes only; cross-origin
        access is caught and silently ignored).
        """
        for script in (
            "var t=document.getElementById('dev-environment-unstable');"
            "if(t){t.click();t.remove();}",
            "try{var t=window.parent.document"
            ".getElementById('dev-environment-unstable');"
            "if(t){t.click();t.remove();}}catch(e){}",
        ):
            try:
                self.driver.execute_script(script)
            except Exception:
                pass
        time.sleep(0.4)

    def click(self, locator):
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except ElementClickInterceptedException:
            # _dismiss_page_banner may not reach the parent-doc toast when we
            # are inside a cross-origin iframe (window.parent.document throws
            # SecurityError).  Fall back to a JS click which dispatches a DOM
            # event inside the current frame and bypasses ChromeDriver's
            # coordinate-based interception check entirely.
            self._dismiss_page_banner()
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", element)

    def enter_text(self, locator, text):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        # HTMLInputElement.select() selects all text cross-platform without any
        # keyboard modifier (CTRL+A breaks on macOS, COMMAND+A breaks on Linux).
        # send_keys then replaces the selection and fires React's input events.
        self.driver.execute_script("arguments[0].select();", element)
        element.send_keys(text)

    def get_text(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def wait_for_url(self, url):

        self.wait.until(
            EC.url_to_be(url)
        )

    # ── Shared React Select helpers ──────────────────────────────────────────

    _REACT_OPTION_JS = """
        var text = arguments[0].toLowerCase().trim();
        var candidates = Array.from(document.querySelectorAll(
            '[role="option"],'
            + '[class*="__option"],'
            + '[class*="-option"],'
            + '[class*="select__option"]'
        ));
        return candidates.find(function(el) {
            var r = el.getBoundingClientRect();
            return r.height > 0
                && el.textContent.trim().toLowerCase() === text;
        }) || null;
    """

    def _find_react_option(self, option_text):
        """Find a visible React Select option via JavaScript.

        Works regardless of whether the menu is rendered in-place, portalled
        to document.body, or uses a non-standard ARIA structure.  Searches the
        entire current document for matching text — both @role='option' and
        CSS-class-based options are covered.
        """
        return self.driver.execute_script(self._REACT_OPTION_JS, option_text)

    def select_react_dropdown_option(self, combobox_locator, option_text,
                                      clear_first=True):
        """Open a React Select control, type to filter, and click the option.

        Handles both input-as-combobox (the inner search input is the locator)
        and div-as-combobox (the outer control div is the locator).  Option
        discovery uses :meth:`_find_react_option` so portal configurations are
        transparent.
        """
        combobox = self.wait.until(EC.element_to_be_clickable(combobox_locator))
        self.driver.execute_script("arguments[0].click();", combobox)

        def _get_inner_input():
            el = self.wait.until(EC.element_to_be_clickable(combobox_locator))
            if el.tag_name.lower() == "input":
                return el
            inputs = el.find_elements(By.XPATH, ".//input")
            return inputs[0] if inputs else el

        # Locate the typeable input — either the element itself or a child.
        if combobox.tag_name.lower() == "input":
            inner_input = combobox
        else:
            inputs = combobox.find_elements(By.XPATH, ".//input")
            inner_input = inputs[0] if inputs else combobox

        for _attempt in range(3):
            try:
                if clear_first:
                    self.driver.execute_script("arguments[0].select();", inner_input)
                    inner_input.send_keys(Keys.BACKSPACE)
                inner_input.send_keys(option_text)
                break
            except (StaleElementReferenceException, ElementNotInteractableException):
                if _attempt == 2:
                    raise
                time.sleep(0.5)
                inner_input = _get_inner_input()

        option = WebDriverWait(self.driver, 45).until(
            lambda d: self._find_react_option(option_text)
        )
        self.driver.execute_script("arguments[0].click();", option)

    def hover_element(self, locator):
        """Move the pointer to the centre of the element matched by locator."""
        el = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(el).perform()

    # ── Error / duplicate detection ─────────────────────────────────────────

    _DUPLICATE_KEYWORDS = (
        "already exists", "duplicate", "already in use",
        "name is taken", "must be unique", "already been taken",
        "already used", "conflict",
    )
    _SERVER_ERROR_KEYWORDS = (
        "something went wrong", "internal server error",
        "failed to fetch", "unauthorized", "application error",
    )

    def get_visible_error(self):
        """Return the first visible error text from the current frame body, or None.

        Checks both duplicate-record keywords and generic server-error signals.
        Safe to call at any time; never raises.
        """
        try:
            body = self.driver.find_element(By.TAG_NAME, "body").text.lower()
            for kw in self._DUPLICATE_KEYWORDS + self._SERVER_ERROR_KEYWORDS:
                if kw in body:
                    return body[:600]
        except Exception:  # noqa: BLE001
            pass
        return None

    def duplicate_error_is_visible(self):
        """Return True when a known duplicate-record message is visible on the page."""
        body = (self.get_visible_error() or "")
        return any(kw in body for kw in self._DUPLICATE_KEYWORDS)

    def switch_to_frame_with_retry(self, locator, timeout=90):
        """Switch to an iframe, retrying on StaleElementReferenceException.

        EC.frame_to_be_available_and_switch_to_it only catches NoSuchFrameException.
        React re-mounts iframes during client-side navigation, causing stale element
        errors between find_element and switch_to.frame. This loop handles that race.
        """
        from selenium.common.exceptions import NoSuchFrameException, TimeoutException
        self.driver.switch_to.default_content()
        deadline = time.time() + timeout
        last_exc = None
        while time.time() < deadline:
            try:
                frame = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located(locator)
                )
                self.driver.switch_to.frame(frame)
                return
            except StaleElementReferenceException:
                self.driver.switch_to.default_content()
                time.sleep(0.5)
            except (TimeoutException, NoSuchFrameException) as exc:
                last_exc = exc
                self.driver.switch_to.default_content()
                time.sleep(1)
        from selenium.common.exceptions import TimeoutException as TE
        raise TE("Frame %s not stable after %ss" % (locator, timeout)) from last_exc

    def pagination_controls_present(self, context_el=None):
        """Return True if any pagination controls are visible.

        Searches for prev/next buttons, numbered page buttons, or elements
        with class names containing 'pagination' or 'pager'.  Pass a
        WebElement as *context_el* to restrict the search to that subtree.
        """
        root = context_el if context_el is not None else self.driver
        candidates = root.find_elements(By.XPATH,
            "//*[contains(@class,'pagination') or contains(@class,'pager')] | "
            "//button[@aria-label='Next page' or @aria-label='Previous page' or "
            "@aria-label='Next' or @aria-label='Previous' or "
            "@aria-label='next' or @aria-label='previous'] | "
            "//button[contains(normalize-space(),'Next') or "
            "contains(normalize-space(),'Previous') or "
            "contains(normalize-space(),'Prev')]"
        )
        return any(c.is_displayed() for c in candidates)
