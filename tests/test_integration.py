import json
import os
from datetime import datetime
from pathlib import Path

import pytest

from elspot import main
from elspot_helper import ERROR

DATA = f"""
 <!doctype html>
 <html lang="sv-SE">
 <body data-cmplz=1>
 <tbody>
                 <tr class="bg-gray-300 hover:bg-gray-100">
             <td class="text-left pt-2 pl-2">{datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
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
                             </tbody>
 </body>
 </html>
 """


class ScraperMock:
    def __init__(self):
        self.cntr = 0

    def get_data(self) -> str:
        if self.cntr:
            raise KeyboardInterrupt

        self.cntr += 1
        return DATA


JSON_FILE = 'nisse.json'
CSV_FILE = 'file.csv'
CONFIG_FILE = 'olle.json'


@pytest.fixture
def configfile(tmpdir):
    filename = f"{str(tmpdir)}/{CONFIG_FILE}"
    with open(filename, 'w') as fh:
        fh.write(json.dumps({'json_filename': JSON_FILE, 'csv_filename': CSV_FILE, 'loglevel': 'FATAL',
                             'log_filename': 'loggen.log', "backoff_start": 5,
                             "backoff_multiple": 2,
                             "backoff_stop": 3600}, indent=4))
    return CONFIG_FILE


def test_main(configfile):
    if (Path.cwd() / JSON_FILE).exists():
        os.remove((Path.cwd() / JSON_FILE).as_posix())
    if (Path.cwd() / CSV_FILE).exists():
        os.remove((Path.cwd() / CSV_FILE).as_posix())

    scraper_mock = ScraperMock()
    rty = main(scraper_mock)
    assert rty == ERROR
    # assert (Path.cwd() / JSON_FILE).exists()
    # assert (Path.cwd() / CSV_FILE).exists()
