from page_objects.base_page import BasePage
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver import TouchActions
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import abc
from lib.appium_page_objects import PageElement, MultiPageElement

class MobileBasePage(BasePage):

    def hide_keyboard(self):
        self.driver.hide_keyboard()

    def get_window_size(self):
        return self.driver.get_window_size()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Switch Between Orientations>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def switch_orientation(self):
        if self.driver.orientation == 'LANDSCAPE':
            self.driver.orientation = 'PORTRAIT'
        elif self.driver.orientation == 'PORTRAIT':
            self.driver.orientation = 'LANDSCAPE'

    def switch_orientation_to_landscape(self):
        self.driver.orientation = 'LANDSCAPE'

    def switch_orientation_to_portrait(self):
        self.driver.orientation = 'PORTRAIT'

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Switch Between Contexts>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def switch_context(self):
        if self.driver.context == 'NATIVE_APP':
            self.switch_context_to_webview()
        elif 'WEBVIEW' in self.driver.context:
            self.switch_context_to_native()

    def switch_context_to_native(self):
        self.driver.switch_to.context('NATIVE_APP')

    def switch_context_to_webview(self):
        webview = self.driver.contexts[1]
        self.driver.switch_to.context(webview)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Touch Actions>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def slide_left(self):
        """
        Slide from right-middle side of the page to left-middle side of the page
        """
        page_size = self.get_window_size()
        x = page_size['width']
        y = page_size['height'] / 2
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=5, y=y).release().perform()

    def slide_left_from(self, element: WebElement = None, from_coord: tuple = None):
        """
        Slide from the given element or coordinates to left side of the page
        :param element: WebElement
        :param from_coord: tuple (x, y)
        """
        actions = TouchAction(self.driver)
        if element:
            element_rect = element.rect
            x_coord = element_rect['x'] + element_rect['width'] / 2
            y_coord = element_rect['y'] + element_rect['height'] / 2
            actions.press(x=x_coord, y=y_coord).wait(1000).move_to(x=0, y=y_coord)
        elif from_coord:
            actions.press(x=from_coord[0], y=from_coord[1]).wait(1000).move_to(x=0, y=from_coord[1])
        else:
            self.slide_left()
        actions.release().perform()

    def slide_right(self):
        """
        Slide from left-middle side of the page to right-middle side of the page
        """
        page_size = self.get_window_size()
        x = 5
        y = page_size['height'] / 2
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=page_size['width'] - 5, y=y).release().perform()

    def slide_right_from(self, element: WebElement = None, from_coord: tuple = None):
        """
        Slide from the given element or coordinates to right side of the page
        :param element: WebElement
        :param from_coord: tuple (x, y)
        """
        page_size = self.get_window_size()
        if element:
            x = element.location['x']
            y = element.location['y']
        elif from_coord:
            x = from_coord[0]
            y = from_coord[1]
        else:
            self.slide_right()
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=page_size['width'] - 5, y=y).release().perform()

    def slide_down(self):
        """
        Slide from up-middle side of the page to right-middle side of the page
        """
        page_size = self.get_window_size()
        x = page_size['width'] / 2
        y = 100
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=x, y=page_size['height'] - 200).release().perform()

    def slide_down_from(self, element: WebElement = None, from_coord: tuple = None):
        """
        Slide from the given element or coordinates to down side of the page
        :param element: WebElement
        :param from_coord: tuple (x, y)
        """
        page_size = self.get_window_size()
        if element:
            x = element.location['x']
            y = element.location['y']
        elif from_coord:
            x = from_coord[0]
            y = from_coord[1]
        else:
            self.slide_down()
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=x, y=page_size['height']).release().perform()

    def slide_up(self):
        """
        Slide from down-middle side of the page to up-middle side of the page
        """
        page_size = self.get_window_size()
        x = page_size['width'] / 2
        y = page_size['height'] - 300
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=x, y=0).release().perform()

    def slide_up_from(self, element: WebElement = None, from_coord: tuple = None):
        """
        Slide from the given element or coordinates to up side of the page
        :param element: WebElement
        :param from_coord: tuple (x, y)
        """
        if element:
            x = element.location['x']
            y = element.location['y']
        elif from_coord:
            x = from_coord[0]
            y = from_coord[1]
        else:
            self.slide_down()
        actions = TouchAction(self.driver)
        actions.press(x=x, y=y).wait(1000).move_to(x=x, y=0).release().perform()

    def slide_from_to(self, first_position: tuple = None, second_position: tuple = None,
                      first_element: WebElement = None, second_element: WebElement = None):
        """
        Slide from given coordinate o
        :param first_position: first touch(x coordinate, y coordinate)
        :param second_position: slide to this coordinate (x coordinate, y coordinate)
        :param first_element: WebElement, first touch in the coordinates of this element
        :param second_element: WebElement, slide to the coordinates of this element
        """

        if first_element:
            first_x = first_element.location['x']
            first_y = first_element.location['y']
        elif first_position:
            first_x = first_position[0]
            first_y = first_position[1]

        if second_element:
            second_x = second_element.location['x']
            second_y = second_element.location['y']
        elif second_position:
            second_x = second_position[0]
            second_y = second_position[1]

        actions = TouchAction(self.driver)
        actions.press(x=first_x, y=first_y).wait(1000).move_to(x=second_x, y=second_y).release().perform()

    @abc.abstractmethod
    def scroll_down(self):
        print('scrolling down')

    def scroll_down_element(self, element: PageElement):
        element_rect = element.rect
        x = element_rect['x'] + element_rect['width'] / 2
        first_y = element_rect['y'] + element_rect['height'] - 10
        second_y = element_rect['y']

        self.slide_from_to((x, first_y), (x, second_y))

    def scroll_down_to(self, locator):
        i = 0
        while i < 12:
            try:
                if self.driver.find_element(locator[0], locator[1]):
                    return PageElement(locator)
            except NoSuchElementException:
                self.scroll_down()
                i += 1
        return None

    @abc.abstractmethod
    def scroll_up(self):
        print('scrolling up')

    def scroll_up_element(self, element: PageElement):
        element_rect = element.rect
        x = element_rect['x'] + element_rect['width'] / 2
        first_y = element_rect['y']
        second_y = element_rect['y'] + element_rect['height']

        self.slide_from_to((x, first_y), (x, second_y))

    def scroll_up_to(self, locator):
        i = 0
        while i < 12:
            try:
                if self.driver.find_element(locator[0], locator[1]):
                    return PageElement(locator)
            except NoSuchElementException:
                self.scroll_up()
        return None

    def double_tap_element(self, element: WebElement):
        actions = TouchActions(self.driver)
        actions.double_tap(element)

    def tap_element(self, element: WebElement):
        actions = TouchActions(self.driver)
        actions.tap(element)

    def tap_and_hold_element(self, element: WebElement):
        actions = TouchActions(self.driver)
        actions.tap_and_hold(element.location['x'], element.location['y'])
