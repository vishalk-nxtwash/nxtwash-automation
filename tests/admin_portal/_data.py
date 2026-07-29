"""Central loader for test_data/*.json files.

Usage in any module conftest:

    from tests.admin_portal._data import load as _load
    _D = _load("employees")
    EMP_LAST_NAME = _D["template"]["last_name"]
"""
import json
from pathlib import Path

_ROOT = Path(__file__).parents[2]   # tests/admin_portal -> tests -> project root


def load(module_name: str) -> dict:
    path = _ROOT / "test_data" / f"{module_name}.json"
    return json.loads(path.read_text())
