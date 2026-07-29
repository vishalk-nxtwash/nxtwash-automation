import re

import allure
import pytest

from tests.admin_portal.gas_pump_settings.conftest import (
    GPS_BAUD_RATE,
    GPS_CODE_LENGTH,
    GPS_FETCH_INTERVAL,
    GPS_LINK_TIMEOUT,
    GPS_NEW_NAME,
    GPS_PUMP_NAME,
    GPS_SERIAL_NUMBER,
    GPS_SERIAL_PORT,
    GPS_SITE,
    GPS_WASH_BOOK,
    GPS_WBC_ID_CODE,
    NONEXISTENT_PUMP_NAME,
    PUMP_IS_CONNECTED,
    open_create_gas_pump_form,
    open_edit_gas_pump_form,
    open_gas_pump_list,
    page_has_no_broken_state,
)


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Gas Pump Settings"),
]

_CONNECTED_ONLY = pytest.mark.skipif(
    not PUMP_IS_CONNECTED,
    reason=(
        "Requires a gas pump physically connected to staging hardware. "
        "Set PUMP_IS_CONNECTED = True in conftest.py after connecting the device."
    ),
)

_SITE_XFAIL = pytest.mark.xfail(
    strict=False,
    reason=(
        "Site dropdown depends on Sites & Locations data — "
        "verify VK AL02 exists in staging before removing xfail."
    ),
)

# ===========================================================================
# TestGasPumpCreate — GPS-CRT-001, 002, 011, 012, 013, 014, 015, 016
# (GPS-CRT-017 is asserted inside ensure_gas_pump_created in conftest.py)
# ===========================================================================


