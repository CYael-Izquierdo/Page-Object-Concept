from selenium.webdriver.common.by import By
from lib.page_objects import PageElement


class RedmineLoginPageElements:
    # Defining locators and webelements.
    btn_sign_in_loc = (By.XPATH, "//a[@class='login']")
    btn_sign_in = PageElement(btn_sign_in_loc)

    txt_user_name_loc = (By.ID, "username")
    txt_user_name = PageElement(txt_user_name_loc)

    txt_password_loc = (By.ID, "password")
    txt_password = PageElement(txt_password_loc)

    btn_login_loc = (By.XPATH, "//*[@id='login-submit']")
    btn_login = PageElement(btn_login_loc)

    login_panel_loc = (By.ID, "login-form")
    login_panel = PageElement(login_panel_loc)

    lbl_home_loc = (By.XPATH, "//*[@id ='content']")
    lbl_home = PageElement(lbl_home_loc)


