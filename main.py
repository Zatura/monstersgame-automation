from bot import Bot
from scheduler import Scheduler

bot = Bot()
scheduler = Scheduler()

scheduler.enqueue(bot.login)
scheduler.begin_loop()
scheduler.enqueue(bot.hunt_humans)
scheduler.begin_loop(count=23)
scheduler.enqueue(lambda: bot.hunt_by_registry(1))
scheduler.enqueue(lambda: bot.work(1))
scheduler.end_loop()
scheduler.end_loop()

scheduler.execute()
