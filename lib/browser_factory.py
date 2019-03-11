from lib.browser_driver import BrowserDriver
from retry.api import retry


class BrowserFactory:
    __instance = None

    #
    IMPLICIT_WAIT = 2
    PAGE_LOAD_TIMEOUT = 60

    def __init__(self):
        pass

    def __new__(cls):
        if BrowserFactory.__instance is None:
            BrowserFactory.__instance = object.__new__(cls)

        return BrowserFactory.__instance

    @classmethod
    @retry(exceptions=Exception, tries=5, delay=1)
    def get_driver(cls, browser_name: str,
                   options=None,
                   firefox_profile=None,
                   desired_capabilities=None,
                   platform="WINDOWS"):
        try:
            driver = BrowserDriver.get_browser_driver(browser_name=browser_name, options=options,
                                                      firefox_profile=firefox_profile,
                                                      platform=platform,
                                                      desired_capabilities=desired_capabilities)
        except Exception as e:
            raise Exception(
                4 * "<" + "[ERROR]" + 4 * ">" + "An error occurred during browser initialization."
                + "\nERROR: "
                + format(e)
                + "\n")

        driver.delete_all_cookies()
        driver.maximize_window()
        driver.implicitly_wait(cls.IMPLICIT_WAIT)
        driver.set_page_load_timeout(cls.PAGE_LOAD_TIMEOUT)
        return driver

