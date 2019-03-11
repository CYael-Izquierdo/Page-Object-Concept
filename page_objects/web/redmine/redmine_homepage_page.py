from page_objects.web.webui_base_page import WebuiBasePage
from page_elements.redmine.redmine_homepage_page_element import RedmineHomepagePageElements
from page_objects.android.android_base_page import AndroidBasePage


class RedmineHomePage(WebuiBasePage, AndroidBasePage, RedmineHomepagePageElements):

    def __init__(self, driver, uri=None):
        super(RedmineHomePage, self).__init__(driver)
        if uri is not None:
            self.uri = uri
            self.driver.get(uri)
        self.wait_for_element_to_be_clickable(element_locator=self.menu_projects_loc,
                                              waiting_time=10)

    def click_on_link(self, option: str):
        if option.lower() == "administration":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_administration_loc,
                                                  waiting_time=10)
            self.menu_administration.click()
        elif option.lower() == "help":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_help_loc,
                                                  waiting_time=10)
            self.menu_help.click()
        elif option.lower() == "home":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_home_loc,
                                                  waiting_time=10)
            self.menu_home.click()
        elif option.lower() == "logout":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_logout_loc,
                                                  waiting_time=10)
            self.menu_logout.click()
        elif option.lower() == "my account":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_my_account_loc,
                                                  waiting_time=10)
            self.menu_my_account.click()
        elif option.lower() == "my page":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_my_page_loc,
                                                  waiting_time=10)
            self.menu_my_page.click()
        elif option.lower() == "projects":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_projects_loc,
                                                  waiting_time=10)
            self.menu_projects.click()

        elif option.lower() == "register":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_register_loc,
                                                  waiting_time=10)
            self.menu_register.click()
        elif option.lower() == "sign in":
            self.wait_for_element_to_be_clickable(element_locator=self.menu_sign_in_loc,
                                                  waiting_time=10)
            self.menu_sign_in.click()

    def get_logged_user_label(self):
        self.wait_for_element_to_be_present(element_locator=self.lbl_logged_as_loc, waiting_time=5)
        return self.lbl_logged_as.text

    def get_ui_message(self):
        raise Exception("Method Not Implemented Yet")

    def click_on_mobile_menu(self):
        self.menu_mobile_emulation_menu_button.click()
        self.wait_for_element_to_be_present(element_locator=self.menu_mobile_emulation_panel_loc, waiting_time=5)
