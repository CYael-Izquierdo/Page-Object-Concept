from retry import retry
from selenium.common.exceptions import WebDriverException
from page_objects.mobile_base_page import MobileBasePage


class AndroidBasePage(MobileBasePage):

    FIND_STRATEGY = "by_android_uiautomator"
    driver = None

    def __init__(self, driver):
        super(AndroidBasePage, self).__init__(driver=driver)
        AndroidBasePage.driver = driver

    @classmethod
    def click_on(cls, locator, strategy=FIND_STRATEGY):
        if strategy == cls.FIND_STRATEGY:
            cls.driver.find_element_by_android_uiautomator(locator).click()
        else:
            raise Exception("Finder Strategy not implemented: " + strategy)

    @classmethod
    def get_text(cls, locator):
        return cls.driver.find_element_by_android_uiautomator(locator).text

    @classmethod
    @retry(exceptions=WebDriverException)
    def swipe_until_find_element(cls, element_locator, funct=None):
        attempts = 10
        while True:
            cls.driver.switch_to.context("NATIVE_APP")
            cls.driver.swipe(100, 700, 100, 500)
            cls.driver.switch_to.context("CHROMIUM")
            web_element = MobileBasePage.is_visible(locator_or_we=element_locator, waiting_time=1)

            if web_element:
                break
            else:
                attempts -= 1
                if attempts == 0:
                    raise Exception(4 * "<" + "[ERROR]" + 4 * ">" +
                                    "MAX attempts reached on " + "swipe_until_find_element method." +
                                    "\n")
        if funct:
            f = getattr(web_element, funct)
            f()

    def scroll_down(self):
        self.slide_up()

    def scroll_up(self):
        self.slide_down()
