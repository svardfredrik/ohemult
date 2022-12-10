import csv
import json
import logging
from datetime import datetime, timedelta, date
from pathlib import Path
from types import SimpleNamespace

WRITE_APPEND = "a"
CONFIG_FILE_NAME = 'elspot_config.json'


class ElSpotError(Exception):
    pass


# TODO: do it better with Path!!!!

def read_config(config_filename: str) -> SimpleNamespace:
    config_filename = Path(__file__).with_name(config_filename)

    if not config_filename.exists():
        raise ElSpotError(f'Could not find config file: {config_filename}')

    with open(config_filename) as fh:
        return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


def setup_logger(level: str, filename: str) -> logging.Logger:
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval(f'logging.{level}'))

    return logging.getLogger()


def seconds_until_midnight() -> int:
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=10)
    return int((midnight - datetime.now()).total_seconds())


# TODO: Save header only once ...!
def save_csv(logger: logging.Logger, filename: str, data: dict) -> None:
    def saved_file_date(fname: str) -> date:
        return datetime.fromtimestamp(int(Path(fname).stat().st_mtime)).date() if Path(
            fname).exists() else datetime.fromtimestamp(0).date()

    def file_empty(filename: str) -> bool:
        return Path(filename).stat().st_size == 0

    if datetime.now().date() == saved_file_date(filename):
        logger.error(f'-- save_csv: date already saved! {datetime.now().date()}')
        # return

    with open(filename, WRITE_APPEND) as fh:
        hdr = ['date', 'weekday', 'price']
        writer = csv.DictWriter(fh, fieldnames=hdr)
        writer.writeheader()

        for item in data.items():
            the_date, price = item
            weekday = datetime.strptime(the_date, "%Y-%m-%d %H:%M").weekday()
            writer.writerow({'date': the_date, 'weekday': weekday, 'price': price})
