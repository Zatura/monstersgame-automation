from loops.loop import Loop
import timer


class TimeLoop(Loop):
    def __init__(self, count, stack_position):
        super().__init__()
        self.time = count if count else 315360000
        self.start_time = timer.get_timestamp()
        self.end_time = self.start_time + self.time
        self.position = stack_position

    def has_finished(self):
        current_time = timer.get_timestamp()
        return False if (self.end_time - current_time) > 0 else True

    def reset_count(self):
        self.start_time = timer.get_timestamp()
        self.end_time = self.start_time + self.time
