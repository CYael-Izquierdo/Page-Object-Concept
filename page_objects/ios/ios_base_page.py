from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import TouchActions
from page_objects.mobile_base_page import MobileBasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException


class IosBasePage(MobileBasePage):
    driver = None

    def __init__(self, driver):
        IosBasePage.driver = driver

    def hide_keyboard(self, key_name=None, key=None, strategy=None):
        keyboard = self.driver.find_element_by_class_name('UIAKeyboard')

        if keyboard.is_displayed():
            self.driver.hide_keyboard(key_name, key, strategy)

    def scroll_down(self):
        self.driver.execute_script('mobile: scroll', {'direction': 'down'})

    def scroll_up(self):
        self.driver.execute_script('mobile: scroll', {'direction': 'up'})
