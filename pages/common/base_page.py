import sys
import time

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Select-all modifier: Cmd on macOS, Ctrl elsewhere. Hard-coded Keys.CONTROL
# silently fails to select on macOS, so local runs diverged from Linux CI.
SELECT_ALL_KEY = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL


class BasePage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 45)

    # ── Staging toast dismissal ──────────────────────────────────────────────

    def dismiss_dev_toast(self):
        """Get the staging 'Dev environment is unstable' toast out of the way.

        The toast sits at the top-right of every post-login page on staging and
        intercepts clicks on header buttons (~y=112). Two traps:

        * It is a close-on-click Toastify toast, usually WITHOUT a close button,
          so looking only for "#dev-environment-unstable button" did nothing.
        * It lives in the TOP document, while many admin pages are driven from
          inside a cross-origin legacy iframe — from there the toast is neither
          findable nor reachable via JS. Step out, dismiss, and step back into
          the same iframe (matched by its src).

        Safe to call when the toast is absent.
        """
        try:
            in_frame = self.driver.execute_script("return window.self !== window.top;")
        except Exception:  # noqa: BLE001
            in_frame = False
        if not in_frame:
            self._dismiss_dev_toast_here()
            return

        frame_href = self.driver.execute_script("return window.location.href;")
        self.driver.switch_to.default_content()
        try:
            self._dismiss_dev_toast_here()
        finally:
            self._reenter_frame(frame_href)

    HIDE_DEV_TOAST_CSS_JS = (
        "if (!document.getElementById('nxtwash-hide-dev-toast')) {"
        " const s = document.createElement('style');"
        " s.id = 'nxtwash-hide-dev-toast';"
        " s.textContent = '#dev-environment-unstable{display:none!important;"
        "pointer-events:none!important}';"
        " (document.head || document.documentElement).appendChild(s); }"
    )

    def _dismiss_dev_toast_here(self):
        toast_id = "dev-environment-unstable"
        # Persistent: keeps the toast hidden for this document's lifetime
        # (SPA navigations included), covering direct element.click() calls
        # that bypass BasePage.click's dismiss-and-retry.
        self.driver.execute_script(self.HIDE_DEV_TOAST_CSS_JS)
        if not self.driver.find_elements(By.ID, toast_id):
            return
        self.driver.execute_script(
            "const t = document.getElementById(arguments[0]);"
            "if (!t) return;"
            "const btn = t.querySelector('button');"
            "(btn || t).click();",
            toast_id,
        )
        try:
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located((By.ID, toast_id))
            )
        except Exception:  # noqa: BLE001 — fall back to hiding it outright
            self.driver.execute_script(
                "const t = document.getElementById(arguments[0]);"
                "if (t) { t.style.display = 'none'; t.style.pointerEvents = 'none'; }",
                toast_id,
            )

    def _reenter_frame(self, frame_href):
        """Switch back into the top-level iframe whose src matches frame_href."""
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        def _norm(url):
            return (url or "").split("#")[0].rstrip("/")
        target = next((f for f in frames if _norm(f.get_attribute("src")) == _norm(frame_href)), None)
        if target is None:  # SPA navigation inside the frame changed its URL
            origin = "/".join(_norm(frame_href).split("/")[:3])
            target = next((f for f in frames if _norm(f.get_attribute("src")).startswith(origin)), None)
        if target is None and frames:
            target = frames[0]
        if target is not None:
            self.driver.switch_to.frame(target)

    def click(self, locator):
        for attempt in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable(locator)).click()
                return
            except ElementClickInterceptedException:
                self.dismiss_dev_toast()
            except StaleElementReferenceException:
                if attempt == 2:
                    raise
                time.sleep(0.3)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_for_any_visible(self, locator):
        """Wait until ANY element matching ``locator`` is displayed.

        EC.visibility_of_element_located only checks the first match; text
        locators like a page title also match hidden sidebar entries that come
        first in the DOM, so that check can time out on a fully loaded page.
        """
        def _visible(d):
            for element in d.find_elements(*locator):
                try:
                    if element.is_displayed():
                        return element
                except StaleElementReferenceException:
                    continue
            return False

        return self.wait.until(_visible)

    _XPATH_TEXTS_JS = """
        const result = document.evaluate(arguments[0], document, null,
            XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
        const texts = [];
        for (let i = 0; i < result.snapshotLength; i++) {
            const t = (result.snapshotItem(i).innerText || "").trim();
            if (t) texts.push(t);
        }
        return texts;
    """

    def stable_texts(self, xpath, timeout=10):
        """Texts of all elements matching ``xpath``, read in one script call.

        Reading ``.text`` element-by-element goes stale when a table re-renders
        mid-read (e.g. right after a filter). A single JS snapshot can't go
        stale; waiting for two identical, non-empty reads skips the loading
        render.
        """
        last = {"texts": None}

        def _settled(d):
            texts = d.execute_script(self._XPATH_TEXTS_JS, xpath)
            same = bool(texts) and texts == last["texts"]
            last["texts"] = texts
            return same

        try:
            WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(_settled)
        except Exception:  # noqa: BLE001 — return the latest snapshot
            pass
        return last["texts"] or []

    def js_click_fresh(self, locator, attempts=3):
        """Re-locate and JS-click an element, retrying on staleness.

        List rows re-render when table data arrives or refreshes, so a row or
        button reference found a moment earlier can go stale before the click.
        Locating inside the retry loop always acts on the current node.
        """
        for attempt in range(attempts):
            try:
                element = self.wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", element
                )
                self.driver.execute_script("arguments[0].click();", element)
                return
            except StaleElementReferenceException:
                if attempt == attempts - 1:
                    raise
                time.sleep(0.5)

    def enter_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if element.tag_name.lower() == "textarea":
            self.driver.execute_script(
                "arguments[0].value=arguments[1];"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                element, text
            )
        else:
            self.driver.execute_script(
                "var s=Object.getOwnPropertyDescriptor("
                "window.HTMLInputElement.prototype,'value').set;"
                "s.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                element, text
            )

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
                    inner_input.send_keys(SELECT_ALL_KEY, "a")
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
        from selenium.webdriver.common.action_chains import ActionChains
        el = self.wait.until(EC.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(el).perform()

    # ── Error / duplicate detection ─────────────────────────────────────────

    _DUPLICATE_KEYWORDS = (
        "already exists", "duplicate", "already in use",
        "name is taken", "must be unique", "already been taken",
        "already used", "conflict", "already associated",
    )
    _SERVER_ERROR_KEYWORDS = (
        "something went wrong", "internal server error",
        "failed to fetch", "unauthorized", "application error",
        # Legacy forms report save failures as "An error occured while ..."
        # (sic) with the API payload inline.
        "error occured", "error occurred",
    )

    def wait_for_legacy_save(self, timeout=20):
        """After clicking Save inside a legacy iframe form, wait for the outcome.

        A successful legacy save redirects by itself within ~1 s: the top URL
        and the iframe leave ``/edit/<id>`` or ``/new``. That redirect is the
        reliable "saved" signal. (Waiting for the Save button to disable and
        re-enable does not work: the button vanishes with the old frame, the
        lookup keeps failing, and WebDriverWait silently polls to its 45 s
        timeout before navigating away blind.)

        Returns ("saved", None) or ("error", text). Raises TimeoutError if the
        page neither redirects nor shows an error — the save did not land, so
        callers must not navigate away as if it had.
        """
        import time as _time
        frame_href = None
        try:
            if self.driver.execute_script("return window.self !== window.top;"):
                frame_href = self.driver.execute_script("return window.location.href;")
        except Exception:  # noqa: BLE001
            pass
        deadline = _time.time() + timeout
        last_text = ""
        while _time.time() < deadline:
            _time.sleep(0.5)
            self.driver.switch_to.default_content()
            top = self.driver.current_url or ""
            if "/edit/" not in top and not top.rstrip("/").endswith("/new"):
                return "saved", None
            if frame_href:
                try:
                    self._reenter_frame(frame_href)
                except Exception:  # noqa: BLE001
                    continue
            error = self.get_visible_error()
            if error:
                return "error", error
            try:
                last_text = self.driver.find_element(By.TAG_NAME, "body").text[:400]
            except Exception:  # noqa: BLE001
                pass
        raise TimeoutError(
            "Save did not complete within %ss — still on %s. Page text: %s"
            % (timeout, self.driver.current_url, last_text)
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
                    # Prefix the matched keyword — a large page (e.g. a data
                    # grid) can contain one of these words incidentally, and
                    # without this callers can't tell a real error banner
                    # from a false-positive substring match.
                    return "[matched keyword: %r] %s" % (kw, body[:600])
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

    def wait_clickable_with_retry(self, locator, timeout=45):
        """Wait for an element to be clickable, retrying on staleness.

        EC.element_to_be_clickable re-finds the element by locator on every
        poll, but then calls .is_displayed()/.is_enabled() on that specific
        reference. If the element re-renders (e.g. a React filter modal) in
        the gap between the find and that check, the call raises
        StaleElementReferenceException — and WebDriverWait, which by default
        only ignores NoSuchElementException, aborts the whole wait on the
        first such hit instead of retrying with the time left on the clock.
        """
        from selenium.common.exceptions import TimeoutException as TE
        deadline = time.time() + timeout
        last_exc = None
        while time.time() < deadline:
            try:
                remaining = max(1, deadline - time.time())
                return WebDriverWait(self.driver, remaining).until(
                    EC.element_to_be_clickable(locator)
                )
            except StaleElementReferenceException as exc:
                last_exc = exc
                time.sleep(0.3)
        raise TE("Element %s not stable after %ss" % (locator, timeout)) from last_exc

    def wait_visible_with_retry(self, locator, timeout=45):
        """Wait for an element to be visible, retrying on staleness.

        Same TOCTOU gap as wait_clickable_with_retry, for the
        EC.visibility_of_element_located gate used by list/page-load checks
        (e.g. a PAGE_TITLE or grid-header check right after a frame switch).
        """
        from selenium.common.exceptions import TimeoutException as TE
        deadline = time.time() + timeout
        last_exc = None
        while time.time() < deadline:
            try:
                remaining = max(1, deadline - time.time())
                return WebDriverWait(self.driver, remaining).until(
                    EC.visibility_of_element_located(locator)
                )
            except StaleElementReferenceException as exc:
                last_exc = exc
                time.sleep(0.3)
        raise TE("Element %s not stable after %ss" % (locator, timeout)) from last_exc

    def wait_for_persisted_value(
        self, value_getter, expected, reopen=None, attempts=6, per_try=5, max_seconds=120
    ):
        """Poll a just-saved field until it reflects the persisted value.

        Some staging endpoints have read-after-write lag: the per-record detail
        fetch (or a list search) can briefly return pre-save data right after
        Save returns. A single read immediately after reopening a record is not
        trustworthy for a field that was just changed — poll instead, optionally
        calling `reopen` (a zero-arg callable, typically "reopen the edit form")
        between attempts to force a fresh fetch rather than re-reading a DOM
        value that will never change on its own.

        reopen/value_getter are allowed to raise (e.g. a frame not stabilizing
        under load) without ending the retry loop early — under contention
        (many parallel jobs hitting staging at once) that's just another kind
        of transient lag. A raise consumes one attempt like a value mismatch
        does; only the last attempt's exception propagates.

        max_seconds bounds total wall-clock time, not just attempt count:
        reopen() has its own internal timeout (e.g. switch_to_frame_with_retry's
        90s), so `attempts` slow/failing reopens can otherwise take several
        times pytest's own per-test timeout (420s) before this loop gives up.
        Stop starting new attempts once the budget is spent instead.
        """
        from selenium.common.exceptions import WebDriverException
        deadline = time.time() + max_seconds
        value = None
        last_exc = None
        for attempt in range(attempts):
            try:
                if value is None:
                    value = value_getter()
                if value == expected:
                    return value
            except WebDriverException as exc:
                last_exc = exc
                value = None
            if attempt == attempts - 1 or time.time() >= deadline:
                break
            time.sleep(per_try)
            try:
                if reopen:
                    reopen()
                value = value_getter()
            except WebDriverException as exc:
                last_exc = exc
                value = None
        if value is None and last_exc is not None:
            raise last_exc
        return value

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
