from selenium.webdriver.common.by import By
from lib.page_objects import PageElement


class RedmineHomepagePageElements:

    menu_home_loc = (By.XPATH, "//a[@href='/']")
    menu_home = PageElement(menu_home_loc)

    menu_my_page_loc = (By.XPATH,"//a[@href='/my/page']")
    menu_my_page = PageElement(menu_my_page_loc)

    menu_projects_loc = (By.XPATH,"//a[@href='/projects']")
    menu_projects = PageElement(menu_projects_loc)

    menu_administration_loc = (By.XPATH,"//a[@href='/admin']")
    menu_administration = PageElement(menu_administration_loc)

    menu_help_loc = (By.XPATH,"//a[@href='https://www.test_redmine.org/guide']")
    menu_help = PageElement(menu_help_loc)

    menu_my_account_loc = (By.XPATH, "//a[@href='/my/account']")
    menu_my_account = PageElement(menu_my_account_loc)

    menu_sign_in_loc = (By.XPATH, "//a[@href='/login']")
    menu_sign_in = PageElement(menu_sign_in_loc)

    menu_register_loc = (By.XPATH, "//a[@href='/account/register']")
    menu_register = PageElement(menu_register_loc)

    menu_logout_loc = (By.XPATH, "//a[@href='/logout']")
    menu_logout = PageElement(menu_logout_loc)

    lbl_home_page_label_loc = (By.XPATH, "//div[@id='content']/h2")
    lbl_home_page_label = PageElement(lbl_home_page_label_loc)

    lbl_logged_as_loc = (By.ID, "loggedas")
    lbl_logged_as = PageElement(lbl_logged_as_loc)

    menu_mobile_emulation_menu_button_loc = (By.CSS_SELECTOR, "#header > a")
    menu_mobile_emulation_menu_button = PageElement(menu_mobile_emulation_menu_button_loc)

    menu_mobile_emulation_panel_loc = (By.XPATH, "//*[@class='flyout-menu js-flyout-menu']")
    menu_mobile_emulation_panel = PageElement(menu_mobile_emulation_panel_loc)
