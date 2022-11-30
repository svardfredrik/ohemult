import logging
import re
from urllib.request import urlopen

import pytest

from parser import ElSpotHTMLParser
from scraper import Scraper


def assert_content(response, mimetype="text/html"):
    msg = "No Content-Type header found"
    assert "Content-Type" in response.headers, msg

    content_type = response.headers["Content-Type"]
    msg = f"Incorrect Content Type set, expected:{mimetype}"
    assert mimetype in content_type, msg

    body = response.read()
    assert len(body) > 1, "Expected content size to be bigger than 1!"


@pytest.mark.integration
def test_elspot_website_any_content():
    response = urlopen(Scraper.URL)
    assert response.getcode() == Scraper.HTTP_OK

    assert_content(response)
    response.close()


def test_elspot_website_compatible():
    response = urlopen(Scraper.URL)
    assert response.getcode() == Scraper.HTTP_OK
    tm = ElSpotHTMLParser(logging)
    body = response.read().decode("utf-8")
    response.close()
    tm.feed(body)
    it_all = tm.get_elprices()
    assert isinstance(it_all, dict)

    dates = it_all.keys()
    prices = it_all.values()
    date_pattern = ElSpotHTMLParser.date_pattern
    prices_pattern = re.compile(r"(-)?(\d{1,4}).(\d{1,4})(.*)")
    result = all(date_pattern.match(the_date) is not None for the_date in dates)
    assert result

    result2 = all(prices_pattern.match(price) is not None for price in prices)
    assert result2
