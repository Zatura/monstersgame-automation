from loops.loop_control import LoopControl


class Scheduler:
    def __init__(self):
        self._queue = []
        self.loop_control = LoopControl()
        self._loops = []
        self._position = 0

    def enqueue(self, action):
        self._queue.append(action)

    def dequeue(self):
        try:
            self._queue.pop()
            self._position -= 1
            self._position = max(0, self._position)
        except IndexError:
            print('Queue is already empty')

    def add_next(self, action):
        self._queue.insert(self._position, action)

    def execute(self):
        while True:
            if self._position < len(self._queue):
                self._queue[self._position]()
                self._position += 1
            else:
                break

    def begin_loop(self, count=None, time=None):
        position = len(self._queue)
        self.loop_control.add(count=count, time=time, queue_position=position)
        self.enqueue(self.loop_control.start_iteration)

    def end_loop(self):
        self.enqueue(self._check_loop)

    def _check_loop(self):
        if not self.loop_control.end_loop():
            loop = self.loop_control.current_loop()
            loop.increment_count()
            self._position = loop.position
        else:
            self.loop_control.next()
