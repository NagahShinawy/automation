from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from log import logger


class BrowserAutomation:
    url = 'http://automationpractice.com/index.php?controller=authentication&back=my-account'

    def __init__(self):
        # print('*' * 30, 'Starting Driver', '*' * 30)
        logger.debug('Starting Driver')
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        self.driver.set_window_position(400, 0)
        self.driver.set_window_size(1024, 768)  # screen resolution
        self.wait = WebDriverWait(driver=self.driver, timeout=15)
        time.sleep(.5)
        self.driver.execute_script("window.scrollTo(0, 100)")  # scroll down little bit

        # print('*' * 30, 'Finishing driver', '*' * 30)
        logger.debug('Finishing Driver')