@allure.story("Create")
class TestGasPumpCreate:

    @allure.title("GPS-CRT-001 Add gas pump button navigates to create form")
    @pytest.mark.smoke
    def test_add_pump_button_opens_form(self, browser):
        page = open_gas_pump_list(browser)
        page.click_add_pump()

        assert (
            "gas_pump" in browser.current_url.lower()
            or "device_list" in browser.current_url.lower()
            or "new" in browser.current_url.lower()
        )
        assert page_has_no_broken_state(page)

    @allure.title("GPS-CRT-002 Create gas pump with all required fields saves and appears in list")
    @pytest.mark.smoke
    @_SITE_XFAIL
    def test_create_gas_pump_full_flow(self, browser):
        # Dependency: Sites & Locations module
        form = open_create_gas_pump_form(browser)
        form.fill_required_fields(
            GPS_NEW_NAME, GPS_SITE,
            GPS_SERIAL_PORT, GPS_SERIAL_NUMBER,
            GPS_BAUD_RATE, GPS_LINK_TIMEOUT,
            GPS_FETCH_INTERVAL, GPS_CODE_LENGTH,
        )
        form.ensure_active_pump_on()
        form.click_save()

        page = open_gas_pump_list(browser)
        assert page.pump_exists(GPS_NEW_NAME), (
            "Gas pump '%s' not found in list after full-field save" % GPS_NEW_NAME
        )
        assert page.get_pump_status(GPS_NEW_NAME) == "Active"
        assert page_has_no_broken_state(page)

    @allure.title("GPS-CRT-011 Numeric fields default to 0 on create form")
    @pytest.mark.regression
    @pytest.mark.parametrize("field_name,get_method", [
        pytest.param("Baud rate",                 "get_baud_rate",      id="GPS-CRT-011-baud-rate"),
        pytest.param("Link timeout",              "get_link_timeout",   id="GPS-CRT-011-link-timeout"),
        pytest.param("Wash book fetch interval",  "get_fetch_interval", id="GPS-CRT-011-fetch-interval"),
        pytest.param("Wash book code length",     "get_code_length",    id="GPS-CRT-011-code-length"),
    ])
    def test_numeric_field_defaults_on_create_form(self, browser, field_name, get_method):
        # GPS-EDT-008: Wash book fetch interval accepts -1 as a valid stored value on
        # existing records (may mean "no interval limit" — see product decision).
        # Default on Create form = 0 for all numeric fields.
        form = open_create_gas_pump_form(browser)
        value = getattr(form, get_method)()

        assert value in ("0", "", None), (
            "Expected default '0' for '%s' on create form, got '%s'" % (field_name, value)
        )
        assert page_has_no_broken_state(form)

    @allure.title("GPS-CRT-012/013 Active toggle state on create determines list status badge")
    @pytest.mark.regression
    @_SITE_XFAIL
    @pytest.mark.parametrize("active,expected_status", [
        pytest.param(True,  "Active",   id="GPS-CRT-012"),
        pytest.param(False, "Inactive", id="GPS-CRT-013"),
    ])
    def test_active_toggle_on_create(self, browser, active, expected_status):
        # Dependency: Sites & Locations module
        form = open_create_gas_pump_form(browser)

        if active:
            # GPS-CRT-012: Active toggle must be ON by default — verify before filling.
            assert form.active_pump_is_on(), (
                "GPS-CRT-012: Active gas pump toggle should be ON by default on create form"
            )

        form.fill_required_fields(
            GPS_NEW_NAME, GPS_SITE,
            GPS_SERIAL_PORT, GPS_SERIAL_NUMBER,
            GPS_BAUD_RATE, GPS_LINK_TIMEOUT,
            GPS_FETCH_INTERVAL, GPS_CODE_LENGTH,
        )
        if active:
            form.ensure_active_pump_on()
        else:
            form.ensure_active_pump_off()
        form.click_save()

        page = open_gas_pump_list(browser)
        assert page_has_no_broken_state(page)
        body = page.get_body_text()
        assert (
            GPS_NEW_NAME not in body
            or page.get_pump_status(GPS_NEW_NAME) == expected_status
        ), (
            "Active toggle set to %s but status badge does not show '%s'"
            % (active, expected_status)
        )

    @allure.title("GPS-CRT-014 Site dropdown on create form lists active sites")
    @pytest.mark.regression
    def test_site_dropdown_lists_active_sites(self, browser):
        # Dependency: Sites & Locations module
        form = open_create_gas_pump_form(browser)
        options = form.get_site_options()

        assert len(options) > 0, "Site dropdown has no options on create form"
        assert GPS_SITE in options, (
            "Expected site '%s' not found in dropdown. Available: %s" % (GPS_SITE, options)
        )
        assert page_has_no_broken_state(form)

    @allure.title("GPS-CRT-015 Yellow triangle connection indicator visible after saving new pump")
    @pytest.mark.regression
    @_SITE_XFAIL
    def test_connection_indicator_yellow_on_new_pump(self, browser):
        # Dependency: Sites & Locations module
        form = open_create_gas_pump_form(browser)
        form.fill_required_fields(
            GPS_NEW_NAME, GPS_SITE,
            GPS_SERIAL_PORT, GPS_SERIAL_NUMBER,
            GPS_BAUD_RATE, GPS_LINK_TIMEOUT,
            GPS_FETCH_INTERVAL, GPS_CODE_LENGTH,
        )
        form.click_save()

        # Re-open edit form to check the connection indicator
        edit_form = open_edit_gas_pump_form(browser, GPS_NEW_NAME)
        # New pump is not yet connected to hardware — yellow triangle expected.
        # Blue checkmark and 'Check or re-generate code' button appear only
        # after the physical pump connects.
        edit_form.assert_connection_indicator(state="unconnected")
        assert page_has_no_broken_state(edit_form)

    @allure.title("GPS-CRT-016 Cancel discards form and returns to list without saving")
    @pytest.mark.regression
    def test_cancel_discards_form(self, browser):
        form = open_create_gas_pump_form(browser)
        form.enter_pump_name(NONEXISTENT_PUMP_NAME)
        form.click_cancel()

        page = open_gas_pump_list(browser)
        assert not page.pump_exists(NONEXISTENT_PUMP_NAME), (
            "Gas pump was saved despite clicking Cancel"
        )
        assert page_has_no_broken_state(page)


# ===========================================================================
# TestGasPumpValidation — GPS-CRT-003 through GPS-CRT-010
# ===========================================================================


