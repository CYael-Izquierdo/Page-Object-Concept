from selenium.webdriver.common.by import By
from lib.page_objects import PageElement, MultiPageElement


class RedmineAdminProjectsPageElements:
    # Defining locators and webelements.

    txt_project_name_loc = (By.XPATH, "//*[@id='name']")
    txt_project_name = PageElement(txt_project_name_loc)

    tbl_project_list_loc = (By.XPATH, "//div[@class='autoscroll']//tbody")
    tbl_project_list = PageElement(tbl_project_list_loc)

    delete_projects_bnt_list_loc = (By.XPATH, "//a[@data-method='delete']")
    delete_projects_bnt_list = MultiPageElement(delete_projects_bnt_list_loc)

    chk_confirm_delete_project_loc = (By.ID, "confirm")
    chk_confirm_delete_project = PageElement(chk_confirm_delete_project_loc)

    btn_delete_project_loc = (By.XPATH, "//input[@name='commit']")
    btn_delete_project = PageElement(btn_delete_project_loc)


