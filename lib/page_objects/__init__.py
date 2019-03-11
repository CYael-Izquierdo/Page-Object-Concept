from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from lib.image_based_testing.image_webdriver_handler import ImageWebdriverHandler
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# from lib.image_based_testing.image_desktop_handler import ImageDesktopHandler


# Map PageElement constructor arguments to webdriver locator enums
_LOCATOR_MAP = {'css': By.CSS_SELECTOR,
                'id_': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'link_text': By.LINK_TEXT,
                'partial_link_text': By.PARTIAL_LINK_TEXT,
                'tag_name': By.TAG_NAME,
                'class_name': By.CLASS_NAME,
                }


class PageObject(object):
    """Page Object pattern.

    :param webdriver: `selenium.webdriver.WebDriver`
        Selenium webdriver instance
    :param root_uri: `str`
        Root URI to base any calls to the ``PageObject.get`` method. If not defined
        in the constructor it will try and look it from the webdriver object.
    """
    def __init__(self, webdriver, root_uri=None):
        self.driver = webdriver
        self.root_uri = root_uri if root_uri else getattr(self.driver, 'root_uri', None)

    def get(self, uri):
        """
        :param uri:  URI to GET, based off of the root_uri attribute.
        """
        root_uri = self.root_uri or ''
        self.driver.get(root_uri + uri)


class PageElement(object):
    # Page Element descriptor.
    #
    # :parameter css:    `str`
    #     Use this css locator
    # :param id_:    `str`
    #     Use this element ID locator
    # :param name:    `str`
    #     Use this element name locator
    # :param xpath:    `str`
    #     Use this xpath locator
    # :param link_text:    `str`
    #     Use this link text locator
    # :param partial_link_text:    `str`
    #     Use this partial link text locator
    # :param tag_name:    `str`
    #     Use this tag name locator
    # :param class_name:    `str`
    #     Use this class locator
    #
    # :param context: `bool`
    #     This element is standard to be called with context
    #
    # Page Elements are used to access elements on a page. The are constructed
    # using this factory method to specify the locator for the element.
    #
    #     # >>> from page_objects import PageObject, PageElement
    #     # >>> class MyPage(PageObject):
    #             elem1 = PageElement(css='div.myclass')
    #             elem2 = PageElement(id_='foo')
    #             elem_with_context = PageElement(name='bar', context=True)
    #
    # Page Elements act as property descriptors for their Page Object, you can get
    # and set them as normal attributes.
    def __init__(self, locator_tuple, context=False):

        self.locator = locator_tuple
        self.has_context = bool(context)

    def find(self, context):
        try:
            return context.find_element(*self.locator)
        except NoSuchElementException:
            return None

    def __get__(self, instance, owner, context=None):
        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            context = instance.driver

        return self.find(context)

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")
        elem.send_keys(value)


class MultiPageElement(PageElement):
    """ Like `PageElement` but returns multiple results.

        # >>> from page_objects import PageObject, MultiPageElement
        # >>> class MyPage(PageObject):
                all_table_rows = MultiPageElement(tag='tr')
                elem2 = PageElement(id_='foo')
                elem_with_context = PageElement(tag='tr', context=True)
    """
    def find(self, context):
        try:
            return context.find_elements(*self.locator)
        except NoSuchElementException:
            return []

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elems = self.__get__(instance, instance.__class__)
        if not elems:
            raise ValueError("Can't set value, no elements found")
        [elem.send_keys(value) for elem in elems]


# Backwards compatibility with previous versions that used factory methods
page_element = PageElement
multi_page_element = MultiPageElement


class ImageWebdriverPageElement(object):
    def __init__(self, locator_tuple, context=False, threshold=0.95):
        self.context = context
        self.threshold = threshold
        self.element_coordinates = None
        self.has_context = bool(context)
        self.locator = locator_tuple
        self.page_image = ImageWebdriverHandler(target_img_path=self.locator[1],
                                                full_img_path=self.locator[2],
                                                threshold=threshold)

    def __get__(self, instance, owner, context=None):
        self.element_coordinates = self.page_image.get_image_occurrence_coordinates(
            target_image_path=self.locator[1],
            full_image_path=self.locator[2],
            window_size=instance.driver.get_window_size())

        if not instance:
            return None

        if not context and self.has_context:
            return lambda ctx: self.__get__(instance, owner, context=ctx)

        if not context:
            self.context = instance.driver

        return self

    def __set__(self, instance, value):
        if self.has_context:
            raise ValueError("Sorry, the set descriptor doesn't support elements with context.")
        elem = self.__get__(instance, instance.__class__)
        if not elem:
            raise ValueError("Can't set value, element not found")

        self.send_keys(value)

    def send_keys(self, value):
        action = ActionChains(self.context)
        action.move_by_offset(self.element_coordinates[0], self.element_coordinates[1])
        action.send_keys(value)
        action.key_down(value=Keys.TAB)
        action.perform()

    def click(self):
        action = ActionChains(self.context)
        action.move_by_offset(self.element_coordinates[0], self.element_coordinates[1])
        action.click()
        action.perform()

    def submit(self):
        action = ActionChains(self.context)
        action.move_by_offset(self.element_coordinates[0], self.element_coordinates[1])
        action.key_down(Keys.ENTER)
        action.perform()


class ImageDesktopPageElement(object):
    def __init__(self, **kwargs):
        self.screenshot_output_folder_path = kwargs.get("desktop_image_path")

        self.threshold = kwargs.get("threshold", 0.99)
        self.locator = kwargs.get("locator")

        self.image_handler = ImageDesktopHandler(target_img_path=self.locator)
        self.method = self.image_handler.get_template_matching_method(kwargs.get("method", None))

    def __get__(self, instance, owner, context=None):
        # FULL DESKTOP
        self.image_handler.grab_screen(path=self.screenshot_output_folder_path)
        self.desktop_img = self.image_handler.get_image(
            image_path=self.screenshot_output_folder_path)

        # TARGET
        self.target_img = self.image_handler.get_image(image_path=self.locator)

        # Target matching result
        result = self.image_handler.find_matching(target_img=self.target_img, full_image=self.desktop_img, method=self.method[1])
        if not self.image_handler.is_image_found(result=result, threshold=self.threshold):
            raise Exception(
                4 * "<" + "[ERROR]" + 4 * "> " + "No matching image found." + "\n" +
                "THRESHOLD: " + str(self.threshold) + "\n" +
                "Template Matching Method: " + self.method[0]
            )

        # # TODO: DELETE WHEN DEVELOPMENT IS DONE
        # self.image_handler.set_result_img_path(self.screenshot_output_folder_path)
        # self.image_handler.find_img_on_screen(target_img_path=self.locator,
        #                                       full_img_path=self.screenshot_output_folder_path,
        #                                       draw_rectangle=True)
        # # END TODO
        return self.image_handler

    def __set__(self, instance, value):
        self.image_handler.keyboard.type_string(value)
        return self.image_handler
