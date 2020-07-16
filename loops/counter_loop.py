from loops.loop import Loop


class CounterLoop(Loop):
    def __init__(self, count, stack_position):
        super().__init__()
        self.start_count = 1
        self.end_count = count
        self.current_count = self.start_count
        self.position = stack_position

    def has_finished(self):
        return False if (self.current_count < self.end_count) else True
        pass

    def increment_count(self):
        self.current_count += 1
        pass

    def reset_count(self):
        self.current_count = self.start_count
