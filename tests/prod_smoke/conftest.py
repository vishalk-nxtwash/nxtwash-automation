# Production smoke suite — shared helpers.
#
# ALL tests in this directory must be READ-ONLY.
# No creates, edits, or deletes against the production environment.
#
# Run with:
#   pytest tests/prod_smoke/ --env production --headless -v
#
# Required env vars for production credentials:
#   ADMIN_PORTAL_USERNAME   (prod admin email)
#   ADMIN_PORTAL_PASSWORD   (prod admin password)

from selenium.webdriver.common.by import By


_BROKEN_KEYWORDS = [
    "Something went wrong",
    "Internal Server Error",
    "404",
    "Unauthorized",
    "Failed to fetch",
    "Page not found",
    "Cannot GET",
    "ChunkLoadError",
]


def page_is_up(driver):
    """Return True if the page loaded without a known error state."""
    if "/login" in driver.current_url:
        return False
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
    except Exception:
        return False
    return not any(k in body for k in _BROKEN_KEYWORDS)
