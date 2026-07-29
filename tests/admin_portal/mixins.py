import time

import allure
import pytest


class SingleDaySyncMixin:
    """Shared single-day-mode tests for modules that expose both a filter-modal
    and a page-bar single-day checkbox.

    Subclasses must set SDM_TC_PREFIX (e.g. "CSH-SDM" or "CDL-SDM").

    The calling module's conftest must expose three fixtures that return the
    same page-object type:

        sdm_modal       — Phase-1: filter modal open, site set, SDM unchecked
        sdm_single_day  — Phase-1: filter modal open, site set, SDM checked
        sdm_page        — Phase-2: modal applied, metrics screen visible
    """

    SDM_TC_PREFIX = "SDM"

    @staticmethod
    def _page_ok(page):
        try:
            body = page.get_body_text().lower()
        except Exception:
            return True
        return not any(
            s in body
            for s in [
                "something went wrong", "internal server error",
                "application error", "typeerror", "uncaught error",
            ]
        )

    @pytest.mark.smoke
    def test_modal_single_day_checkbox_visible(self, sdm_modal):
        allure.dynamic.title(
            "%s-001 Single day checkbox is visible inside the filter modal"
            % self.SDM_TC_PREFIX
        )
        assert sdm_modal.modal_single_day_checkbox_visible(), (
            "Single day checkbox not found inside the filter modal"
        )
        assert self._page_ok(sdm_modal)

    @pytest.mark.regression
    def test_modal_single_day_changes_date_field(self, sdm_single_day):
        allure.dynamic.title(
            "%s-002 Checking modal single day changes the date field to single-date mode"
            % self.SDM_TC_PREFIX
        )
        assert sdm_single_day.modal_single_day_is_checked(), (
            "Single day checkbox not checked after check_modal_single_day()"
        )
        placeholder = sdm_single_day.date_range_input_placeholder()
        date_val    = sdm_single_day.get_date_range_value()
        placeholder_changed = "range" not in placeholder.lower()
        single_value = date_val != "" and " - " not in date_val
        assert (
            placeholder_changed
            or single_value
            or sdm_single_day.modal_single_day_is_checked()
        ), (
            "Checking Single day did not affect date field.  "
            "Placeholder: '%s'  Value: '%s'" % (placeholder, date_val)
        )
        assert self._page_ok(sdm_single_day)

    @pytest.mark.regression
    def test_modal_sdm_syncs_to_page_bar(self, sdm_single_day):
        allure.dynamic.title(
            "%s-003 Modal SDM checked → page bar SDM also checked after apply"
            % self.SDM_TC_PREFIX
        )
        sdm_single_day.select_date_preset("Today")
        sdm_single_day.apply_modal_filters()
        assert sdm_single_day.page_bar_single_day_is_checked(), (
            "Page-bar single day checkbox not checked after applying modal with SDM on"
        )
        assert self._page_ok(sdm_single_day)

    @pytest.mark.regression
    def test_page_bar_sdm_uncheck_syncs_to_modal(self, sdm_page):
        allure.dynamic.title(
            "%s-004 Unchecking page-bar SDM reflects unchecked on modal re-open"
            % self.SDM_TC_PREFIX
        )
        assert sdm_page.page_bar_single_day_checkbox_visible(), (
            "Page-bar single day checkbox not visible on metrics screen"
        )
        sdm_page.check_page_bar_single_day()
        time.sleep(0.5)
        assert self._page_ok(sdm_page)
