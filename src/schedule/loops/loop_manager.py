from src.schedule.loops import Loop


class LoopManager:
    def __init__(self):
        self._loops = []
        self._position = -1
        self.current_loop = None

    def add(self, loop: Loop, stack_position: int):
        loop.stack_position = stack_position
        self._loops.append(loop)

    def start_iteration(self):
        self._position += 1
        self.update_current_loop()
        self.current_loop.reset_count()

    def _has_finished(self) -> bool:
        loop = self.current_loop
        return loop.has_finished()

    def _next(self):
        if self._position >= 0:
            self._position -= 1
        self.update_current_loop()

    def update_current_loop(self):
        self.current_loop = self._loops[self._position]

    def check(self):
        if not self._has_finished():
            self.current_loop.increment_count()
            return self.current_loop.stack_position
        else:
            self._next()
            return None
