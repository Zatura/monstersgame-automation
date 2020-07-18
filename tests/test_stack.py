from unittest import TestCase
from src.schedule.stack import Stack


class TestStack(TestCase):
    def test_empty_after_init(self):
        stack = Stack()
        self.assertEqual(len(stack._stack), 0)

    def test_empty_after_pop(self):
        stack = Stack()
        stack.push(lambda: None)
        stack.pop()
        self.assertEqual(len(stack._stack), 0)
        pass

    def test_empty_after_double_pop(self):
        stack = Stack()
        stack.push(lambda: None)
        stack.pop()
        stack.pop()
        self.assertEqual(len(stack._stack), 0)
        pass

    def test_one_item_after_push(self):
        stack = Stack()
        stack.push(lambda: None)
        self.assertEqual(len(stack._stack),  1)
        pass
