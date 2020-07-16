from bot import Bot
from scheduler import Scheduler

bot = Bot()
scheduler = Scheduler()

scheduler.push(lambda: bot.login())
scheduler.begin_loop()
scheduler.push(lambda: bot.hunt_humans())
scheduler.begin_loop(count=23)
scheduler.push(lambda: bot.hunt_by_registry(1))
scheduler.push(lambda: bot.work(1))
scheduler.end_loop()
scheduler.end_loop()

scheduler.execute()
