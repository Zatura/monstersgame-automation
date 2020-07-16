from time import sleep
from datetime import datetime, timezone
import random


def sleep_randomized(seconds, extra_seconds):
    sleep(seconds)
    sleep(random.randint(0, extra_seconds))


def print_time(text):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(current_time, text)


def get_timestamp():
    timestamp = datetime.now(timezone.utc).timestamp()
    return int(timestamp)
