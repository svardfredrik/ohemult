import re
from html.parser import HTMLParser


class ElSpotDataError(Exception):
    pass


class ElSpotHTMLParser(HTMLParser):
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    price_pattern = re.compile(r"(-)?(\d{1,4}),(\d{1,4})(.*)")

    def __init__(self, logging):
        HTMLParser.__init__(self)
        self.logging = logging
        self._recording = False
        self._all = {}
        self._time = None

    @staticmethod
    def _td_tag(tag) -> bool:
        return tag == 'td'

    @staticmethod
    def _is_date(data) -> bool:
        return ElSpotHTMLParser.date_pattern.match(data) is not None

    @staticmethod
    def _is_price(data) -> bool:
        return ElSpotHTMLParser.price_pattern.match(data) is not None

    def handle_starttag(self, tag, attrs):
        self._recording = self._td_tag(tag)

    def handle_endtag(self, tag):
        self._recording = not self._td_tag(tag) and self._recording

    def handle_data(self, data):
        if not self._recording:
            return
        if self._is_date(data):
            self._time = data
            return

        if self._is_price(data):
            if self._time is None:
                raise ElSpotDataError('-- Error timestamp not included in data!!')

            self._all[self._time] = data.split()[0].replace(',', '.')
            self._time = None
            return

        self.logging.error('-- Error some problem with the data!')
        raise ElSpotDataError(f'Error, some problem with data: {str(data)}')

    def get_elprices(self) -> dict:
        if not self._all:
            raise ElSpotDataError('Error, no data was parsed!')

        interim, self._all = self._all, {}
        return interim
