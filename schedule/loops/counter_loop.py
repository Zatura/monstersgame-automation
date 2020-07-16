from schedule.loops.loop import Loop


class CounterLoop(Loop):
    def __init__(self, count: int):
        super().__init__()
        self.start_count = 1
        self.end_count = count
        self.current_count = self.start_count

    def has_finished(self) -> bool:
        return False if (self.current_count < self.end_count) else True

    def increment_count(self):
        self.current_count += 1

    def reset_count(self):
        if __name__ == '__main__':
            self.current_count = self.start_count
