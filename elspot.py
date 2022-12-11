#!/usr/bin/env python
import sys
import time
from datetime import datetime, timedelta

from elspot_helper import ElSpotError, setup_logger, read_config, seconds_until_midnight, save_csv, CONFIG_FILE_NAME, \
    ERROR
from parser import ElSpotHTMLParser, ElSpotDataError
from repo import Repo
from scraper import Scraper, ElSpotCommError
from sleep_controller import SleepController


def main(mock_scraper=None, config_filename=CONFIG_FILE_NAME):
    config = read_config(config_filename=config_filename)
    logger = setup_logger(config.loglevel, config.log_filename)

    if sys.version_info < (3, 7):
        logger.error('Need to be python 3.7 or later ...')
        return ERROR

    scraper = mock_scraper or Scraper(logging=logger)
    sleep_controller = SleepController(config)
    elspot_parser = ElSpotHTMLParser(logger)
    repo = Repo(logger, config.json_filename)
    time_to_sleep = 0
    while True:
        try:
            time_to_sleep: int = sleep_controller.current_backoff()
            data: str = scraper.get_data()
            elspot_parser.feed(data)
            el_prices: dict = elspot_parser.get_elprices()
            repo.save(el_prices)
        except (ElSpotCommError, ElSpotDataError, ElSpotError) as e:
            logger.debug(f'-- failure , will backoff {time_to_sleep} seconds{str(e)}')
            del data

        except KeyboardInterrupt:
            logger.error('-- user killed the script!!...')
            return ERROR

        except Exception as e:
            logger.error(f'-- unknown error {str(e)}')

        if datetime.now().date() <= repo.saved_file_date():
            logger.debug('-- success, file saved')
            time_to_sleep: int = 0 if mock_scraper else seconds_until_midnight()
            sleep_controller.reset()
            save_csv(logger, config.csv_filename, el_prices)

        logger.debug(f'-- will sleep,  {str(timedelta(seconds=time_to_sleep))} hours')
        time.sleep(time_to_sleep)


if __name__ == "__main__":
    sys.exit(main())
