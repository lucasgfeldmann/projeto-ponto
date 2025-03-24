from csv import DictReader
from datetime import datetime, date
import sys


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


def list_data():
    with open("/home/lucas/Projetos/DNosPonto/ponto.csv", "r") as file:
        data = DictReader(file)
        anterior = ""
        anterior_tempo = ""
        total_horal = 0
        for i in data:
            data = datetime.fromtimestamp(float(i["DATETIME"]))
            if anterior != data.date():
                if anterior != "":
                    print(
                        f"TOTAL HORAS: {int(total_horal//3600)}h{int(total_horal%3600//60)}m"
                    )
                    total_horal = 0
                print(f"\nDATA: {data.date()}")
            print(f"   {"Entrou" if i["TIPO"] == "I" else "Saiu" }: {data.time()}")
            if i["TIPO"] == "O":
                print(
                    f"      HORAS: {int((data - anterior_tempo).total_seconds()//3600)}h{int((data - anterior_tempo).total_seconds()%3600//60)}m"
                )
                total_horal += int((data - anterior_tempo).total_seconds())

            anterior_tempo = data
            anterior = data.date()
        print(f"TOTAL HORAS: {int(total_horal//3600)}h{int(total_horal%3600//60)}m")
        total_horal = 0


def main():
    registrador: Recorder = Recorder(
        path="/home/lucas/Projetos/DNosPonto/ponto.csv", delimiter=","
    )
    provider: ListProvider = ListProvider(
        path="/home/lucas/Projetos/DNosPonto/ponto.csv", delimiter=","
    )
    try:
        tipo = sys.argv[1].upper()  # Primeiro argumento: I (entrada) ou O (saída)

        if tipo == "L":
            # provider.show()
            provider.show_day("Lucas", date(year=2025, month=3, day=24))
            # list_data()
            return

        horario_str = sys.argv[
            2
        ].upper()  # Segundo argumento: "NOW" ou data/hora manual

        if tipo not in ["I", "O"]:
            print("Erro: Use 'I' para entrada ou 'O' para saída.")
            return

        if horario_str == "NOW":
            horario = datetime.now()
        else:
            horario = datetime.strptime(horario_str, "%Y-%m-%d %H:%M")
        resposta = input(f"Confirma esse horario: {horario}/nDeseja confirmar [Y/N]: ")

        while True:
            if resposta.lower() == "y":
                registrador.registrar(tipo, horario, "Lucas")
                return
            elif resposta.lower() == "n":
                print("Cancelado o registro")
                return
            else:
                print("Resposta Invalida!")
                return

    except (IndexError, ValueError):
        print(
            "Uso correto: python ponto.py I NOW ou python ponto.py O 'YYYY-MM-DD HH:MM'"
        )


if __name__ == "__main__":
    main()
