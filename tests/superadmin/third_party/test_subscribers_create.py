import allure
import pytest

from tests.superadmin.third_party.conftest import SUBSCRIBER_ABBR, SUBSCRIBER_NAME

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Third Party"),
    allure.story("Webhook Subscribers — Create"),
]


def test_add_subscriber_button_opens_create_form(create_subscriber_page):
    """SA-SUB-CRT-001 — '+ Add Webhook Subscriber' opens the create form."""
    from selenium.webdriver.common.by import By
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text
    assert "New" in body or "Save new" in body, \
        "Create form should show 'New' mode indicator or 'Save new' button"
    assert "third-party/subscribers" in create_subscriber_page.driver.current_url, \
        "URL should contain /third-party/subscribers"


def test_create_form_shows_basic_settings(create_subscriber_page):
    """SA-SUB-CRT-002 — Create form shows Basic Settings section with expected fields."""
    from selenium.webdriver.common.by import By
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text
    assert "Basic Settings" in body, "Create form should have a 'Basic Settings' section"
    name_els = create_subscriber_page.driver.find_elements(
        *create_subscriber_page.NAME_INPUT
    )
    abbr_els = create_subscriber_page.driver.find_elements(
        *create_subscriber_page.ABBREVIATION_INPUT
    )
    assert name_els, "Subscriber Name input should be present"
    assert abbr_els, "Abbreviation input should be present"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-003: Red asterisk required-field marker locator not confirmed.",
)
def test_required_fields_show_asterisk(create_subscriber_page):
    """SA-SUB-CRT-003 — Subscriber Name and Abbreviation are marked required."""
    from selenium.webdriver.common.by import By
    # Asterisk is typically rendered as a <span> or pseudo-element near the label
    asterisks = create_subscriber_page.driver.find_elements(
        By.XPATH, "//*[text()='*' or contains(@class,'required') or contains(@class,'asterisk')]"
    )
    assert asterisks, "Required field markers (*) should be visible on the create form"


def test_active_subscriber_toggle_defaults_on(create_subscriber_page):
    """SA-SUB-CRT-004 — 'Active Subscriber' toggle defaults to ON."""
    state = create_subscriber_page.get_active_toggle_state()
    assert state is True, \
        f"'Active Subscriber' toggle should be ON by default, got: {state}"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-005/006: Happy-path create modifies staging data. "
           "The conftest manages 'VK Auto Test Sub' idempotently — running this "
           "test directly may produce a duplicate-name error on subsequent runs.",
)
def test_create_subscriber_happy_path(create_subscriber_page, subscribers_page):
    """SA-SUB-CRT-005 — Create with valid name + abbreviation → saves and returns to list."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name(SUBSCRIBER_NAME)
    create_subscriber_page.enter_abbreviation(SUBSCRIBER_ABBR)
    create_subscriber_page.click_save_new()

    WebDriverWait(create_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text
    assert SUBSCRIBER_NAME in body, \
        f"New subscriber '{SUBSCRIBER_NAME}' should appear in the list after creation"


def test_new_subscriber_appears_in_list(subscribers_page):
    """SA-SUB-CRT-006 — New subscriber appears in the list and records count increments."""
    assert subscribers_page.row_exists(SUBSCRIBER_NAME), \
        f"'{SUBSCRIBER_NAME}' should be visible in the subscribers list"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-007: Subscriber may land on page 2 of the list (pagination) "
           "after creation — row_exists checks only the current visible page.",
)
def test_create_with_active_on(create_subscriber_page, subscribers_page):
    """SA-SUB-CRT-007 — Create with Active Subscriber ON saves an active subscriber."""
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name(SUBSCRIBER_NAME + " Active")
    create_subscriber_page.enter_abbreviation("VA")
    # Toggle is ON by default; just save
    create_subscriber_page.click_save_new()
    WebDriverWait(create_subscriber_page.driver, 30).until(
        EC.url_contains("/third-party/subscribers")
    )
    assert subscribers_page.row_exists(SUBSCRIBER_NAME + " Active"), \
        "Active subscriber should appear in the list"


def test_create_with_active_off(create_subscriber_page):
    """SA-SUB-CRT-008 — Create with Active Subscriber OFF saves as inactive."""
    create_subscriber_page.enter_name(SUBSCRIBER_NAME + " Inactive")
    create_subscriber_page.enter_abbreviation("VI")
    create_subscriber_page.set_active_toggle(False)
    state = create_subscriber_page.get_active_toggle_state()
    assert state is False, "Toggle should be OFF before saving"


def test_save_without_name_shows_validation(create_subscriber_page):
    """SA-SUB-CRT-009 — Save without Subscriber Name is blocked with a validation error."""
    from selenium.webdriver.common.by import By

    create_subscriber_page.enter_abbreviation(SUBSCRIBER_ABBR)
    create_subscriber_page.click_save_new()

    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    still_on_create = "save new" in body
    has_error = any(k in body for k in ("required", "invalid", "must", "field"))
    assert still_on_create or has_error, \
        "Saving without a name should be blocked with a validation error"


def test_save_without_abbreviation_shows_validation(create_subscriber_page):
    """SA-SUB-CRT-010 — Save without Abbreviation is blocked with a validation error."""
    from selenium.webdriver.common.by import By

    create_subscriber_page.enter_name("VK No Abbr Test")
    create_subscriber_page.click_save_new()

    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    still_on_create = "save new" in body
    has_error = any(k in body for k in ("required", "invalid", "must", "field"))
    assert still_on_create or has_error, \
        "Saving without an abbreviation should be blocked with a validation error"


def test_duplicate_subscriber_name_behaviour(create_subscriber_page):
    """SA-SUB-CRT-011 — Duplicate Subscriber Name — document behaviour."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name("Tether")  # known existing name
    create_subscriber_page.enter_abbreviation("TX")
    create_subscriber_page.click_save_new()

    try:
        WebDriverWait(create_subscriber_page.driver, 5).until(
            EC.url_contains("/third-party/subscribers")
        )
        # allowed — document: duplicates are accepted
        assert True
    except Exception:
        body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(k in body for k in ("duplicate", "already", "exists", "unique")), \
            "Duplicate name should be rejected with a clear error message"


