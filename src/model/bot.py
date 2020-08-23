from selenium import webdriver
import logging
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auth.credentials import usr, pwd
from model.action import Action
from model.character import Character
from model.navigation import Navigation
from model.storage import Storage
from schedule.timer import sleep_randomized
from datetime import datetime, timezone
import json
import sys

HOUR_IN_SECONDS = 60 * 60
PUNCH_CLOCK = 'data/punch_clock.json'


class Bot:
    def __init__(self, driver=None, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=4141")
        self.driver = driver if driver else webdriver.Chrome(options=options)
        self._storage = Storage()
        self.navigate = Navigation(self.driver)
        self.perform = Action(self.driver, self._storage)
        self.character = None
        self.enemy = None
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S',
                            stream=sys.stdout)
        self.__load_storage_data()

    def __load_storage_data(self):
        try:
            self._storage.download_file(key="data/bounties.json", filename="../../data/bounties.json")
            self._storage.download_file(key="data/punch_clock.json", filename="../../data/punch_clock.json")
        except Exception as e:
            logging.error(e)

    def login(self):
        self.navigate.login_page()
        self.perform.login(usr, pwd)
        self.character = Character(self.driver)
        self.character.load_from_status()
        self.navigate.graveyard_page()

    def train(self):
        self.navigate.training_page()
        self.perform.train_attribute(self.character)

    def use_potion(self):
        self.navigate.status_page()
        self.character.load_from_status()
        self.perform.use_potion()
        self.character.load_from_status()

    def buy_potion(self):
        self.navigate.potion_merchant_page()
        self.perform.buy_potion()

    def restore_vital_energy_above(self, limit):
        try:
            if self.character.vital_energy < limit:
                before = self.character.vital_energy
                self.buy_potion()
                self.use_potion()
                after = self.character.vital_energy
                logging.info("Vital energy restored from {} to {}".format(before, after))
        except Exception as e:
            logging.error(e)

    def work(self, hours):
        self.navigate.graveyard_page()
        self.perform.work(hours)
        self.__save_punch_clock(hours)
        sleep_randomized(hours*3630, 10)
        self.navigate.graveyard_page()

    def hunt_enemies(self):
        while True:
            self.navigate.hunt_page()
            self.perform.hunt_enemies()
            self.enemy = self.__find_enemy()
            can_attack = (self.enemy.agility <= 38) and (self.enemy.resistance <= 38)
            if can_attack:
                self.perform.attack(self.enemy)

    def hunt_humans(self):
        self.navigate.hunt_page()
        self.perform.hunt_humans()
        while True:
            try:
                self.navigate.hunt_page()
                self.perform.repeat_hunt_humans()
            except NoSuchElementException:
                logging.info("Finish hunt")
                break

    def try_hunt_humans(self):
        try:
            self.hunt_humans()
        except NoSuchElementException:
            logging.info("Hunt humans not available")

    def hunt_by_list(self, hunt_list):
        for name in hunt_list:
            try:
                self.navigate.hunt_page()
                self.enemy = self.__find_enemy_by_name(name)
                self.perform.attack(self.enemy)
            except NoSuchElementException:
                logging.info('Could not attack ' + name)
                logging.info('Sleeping ~360 seconds')
                sleep_randomized(300, 60)
                continue
        logging.info("Finish hunt")

    def hunt_by_registry(self, quantity=-1):
        with open('data/bounties.json', "r") as file:
            try:
                enemies = json.load(file)
            except json.decoder.JSONDecodeError:
                logging.info('You have not performed any attack yet')
        hunt_last_time = self.__get_hunt_last_time(enemies)
        elapsed_minutes = int((self.__timestamp() - hunt_last_time) / 60)
        if elapsed_minutes < 15:
            wait_minutes = 15 - elapsed_minutes
            logging.info('You must wait {} minutes to hunt, sleeping...'.format(wait_minutes))
            sleep_randomized(wait_minutes*60, 20)
        enemies = sorted(enemies.items(), key=lambda entry: self.bounty_from_entry(enemies, entry), reverse=True)
        enemies = dict(enemies)

        for index, name in enumerate(enemies):
            try:
                if not quantity:
                    break
                hours = (self.__timestamp() - enemies[name]['timestamp']) / HOUR_IN_SECONDS
                if hours > 12:
                    self.navigate.hunt_page()
                    self.enemy = self.__find_enemy_by_name(name)
                    self.perform.attack(self.enemy)
                else:
                    logging.info('Could not attack {}, last attack was {} hours ago.'.format(name, round(hours, 1)))
                    continue
                quantity -= 1
            except NoSuchElementException:
                logging.info('Could not attack ' + name + ' NoSuchElementException')
                sleep_randomized(5, 5)
                continue
        logging.info("Finish hunt")

    def __get_hunt_last_time(self, enemies):
        enemies = sorted(enemies.items(), key=lambda entry: self.timestamp_from_entry(enemies, entry), reverse=True)
        enemies = dict(enemies)
        entry = next(iter(enemies.values()))
        return entry['timestamp']

    @staticmethod
    def bounty_from_entry(enemies, entry):
        name = entry[0]
        return enemies[name]['bounty']

    @staticmethod
    def timestamp_from_entry(enemies, entry):
        name = entry[0]
        return enemies[name]['timestamp']

    def __find_enemy(self):
        enemy = Character(self.driver)
        while True:
            try:
                enemy.load_from_hunt()
                break
            except NoSuchElementException:
                self.perform.repeat_hunt_enemies()
        return enemy

    def __find_enemy_by_name(self, name):
        self.perform.insert_enemy_name(name)
        enemy = Character(self.driver)
        attempt = 0
        while True:
            try:
                logging.info('Searching for ' + name)
                enemy.load_from_hunt()
                attempt += 1
                break
            except NoSuchElementException:
                self.perform.repeat_hunt_targeted_enemy()
            if attempt > 20:
                raise NoSuchElementException
        return enemy

    def __save_punch_clock(self, hours):
        with open(PUNCH_CLOCK, "a+") as file:
            try:
                file.seek(0)
                entries = json.load(file)
            except json.decoder.JSONDecodeError:
                entries = []
            entry = {}
            timestamp = self.__timestamp()
            entry[timestamp] = hours
            entries.append(entry)
        with open(PUNCH_CLOCK, "w") as file:
            json.dump(entries, file, indent=4)
        self._storage.upload_file(PUNCH_CLOCK)

    @staticmethod
    def __load():
        with open('data/bounties.json', "r") as file:
            enemies = json.load(file)
        return enemies

    @staticmethod
    def __timestamp():
        timestamp = datetime.now(timezone.utc).timestamp()
        return int(timestamp)
