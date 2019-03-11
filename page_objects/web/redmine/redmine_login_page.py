from assertpy import assert_that
from selenium.webdriver.common.keys import Keys
from page_elements.redmine.redmine_login_page_elements import RedmineLoginPageElements
from page_objects.web.webui_base_page import WebuiBasePage
from page_objects.android.android_base_page import AndroidBasePage
from page_objects.web.redmine.redmine_homepage_page import RedmineHomePage
import pytest


class RedmineLoginPage(WebuiBasePage, AndroidBasePage, RedmineLoginPageElements):
    end_point = '/login'

    # Define constructor and methods.
    def __init__(self, driver, uri=None):
        super(RedmineLoginPage, self).__init__(driver)
        self.is_mobile = self.check_is_mobile_emulation()
        self.is_android = self.is_android_test()
        self.is_ios = self.is_ios_test()
        if uri:
            self.url = uri
        else:
            self.url = self._get_login_url()
        self._goto_login_page()
        self.homepage_po = RedmineHomePage(self.driver)
        self.wait_for_element_to_be_present(self.txt_user_name_loc, 10)
        assert_that(self.txt_user_name_loc).is_true().described_as("System login page cannot be reached.")

    def _get_login_url(self):
        sut_url = pytest.cfg.get('pytest.environment.redmine').get('sut_url')
        return sut_url + self.end_point

    def _goto_login_page(self):
        self.driver.get(self.url)

    def login(self, username: str = 'admin') -> RedmineHomePage:
        user_name_cred, password_cred = pytest.cfg.get('pytest.environment.redmine').get(username).split("/")
        self.fill_username(user_name_cred)
        self.fill_password(password_cred)
        self.btn_login.submit()
        self.wait_for_invisibility_of_element(element_locator=self.txt_user_name_loc, waiting_time=5)
        return RedmineHomePage(self.driver)

    def fill_username(self, username: str):
        self.txt_user_name = username
        self.txt_user_name = Keys.TAB

    def fill_password(self, password):
        self.txt_password = password
        self.txt_password = Keys.TAB

    def get_login_text(self):
        return self.login_panel.text
