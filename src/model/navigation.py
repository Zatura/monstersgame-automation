import logging

from schedule.timer import sleep_randomized


class Navigation:
    def __init__(self, driver):
        self.driver = driver

    def hunt_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=raubzug")
        logging.info('Navigate hunt page')
        sleep_randomized(2, 3)

    def login_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=loginpage")
        logging.info('Navigate login page')
        sleep_randomized(3, 2)

    def status_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=status")
        logging.info('Navigate status page')
        sleep_randomized(1, 2)

    def training_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=training")
        logging.info('Navigate training page')
        sleep_randomized(0, 2)

    def potion_merchant_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=stadt&sac=warenhaendler&waren=items&"
                        "prod_group=4")
        logging.info('Navigate potion merchant')
        sleep_randomized(0, 2)

    def graveyeard_page(self):
        self.driver.get("http://pt1.monstersgame.moonid.net/index.php?ac=friedhof")
        logging.info('Navigate graveyard')
        sleep_randomized(0, 2)
