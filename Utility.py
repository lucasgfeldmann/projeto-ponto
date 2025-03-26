class Utility:
    def __init__(self, path: str, delimiter: str, mode: str):
        self.__path: str = path
        self._file = None
        self.__delimiter: str = delimiter
        self.__mode: str = mode

        self._open()

    def _open(self):
        self._file = open(file=self.__path, mode=self.__mode)

    def _close(self):
        self._file.close()

    @property
    def delimiter(self) -> str:
        return self.__delimiter
