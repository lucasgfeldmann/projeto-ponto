from csv import DictReader
from datetime import datetime
import sys


class Utility:
    def __init__(self, path: str, delimiter: str, mode: str):
        self.__path: str = path
        self._file = None
        self.__delimiter: str = delimiter
        self.__mode: str = mode

    def _open(self):
        print("OPEN")
        self._file = open(file=self.__path, mode=self.__mode)

    def _close(self):
        print("CLOSE")
        self._file.close()

    @property
    def get_delimiter(self) -> str:
        return self.__delimiter


class Recorder(Utility):
    """This is a class that makes the records of the data in the CSV"""

    def __init__(self, path: str, delimiter: str, mode: str):
        super().__init__(path, delimiter, mode)

    def registrar(self, type, time, user_name):
        self._open()
        self._file.write(
            f"{type}{self.get_delimiter}"
            f"{time.timestamp()}{self.get_delimiter}"
            f"{user_name}\n"
        )
        self._close()


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
        path="/home/lucas/Projetos/DNosPonto/ponto.csv", delimiter=",", mode="a"
    )
    try:
        tipo = sys.argv[1].upper()  # Primeiro argumento: I (entrada) ou O (saída)

        if tipo == "L":
            list_data()
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
