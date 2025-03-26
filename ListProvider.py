from datetime import datetime, date
from DictUtility import DictUtility


class ListProvider(DictUtility):
    def __init__(self, path: str, delimiter: str):
        super().__init__(path, delimiter, "r")

    def to_dict(self) -> dict:
        data: dict = dict()
        for line in self._dict:
            timestamp = datetime.fromtimestamp(float(line["DATETIME"]))
            date = timestamp.date()

            if line["PESSOA"] not in data:
                data[line["PESSOA"]] = {date: {"I": [], "O": []}}

            if date not in data[line["PESSOA"]]:
                data[line["PESSOA"]][date] = {"I": [], "O": []}

            data[line["PESSOA"]][date][line["TIPO"]].append(timestamp)

        return data

    @staticmethod
    def recursive_show(data, tab=0):
        if type(data) == dict:
            for i, v in data.items():
                print(f"{tab * " "}{"|__" if tab else ""}{i}")
                if v:
                    ListProvider.recursive_show(v, tab + 3)
        elif type(data) == list:
            for i in data:
                print(f"{tab * " "}{i}")

    def show(self):
        ListProvider.recursive_show(self.to_dict())

    def show_day(self, user: str, date_target: date):
        filtred_data = self.to_dict()[user][date_target]
        print("----", date_target, "----")
        ListProvider.recursive_show(filtred_data)

    def all_records(self):
        lines = self._file.readlines()
        for line in lines:
            print(line)
