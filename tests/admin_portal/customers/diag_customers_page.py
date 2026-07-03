"""
Diagnostic — finds Apply/Reset filter buttons and Active customer switch HTML.
Run:  venv/bin/pytest tests/admin_portal/customers/diag_customers_page.py -v -s
"""
import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from tests.admin_portal.admin_session import open_admin_path


def test_dump_filter_and_switch_details(browser):
    open_admin_path(browser, "/customers")
    wait = WebDriverWait(browser, 20)

    # Switch to customers iframe
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    browser.switch_to.frame(iframes[0])
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Open filter panel
    filter_btns = [b for b in browser.find_elements(By.TAG_NAME, "button")
                   if "filter" in b.text.lower() and b.is_displayed()]
    browser.execute_script("arguments[0].click();", filter_btns[0])
    time.sleep(2)

    # Scroll page + any panel containers to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    browser.execute_script("""
        document.querySelectorAll('*').forEach(el => {
            if (el.scrollHeight > el.clientHeight) {
                el.scrollTop = el.scrollHeight;
            }
        });
    """)
    time.sleep(0.5)

    # Full body text — no limit
    full_body = browser.find_element(By.TAG_NAME, "body").text
    print("\n\n=== FULL FILTER PANEL BODY TEXT ===")
    print(full_body)

    # Every button with all useful attributes
    buttons = browser.find_elements(By.TAG_NAME, "button")
    print(f"\n=== ALL BUTTONS WITH ATTRIBUTES ({len(buttons)} found) ===")
    for b in buttons:
        try:
            print(
                f"  text={b.text.strip()!r}"
                f"  aria-label={b.get_attribute('aria-label')!r}"
                f"  title={b.get_attribute('title')!r}"
                f"  type={b.get_attribute('type')!r}"
                f"  role={b.get_attribute('role')!r}"
                f"  aria-checked={b.get_attribute('aria-checked')!r}"
                f"  visible={b.is_displayed()}"
            )
        except Exception:
            pass

    # Now close filter and open create form, find Active customer switch HTML
    browser.switch_to.default_content()
    iframes = browser.find_elements(By.TAG_NAME, "iframe")
    browser.switch_to.frame(iframes[0])

    add_btns = [b for b in browser.find_elements(By.TAG_NAME, "button")
                if "add customer" in b.text.lower() and b.is_displayed()]
    if add_btns:
        browser.execute_script("arguments[0].click();", add_btns[0])
        time.sleep(2)

        browser.switch_to.default_content()
        iframes2 = browser.find_elements(By.TAG_NAME, "iframe")
        for f in iframes2:
            src = f.get_attribute("src") or ""
            if "customers/new" in src or ("customer" in src and "new" in src):
                browser.switch_to.frame(f)
                break
        else:
            browser.switch_to.frame(iframes2[0])

        time.sleep(1)

        # Find the "Active customer" area and dump surrounding HTML
        active_els = browser.find_elements(
            By.XPATH, "//*[normalize-space()='Active customer']"
        )
        print(f"\n=== 'Active customer' ELEMENTS FOUND: {len(active_els)} ===")
        for el in active_els:
            try:
                parent_html = browser.execute_script(
                    "return arguments[0].parentElement.outerHTML;", el
                )
                print(f"  tag={el.tag_name}  parent HTML:\n{parent_html[:800]}\n")
            except Exception as e:
                print(f"  Error: {e}")

        # Also dump all switch buttons in create form
        switches = browser.find_elements(By.XPATH, "//button[@role='switch']")
        print(f"\n=== SWITCH BUTTONS in CREATE FORM ({len(switches)} found) ===")
        for sw in switches:
            try:
                parent_text = browser.execute_script(
                    "return arguments[0].parentElement.innerText;", sw
                )
                print(
                    f"  aria-checked={sw.get_attribute('aria-checked')!r}"
                    f"  aria-label={sw.get_attribute('aria-label')!r}"
                    f"  parent text={parent_text!r}"
                )
            except Exception:
                pass

    assert True
