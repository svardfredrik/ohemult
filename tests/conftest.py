import json
from dataclasses import dataclass

import pytest

from tests.test_elspot_helper import CONFIG_FILE, JSON_FILE, CSV_FILE


@pytest.fixture
def configfile(tmpdir):
    filename = f"{str(tmpdir)}/{CONFIG_FILE}"
    with open(filename, 'w') as fh:
        fh.write(json.dumps({'json_filename': JSON_FILE, 'csv_filename': CSV_FILE, 'loglevel': 'FATAL',
                             'log_filename': 'loggen.log', "backoff_start": 5,
                             "backoff_multiple": 2,
                             "backoff_stop": 3500}, indent=4))
    return CONFIG_FILE


@pytest.fixture()
def config():
    @dataclass
    class Config:
        backoff_start: int = 5
        backoff_multiple: int = 2
        backoff_stop: int = 100

    return Config()


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true",
                     help="run integration tests")


def pytest_runtest_setup(item):
    if 'integration' in item.keywords and not \
            item.config.getvalue("integration"):
        pytest.skip("need --integration option to run")
