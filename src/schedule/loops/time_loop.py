from schedule.loops.loop import Loop
from schedule import timer

FOREVER = 9999999999


class TimeLoop(Loop):
    def __init__(self, count=None):
        super().__init__()
        self.time = count if count else FOREVER
        self.start_time = timer.get_timestamp()
        self.end_time = self.start_time + self.time

    def has_finished(self) -> bool:
        current_time = timer.get_timestamp()
        return False if (self.end_time - current_time) > 0 else True

    def reset_count(self):
        self.start_time = timer.get_timestamp()
        self.end_time = self.start_time + self.time
