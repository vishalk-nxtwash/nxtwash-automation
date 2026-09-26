# Superadmin production smoke suite — shared fixtures.
#
# ALL tests in this directory must be READ-ONLY against the live superadmin app.
# No creates, edits, deletes, deactivations, or "Login To" launches into a real
# company's Admin Portal / POS / Tunnel / CRM.
#
# Superadmin (https://superadmin.nxtwash.com) is a single shared instance —
# config/staging.yaml and config/production.yaml point at the same URL — so
# this suite is the safety net for the one live app that manages both staging
# and production company data. Never filter by or assume a specific
# company/user/role/subscriber exists here; that data changes independently
# of the automation's dedicated staging test fixtures (used by tests/superadmin/).
#
# Run with:
#   pytest tests/prod_smoke/superadmin/ --env production --headless -v
#
# Required env vars for superadmin credentials:
#   SUPERADMIN_USERNAME
#   SUPERADMIN_PASSWORD

import pytest

from pages.superadmin.login_page import LoginPage
from pages.superadmin.sidebar import Sidebar


@pytest.fixture
def superadmin_session(browser):
    """Log in to Superadmin once; return the authenticated browser."""
    login_page = LoginPage(browser)
    login_page.open()
    login_page.login()
    login_page.wait_for_overview()
    return browser


@pytest.fixture
def sidebar(superadmin_session):
    return Sidebar(superadmin_session)
