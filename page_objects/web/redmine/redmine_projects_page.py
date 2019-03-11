from page_objects.web.webui_base_page import WebuiBasePage
from page_elements.redmine.redmine_projects_page_elements import RedmineProjectsPageElements
from page_objects.android.android_base_page import AndroidBasePage
from page_objects.ios.ios_base_page import IosBasePage
from selenium.common.exceptions import WebDriverException
from page_objects.web.redmine.redmine_login_page import RedmineLoginPage
from page_objects.web.redmine.redmine_homepage_page import RedmineHomePage


class RedmineProjectsPage(WebuiBasePage, RedmineProjectsPageElements):

    def __init__(self, driver, user=None):
        super(RedmineProjectsPage, self).__init__(driver=driver)
        self.is_mobile_emulation = self.check_is_mobile_emulation()
        self.is_android = self.is_android_test()
        self.is_ios = self.is_ios_test()
        if self.is_android:
            self.mobile_po = AndroidBasePage(driver)
        elif self.is_ios:
            self.mobile_po = IosBasePage(driver)
        if user:
            login_po = RedmineLoginPage(self.driver)
            home_po = login_po.login(user)
            home_po.click_on_link('projects')
            self.wait_for_element_to_be_present(element_locator=self.btn_new_project_loc,
                                                waiting_time=5)
        self.homepage_po = RedmineHomePage(self.driver)
        self.wait_for_element_to_be_present(self.homepage_po.menu_projects_loc)

    def create_project(self, td):
        self.btn_new_project.click()
        self.wait_for_element_to_be_present(element_locator=self.txt_project_name_loc,
                                            waiting_time=5)
        self.txt_project_name = td.get("project_name")

        if td.get("description", None):
            self.txt_project_description = td["description"]

        if td.get("homepage", None):
            self.txt_homepage = td["homepage"]

        if td.get("public", None):
            self.click_check_box(web_element=self.chk_public, uncheck=False)

        if td.get("subproject_of", None):
            self.sel_subproject_of = td["subproject_of"]

        if td.get("inherit_members", None):
            if self.is_android:
                if self.driver.is_keyboard_shown():
                    try:
                        self.driver.hide_keyboard()
                    except WebDriverException as e:
                        print(4 * "<" + "[WARNING]" + 4 * ">" + "Not able to hide keyboard. (Android device)"
                              + "\nERROR: "
                              + format(e)
                              + "\n")

            self.click_check_box(web_element=self.chk_inherit_members, uncheck=False)

        if td.get("modules", None):
            for module in td["modules"]:
                if td["modules"][module]:
                    self.click_check_box_by_name(web_elements=self.chk_modules_list, checkbox_name=module)

        if self.is_android:
            self.scroll_to(web_element=self.btn_create)

        self.btn_create.click()

    def get_ui_message(self):
        self.wait_for_element_to_be_present(element_locator=self.lbl_message_loc, waiting_time=5)
        return self.lbl_message.text

    def save_project(self):
        self.btn_save.click()

    def get_project_list(self):
        self.homepage_po = RedmineHomePage(self.driver)
        self.homepage_po.click_on_link('Projects')
        p_list = []
        for p in self.tbl_projects_list:
            p_list.append(p.text)

        return p_list

    def find_project(self, project_name):
        self.homepage_po = RedmineHomePage(self.driver)
        if self.is_mobile_emulation:
            self.homepage_po.click_on_mobile_menu()
        self.homepage_po.click_on_link('Projects')
        if self.is_ios or self.is_android:
            i = 0
            while i < 12:
                for project in self.tbl_projects_list:
                    if project.text == project_name and project.is_displayed():
                        return project
                self.mobile_po.scroll_down()
            return None
        else:
            for project in self.tbl_projects_list:
                if project.text == project_name:
                    return project
            return None
