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
scheduler.push(lambda: bot.restore_vital_energy_above(25))
scheduler.push(lambda: bot.train())
scheduler.end()

scheduler.execute()
