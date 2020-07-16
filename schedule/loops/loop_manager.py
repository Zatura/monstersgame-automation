from schedule.loops.loop import Loop


class LoopManager:
    def __init__(self):
        self._loops = []
        self._stack_position = -1

    def add(self, loop: Loop, stack_position: int):
        loop.stack_position = stack_position
        self._loops.append(loop)

    def start_iteration(self):
        self._stack_position += 1
        loop = self.current_loop()
        loop.reset_count()

    def _has_finished(self) -> bool:
        loop = self.current_loop()
        return loop.has_finished()

    def _next(self):
        if self._stack_position >= 0:
            self._stack_position -= 1

    def check(self):
        if not self._has_finished():
            loop = self._loops[self._stack_position]
            loop.increment_count()
            self._stack_position = loop.stack_position
        else:
            self._next()
