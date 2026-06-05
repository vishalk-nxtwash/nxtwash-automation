from pages.superadmin.login_page import LoginPage


def test_superadmin_login(browser):

    login_page = LoginPage(browser)

    login_page.open()

    login_page.login()

    login_page.wait_for_url(
        "https://superadmin.nxtwash.com/"
    )

    assert login_page.get_overview_text() == "Overview"