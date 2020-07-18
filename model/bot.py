from selenium import webdriver
import logging
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from auth.credentials import usr, pwd
from model.character import Character
from schedule.timer import sleep_randomized
from datetime import datetime, timezone
import random
import re
import json
import sys


class Bot:
    def __init__(self, driver=None):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=4141")
        self.driver = driver if driver else webdriver.Chrome(options=options)
        self.character = None
        self.enemy = None
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%m-%d-%Y %H:%M:%S',
                            stream=sys.stdout)

    def login(self):
        self._navigate_loginpage()
        self.input_username(usr)
        self.input_password(pwd)
        send_btn = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/input')
        send_btn.click()
        logging.info('Login successful')
        self.character = Character(self.driver)
        self.character.load_from_status()
        self._navigate_graveyeard()

    def _navigate_loginpage(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=loginpage")
        logging.info('Navigate loginpage')
        sleep_randomized(3, 2)

    def _navigate_hunt_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=raubzug")
        logging.info('Navigate huntpage')
        sleep_randomized(2, 3)

    def _navigate_graveyeard(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=friedhof")
        logging.info('Navigate graveyard')
        sleep_randomized(3, 2)

    def work(self, hours):
        self._navigate_graveyeard()
        dropdown = self.driver.find_element_by_xpath('//*[@id="jobler"]/div[4]/p/select')
        property = dropdown.get_property(str(hours - 1))
        property.click()
        graves = self.driver.find_element_by_xpath('//*[@id="bonuses"]')
        graves_list = graves.find_elements_by_class_name('w_tooltip')
        size = len(graves.find_elements_by_class_name('w_tooltip'))
        index = random.randint(0, size - 1)
        graves_list[index].click()
        logging.info('Start working {} hours at graveyard'.format(hours))
        self._save_punch_clock(hours)
        sleep_randomized(hours*3600, 10)
        self._navigate_graveyeard()

    def hunt_enemies(self):
        while True:
            self._navigate_hunt_page()
            self.start_hunt_enemies()
            self.enemy = self.find_enemy()
            can_attack = (self.enemy.agility <= 38) and (self.enemy.resistence <= 38)
            if can_attack:
                self.attack()

    def hunt_humans(self):
        self._navigate_hunt_page()
        self.start_hunt_humans()
        while True:
            try:
                self._navigate_hunt_page()
                self.repeat_hunt_humans()
            except NoSuchElementException:
                logging.info("Finish hunt")
                break

    def hunt_by_list(self, hunt_list):
        for name in hunt_list:
            try:
                self._navigate_hunt_page()
                self.enemy = self.find_enemy_by_name(name)
                self.attack()
            except NoSuchElementException:
                logging.info('Could not attack ' + name)
                logging.info('Sleeping ~360 seconds')
                sleep_randomized(300, 60)
                continue
        logging.info("Finish hunt")

    def hunt_by_registry(self, quantity=None):
        with open('./data/bounties.json', "r") as file:
            try:
                enemies = json.load(file)
            except json.decoder.JSONDecodeError:
                logging.info('You have not performed any attack yet')
        hunt_last_time = self.get_hunt_last_time(enemies)
        elapsed_minutes = int((self._timestamp() - hunt_last_time) / 60)
        if elapsed_minutes < 15:
            wait_minutes = 15 - elapsed_minutes
            logging.info('You must wait {} minutes to hunt, sleeping...'.format(wait_minutes))
            sleep_randomized(wait_minutes*60, 20)
        enemies = sorted(enemies.items(), key=lambda entry: self.bounty_from_entry(enemies, entry), reverse=True)
        enemies = dict(enemies)

        for index, name in enumerate(enemies):
            try:
                if index == quantity:
                    break
                hours = (self._timestamp() - enemies[name]['timestamp'])/60/60
                if hours > 12:
                    self._navigate_hunt_page()
                    self.enemy = self.find_enemy_by_name(name)
                    self.attack()
                else:
                    logging.info('Could not attack ' + name, ', last attack was ', hours, ' ago.')
            except NoSuchElementException:
                logging.info('Could not attack ' + name)
                sleep_randomized(200, 100)
                continue
        logging.info("Finish hunt")

    @staticmethod
    def bounty_from_entry(enemies, entry):
        name = entry[0]
        return enemies[name]['bounty']

    @staticmethod
    def timestamp_from_entry(enemies, entry):
        name = entry[0]
        return enemies[name]['timestamp']

    def get_hunt_last_time(self, enemies):
        enemies = sorted(enemies.items(), key=lambda entry: self.timestamp_from_entry(enemies, entry), reverse=True)
        enemies = dict(enemies)
        entry = next(iter(enemies.values()))
        return entry['timestamp']

    def find_enemy(self):
        enemy = Character(self.driver)
        while True:
            try:
                enemy.load_from_hunt()
                break
            except NoSuchElementException:
                self.repeat_hunt_enemies()
        return enemy

    def attack(self):
        try:
            self._attack_1()
        except NoSuchElementException:
            sleep_randomized(1, 0)
            self._attack_2()
        finally:
            winner, gold = self.get_enemy_hunt_result()
            result = "WIN " if winner != self.enemy.name else "LOST"
            logging.info("Attack  " + result + " Name: " + self.enemy.name + "  Bounty: " + str(gold))
            if winner != self.enemy.name:
                self._save_bounty(self.enemy.name, gold)
            sleep_randomized(902, 60)

    def repeat_hunt_enemies(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[4]/input').click()
        sleep_randomized(1, 2)

    def repeat_hunt_targeted_enemy(self):
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div[4]/input').click()
        sleep_randomized(0.1, 1)

    def start_hunt_enemies(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form[3]/div[4]/input').click()
        sleep_randomized(1, 3)

    def repeat_hunt_humans(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="maincontent"]/div[4]/center/form[1]/input[4]').click()
        except NoSuchElementException:
            try:
                self.driver.find_element_by_xpath('//*[@id="maincontent"]/div[5]/center/form[1]/input[4]').click()
            except NoSuchElementException:
                self.driver.find_element_by_xpath('//*[@id="maincontent"]/div[3]/center/form[1]/input[4]').click()

        logging.info("Repeat hunt")
        sleep_randomized(602, 50)

    def start_hunt_humans(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form[1]/div[5]/table/tbody/tr/td[2]/input').click()
        logging.info("Start hunt")
        sleep_randomized(602, 50)

    def _attack_1(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[12]/input').click()
        sleep_randomized(1, 3)

    def _attack_2(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[10]/input').click()
            sleep_randomized(1, 3)
        except NoSuchElementException:
            raise NoSuchElementException

    def input_username(self, username):
        usr_input = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[2]/input')
        usr_input.click()
        usr_input.send_keys(username)

    def input_password(self, password):
        pwd_input = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[3]/td[2]/input')
        pwd_input.click()
        pwd_input.send_keys(password)

    def get_enemy_hunt_result(self):
        text = self.driver.find_element_by_xpath('//*[@id="maincontent"]/div[12]/table/tbody/tr[5]/td').text
        pattern = re.compile(r'(?P<winner>(\w| )+) conquistou (?P<gold>\d+)')
        winner = pattern.search(text).group("winner")
        gold = pattern.search(text).group("gold")
        return winner, int(gold)

    def find_enemy_by_name(self, name):
        self.insert_enemy_name(name)
        enemy = Character(self.driver)
        attempt = 0
        while True:
            try:
                logging.info('Searching for ' + name)
                enemy.load_from_hunt()
                attempt += 1
                break
            except NoSuchElementException:
                self.repeat_hunt_targeted_enemy()
            if attempt > 20:
                raise NoSuchElementException
        return enemy

    def insert_enemy_name(self, name):
        name_input = self.driver.find_element_by_xpath('//*[@id="searchthing"]')
        name_input.click()
        name_input.send_keys(name)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form[2]/div[5]/input').click()
        sleep_randomized(2, 3)

    def _save_bounty(self, name, bounty):
        with open('../data/bounties.json', "a+") as file:
            try:
                file.seek(0)
                enemies = json.load(file)
            except json.decoder.JSONDecodeError:
                enemies = {}
            enemies[name] = {}
            enemies[name]['bounty'] = bounty
            enemies[name]['timestamp'] = self._timestamp()
        with open('../data/bounties.json', "w") as file:
            json.dump(enemies, file, indent=4)

    def _save_punch_clock(self, hours):
        with open('../data/punch_clock.json', "a+") as file:
            try:
                file.seek(0)
                entries = json.load(file)
            except json.decoder.JSONDecodeError:
                entries = []
            entry = {}
            timestamp = self._timestamp()
            entry[timestamp] = hours
            entries.append(entry)
        with open('../data/punch_clock.json', "w") as file:
            json.dump(entries, file, indent=4)

    @staticmethod
    def _load():
        with open('../data/bounties.json', "r") as file:
            enemies = json.load(file)
        return enemies

    @staticmethod
    def _timestamp():
        timestamp = datetime.now(timezone.utc).timestamp()
        return int(timestamp)
