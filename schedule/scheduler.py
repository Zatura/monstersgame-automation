from schedule.loops.loop_manager import LoopManager
from schedule.stack import Stack


class Scheduler(Stack):
    def __init__(self):
        super().__init__()
        self.loop_manager = LoopManager()
        self._loops = []

    def begin(self, loop):
        stack_position = len(self._stack)
        self.loop_manager.add(loop, stack_position)
        self.push(lambda: self.loop_manager.start_iteration())

    def end(self):
        self.push(lambda: self.loop_manager.check())
