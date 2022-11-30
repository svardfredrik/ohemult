import json
import logging
from datetime import datetime, timedelta, date
from pathlib import Path
from types import SimpleNamespace

WRITE_APPEND = "a"
CONFIG_FILE_NAME = 'elspot_config.json'


class ElSpotError(Exception):
    pass


def read_config(config_filename):
    config_filename = str(Path(__file__).with_name(config_filename))

    if not Path(config_filename).exists():
        raise ElSpotError(f'Could not find config file: {config_filename}')

    with open(config_filename) as fh:
        return json.loads(fh.read(), object_hook=lambda d: SimpleNamespace(**d))


def setup_logger(level, filename):
    logging.basicConfig(filename=filename, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=eval(f'logging.{level}'))

    return logging.getLogger()


def seconds_until_midnight():
    tomorrow = datetime.now() + timedelta(1)
    midnight = datetime(year=tomorrow.year, month=tomorrow.month,
                        day=tomorrow.day, hour=0, minute=0, second=10)
    return int((midnight - datetime.now()).total_seconds())


def save_csv(logger, filename, data: dict) -> None:
    def saved_file_date(fname) -> date:
        return datetime.fromtimestamp(int(Path(fname).stat().st_mtime)).date() if Path(
            fname).exists() else datetime.fromtimestamp(0).date()

    if datetime.now().date() == saved_file_date(filename):
        logger.error(f'-- save_csv: date already saved! {datetime.now().date()}')
        return

    with open(filename, WRITE_APPEND) as fh:
        if not Path(filename).exists():
            fh.write('date time weekday price\n')
        sorted_by_hour = sorted(data.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M"))

        for d in sorted_by_hour:
            the_date, price = d
            weekday = datetime.strptime(the_date, "%Y-%m-%d %H:%M").weekday()
            the_string = f'{the_date} {str(weekday)} ' + price.replace('.', ',') + '\n'
            fh.write(the_string)
