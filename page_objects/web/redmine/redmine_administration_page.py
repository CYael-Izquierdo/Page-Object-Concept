from page_objects.web.webui_base_page import WebuiBasePage
from page_elements.redmine.redmine_administration_page_elements import RedmineAdministrationPageElements
from page_objects.web.redmine.redmine_homepage_page import RedmineHomePage
from page_objects.android.android_base_page import AndroidBasePage


class RedmineAdministrationPage(WebuiBasePage, AndroidBasePage, RedmineAdministrationPageElements):
    def __init__(self, driver):
        super(RedmineAdministrationPage, self).__init__(driver=driver)
        self.homepage_po = RedmineHomePage(self.driver)

    def navigate_to(self, section):
        if section.upper() == "PROJECTS":
            self.btn_project.click()

