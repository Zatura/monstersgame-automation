class Stack:
    def __init__(self):
        self._stack = []
        self._position = 0

    def push(self, action):
        self._stack.append(action)

    def pop(self):
        try:
            self._stack.pop()
            self._position -= 1
            self._position = max(0, self._position)
        except IndexError:
            print('Queue is already empty')

    def execute(self):
        while True:
            if self._position < len(self._stack):
                self._stack[self._position]()
                self._position += 1
            else:
                break
