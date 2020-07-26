from src.schedule.loops.loop_manager import LoopManager
from src.schedule.loops.loop import Loop
from src.schedule.stack import Stack


class Scheduler(Stack):
    def __init__(self):
        super().__init__()
        self.loop_manager = LoopManager()

    def begin(self, loop: Loop):
        stack_position = len(self._stack)
        self.loop_manager.add(loop, stack_position)
        self.push(lambda: self.loop_manager.start_iteration())

    def end(self):
        self.push(lambda: self.loop_check())

    def loop_check(self):
        position = self.loop_manager.check()
        if position:
            self._position = position

