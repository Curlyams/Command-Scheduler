# models/schedule.py

class Schedule:
    def __init__(self, command: str, interval: int):
        self.command = command
        self.interval = interval

    def get_command(self):
        return self.command

    def get_interval(self):
        return self.interval