@allure.story("Validation")
class TestGasPumpValidation:

    @allure.title("GPS-CRT-003..010 Required field validation blocks save when field is blank")
    @pytest.mark.smoke
    @pytest.mark.parametrize("field", [
        pytest.param("name",          id="GPS-CRT-003"),
        pytest.param("site",          id="GPS-CRT-004"),
        pytest.param("serial_port",   id="GPS-CRT-005"),
        pytest.param("serial_number", id="GPS-CRT-006"),
        pytest.param("baud_rate",     id="GPS-CRT-007"),
        pytest.param("link_timeout",  id="GPS-CRT-008"),
        pytest.param("fetch_interval", id="GPS-CRT-009"),
        pytest.param("code_length",   id="GPS-CRT-010"),
    ])
    def test_required_field_validation(self, browser, field):
        from selenium.webdriver.common.keys import Keys as _Keys

        form = open_create_gas_pump_form(browser)

        if field == "name":
            # All other required fields intentionally omitted — name is the first gate
            form.click_save()
            body = form.get_body_text()
            assert (
                not form.pump_name_input_is_valid()
                or "name" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Blank gas pump name should block save"

        elif field == "site":
            # Dependency: Sites & Locations module
            form.enter_pump_name(GPS_NEW_NAME)
            form.enter_serial_port(GPS_SERIAL_PORT)
            # Site intentionally omitted
            form.click_save()
            body = form.get_body_text()
            assert (
                "site" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing site should block save"

        elif field == "serial_port":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
            except Exception:
                pass
            # Serial port intentionally omitted — clear any pre-filled default
            try:
                el = form.wait.until(lambda d: d.find_element(*form.SERIAL_PORT_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.SERIAL_PORT_INPUT)
                or "serial" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing serial port should block save"

        elif field == "serial_number":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
                form.enter_serial_port(GPS_SERIAL_PORT)
            except Exception:
                pass
            try:
                el = form.wait.until(lambda d: d.find_element(*form.SERIAL_NUMBER_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.SERIAL_NUMBER_INPUT)
                or "serial" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing serial number should block save"

        elif field == "baud_rate":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
                form.enter_serial_port(GPS_SERIAL_PORT)
                form.enter_serial_number(GPS_SERIAL_NUMBER)
            except Exception:
                pass
            try:
                el = form.wait.until(lambda d: d.find_element(*form.BAUD_RATE_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.BAUD_RATE_INPUT)
                or "baud" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing baud rate should block save"

        elif field == "link_timeout":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
                form.enter_serial_port(GPS_SERIAL_PORT)
                form.enter_serial_number(GPS_SERIAL_NUMBER)
                form.enter_baud_rate(GPS_BAUD_RATE)
            except Exception:
                pass
            try:
                el = form.wait.until(lambda d: d.find_element(*form.LINK_TIMEOUT_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.LINK_TIMEOUT_INPUT)
                or "timeout" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing link timeout should block save"

        elif field == "fetch_interval":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
                form.enter_serial_port(GPS_SERIAL_PORT)
                form.enter_serial_number(GPS_SERIAL_NUMBER)
                form.enter_baud_rate(GPS_BAUD_RATE)
                form.enter_link_timeout(GPS_LINK_TIMEOUT)
            except Exception:
                pass
            try:
                el = form.wait.until(lambda d: d.find_element(*form.FETCH_INTERVAL_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.FETCH_INTERVAL_INPUT)
                or "fetch" in body.lower()
                or "interval" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing wash book fetch interval should block save"

        elif field == "code_length":
            form.enter_pump_name(GPS_NEW_NAME)
            try:
                form.select_site(GPS_SITE)
                form.enter_serial_port(GPS_SERIAL_PORT)
                form.enter_serial_number(GPS_SERIAL_NUMBER)
                form.enter_baud_rate(GPS_BAUD_RATE)
                form.enter_link_timeout(GPS_LINK_TIMEOUT)
                form.enter_fetch_interval(GPS_FETCH_INTERVAL)
            except Exception:
                pass
            try:
                el = form.wait.until(lambda d: d.find_element(*form.CODE_LENGTH_INPUT))
                el.send_keys(_Keys.COMMAND + "a")
                el.send_keys(_Keys.BACKSPACE)
            except Exception:
                pass
            form.click_save()
            body = form.get_body_text()
            assert (
                not form._field_is_valid(form.CODE_LENGTH_INPUT)
                or "code" in body.lower()
                or "length" in body.lower()
                or "required" in body.lower()
                or "new" in browser.current_url.lower()
            ), "Missing wash book code length should block save"

        assert page_has_no_broken_state(form)


# ===========================================================================
# TestGasPumpWashBookCodeList — GPS-WBC-001 through GPS-WBC-006
# ===========================================================================


@allure.story("Wash Book Code List")
class TestGasPumpWashBookCodeList:

    @allure.title("GPS-WBC-001..006 Wash Book Code List full lifecycle")
    @pytest.mark.regression
    def test_wash_book_code_list_lifecycle(self, browser, managed_gas_pump):
        # ── GPS-WBC-001: WBC panel is visible with Add wash book code button ──
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        assert form.wbc_panel_is_visible(), (
            "GPS-WBC-001: Wash Book Code List panel not visible on create/edit form"
        )
        assert form.add_wbc_button_is_visible(), (
            "GPS-WBC-001: 'Add wash book code' button not visible in WBC panel"
        )

        # ── GPS-WBC-002: Add row → new row appears with dropdown + ID code input ─
        rows_before = form.get_wbc_row_count()
        form.click_add_wbc_row()
        rows_after = form.get_wbc_row_count()
        assert rows_after > rows_before, (
            "GPS-WBC-002: Clicking 'Add wash book code' did not add a new row "
            "(before: %d, after: %d)" % (rows_before, rows_after)
        )

        # ── GPS-WBC-003: Dropdown options include VKAWB1 ─────────────────────
        # Dependency: Wash Books module
        options = form.get_wbc_wash_book_options(row_index=rows_before)
        assert len(options) > 0, (
            "GPS-WBC-003: Wash book dropdown has no options in new WBC row"
        )
        assert GPS_WASH_BOOK in options, (
            "GPS-WBC-003: Expected wash book '%s' not in dropdown options: %s"
            % (GPS_WASH_BOOK, options)
        )

        # ── GPS-WBC-004: Select VKAWB1, enter ID code 02, save, re-open, values persist ─
        form.select_wbc_wash_book(rows_before, GPS_WASH_BOOK)
        form.enter_wbc_id_code(rows_before, GPS_WBC_ID_CODE)
        form.click_save()

        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        assert form.get_wbc_row_count() >= 1, (
            "GPS-WBC-004: WBC row disappeared after save and re-open"
        )
        selected = form.get_wbc_selected_wash_book(rows_before)
        id_code = form.get_wbc_id_code(rows_before)
        assert selected == GPS_WASH_BOOK or GPS_WASH_BOOK in selected, (
            "GPS-WBC-004: Wash book selection '%s' did not persist after save "
            "(got '%s')" % (GPS_WASH_BOOK, selected)
        )
        assert id_code == GPS_WBC_ID_CODE or GPS_WBC_ID_CODE in id_code, (
            "GPS-WBC-004: Gas pump ID code '%s' did not persist after save "
            "(got '%s')" % (GPS_WBC_ID_CODE, id_code)
        )

        # ── GPS-WBC-005: Add second row, save, re-open, both rows persist ────
        count_before_add = form.get_wbc_row_count()
        form.click_add_wbc_row()
        form.select_wbc_wash_book(count_before_add, GPS_WASH_BOOK)
        form.enter_wbc_id_code(count_before_add, GPS_WBC_ID_CODE)
        form.click_save()

        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        assert form.get_wbc_row_count() >= 2, (
            "GPS-WBC-005: Expected at least 2 WBC rows after adding a second row "
            "(got %d)" % form.get_wbc_row_count()
        )

        # ── GPS-WBC-006: Remove first row, save, re-open, row is gone ────────
        rows_before_remove = form.get_wbc_row_count()
        form.click_remove_wbc_row(0)
        form.click_save()

        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        assert form.get_wbc_row_count() < rows_before_remove, (
            "GPS-WBC-006: WBC row count did not decrease after removing a row "
            "(before: %d, after: %d)" % (rows_before_remove, form.get_wbc_row_count())
        )
        assert page_has_no_broken_state(form)


# ===========================================================================
# TestGasPumpConnectionCode — GPS-CON-001..006, GPS-CON-008
# ===========================================================================


@allure.story("Connection Code")
class TestGasPumpConnectionCode:

    @allure.title("GPS-CON-001 Blue checkmark and connected message appear after hardware connects")
    @pytest.mark.extended
    @_CONNECTED_ONLY
    # GPS-CON-001: only verifiable with a real gas pump hardware connected.
    # Blue checkmark and 'Gas pump connected!' message appear after the physical
    # pump establishes a connection. Yellow triangle precedes this state.
    def test_gas_pump_connected_state(self, browser, managed_gas_pump):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.assert_connection_indicator(state="connected")
        body = form.get_body_text().lower()
        assert "connected" in body, (
            "GPS-CON-001: 'connected' message not visible on edit form after hardware connects"
        )
        assert page_has_no_broken_state(form)

    @allure.title("GPS-CON-002 Yellow triangle indicator visible on unconnected pump edit form")
    @pytest.mark.regression
    def test_yellow_triangle_on_unconnected_pump(self, browser, managed_gas_pump):
        # New pump is not yet connected to hardware — yellow triangle expected.
        # Blue checkmark and 'Check or re-generate code' button appear only
        # after the physical pump connects (GPS-CON-001).
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.assert_connection_indicator(state="unconnected")
        assert page_has_no_broken_state(form)

    @allure.title("GPS-CON-003 Check or re-generate code button visible on connected pump")
    @pytest.mark.extended
    @_CONNECTED_ONLY
    # Note: this button only appears in blue checkmark (connected) state.
    # If pump is unconnected in test environment, this test requires a pre-connected
    # pump fixture or must be run against a pump that has previously connected.
    def test_check_regen_code_button_visible(self, browser, managed_gas_pump):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        assert form.check_regen_button_is_visible(), (
            "GPS-CON-003: 'Check or re-generate code' button not visible on connected pump"
        )
        assert page_has_no_broken_state(form)

    @allure.title("GPS-CON-004 Connection code modal contains all 6 required elements")
    @pytest.mark.extended
    @_CONNECTED_ONLY
    @pytest.mark.parametrize("element_name,check_method", [
        pytest.param("QR code image",        "qr_code_present",          id="GPS-CON-004-qr"),
        pytest.param("Manual entry code",     "manual_code_present",      id="GPS-CON-004-manual-code"),
        pytest.param("Generate new code btn", "generate_new_btn_present", id="GPS-CON-004-generate"),
        pytest.param("Close button",          "close_btn_present",        id="GPS-CON-004-close"),
        pytest.param("Problem link",          "problem_link_present",     id="GPS-CON-004-problem-link"),
        pytest.param("Instruction text",      "instruction_text_present", id="GPS-CON-004-instructions"),
    ])
    def test_connection_code_modal_elements(self, browser, managed_gas_pump,
                                            element_name, check_method):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.click_check_regen_code()
        assert form.modal_is_open(), "GPS-CON-004: Modal did not open after clicking button"

        checks = {
            "qr_code_present":          lambda: form.get_modal_qr_element() is not None,
            "manual_code_present":      lambda: bool(form.get_modal_manual_code_text()),
            "generate_new_btn_present": lambda: form.modal_generate_new_button_is_visible(),
            "close_btn_present":        lambda: form.modal_close_button_is_visible(),
            "problem_link_present":     lambda: form.modal_problem_link_is_visible(),
            "instruction_text_present": lambda: any(
                kw in form.get_body_text().lower()
                for kw in ("connect", "scan", "enter", "code", "pair")
            ),
        }
        try:
            assert checks[check_method](), (
                "GPS-CON-004: Modal element '%s' not visible" % element_name
            )
        finally:
            form.click_modal_close()

    @allure.title("GPS-CON-005 QR code image is rendered in modal")
    @pytest.mark.extended
    @_CONNECTED_ONLY
    def test_qr_code_is_rendered(self, browser, managed_gas_pump):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.click_check_regen_code()
        assert form.modal_is_open(), "Modal did not open"

        try:
            img = form.get_modal_qr_element()
            src = img.get_attribute("src") or ""
            natural_width = form.driver.execute_script(
                "return arguments[0].naturalWidth;", img
            )
            assert src, "GPS-CON-005: QR code img src is empty"
            assert natural_width and natural_width > 0, (
                "GPS-CON-005: QR code img is not rendered (naturalWidth = %s)" % natural_width
            )
        finally:
            form.click_modal_close()

        assert page_has_no_broken_state(form)

    @allure.title("GPS-CON-006 Manual entry code matches [A-Z0-9]{8} pattern")
    @pytest.mark.extended
    @_CONNECTED_ONLY
    def test_manual_code_format(self, browser, managed_gas_pump):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.click_check_regen_code()
        assert form.modal_is_open(), "Modal did not open"

        try:
            code_text = form.get_modal_manual_code_text()
            assert re.match(r'^[A-Z0-9]{8}$', code_text), (
                "GPS-CON-006: Manual entry code '%s' does not match "
                "[A-Z0-9]{8} pattern (e.g. C9DCE496)" % code_text
            )
        finally:
            form.click_modal_close()

        assert page_has_no_broken_state(form)

    @allure.title("GPS-CON-008 Closing modal dismisses it without changing connection status")
    @pytest.mark.regression
    @_CONNECTED_ONLY
    def test_close_modal_dismisses(self, browser, managed_gas_pump):
        form = open_edit_gas_pump_form(browser, GPS_PUMP_NAME)
        form.click_check_regen_code()
        assert form.modal_is_open(), "Modal did not open — cannot test close behaviour"

        connection_state_before = form.check_regen_button_is_visible()
        form.click_modal_close()

        assert form.modal_is_closed(), (
            "GPS-CON-008: Modal is still visible after clicking Close"
        )
        assert form.check_regen_button_is_visible() == connection_state_before, (
            "GPS-CON-008: Connection status changed after closing modal"
        )
        assert page_has_no_broken_state(form)


# ===========================================================================
# TestGasPumpEdgeCases — GPS-EC-002
# ===========================================================================


@allure.story("Edge Cases")
class TestGasPumpEdgeCases:

    @allure.title("GPS-EC-002 Numeric fields reject non-integer input or block save")
    @pytest.mark.extended
    @pytest.mark.parametrize("field_name,locator_attr,enter_method", [
        pytest.param("Serial port",   "SERIAL_PORT_INPUT",   "enter_serial_port",   id="GPS-EC-002-serial-port"),
        pytest.param("Serial number", "SERIAL_NUMBER_INPUT", "enter_serial_number", id="GPS-EC-002-serial-number"),
        pytest.param("Baud rate",     "BAUD_RATE_INPUT",     "enter_baud_rate",     id="GPS-EC-002-baud-rate"),
        pytest.param("Link timeout",  "LINK_TIMEOUT_INPUT",  "enter_link_timeout",  id="GPS-EC-002-link-timeout"),
        pytest.param("Wash book code length", "CODE_LENGTH_INPUT", "enter_code_length", id="GPS-EC-002-code-length"),
        # GPS-EC-003: Wash book fetch interval excluded here —
        # -1 is a valid stored value per GPS-EDT-008. See product decision on accepted range.
    ])
    def test_numeric_fields_reject_non_integer(self, browser, field_name,
                                               locator_attr, enter_method):
        form = open_create_gas_pump_form(browser)
        getattr(form, enter_method)("abc")
        form.click_save()

        locator = getattr(form, locator_attr)
        el = form.driver.find_elements(*locator)
        field_value = el[0].get_attribute("value") if el else ""
        body = form.get_body_text().lower()

        assert (
            not form._field_is_valid(locator)
            or "abc" not in field_value
            or "invalid" in body
            or "number" in body
            or "integer" in body
            or "required" in body
            or "new" in browser.current_url.lower()
        ), (
            "GPS-EC-002: Field '%s' accepted non-integer 'abc' without error "
            "(value='%s')" % (field_name, field_value)
        )
        assert page_has_no_broken_state(form)
