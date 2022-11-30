from urllib.error import URLError
from urllib.request import urlopen


class ElSpotCommError(Exception):
    pass


class Scraper:
    HTTP_OK = 200
    URL = 'https://elspot.nu/dagens-spotpris/timpriser-pa-elborsen-for-elomrade-se3-stockholm'

    def __init__(self, logging, urler=None):
        self.logging = logging
        self.urler = urler

    def get_data(self) -> str:

        self.logging.info('-- get_elspot data')
        try:
            response = self.urler or urlopen(Scraper.URL)
            if response.getcode() != Scraper.HTTP_OK:
                raise ElSpotCommError(f'Error: did not get a proper reply{response.getcode()}')

        except URLError as e:
            self.logging.error(f'-- get_elspot com failure {str(e)}')
            raise ElSpotCommError('Error: did not get a proper reply') from e

        except Exception as e:
            self.logging.error(f'-- get_elspot unknown error {e}')
            raise e

        body = response.read()
        response.close()
        return body.decode("utf-8")
