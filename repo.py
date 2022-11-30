import json
from datetime import datetime, date
from pathlib import Path

from elspot_helper import ElSpotError


class Repo:
    WRITE_TRUNCATE = 'w'

    def __init__(self, logging, json_filename):
        self.filename = json_filename
        self.logging = logging

    @staticmethod
    def _today_date(d: dict) -> bool:
        dates = [d.split()[0] for d in d]
        return any(datetime.now().strftime('%Y-%m-%d') == item for item in dates)

    def save(self, data: dict) -> None:
        if not Repo._today_date(data):
            raise ElSpotError(f'Wrong date: {list(data.keys())[0]}')

        self.logging.info('-- save_to_file ...')
        with open(self.filename, Repo.WRITE_TRUNCATE) as outfile:
            json.dump(data, outfile, indent=2)

    def saved_file_date(self) -> date:
        return datetime.fromtimestamp(int(Path(self.filename).stat().st_ctime)).date() \
            if Path(self.filename).exists() else datetime.fromtimestamp(0).date()
