import logging

import pytest

from parser import ElSpotHTMLParser, ElSpotDataError


def test_parser_normal():
    data = """
    <!doctype html>
    <html lang="sv-SE">
    <body data-cmplz=1>
    <tbody>
                    <tr class="bg-gray-300 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 00:00</td>
                                    <td class="text-right pt-2 pr-2">0,08 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-200 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 01:00</td>
                                    <td class="text-right pt-2 pr-2">0,07 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-300 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 02:00</td>
                                    <td class="text-right pt-2 pr-2">0,45 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-200 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 03:00</td>
                                    <td class="text-right pt-2 pr-2">1,15 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-300 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 04:00</td>
                                    <td class="text-right pt-2 pr-2">2,27 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-200 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 05:00</td>
                                    <td class="text-right pt-2 pr-2">8,52 öre/kWh</td>
                                </tr>
                        <tr class="bg-gray-300 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">2022-10-11 06:00</td>
                                    <td class="text-right pt-2 pr-2">12,02 öre/kWh</td>
                                </tr>
                                </tbody>
    </body>
    </html>
    """
    tm = ElSpotHTMLParser(logging)
    tm.feed(data)
    it_all = tm.get_elprices()
    assert isinstance(it_all, dict)


def test_wrong_date():
    wrong_date = """
    <!doctype html>
    <html lang="sv-SE">
    <body data-cmplz=1>
    <tbody>
                    <tr class="bg-gray-300 hover:bg-gray-100">
                <td class="text-left pt-2 pl-2">20223-10-11 00:00</td>
                                    <td class="text-right pt-2 pr-2">0,08 öre/kWh</td>
                                </tr>
                        <
                                </tbody>
    </body>
    </html>
    """
    tm = ElSpotHTMLParser(logging)
    with pytest.raises(ElSpotDataError):
        tm.feed(wrong_date)


def test_wrong_no_date():
    wrong_date = """
    <!doctype html>
    <html lang="sv-SE">
    <body data-cmplz=1>
    <tbody>
                    <tr class="bg-gray-300 hover:bg-gray-100">
                                    <td class="text-right pt-2 pr-2">0,08 öre/kWh</td>
                                </tr>
                        <
                                </tbody>
    </body>
    </html>
    """
    tm = ElSpotHTMLParser(logging)
    with pytest.raises(ElSpotDataError):
        tm.feed(wrong_date)


def test_wrong_price():
    wrong_price = """
        <!doctype html>
        <html lang="sv-SE">
        <body data-cmplz=1>
        <tbody>
                        <tr class="bg-gray-300 hover:bg-gray-100">
                    <td class="text-left pt-2 pl-2">2022-10-11 00:00</td>
                                        <td class="text-right pt-2 pr-2">10000,08 öre/kWh</td>
                                    </tr>
                            <
                                    </tbody>
        </body>
        </html>
        """
    tm = ElSpotHTMLParser(logging)
    with pytest.raises(ElSpotDataError):
        tm.feed(wrong_price)
