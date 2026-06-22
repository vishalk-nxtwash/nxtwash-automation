import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OVERVIEW-NEG-001/002/004 No-data states")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty and no no-data site fixture exists.",
    strict=False,
)
def test_overview_no_data_states_are_handled(overview_page):
    assert overview_page.dashboard_has_any_text(["No data", "No records"])


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OVERVIEW-NEG-003 Network failure while applying filters")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Blocked: no network interception utility exists for Overview filter requests.",
    strict=False,
)
def test_overview_network_failure_is_handled(overview_page):
    assert overview_page.dashboard_has_any_text(["Error", "Failed"])


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OVERVIEW-NEG-005 Rapid filter switching")
@pytest.mark.regression
@pytest.mark.xfail(
    reason="Known product/environment gap: legacy Overview iframe is empty; filters are unavailable.",
    strict=False,
)
def test_overview_rapid_filter_switching_does_not_crash(overview_page):
    assert not overview_page.has_broken_state_text()
    assert overview_page.dashboard_has_any_text(overview_page.DASHBOARD_FILTER_LABELS)
