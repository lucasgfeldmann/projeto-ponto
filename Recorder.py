from Utility import Utility


class Recorder(Utility):
    """This is a class that makes the records of the data in the CSV"""

    def __init__(self, path: str, delimiter: str):
        super().__init__(path, delimiter, "a")

    def registrar(self, type, time, user_name):
        self._file.write(
            f"{type}{self.delimiter}"
            f"{time.timestamp()}{self.delimiter}"
            f"{user_name}\n"
        )
        self._close()
