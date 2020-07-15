from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from credentials import usr, pwd
from character import Character
from enemies import known_enemies
from timer import sleep_randomized, print_time
from datetime import datetime, timezone
import re
import json

class Bot():
	def __init__(self, driver=None):
		options = Options()
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--remote-debugging-port=4141")
		self.driver = driver if driver else webdriver.Chrome(options=options)
		self.character = None

	def login(self):
		self._navigate_loginpage()
		self.input_username(usr)
		self.input_password(pwd)
		send_btn = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[2]/table/tbody/tr[2]/td[2]/table/tbody/tr[4]/td/input')
		send_btn.click()
		self.character = Character(self.driver)
		self.character.load_from_status()



	def _navigate_loginpage(self):
		self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=loginpage")
		sleep_randomized(3, 2)

	def _navigate_hunt_page(self):
		self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=raubzug")
		sleep_randomized(2, 3)

	def _navigate_graveyeard(self):
		self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=friedhof")
		sleep_randomized(0, 2)



	def hunt_enemies(self):
		while(True):
			self._navigate_hunt_page()
			self.start_hunt_enemies()
			self.enemy = self.find_enemy()
			can_attack = (self.enemy.agility <= 28) and (self.enemy.resistence <= 28)
			if can_attack:
				self.attack()

	def hunt_humans(self):
		self._navigate_hunt_page()
		self.start_hunt_humans()
		while(True):
			try:
				self._navigate_hunt_page()
				self.repeat_hunt_humans()
			except NoSuchElementException:
				print_time("[ HUNT FINISH ]")
				break

	def hunt_by_list(self, list):
		for item in list:
			self._navigate_hunt_page()
			self.enemy = self.find_enemy_by_name(item)
			self.attack()
		print_time("[ END HUNT ]")

	# def hunt_known_enemies(self):
	# 	enemies = self._load()
	# 	for enemy in enemies:
	# 		a = [{'t':{'a':'1', "b":"2"}}, {'r':{'a':'2', "b":"3"}}]
	# 		a.sort()


		for item in list:
			self._navigate_hunt_page()
			self.enemy = self.find_enemy_by_name(item)
			self.attack()
		print_time("[ END HUNT ]")

	def find_enemy(self):
		enemy = Character(self.driver)
		while(True):
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
			sleep_randomized(1,0)
			self._attack_2()
		finally:
			winner, gold = self.get_enemy_hunt_result()
			result = "WIN " if winner != self.enemy.name else "LOST"
			print_time("[ ATTACK ]  " + result + " Name: " + self.enemy.name + "  Bounty: " + str(gold))
			if winner != self.enemy.name:
				self._save(self.enemy.name, gold)
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

		print_time("[ HUNT ]")
		sleep_randomized(602, 50)

	def start_hunt_humans(self):
		self.driver.find_element_by_xpath('//*[@id="maincontent"]/form[1]/div[5]/table/tbody/tr/td[2]/input').click()
		print_time("[ HUNT ]")
		sleep_randomized(602, 50)

	def _attack_1(self):
		self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[12]/input').click()
		sleep_randomized(1, 3)

	def _attack_2(self):
		try:
			self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[10]/input').click()
			sleep_randomized(1, 3)
		except NoSuchElementException:
			print('ihh')
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
		while(True):
			try:
				enemy.load_from_hunt()
				break
			except NoSuchElementException:
				self.repeat_hunt_targeted_enemy()
		return enemy

	def insert_enemy_name(self, name):
		name_input = self.driver.find_element_by_xpath('//*[@id="searchthing"]')
		name_input.click()
		name_input.send_keys(name)
		self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/form[2]/div[5]/input').click()
		sleep_randomized(2, 3)

	def _save(self, name, bounty):
		with open('data/bounties.json', "r") as file:
		    enemies = json.load(file)
		enemies[name] = {}
		enemies[name]['bounty'] = bounty
		enemies[name]['timestamp'] = self._timestamp()
		with open('data/bounties.json', "w") as file:
			json.dump(enemies, file, indent=4)

	def _load(self):
		with open('data/bounties.json', "r") as file:
		    enemies = json.load(file)
		return enemies

	def _timestamp(self):
		timestamp = datetime.now(timezone.utc).timestamp()
		return int(timestamp)
