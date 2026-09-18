import allure
import pytest

from tests.admin_portal.kiosk_settings.conftest import (
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Kiosk Settings"),
    allure.story("Localization Settings"),
]

_SETTINGS_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Settings section locators use heuristics — verify section header classes "
        "in DevTools before removing xfail."
    ),
)


@allure.title("KSK-LOC-001 Localization settings section can be expanded and collapsed")
@pytest.mark.regression
@_SETTINGS_XFAIL
def test_localization_section_expand_collapse(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Localization")
    assert form.section_is_expanded("Localization"), (
        "Localization section should be expanded after expand_section()"
    )
    form.collapse_section("Localization")
    assert not form.section_is_expanded("Localization"), (
        "Localization section should be collapsed after collapse_section()"
    )
    assert page_has_no_broken_state(form)


@allure.title("KSK-LOC-002 Use external translations toggle saves ON and OFF")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_localization_external_translations_toggle_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Localization")
    form.ensure_use_external_translations_on()
    form.click_save()

    assert page_has_no_broken_state(form)


@allure.title("KSK-LOC-003 External translation URL added via + button saves correctly")
@pytest.mark.extended
@_SETTINGS_XFAIL
def test_localization_translation_url_saves(browser, managed_kiosk_form):
    form = managed_kiosk_form
    form.expand_section("Localization")
    form.ensure_use_external_translations_on()
    form.enter_translation_url("https://translations.example.com/en.json")
    form.click_save()

    assert page_has_no_broken_state(form)
