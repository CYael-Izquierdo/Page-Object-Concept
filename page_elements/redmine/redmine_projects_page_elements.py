from selenium.webdriver.common.by import By
from lib.page_objects import PageElement, MultiPageElement


class RedmineProjectsPageElements:
    # Defining locators and webelements.
    btn_new_project_loc = (By.XPATH, "//a[text()='New project']")
    btn_new_project = PageElement(btn_new_project_loc)

    txt_project_name_loc = (By.ID, "project_name")
    txt_project_name = PageElement(txt_project_name_loc)

    __txt_project_description_loc = (By.ID, "project_description")
    txt_project_description = PageElement(__txt_project_description_loc)

    __txt_project_identifier_loc = (By.ID, "project_identifier")
    txt_project_identifier = PageElement(__txt_project_identifier_loc)

    __txt_homepage_loc = (By.ID, "project_homepage")
    txt_homepage = PageElement(__txt_homepage_loc)

    __chk_public_loc = (By.ID, "project_is_public")
    chk_public = PageElement(__chk_public_loc)

    __sel_subproject_of_loc = (By.ID, "project_parent_id")
    sel_subproject_of = PageElement(__sel_subproject_of_loc)

    chk_inherit_members_loc = (By.ID, "project_inherit_members")
    chk_inherit_members = PageElement(chk_inherit_members_loc)

    __chk_modules_list_loc = (By.XPATH, "//legend[text()='Modules']/parent::fieldset//input[@type='checkbox']")
    chk_modules_list = MultiPageElement(__chk_modules_list_loc)

    __chk_trackers_list_loc = (By.XPATH, "//legend[text()='Trackers']/parent::fieldset//input[@type='checkbox']")
    chk_trackers_list = MultiPageElement(__chk_trackers_list_loc)

    btn_create_loc = (By.NAME, "commit")
    btn_create = PageElement(btn_create_loc)

    __btn_create_and_continue_loc = (By.NAME, "continue")
    btn_create_and_continue = PageElement(__btn_create_and_continue_loc)

    __btn_save_loc = (By.XPATH, "//form[@id='edit_project_5']/input[@value='Save']")
    btn_save = PageElement(__btn_save_loc)

    lbl_message_loc = (By.ID, "flash_notice")
    lbl_message = PageElement(lbl_message_loc)

    __tbl_projects_list_loc = (By.XPATH, "//*[@id='projects-index']//a")
    tbl_projects_list = MultiPageElement(__tbl_projects_list_loc)
