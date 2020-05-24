class Scheduler():
    def __init__(self):
        self._queue = []
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
