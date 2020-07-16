from model.bot import Bot
from schedule.loops.time_loop import TimeLoop
from schedule.loops.counter_loop import CounterLoop
from schedule.scheduler import Scheduler

bot = Bot()
scheduler = Scheduler()

scheduler.push(lambda: bot.login())
scheduler.begin(TimeLoop())
scheduler.push(lambda: bot.hunt_humans())
scheduler.begin(CounterLoop(23))
scheduler.push(lambda: bot.hunt_by_registry(1))
scheduler.push(lambda: bot.work(1))
scheduler.end()
scheduler.end()

scheduler.execute()
