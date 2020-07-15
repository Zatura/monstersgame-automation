from loops.loop import Loop
from loops.counted_loop import CountedLoop
from loops.timed_loop import TimedLoop


class LoopControl:
    def __init__(self):
        self._loops = []
        self._position = -1

    def add(self, count=None, time=None, queue_position=None):
        loop = CountedLoop(count, queue_position) if count else TimedLoop(time, queue_position)
        self._loops.append(loop)

    def start_iteration(self):
        self._position += 1
        loop = self.current_loop()
        loop.reset_count()

    def end_loop(self):
        loop = self.current_loop()
        return loop.end_loop()

    def current_loop(self) -> Loop:
        return self._loops[self._position]

    def next(self):
        if self._position >= 0:
            self._position -= 1
