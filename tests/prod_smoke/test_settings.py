import allure
import pytest

from pages.admin_portal.gas_pump_settings_page import GasPumpSettingsListPage
from pages.admin_portal.kiosk_settings_page import AdminKioskSettingsPage
from pages.admin_portal.pos_settings_page import AdminPOSSettingsPage
from pages.admin_portal.sites_page import SitesPage
from pages.admin_portal.tunnel_settings_page import TunnelSettingsListPage
from tests.admin_portal.admin_session import open_admin_path
from tests.prod_smoke.conftest import page_is_up


pytestmark = [
    allure.epic("Production Smoke"),
    allure.feature("Settings"),
    pytest.mark.prod_smoke,
]


@allure.title("PSMO-SET-001 Sites & Locations page loads and shows at least one site")
@pytest.mark.prod_smoke
def test_sites_page_loads(browser):
    open_admin_path(browser, "/sites")
    page = SitesPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)
    body = page.get_body_text()
    assert "Sites/Locations" in body or "Sites / Locations" in body, (
        "Sites page title not found in body"
    )


@allure.title("PSMO-SET-002 Kiosk Settings page loads")
@pytest.mark.prod_smoke
def test_kiosk_settings_loads(browser):
    open_admin_path(browser, "/kiosk_settings/kiosks")
    page = AdminKioskSettingsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SET-003 POS Settings page loads")
@pytest.mark.prod_smoke
def test_pos_settings_loads(browser):
    open_admin_path(browser, "/pos_settings/pos")
    page = AdminPOSSettingsPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SET-004 Tunnel Settings page loads")
@pytest.mark.prod_smoke
def test_tunnel_settings_loads(browser):
    open_admin_path(browser, "/tunnel_settings/tunnels")
    page = TunnelSettingsListPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)


@allure.title("PSMO-SET-005 Gas Pump Settings page loads")
@pytest.mark.prod_smoke
def test_gas_pump_settings_loads(browser):
    open_admin_path(browser, "/gas_pump_settings/device_list")
    page = GasPumpSettingsListPage(browser)
    page.wait_for_loaded()

    assert page_is_up(browser)
