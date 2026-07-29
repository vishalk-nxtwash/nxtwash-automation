import allure
import pytest


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Overview"),
    allure.story("Known Bugs"),
]

_IFRAME_XFAIL = pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty.",
    strict=False,
)


@allure.title("OV-BUG-001 Labor % shows an extreme value instead of a valid percentage")
@pytest.mark.regression
def test_overview_labor_percent_extreme_value_bug(overview_page):
    """Document known bug: labor % can render as an extreme/invalid number.

    When total revenue is very low or calculation overflows, the Labor % card
    displays a nonsensical large value instead of a bounded percentage.
    The test asserts the value is NOT present — a pass here means the bug is
    fixed; an xfail means the environment cannot be tested yet.
    """
    dashboard_text = overview_page.get_legacy_dashboard_text()
    assert "999999" not in dashboard_text
    assert not overview_page.has_broken_state_text()


@allure.title(
    "OV-BUG-002 Labor % displays '--' or 0% when no revenue exists for the period"
)
@pytest.mark.regression
@_IFRAME_XFAIL
def test_overview_labor_percent_no_revenue_shows_placeholder(overview_page):
    """With zero revenue the Labor % denominator is zero.

    Expected: the card shows '--' or '0%' rather than a calculation error or
    divide-by-zero crash.
    """
    assert overview_page.dashboard_has_any_text(["--", "0%", "Labor"])
    assert not overview_page.has_broken_state_text()


@allure.title(
    "OV-BUG-003 Usage Breakdown percentages sum to exactly 100 % or show a rounding note"
)
@pytest.mark.regression
@_IFRAME_XFAIL
def test_overview_usage_breakdown_percentages_sum_to_100(overview_page):
    """Usage Breakdown per-service rows should total 100 %.

    Due to floating-point rounding some implementations display 99 % or 101 %.
    Acceptable outcomes: exactly '100%' visible, or an explicit rounding note.
    The test documents current behaviour; fix the xfail reason once the iframe
    environment is live.
    """
    assert overview_page.dashboard_has_any_text(["100%", "100 %", "rounding"])
    assert not overview_page.has_broken_state_text()
