import json
import logging
import random
import re
from datetime import datetime, timezone
from enum import Enum
from selenium.common.exceptions import NoSuchElementException
from schedule.timer import sleep_randomized

BOUNTIES = 'data/bounties.json'


class Attribute(Enum):
    STRENGTH = "strength"
    DEFENSE = "defense"
    AGILITY = "agility"
    RESISTANCE = "resistance"
    ABILITY = "ability"


class Action:
    def __init__(self, driver, storage):
        self.driver = driver
        self.__storage = storage

    def __input_username(self, username):
        usr_input = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/'
                                                      'table/tbody/tr[2]/td[2]/input')
        usr_input.click()
        usr_input.send_keys(username)

    def __input_password(self, password):
        pwd_input = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/'
                                                      'table/tbody/tr[3]/td[2]/input')
        pwd_input.click()
        pwd_input.send_keys(password)

    def login(self, user, password):
        self.__input_username(user)
        self.__input_password(password)
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/table/'
                                          'tbody/tr[4]/td/input').click()
        logging.info('Login successful')

    def attack(self, enemy):
        try:
            self.__attack_1()
        except NoSuchElementException:
            sleep_randomized(1, 0)
            self.__attack_2()
        finally:
            winner, gold = self.__get_enemy_hunt_result()
            result = "WIN " if winner != enemy.name else "LOST"
            logging.info("Attack  " + result + " Name: " + enemy.name + "  Bounty: " + str(gold))
            if winner != enemy.name:
                self.__save_bounty(enemy.name, gold)

    def __attack_1(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[12]/input').click()
        sleep_randomized(1, 3)

    def __attack_2(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[10]/input').click()
        sleep_randomized(1, 3)

    def __get_enemy_hunt_result(self):
        text = self.driver.find_element_by_xpath('//*[@id="maincontent"]/div[12]/table/tbody/tr[5]/td').text
        pattern = re.compile(r'(?P<winner>(\w| )+) conquistou (?P<gold>\d+)')
        winner = pattern.search(text).group("winner")
        gold = pattern.search(text).group("gold")
        return winner, int(gold)

    def __save_bounty(self, name, bounty):
        with open(BOUNTIES, "a+") as file:
            try:
                file.seek(0)
                enemies = json.load(file)
            except json.decoder.JSONDecodeError:
                enemies = {}
            enemies[name] = {}
            enemies[name]['bounty'] = bounty
            enemies[name]['timestamp'] = self.__timestamp()
        with open(BOUNTIES, "w") as file:
            json.dump(enemies, file, indent=4)
        self.__storage.upload_file(BOUNTIES)

    def train_attribute(self, character):
        attribute = self.__get_attribute_to_train(character)
        try:
            if attribute == Attribute.STRENGTH:
                self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training&typ=staerke")
            if attribute == Attribute.DEFENSE:
                self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training&typ=verteidigung")
            if attribute == Attribute.AGILITY:
                self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training&typ=gewandtheit")
            if attribute == Attribute.RESISTANCE:
                self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training&typ=ausdauer")
            if attribute == Attribute.ABILITY:
                self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training&typ=charisma")
        except NoSuchElementException:
            logging.info("Couldn't train {}, NoSuchElementException".format(attribute))

    def buy_potion(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=stadt&sac=warenhaendler&action=buy&item_id=2&"
                        "prod_group=4&currency=gold&sc=")
        self.driver.find_element_by_xpath('//*[@id="trader_btn"]').click()
        sleep_randomized(1, 2)

    def use_potion(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=status&useitem=2")
        sleep_randomized(1, 2)

    def work(self, hours):
        dropdown = self.driver.find_element_by_xpath('//*[@id="jobler"]/div[4]/p/select')
        selected_hours = dropdown.get_property(str(hours - 1))
        selected_hours.click()
        graves = self.driver.find_element_by_xpath('//*[@id="bonuses"]')
        graves_list = graves.find_elements_by_class_name('w_tooltip')
        size = len(graves.find_elements_by_class_name('w_tooltip'))
        index = random.randint(0, size - 1)
        graves_list[index].click()
        logging.info('Start working {} hours at graveyard'.format(hours))

    def repeat_hunt_enemies(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[4]/input').click()
        sleep_randomized(1, 2)

    def repeat_hunt_targeted_enemy(self):
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form/div[4]/input').click()
        sleep_randomized(0.1, 1)

    def hunt_enemies(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form[3]/div[4]/input').click()
        sleep_randomized(1, 3)

    def insert_enemy_name(self, name):
        name_input = self.driver.find_element_by_xpath('//*[@id="searchthing"]')
        name_input.click()
        name_input.send_keys(name)
        self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form[2]/div[5]/input').click()
        sleep_randomized(2, 3)

    def hunt_humans(self):
        self.driver.find_element_by_xpath('//*[@id="maincontent"]/form[1]/div[5]/table/tbody/tr/td[2]/input').click()
        logging.info("Start hunt")
        sleep_randomized(602, 50)

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

    @staticmethod
    def __get_attribute_to_train(character):
        ratio = character.agility / character.resistance
        if ratio < 1.3:
            return Attribute.AGILITY

        ratio = character.resistance / character.strength
        if ratio < 1.2:
            return Attribute.RESISTANCE

        ratio = character.strength / character.defense
        if ratio < 1.3:
            return Attribute.STRENGTH
        else:
            return Attribute.DEFENSE

    @staticmethod
    def __timestamp():
        timestamp = datetime.now(timezone.utc).timestamp()
        return int(timestamp)
