import logging
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from repo import Repo, ElSpotError


@pytest.fixture
def tmpfile(tmpdir):
    return f'{tmpdir}tmp.json'


def test_repo(tmpfile):
    repo = Repo(logging, tmpfile)
    today = datetime.now().strftime('%Y-%m-%d')
    later = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d')
    data = {
        today: "1.03",
        later: "0.32"
    }

    repo.save(data)
    assert Path(tmpfile).exists()


def test_repo_file_exist(tmpfile):
    repo = Repo(logging, tmpfile)
    today = datetime.now().strftime('%Y-%m-%d')
    later = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d')
    data = {
        today: "1.03",
        later: "0.32"
    }

    repo.save(data)
    assert repo.saved_file_date() == datetime.now().date()


def test_repo_no_file_exist(tmpfile):
    repo = Repo(logging, tmpfile)

    assert repo.saved_file_date() < datetime.now().date()


def test_no_date_today():
    repo = Repo(logging, tmpfile)
    today = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    later = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    data = {
        today: "1.03",
        later: "0.32"
    }
    with pytest.raises(ElSpotError):
        repo.save(data)
