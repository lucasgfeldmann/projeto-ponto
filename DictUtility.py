from Utility import Utility
from csv import DictReader


class DictUtility(Utility):
    def __init__(self, path: str, delimiter: str, mode: str):
        self._dict = None
        super().__init__(path, delimiter, mode)

    def _open(self):
        super()._open()
        self._dict = DictReader(self._file, delimiter=self.delimiter)

    def _close(self):
        super()._close()
        self._dict = None