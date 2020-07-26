from unittest import TestCase
from unittest.mock import Mock
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

    def test_empty_after_double_pop(self):
        self.stack.push(lambda: None)
        self.stack.pop()
        self.stack.pop()
        self.assertEqual(len(self.stack._stack), 0)

    def test_one_item_after_push(self):
        self.stack.push(lambda: None)
        self.assertEqual(len(self.stack._stack), 1)

    def test_has_executed(self, mock):
        mock = Mock()
        self.stack.push(lambda: mock.method())
        self.stack.execute()
        mock.method.assert_called_once()
