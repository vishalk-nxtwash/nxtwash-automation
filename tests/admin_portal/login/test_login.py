import allure


pytestmark = [
    allure.epic("Admin Portal"),
    allure.feature("Login"),
    allure.story("Smoke"),
]


def test_admin_login(browser, login_page):

    login_page.login()
    login_page.wait_for_overview()

    assert browser.current_url == login_page.config.get_url(login_page.PORTAL)
    assert login_page.get_overview_text() == "Overview"
