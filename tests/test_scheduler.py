from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.schedule.loops.counter_loop import CounterLoop
from src.schedule.scheduler import Scheduler


class TestScheduler(TestCase):
    def setUp(self):
        self.mock = Mock()

    def test_iterate_once(self):
        scheduler = Scheduler()
        scheduler.begin(CounterLoop(1))
        scheduler.push(lambda: self.mock.method())
        scheduler.end()
        scheduler.execute()
        self.mock.method.assert_called_once()

    def test_iterate_twice(self):
        scheduler = Scheduler()
        scheduler.begin(CounterLoop(2))
        scheduler.push(lambda: self.mock.method())
        scheduler.end()
        scheduler.execute()
        self.assertEqual(2, self.mock.method.call_count)
