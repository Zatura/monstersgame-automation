from loops.loop import Loop


class CountedLoop(Loop):
    def __init__(self, count, queue_position):
        super().__init__()
        self.start_count = 1
        self.end_count = count
        self.current_count = self.start_count
        self.position = queue_position

    def end_loop(self):
        return False if (self.current_count < self.end_count) else True
        pass

    def increment_count(self):
        self.current_count += 1
        pass

    def reset_count(self):
        self.current_count = self.start_count
