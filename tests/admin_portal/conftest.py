"""Admin Portal suite-wide collection rules."""
import pytest

# Helpers in tests/admin_portal/_managed.py, not record fixtures.
_NOT_RECORDS = {"managed_name", "managed_resource"}


def pytest_collection_modifyitems(config, items):
    """Keep tests that share a managed staging record on ONE xdist worker.

    Each module keeps dedicated records (managed_customer, managed_membership,
    managed_kiosk / managed_kiosk_form, ...) that tests edit and reset. Run on
    different workers at the same time they race: one test sees another's
    edit mid-flight ('auto customer1 edited' != 'auto customer1'). Any test
    using a managed_* fixture joins its module's group (requires --dist
    loadgroup, set in pytest.ini); the module's other tests stay parallel.
    Explicit xdist_group markers win.
    """
    for item in items:
        path = str(item.fspath).replace("\\", "/")
        if "/tests/admin_portal/" not in path or item.get_closest_marker("xdist_group"):
            continue
        uses_managed = any(
            name.startswith("managed_") and name not in _NOT_RECORDS
            for name in getattr(item, "fixturenames", ())
        )
        if uses_managed:
            module = path.split("/tests/admin_portal/")[1].split("/")[0]
            item.add_marker(pytest.mark.xdist_group("admin-managed-%s" % module))
