from selenium.webdriver import ActionChains
from page_objects.base_page import BasePage
from selenium.webdriver.common.touch_actions import TouchActions


class WebuiBasePage(BasePage):

    def __init__(self, driver):
        super(WebuiBasePage, self).__init__(driver=driver)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<ACTION CHAINS METHODS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    @classmethod
    def click_on_element_by_coordinates(cls, element_coordinates: tuple):
        x_webdriver = element_coordinates[0]
        y_webdriver = element_coordinates[1]
        actions = ActionChains(cls.driver)
        actions.move_by_offset(x_webdriver, y_webdriver)
        actions.click()
        actions.perform()

    @classmethod
    def click_menu(cls, menu):
        actions = ActionChains(cls.driver)
        actions.move_to_element(menu)
        actions.click().perform()

    @classmethod
    def select_submenu(cls, menu, submenu):
        actions = ActionChains(cls.driver)
        actions.move_to_element(menu)
        actions.click(submenu)
        actions.perform()

    @classmethod
    def do_right_click(cls, element):
        actions = ActionChains(cls.driver)
        actions.move_to_element(element)
        actions.context_click(element).perform()

    @classmethod
    def do_double_click(cls, element):
        actions = ActionChains(cls.driver)
        actions.move_to_element(element)
        actions.double_click(element).perform()

    @classmethod
    def do_drag_and_drop(cls, ele_source, ele_target):
        actions = ActionChains(cls.driver)
        actions.drag_and_drop(ele_source, ele_target).perform()

    @classmethod
    def do_click_and_hold(cls, element):
        actions = ActionChains(cls.driver)
        actions.click_and_hold(element).perform()

    @classmethod
    def do_mouseover(cls, *locator):
        """
        Performs mouseover at webelement
        :param locator: Webelement locator
        :return: None
        """
        element = cls.driver.find_element(*locator)
        actions = ActionChains(cls.driver)
        actions.move_to_element(element)
        actions.perform()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>END ACTION CHAINS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    @classmethod
    def scroll_to(cls, web_element):
        ta = TouchActions(cls.driver)
        coords = web_element.location_once_scrolled_into_view
        ta.scroll(coords.get("x"), coords.get("y"))
        ta.perform()

    @classmethod
    def get_browser_on_top(cls):
        """
        Set the browser on top.
        :return: None
        """
        cls.driver.switch_to.window(cls.driver.current_window_handle)