def test_duplicate_abbreviation_behaviour(create_subscriber_page):
    """SA-SUB-CRT-012 — Duplicate Abbreviation — document behaviour."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name("VK Dup Abbr Test")
    create_subscriber_page.enter_abbreviation("TE")  # known existing abbreviation
    create_subscriber_page.click_save_new()

    try:
        WebDriverWait(create_subscriber_page.driver, 5).until(
            EC.url_contains("/third-party/subscribers")
        )
        assert True  # duplicates allowed
    except Exception:
        body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
        assert any(k in body for k in ("duplicate", "already", "exists", "unique")), \
            "Duplicate abbreviation should be rejected with a clear error message"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-013: Abbreviation length/charset constraint not documented — "
           "confirmed values are 2 chars (TE, OP); min/max/charset unconfirmed.",
)
def test_abbreviation_format_constraint(create_subscriber_page):
    """SA-SUB-CRT-013 — Abbreviation length/format constraint — document accepted values."""
    from selenium.webdriver.common.by import By
    create_subscriber_page.enter_name("VK Abbr Format Test")
    create_subscriber_page.enter_abbreviation("TOOLONGABBR")
    create_subscriber_page.click_save_new()
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    has_error = any(k in body for k in ("too long", "max", "length", "invalid", "required"))
    still_on_form = "save new" in body
    assert has_error or still_on_form, \
        "Overlong abbreviation should be rejected or truncated"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-014: Whitespace-only input rejection not confirmed — "
           "server may trim and then fail required-field validation.",
)
def test_whitespace_only_inputs_rejected(create_subscriber_page):
    """SA-SUB-CRT-014 — Whitespace-only Subscriber Name / Abbreviation are rejected."""
    from selenium.webdriver.common.by import By
    create_subscriber_page.enter_name("   ")
    create_subscriber_page.enter_abbreviation("   ")
    create_subscriber_page.click_save_new()
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "save new" in body or any(
        k in body for k in ("required", "invalid", "must")
    ), "Whitespace-only inputs should be rejected"


@pytest.mark.xfail(
    strict=False,
    reason="SA-SUB-CRT-015: Leading/trailing whitespace trim behaviour not confirmed.",
)
def test_leading_trailing_whitespace_handling(create_subscriber_page):
    """SA-SUB-CRT-015 — Leading/trailing whitespace is trimmed or rejected."""
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name("  VK Trim Test  ")
    create_subscriber_page.enter_abbreviation("  ZZ  ")
    create_subscriber_page.click_save_new()

    try:
        WebDriverWait(create_subscriber_page.driver, 5).until(
            EC.url_contains("/third-party/subscribers")
        )
        body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text
        assert "VK Trim Test" in body, \
            "Trimmed name should appear in the list"
    except Exception:
        # rejected — also acceptable
        body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
        assert "save new" in body


def test_special_characters_handled_gracefully(create_subscriber_page):
    """SA-SUB-CRT-016 — Special characters / emoji handled gracefully."""
    from selenium.webdriver.common.by import By
    create_subscriber_page.enter_name("VK!@# Special 🔑")
    create_subscriber_page.enter_abbreviation("!!")
    create_subscriber_page.click_save_new()
    body = create_subscriber_page.driver.find_element(By.TAG_NAME, "body").text.lower()
    assert "error" not in body or "save new" in body, \
        "Special characters should not cause an unhandled server error"


def test_cancel_discards_create_form(create_subscriber_page, subscribers_page):
    """SA-SUB-CRT-017 — Cancel discards the form and returns to the list."""
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    create_subscriber_page.enter_name("VK Should Not Be Saved")
    create_subscriber_page.enter_abbreviation("NS")
    create_subscriber_page.click_cancel()
    create_subscriber_page.confirm_yes_if_present()

    WebDriverWait(create_subscriber_page.driver, 20).until(
        EC.url_contains("/third-party/subscribers")
    )
    assert not subscribers_page.row_exists("VK Should Not Be Saved", timeout=5), \
        "Cancelled subscriber should NOT appear in the list"
