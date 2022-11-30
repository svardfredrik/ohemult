import logging
from http import HTTPStatus
from urllib.error import URLError
from urllib.request import urlopen

import pytest

from scraper import Scraper, ElSpotCommError


@pytest.mark.skip
def test_scraper():
    xr = Scraper(logging=logging, urler=urlopen(Scraper.URL))
    assert isinstance(xr.get_data(), str)


def test_scraper_okay():
    class Nisse:
        def read(self):
            return 'hello'.encode('utf-8')

        def getcode(self):
            return HTTPStatus.OK

        def close(self):
            ...

    my_urlopen = Nisse()
    xr = Scraper(logging=logging, urler=my_urlopen)
    assert 'hello', xr.get_data()


def test_scraper_status_code_error():
    class Nisse:
        def read(self):
            return 'hello'.encode('utf-8')

        def getcode(self):
            return HTTPStatus.INTERNAL_SERVER_ERROR

        def close(self):
            ...

    my_urlopen = Nisse()

    xr = Scraper(logging=logging, urler=my_urlopen)
    with pytest.raises(ElSpotCommError):
        xr.get_data()


def test_scraper_urlerror():
    class Nisse:
        def read(self):
            raise URLError(reason='Aj')

        def getcode(self):
            return HTTPStatus.OK

        def close(self):
            ...

    my_urlopen = Nisse()

    xr = Scraper(logging=logging, urler=my_urlopen)
    with pytest.raises(URLError):
        xr.get_data()


def test_scraper_urlerror_twice():
    class Nisse:
        def __init__(self):
            self.error = HTTPStatus.INTERNAL_SERVER_ERROR

        def set_code(self, code):
            self.error = code

        def read(self):
            return 'hello'.encode('utf-8')

        def getcode(self):
            return self.error

        def close(self):
            ...

    my_urlopen = Nisse()

    xr = Scraper(logging=logging, urler=my_urlopen)
    with pytest.raises(ElSpotCommError):
        xr.get_data()

    my_urlopen.set_code(HTTPStatus.OK)

    alla = xr.get_data()
    assert alla


def test_scraper_no_encode():
    class Nisse:
        def read(self):
            return 'helloa'

        def getcode(self):
            return HTTPStatus.OK

        def close(self):
            ...

    my_urlopen = Nisse()

    xr = Scraper(logging=logging, urler=my_urlopen)
    with pytest.raises(Exception):
        xr.get_data()
