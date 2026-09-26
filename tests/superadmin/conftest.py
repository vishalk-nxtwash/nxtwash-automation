import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--seed",
        action="store_true",
        default=False,
        help="Run @pytest.mark.seed tests to create initial staging test data. "
             "Omit on normal runs — seed tests are skipped by default.",
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--seed"):
        skip = pytest.mark.skip(
            reason="Seed test — staging data already exists. Re-run with --seed to re-initialize."
        )
        for item in items:
            if "seed" in item.keywords:
                item.add_marker(skip)
