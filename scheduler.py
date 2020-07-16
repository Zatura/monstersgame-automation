from loops.loop_control import LoopManager
from stack import Stack


class Scheduler(Stack):
    def __init__(self):
        super().__init__()
        self.loop_manager = LoopManager()
        self._loops = []

    def begin_loop(self, count=None, time=None):
        stack_position = len(self._stack)
        self.loop_manager.add(count=count, time=time, stack_position=stack_position)
        self.push(lambda: self.loop_manager.start_iteration())

    def end_loop(self):
        self.push(lambda: self.loop_manager.check_loop())
