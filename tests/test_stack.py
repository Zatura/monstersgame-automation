from unittest import TestCase
from unittest.mock import MagicMock
from src.schedule.stack import Stack


class TestStack(TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_empty_after_init(self):
        self.assertEqual(len(self.stack._stack), 0)

    def test_empty_after_pop(self):
        self.stack.push(lambda: None)
        self.stack.pop()
        self.assertEqual(len(self.stack._stack), 0)
        help(self.setUp)
        pass

    def test_empty_after_double_pop(self):
        self.stack.push(lambda: None)
        self.stack.pop()
        self.stack.pop()
        self.assertEqual(len(self.stack._stack), 0)
        pass

    def test_one_item_after_push(self):
        self.stack.push(lambda: None)
        self.assertEqual(len(self.stack._stack), 1)
        pass

    def test_has_executed(self, mock):
        first_function = MagicMock()
        self.stack.push(lambda: first_function())
        self.stack.execute()
        self.assertEqual(len(self.stack._stack), 1)
        pass
