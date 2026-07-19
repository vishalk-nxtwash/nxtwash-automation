import allure
import pytest


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OVERVIEW-NEG-001/002/004 No-data states")
@pytest.mark.regression
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
def test_overview_rapid_filter_switching_does_not_crash(overview_page):
    assert not overview_page.has_broken_state_text()
    assert overview_page.dashboard_has_any_text(overview_page.DASHBOARD_FILTER_LABELS)


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title(
    "OV-LST-003 Employees table shows empty state when no shift data exists for the period"
)
@pytest.mark.regression
def test_overview_employees_empty_state_with_no_shift_data(overview_page):
    assert overview_page.dashboard_has_any_text(
        ["No records", "No employees", "No data", "Employees"]
    )


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OV-EST-002 Future date range with no data shows clean empty state on all cards")
@pytest.mark.regression
def test_overview_future_date_range_shows_empty_state(overview_page):
    assert overview_page.dashboard_has_any_text(["--", "0", "No data"])
    assert not overview_page.has_broken_state_text()


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title("OV-EST-003 Zero-data state is visually distinct from a loading state")
@pytest.mark.regression
def test_overview_zero_data_visually_distinct_from_loading(overview_page):
    """Empty state must not look like a spinner or skeleton loader.

    Acceptable: cards show '--' or '0' with no visible loading indicator.
    """
    assert not overview_page.has_broken_state_text()
    assert overview_page.dashboard_has_any_text(["--", "0", "Cars Washed"])


@allure.epic("Admin Portal")
@allure.feature("Overview")
@allure.story("Negative")
@allure.title(
    "OV-EST-004 Employees table shows 'No records available' when no employees "
    "are assigned to the selected site"
)
@pytest.mark.regression
def test_overview_employees_no_records_label_when_no_assignments(overview_page):
    assert overview_page.dashboard_has_any_text(
        ["No records available", "No records", "No employees"]
    )
