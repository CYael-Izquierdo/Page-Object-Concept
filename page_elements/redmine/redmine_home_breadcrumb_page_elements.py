from selenium.webdriver.common.by import By
from lib.page_objects import PageElement


class RedmineHomeBreadcrumbPageElements:
    # Defining locators and webelements.

    link_home_breadcrum_loc = (By.XPATH, "//a[@href='/']")
    link_home_breadcrum = PageElement(link_home_breadcrum_loc)

    link_projects_breadcrum_loc = (By.XPATH, "//a[@href='/projects']")
    link_projects_breadcrum = PageElement(link_projects_breadcrum_loc)

    link_help_breadcrum_loc = (By.LINK_TEXT, "Help']")
    link_help_breadcrum = PageElement(link_help_breadcrum_loc)

    link_signin_breadcrum_loc = (By.XPATH, "//a[@href='/login']")
    link_signin_breadcrum = PageElement(link_signin_breadcrum_loc)

    link_register_breadcrum_loc = (By.XPATH, "//a[@href='/account/register']")
    link_register_breadcrum = PageElement(link_register_breadcrum_loc)

    link_mypage_breadcrum_loc = (By.XPATH, "//a[@href='/my/page']")
    link_mypage_breadcrumb = PageElement(link_mypage_breadcrum_loc)

    link_administration_breadcrum_loc = (By.XPATH, "//a[@href='/admin']")
    link_administration_breadcrum = PageElement(link_administration_breadcrum_loc)

    link_myaccount_breadcrum_loc = (By.XPATH, "//a[@href='/my/account']")
    link_myaccount_breadcrum = PageElement(link_myaccount_breadcrum_loc)

    link_signout_breadcrum_loc = (By.XPATH, "//a[@href='/account/register']")
    link_signout_breadcrum = PageElement(link_signout_breadcrum_loc)

    lbl_logged_as_loc = (By.ID, "loggedas")
    lbl_logged_as = PageElement(lbl_logged_as_loc)