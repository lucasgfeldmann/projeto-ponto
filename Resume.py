from datetime import datetime, date, timedelta


class Resume:
    def __init__(self, data: dict, user: str):
        self.data: dict = data
        self.user: str = user

    @staticmethod
    def date_now() -> date:
        return datetime.now().date()

    def today(self) -> timedelta | None:
        today_data = self.data[self.user][Resume.date_now()]

        if len(today_data["I"]) == 0:
            return None

        last_entry: datetime = today_data["I"][-1]
        if len(today_data["O"]) == 0:
            return datetime.now() - last_entry

        last_out: datetime = today_data["O"][-1]

        diff = last_out - last_entry

        if diff < timedelta(0):
            return datetime.now() - last_entry

        return diff
