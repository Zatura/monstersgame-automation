from model.bot import Bot
from schedule.loops.time_loop import TimeLoop
from schedule.scheduler import Scheduler

bot = Bot()
scheduler = Scheduler()

scheduler.push(lambda: bot.login())
scheduler.begin(TimeLoop())
scheduler.push(lambda: bot.try_hunt_humans())
scheduler.push(lambda: bot.hunt_by_registry(1))
scheduler.push(lambda: bot.work(1))
scheduler.push(lambda: bot.login())
scheduler.end()

scheduler.execute()
