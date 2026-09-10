import allure

pytestmark = [
    allure.epic("Superadmin"),
    allure.feature("Companies"),
    allure.story("Public Settings"),
]


def test_default_language_defaults_to_english(edit_company_page):
    """SA-CMP-PUB-001 — Default language dropdown is present and defaults to English."""
    language = edit_company_page.get_default_language()

    assert language is not None, \
        "Default language dropdown should be present in Public Settings"
    assert "english" in (language or "").lower(), \
        f"Default language should be English, got: {language!r}"
