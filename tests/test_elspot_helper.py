import logging
import time
from pathlib import Path

import pytest

from elspot_helper import seconds_until_midnight, save_csv, read_config, CONFIG_FILE_NAME, ElSpotError

JSON_FILE = 'nisse.json'
CSV_FILE = 'file.csv'
CONFIG_FILE = 'olle.json'


@pytest.fixture
def tempfile(tmpdir):
    return f'{tmpdir}nisse.csv'


def test_config_normal(configfile):
    mr = read_config(CONFIG_FILE_NAME)
    assert mr.loglevel == "DEBUG"


def test_config_no_config_file():
    with pytest.raises(ElSpotError):
        read_config('dummy.json')


def test_midnight():
    first = seconds_until_midnight()
    time.sleep(1)
    second = seconds_until_midnight()
    assert first > second


# TODO: Use a tempfile or file object. Veridy file content??
# check saved only once a day.
# check of sorted on time!
def test_save_csv(tempfile):
    save_csv(logger=logging, filename=tempfile, data={"2022-11-11 06:00": "0.90"})
    assert Path(tempfile).exists()
