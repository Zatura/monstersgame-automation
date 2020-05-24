from bot import Bot
from scheduler import Scheduler
from datetime import datetime, timezone
from enemies import known_enemies
import json

bot = Bot()
scheduler = Scheduler()
scheduler.enqueue(bot.login)
scheduler.enqueue(bot._navigate_graveyeard)
scheduler.enqueue(bot.hunt_humans)
scheduler.enqueue(lambda: bot.hunt_by_list(known_enemies))
scheduler.enqueue(bot.hunt_enemies)
scheduler.execute()
