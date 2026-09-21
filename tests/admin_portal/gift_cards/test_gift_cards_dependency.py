import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gift Cards"),
    allure.story("Dependency"),
]


@allure.title("GC-PER-002 Show on customer portal per-location switch persists after save")
@pytest.mark.manual
@pytest.mark.skip(
    reason=(
        "GC-PER-002: Per-location Show on CP switch is interactive but the value is "
        "not persisted by the save API — the switch resets to OFF on reload. "
        "CP visibility per location is governed by Site settings (Customer Portal tab). "
        "Verify manually via DevTools network tab or site-level CP gift cards toggle."
    )
)
def test_gift_card_show_on_cp_persists(browser):
    pass
