from selenium.webdriver.common.by import By
from lib.page_objects import PageElement, MultiPageElement


class RedmineAdministrationPageElements:
    # Defining locators and webelements.
    btn_project_loc = (By.XPATH, "//a[@class='icon icon-projects projects']")
    btn_project = PageElement(btn_project_loc)



