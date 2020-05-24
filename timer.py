from time import sleep
from datetime import datetime
import random

extra_seconds = 10
def sleep_randomized(seconds, extra_seconds):
    sleep(seconds)
    sleep(random.randint(0, extra_seconds))

def print_time(text):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(current_time, text)
