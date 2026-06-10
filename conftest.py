from fixtures.browser import browser
def pytest_addoption(parser):  #here browser will stay open bydefault and 

    parser.addoption(
        "--close-browser",
        action="store_true",
        default=False,
        help="Close browser after test execution"
    )
    parser.addoption(
        "--single-window",
        action="store_true",
        default=False,
        help="Reuse one browser window for grouped screen suites"
    )

#When we want brownser to stay open, currently browser will close upon runnung script
"""
def pytest_addoption(parser):

    parser.addoption(
        "--keep-browser-open",
        action="store_true",
        default=False,
        help="Keep browser open after test execution"
    )
"""
