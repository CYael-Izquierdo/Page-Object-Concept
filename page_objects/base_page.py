from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from lib.appium_page_objects import PageObject
from retry import retry
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.remote.webelement import WebElement


class BasePage(PageObject):

    def __init__(self, driver):
        super(BasePage, self).__init__(webdriver=driver)

    def check_is_mobile_emulation(self):
        """
        Check if the test running is a mobile test (mobileEmulation, Android or iOs Test)
        :return: True if is a mobile test. False otherwise.
        """
        if self.driver.capabilities.get("mobileEmulationEnabled", False) or \
                self.driver.capabilities.get("automationName", {}) in ["UiAutomator2", "XCUITest"]:
            return True
        else:
            return False

    def is_android_test(self):
        if self.driver.capabilities.get("automationName", {}) == "UiAutomator2":
            return True
        else:
            return False

    def is_ios_test(self):
        if self.driver.capabilities.get("automationName", {}) == "XCUITest":
            return True
        else:
            return False

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>COMMON CUSTOM WEBUI INTERACTION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    @classmethod
    def answer_yes_no_question(cls, locator_by: str, locator_xpath: str, answer: str):
        """
        Answers YES/NO question
        :param locator_by:
        :param locator_xpath:
        :param answer: Yes/No
        :return: None
        """
        # first letter to Uppercase
        answer = answer[0].upper() + answer[1::].lower()

        # Adding "//input[@title='Yes']' or //input[@title='No'] at the end of question Xpath
        locator_xpath += "//input[@title='" + answer + "']"
        cls.click_on(locator_by, locator_xpath)

    @classmethod
    def select_on(cls, web_element: WebElement, value_to_select: str):
        """
        Select value from dropdown.
        :param web_element: WebElement reference
        :param value_to_select: Value to be selected
        :return: None
        """
        sel = Select(web_element)
        if value_to_select.lower() not in ["any", "highest"]:
            sel.select_by_visible_text(value_to_select)
        elif value_to_select.lower() == "any":
            sel.select_by_index(1)
        elif value_to_select.lower() == "highest":
            cls.select_highest_dropdown_option(web_element)

    # TODO: Replace locator_by and locator_xpath for locator tuple. eg. (by.XPATH, '//input')
    def write_on(self, locator_by, locator, text_input, time_out=1, verify_element=False):
        """
        Writes into a text field component.
        :param locator_by:
        :param locator:
        :param text_input: Test to be written.
        :param time_out: Maximum amount of time waiting the element's visibility.
        :param verify_element: If it is needed to check element's visibility
        :return:
        """
        if verify_element:
            we = self.is_visible((locator_by, locator), time_out)
        else:
            we = self.driver.find_element(*(locator_by, locator))

        if we:
            if we.is_enabled():
                we.clear()
                we.send_keys(text_input)
                we.send_keys(Keys.ENTER)
                we.send_keys(Keys.TAB)
        else:
            print("Missing: element " + locator + " Was not found")

    # TODO: Replace locator_by and locator_xpath for locator tuple. eg. (by.XPATH, '//input')
    def click_on(self, locator_by: str, locator_xpath: str, time_out=1, verify_element=False):
        """
        Clicks on a clickable component.
        :param locator_by:
        :param locator_xpath:
        :param time_out: Maximum amount of time waiting the element's visibility.
        :param verify_element: If it is needed to check element's visibility.
        :return: True or False
        """
        if verify_element:
            we = self.is_visible((locator_by, locator_xpath), time_out)
        else:
            we = self.driver.find_element(*(locator_by, locator_xpath))

        if we:
            we.click()
            return True
        else:
            print("Missing: element " + locator_xpath + " Was not found")
            return False

    @staticmethod
    def click_check_box(web_element: WebElement, uncheck=False):
        """
        Clicks a checkbox for checking or unchecking.
        If uncheck=False and element is not already checked then check it.
        If uncheck=True and element and element is checked then uncheck it.
        :param web_element:
        :param uncheck:
        :return: None
        """
        if (not web_element.is_selected() and not uncheck) or (web_element.is_selected() and uncheck):
            web_element.click()

    @staticmethod
    def click_check_box_by_name(web_elements: WebElement, checkbox_name: str):
        """

        :param web_elements: a list of checkboxes elements type
        :param checkbox_name: Checkbox visible name to be selected
        :return: None
        """
        for chk in web_elements:
            if chk.get_attribute('value') == checkbox_name:
                chk.click()
                break

    @staticmethod
    def select_option_from_list(web_element_list: list, option):
        """
        Selects/Clicks an option from a list. It could be a Link or Dropdown option.
        :param web_element_list: list of WebElement
        :param option: Option to be selected
        :return: True or Raises an exception
        """
        for we in web_element_list:
            if we.text == option:
                we.click()
                return True

        raise Exception(option + " was not FOUND.")

    @classmethod
    def select_highest_dropdown_option(cls, web_element: WebElement):
        """
        Selects the highest value from a dropdown
        :param web_element:
        :return: None
        """
        excluded_options = ["- Select -", "No Coverage"]
        option_list = cls.get_dropdown_options_list(web_element)

        filtered_list = []
        for o in option_list:
            if o not in excluded_options:
                filtered_list.append(o)

        highest_value = max(filtered_list)

        select = Select(web_element)
        select.select_by_visible_text(highest_value)

    @staticmethod
    def get_dropdown_options_list(web_element: WebElement):
        """
        Returns a list of options from a dropdown
        :param web_element:
        :return: List of dropdown's elements without - Select - option
        """
        excluded_options = ["- Select -", "No Coverage"]
        item_list = []
        for option in web_element.find_elements_by_tag_name("option"):
            if option.text not in excluded_options:
                item_list.append(option.text)

        return item_list

    @classmethod
    def accept_alert(cls, alert_input=None):
        """
        Accepts the JavaScript alert box that is click on the OK button
        :return: None
        """
        alert = cls.__is_alert_present()
        if alert_input:
            alert.send_keys(alert_input)
        alert.accept()

    @classmethod
    def dismiss_alert(cls):
        """
        Dismisses JavaScript alert box that is click on the Cancel button.
        :return: None
        """
        alert = cls.__is_alert_present()
        alert.dismiss()

    @retry(exceptions=Exception, tries=5, delay=2)
    def switch_to_window(self, window="last"):
        """
        Switches to the last window handle by default or to a windows name
        :param window: window handles number or window name
        :return: None
        """
        if window.lower() in ["last"]:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        elif type(window) is str:
            is_window_found = False
            for w in self.driver.window_handles:
                self.driver.switch_to.window(w)
                if self.driver.title.lower() == window.lower():
                    is_window_found = True
                    break
            if not is_window_found:
                raise Exception("Windows " + window + " NOT Found.")
        else:
            raise Exception("Not supported option: " + window + " in switch_to_window() method.")

    def frame_switch(self, css_selector: str):
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector(css_selector))

    def page_has_loaded(self):
        page_ready = False
        i = 0
        while not page_ready:
            i += 1
            print(i)
            page_ready = self.driver.execute_script(
                'return document.readyState;'
            )

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>END - COMMON CUSTOM WEBUI INTERACTION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<WAITS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def wait_for_invisibility_of_element(self, element_locator, waiting_time=1):
        """ An Expectation for checking that an element is either invisible or not present on the DOM.

                element is either a locator (text) or an WebElement
        """
        try:
            return ui.WebDriverWait(self.driver, timeout=waiting_time, poll_frequency=1.5).until(
                EC.invisibility_of_element(element_locator))
        except TimeoutException:
            raise TimeoutException(
                'Timeout waiting for {} invisibility of element: ' + element_locator.format(element_locator[1]))

    def wait_for_element_to_be_present(self, element_locator, waiting_time=1):
        """To wait until the element is present on the current page

        Args:
            driver (selenium.webdriver.): Selenium webdriver to use.
            element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`.
            waiting_time (int): time in seconds - describes how much to wait.

        Raises:
            selenium.common.exceptions.TimeoutException: timeout waiting for element described by ``element_locator``.

        Example:
            ::

                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium_extensions.core import wait_for_element_to_be_present


                driver = webdriver.Chrome()
                ...
                wait_for_element_to_be_present(driver, (By.CLASS_NAME, 'search_load_btn'))
        """
        try:
            return ui.WebDriverWait(self.driver, waiting_time).until(
                EC.presence_of_element_located(element_locator))
        except TimeoutException:
            raise TimeoutException(
                'Timeout waiting for {} presense'.format(element_locator[1]))

    def element_is_present(self, element_locator, waiting_time=1):
        """To check if the element is present on the current page

        Args:
            element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`.
            waiting_time (int): time in seconds - describes how much to wait.

        Returns:
            bool: True if the element is present on the current page, False otherwise.

        Example:
            ::

                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium_extensions.core import element_is_present


                driver = webdriver.Chrome()
                ...
                if not element_is_present(driver, (By.CLASS_NAME, 'search_photos_block')):
                    pass # Do your things here
        """
        try:
            ui.WebDriverWait(self.driver, waiting_time).until(
                EC.presence_of_element_located(element_locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_be_clickable(self, element_locator, waiting_time=2):
        """Waits for element described by `element_locator` to be clickable

        Args:
            element_locator ((selenium.webdriver.common.by.By., str)): element locator described using `By`.
            waiting_time (int): time in seconds - describes how much to wait.

        Raises:
            selenium.common.exceptions.TimeoutException: timeout waiting for element described by ``element_locator``.

        Example:
            ::

                from selenium import webdriver
                from selenium.webdriver.common.by import By
                from selenium_extensions.core import wait_for_element_to_be_clickable


                driver = webdriver.Chrome()
                ...
                wait_for_element_to_be_clickable(driver, (By.CLASS_NAME, 'form-submit-button'))
        """
        try:
            ui.WebDriverWait(self.driver, waiting_time).until(
                EC.element_to_be_clickable(element_locator))
        except TimeoutException:
            raise TimeoutException(
                'Timeout waiting for {} element to be clickable'.format(element_locator[1]))

    def is_present(self, locator: tuple, waiting_time=15):
        try:
            web_element = ui.WebDriverWait(self.driver, waiting_time, 0.5, TimeoutException).until(
                EC.presence_of_element_located((locator[0], locator[1])))

        except (NoSuchElementException, TimeoutException):
            return False

        return web_element

    def is_visible(self, locator_or_we, waiting_time=3, is_locator=True):
        """
        Checks element's visibility
        :param locator_or_we: (by, locator) tuple or webElement
        :param waiting_time: implicit wait for element
        :param is_locator: If it is a locator or webelement.
        :return: WebElement reference if it was found. Otherwise, False.
        """
        if is_locator:
            return self.__is_visible_by_locator(locator=locator_or_we, waiting_time=waiting_time)
        else:
            return self.__is_visible_by_web_element(web_element=locator_or_we, waiting_time=waiting_time)

    def __is_visible_by_locator(self, locator: tuple, waiting_time):
        """
       An expectation for checking that an element is present on the DOM of a page and visible.
       Visibility means that the element is not only displayed but also has a height and width that is greater than 0.
       locator - used to find the element returns the WebElement once it is located and visible
       :param locator:
       :param waiting_time:
       :return: WebElement reference or False
       """
        try:
            web_element = ui.WebDriverWait(self.driver, waiting_time, 1, TimeoutException).until(
                EC.visibility_of_element_located((locator[0], locator[1])))
        except TimeoutException:
            return False

        return web_element

    def __is_visible_by_web_element(self, web_element: WebElement, waiting_time=1):
        try:
            web_element = ui.WebDriverWait(self.driver, waiting_time, 1, TimeoutException). \
                until(EC.visibility_of(web_element))
        except TimeoutException:
            return False

        return web_element

    def __is_alert_present(self):
        """
        Checks if JavaScript alert pop up is present
        :return: None
        """
        try:
            return self.driver.switch_to.alert
        except NoAlertPresentException:
            raise Exception("Alert not Found.")
