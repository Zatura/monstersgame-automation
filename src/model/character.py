import re
from selenium.common.exceptions import NoSuchElementException


class Character():
    def __init__(self, driver):
        self.strength = 0
        self.defense = 0
        self.agility = 0
        self.resistance = 0
        self.ability = 0
        self.vital_energy = 0
        self.attr_mean = 0
        self.driver = driver
        self.name = ""

    def load_from_status(self):
        try:
            self._load_from_status1()
        except NoSuchElementException:
            self._load_from_status2()

    def _load_from_status1(self):
        self.strength = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[2]/td[2]')
        self.defense = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[3]/td[2]')
        self.agility = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[4]/td[2]')
        self.resistance = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[5]/td[2]')
        self.ability = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[6]/td[2]')
        self.experience = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[6]/td[2]')
        # self.vital_energy = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[7]/td[2]')
        self.attr_mean = (self.strength + self.defense + self.agility + self.resistance) / 4

    def _load_from_status2(self):
        self.strength = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[2]/td[2]')
        self.defense = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[3]/td[2]')
        self.agility = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[4]/td[2]')
        self.resistance = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[5]/td[2]')
        self.ability = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[6]/td[2]')
        self.experience = self._number_from_xpath('//*[@id="maincontent"]/div[10]/table/tbody/tr[6]/td[2]')
        # self.vital_energy = self._number_from_xpath('//*[@id="maincontent"]/div[8]/table/tbody/tr[7]/td[2]')
        self.attr_mean = (self.strength + self.defense + self.agility + self.resistance) / 4

    def load_from_hunt(self):
        try:
            self._load_from_hunt_1()
        except NoSuchElementException:
            self._load_from_hunt_2()

    def _load_from_hunt_1(self):
        text = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[8]').text
        pattern = re.compile(r'As propriedades de (?P<name>([ -~])+):')
        search = pattern.search(text)
        if not search:
            raise NoSuchElementException
        self.name = search.group("name")
        self.strength = self._number_from_xpath('//*[@id="maincontent"]/form/div[9]/table/tbody/tr[2]/td[2]')
        self.defense = self._number_from_xpath('//*[@id="maincontent"]/form/div[9]/table/tbody/tr[3]/td[2]')
        self.agility = self._number_from_xpath('//*[@id="maincontent"]/form/div[9]/table/tbody/tr[4]/td[2]')
        self.resistance = self._number_from_xpath('//*[@id="maincontent"]/form/div[9]/table/tbody/tr[5]/td[2]')
        self.ability = self._number_from_xpath('//*[@id="maincontent"]/form/div[9]/table/tbody/tr[6]/td[2]')
        self.attr_mean = (self.strength + self.defense + self.agility + self.resistance) / 4

    def _load_from_hunt_2(self):
        text = self.driver.find_element_by_xpath('//*[@id="maincontent"]/form/div[10]').text
        if not text:
            raise NoSuchElementException
        pattern = re.compile(r'As propriedades de (?P<name>([ -~])+):')
        search = pattern.search(text)
        if not search:
            raise NoSuchElementException
        self.name = search.group("name")
        self.strength = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[2]/td[2]')
        self.defense = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[3]/td[2]')
        self.agility = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[4]/td[2]')
        self.resistance = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[5]/td[2]')
        self.ability = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[6]/td[2]')
        self.attr_mean = (self.strength + self.defense + self.agility + self.resistance) / 4
        # self.experience = self._number_from_xpath('//*[@id="maincontent"]/form/div[11]/table/tbody/tr[7]/td[2]')

    def _number_from_xpath(self, xpath):
        pattern = re.compile(r'\((?P<number>\w+)\)')
        element = self.driver.find_element_by_xpath(xpath)
        number = pattern.search(element.text).group("number")
        return int(number)
