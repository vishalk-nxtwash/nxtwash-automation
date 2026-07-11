"""
Diagnostic probe v2 — uses real Selenium interaction (not JS click) to open
each dropdown and dumps actual CSS classes, option counts, and full menu HTML.

Run: .venv/bin/python scripts/pfm_dom_probe.py
"""
import sys, time
sys.path.insert(0, ".")

from tests.admin_portal.admin_session import open_admin_path
from core.driver_factory import DriverFactory
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = DriverFactory.get_driver(headless=True)
wait   = WebDriverWait(driver, 20)

def banner(title):
    print("\n" + "=" * 60)
    print("  " + title)
    print("=" * 60)

try:
    open_admin_path(driver, "/performance-metrics")
    time.sleep(3)

    # ── 1. Iframe / frame context ──────────────────────────────────────────────
    banner("1. IFRAME CHECK")
    frames = driver.find_elements(By.TAG_NAME, "iframe")
    print("  iframes on page:", len(frames))
    for f in frames:
        print("    src:", repr(f.get_attribute("src")))
    print("  Current URL:", driver.current_url)

    # ── 2. Confirm Apply filters button ───────────────────────────────────────
    banner("2. APPLY BUTTON")
    try:
        btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(normalize-space(),'Apply')]")))
        print("  FOUND  text=%r  class=%s" % (btn.text.strip(),
              (btn.get_attribute("class") or "")[:60]))
    except TimeoutException:
        print("  NOT FOUND — modal did not load")

    # ── 3. Site multiselect: click inner input, type a letter, inspect options
    banner("3. SITE MULTISELECT — open by clicking inner input")
    site_inputs = driver.find_elements(By.XPATH,
        "//input[contains(@class,'nxt-multi-select__input') or "
        "(ancestor::*[contains(@class,'nxt-multi-select')] and self::input)]")
    print("  nxt-multi-select inputs found:", len(site_inputs))
    if site_inputs:
        inp = site_inputs[0]
        print("  Clicking first input, class=%s" % inp.get_attribute("class"))
        ActionChains(driver).move_to_element(inp).click(inp).perform()
        time.sleep(0.5)
        inp.send_keys("V")          # type one letter to trigger React Select
        time.sleep(2.0)

        # Look for any menu/option/listbox that appeared
        menu_els = driver.find_elements(By.XPATH,
            "//*[@role='listbox'] | //*[@role='option'] | "
            "//*[contains(@class,'menu') and "
            "not(contains(@class,'menu-item'))]"
            "[not(self::script)][not(self::style)]"
        )
        print("  Menu/listbox/option elements after typing 'V':", len(menu_els))
        for el in menu_els[:6]:
            if el.is_displayed():
                cls = (el.get_attribute("class") or "")[:80]
                txt = el.text.strip()[:50]
                print("    role=%-12s  tag=%-6s  class=%s  text=%r" % (
                    el.get_attribute("role") or "",
                    el.tag_name, cls, txt))

        # Also dump all options found via the base_page JS query
        opt_js = driver.execute_script("""
            var candidates = Array.from(document.querySelectorAll(
                '[role="option"],[class*="__option"],[class*="-option"],[class*="select__option"]'
            ));
            return candidates.filter(function(el){
                return el.offsetParent !== null && el.textContent.trim();
            }).map(function(el){
                return { text: el.textContent.trim().slice(0,40),
                         cls: (el.className||'').slice(0,60),
                         tag: el.tagName };
            });
        """)
        print("  _find_react_option JS candidates:", len(opt_js))
        for o in opt_js[:8]:
            print("    tag=%-6s  text=%-30s  class=%s" % (
                o['tag'], repr(o['text']), o['cls']))

        inp.send_keys(Keys.ESCAPE)
        time.sleep(0.5)
    else:
        # Fallback: try clicking the control div
        ctrl = driver.find_elements(By.XPATH,
            "//div[contains(@class,'nxt-multi-select__control')]")
        print("  Trying control div click. Found:", len(ctrl))
        if ctrl:
            ActionChains(driver).move_to_element(ctrl[0]).click(ctrl[0]).perform()
            time.sleep(2)
            opts_all = driver.find_elements(By.XPATH,
                "//*[@role='option'] | //*[contains(@class,'__option')]")
            print("  Options after div click:", len([o for o in opts_all if o.is_displayed()]))

    # ── 4. Date preset: open and inspect options ───────────────────────────────
    banner("4. DATE PRESET DROPDOWN — open and inspect options")
    preset_inputs = driver.find_elements(By.XPATH,
        "//input[contains(@class,'nxt-select__input') and "
        "not(contains(@class,'nxt-multi-select'))]")
    print("  nxt-select inputs (non-multi) found:", len(preset_inputs))
    if preset_inputs:
        inp = preset_inputs[0]
        print("  Input class:", inp.get_attribute("class"))
        # Click the parent control to open
        ctrl = inp.find_element(By.XPATH,
            "ancestor::*[contains(@class,'nxt-select__control')][1]")
        print("  Parent control class:", (ctrl.get_attribute("class") or "")[:80])
        ActionChains(driver).move_to_element(ctrl).click(ctrl).perform()
        time.sleep(2.0)

        menu_els = driver.find_elements(By.XPATH,
            "//*[@role='listbox'] | //*[@role='option'] | "
            "//*[contains(@class,'nxt-select__menu') and "
            "not(contains(@class,'nxt-multi-select'))]")
        print("  Menu/option elements after clicking preset:", len(menu_els))
        for el in menu_els[:10]:
            if el.is_displayed():
                cls = (el.get_attribute("class") or "")[:80]
                txt = el.text.strip()[:40]
                print("    role=%-12s  tag=%-6s  class=%s  text=%r" % (
                    el.get_attribute("role") or "",
                    el.tag_name, cls, txt))

        # JS candidate search
        opt_js2 = driver.execute_script("""
            return Array.from(document.querySelectorAll(
                '[role="option"],[class*="nxt-select__option"],[class*="__option"]'
            )).filter(function(el){
                return el.offsetParent !== null && el.textContent.trim();
            }).map(function(el){
                return { text: el.textContent.trim().slice(0,30),
                         cls: (el.className||'').slice(0,80) };
            });
        """)
        print("  JS candidates for nxt-select__option:", len(opt_js2))
        for o in opt_js2[:8]:
            print("    text=%-25s  class=%s" % (repr(o['text']), o['cls']))

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    # ── 5. Date range input and Single Day checkbox ───────────────────────────
    banner("5. DATE RANGE INPUT + SINGLE DAY")
    date_inputs = driver.find_elements(By.XPATH,
        "//input[@placeholder='Select date range']")
    print("  date-range inputs found:", len(date_inputs))
    for inp in date_inputs:
        print("    placeholder=%r  displayed=%s  class=%s" % (
            inp.get_attribute("placeholder"),
            inp.is_displayed(),
            (inp.get_attribute("class") or "")[:60]
        ))

    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print("  checkboxes found:", len(checkboxes))
    for cb in checkboxes:
        try:
            parent = driver.execute_script(
                "return arguments[0].closest('label,div,span');", cb)
            ptxt = (parent.text if parent else "")[:60].replace("\n", " ")
        except Exception:
            ptxt = ""
        print("    checked=%-5s  name=%-15s  parent=%r" % (
            cb.is_selected(),
            cb.get_attribute("name") or cb.get_attribute("id") or "",
            ptxt))

    # ── 6. Attempt select_site via page object ─────────────────────────────────
    banner("6. LIVE select_site() + select_date_preset() TEST")
    from pages.admin_portal.performance_metrics_page import PerformanceMetricsPage
    page = PerformanceMetricsPage(driver)

    print("  Calling select_site('VK Test carwash 2') ...")
    try:
        page.select_site("VK Test carwash 2")
        chips = page.get_site_chips()
        print("  select_site OK  chips=%s" % chips)
    except Exception as e:
        print("  select_site FAILED: %s" % str(e)[:200])

    print("  Calling select_date_preset('Last month') ...")
    try:
        page.select_date_preset("Last month")
        val = page.get_date_range_value()
        print("  select_date_preset OK  date_range=%r" % val)
    except Exception as e:
        print("  select_date_preset FAILED: %s" % str(e)[:200])

    print("  Calling apply_modal_filters() ...")
    try:
        page.apply_modal_filters()
        print("  apply_modal_filters OK  modal_open=%s" % page.modal_is_open())
    except Exception as e:
        print("  apply_modal_filters FAILED: %s" % str(e)[:200])

    banner("DONE")

finally:
    driver.quit()
