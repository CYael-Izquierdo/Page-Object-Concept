import os
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class BrowserDriver:

    __instance = None
    # Browsers path
    head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))

    __chrome_driver_windows_path = head + "/lfs/webdriver/windows/chromedriver.exe"
    __chrome_driver_linux_path = head + "/lfs/webdriver/linux/chromedriver"
    __chrome_driver_mac_path = head + "/lfs/webdriver/mac/chromedriver"
    __firefox_driver_windows_path = head + "/lfs/webdriver/windows/geckodriver.exe"
    __firefox_driver_linux_path = head + "/lfs/webdriver/linux/geckodriver"
    __firefox_driver_mac_path = head + "/lfs/webdriver/mac/geckodriver"
    __ie_driver_windows_path = head + "/lfs/webdriver/windows/IEDriverServer.exe"
    __edge_driver_windows_path = head + "/lfs/webdriver/windows/MicrosoftWebDriver.exe"
    __phantomjs_driver_windows_path = head + "/lfs/webdriver/windows/phantomjs.exe"
    __phantomjs_driver_linux_path = head + "/lfs/webdriver/linux/phantomjs"
    __phantomjs_driver_mac_path = head + "/lfs/webdriver/mac/phantomjs"
    # Chrome Options
    # URL: https://chromium.googlesource.com/chromium/src/+/master/chrome/common/chrome_switches.cc
    # URL: https://chromium.googlesource.com/chromium/src/+/master/chrome/common/pref_names.cc
    __CHROME_MOBILE_EMULATION = "mobileEmulation"

    # FIREFOX OPTIONS
    FF_HEADLESS = "-headless"

    def __new__(cls):
        if BrowserDriver.__instance is None:
            BrowserDriver.__instance = object.__new__(cls)

        return BrowserDriver.__instance

    @classmethod
    def get_browser_driver(cls, browser_name,
                           options=None,
                           firefox_profile=None,
                           platform="WINDOWS",
                           desired_capabilities=None):
        driver_path = cls.__get_driver_path(browser_name, platform=platform)

        if browser_name.upper() == "CHROME":
            if options:
                options = cls.create_chrome_options(c_options=options)

            return cls.get_chrome_driver(driver_path=driver_path,
                                         chrome_options=options,
                                         desired_capabilities=desired_capabilities)
        elif browser_name.upper() in ["FF", "FIREFOX"]:
            if options:
                options = cls.__get_firefox_options(options_list=options)
            if firefox_profile:
                firefox_profile = cls.create_firefox_profile(firefox_profile)
            return cls.get_firefox_driver(driver_path=driver_path, firefox_options=options,
                                          firefox_profile=firefox_profile,
                                          desired_capabilities=desired_capabilities)
        elif browser_name.upper() == "PHANTOMJS":
            return cls.get_phantomjs_driver(driver_path=driver_path)
        elif browser_name.upper() == "SAFARI":
            return cls.get_safari_driver()
        else:
            raise Exception("Not Supported Browser: " + browser_name)

    @classmethod
    def get_browser_options(cls):
        pass

    @classmethod
    def get_chrome_driver(cls, driver_path, chrome_options=None, desired_capabilities=None):
        chrome_options = chrome_options if chrome_options != {} else None
        try:
            driver = webdriver.Chrome(driver_path, chrome_options=chrome_options, desired_capabilities=desired_capabilities)
        except WebDriverException as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create an Chrome Webdriver instance."
                            + "\nERROR: " + format(e)
                            + "\n")

        return driver

    @classmethod
    def __get_driver_path(cls, browser_name: str, platform="WINDOWS"):
        if browser_name.upper() == "SAFARI":
            return None
        elif browser_name.upper() == "CHROME":
            if platform.upper() == "WINDOWS":
                return cls.__chrome_driver_windows_path
            elif platform.upper() == "LINUX":
                return cls.__chrome_driver_linux_path
            elif platform.upper() in ["MAC", "DARWIN"]:
                return cls.__chrome_driver_mac_path
            else:
                raise Exception("Not Supported Platform: " + platform)
        elif browser_name.upper() == "FIREFOX":
            if platform.upper() == "WINDOWS":
                return cls.__firefox_driver_windows_path
            elif platform.upper() == "LINUX":
                return cls.__firefox_driver_linux_path
            elif platform.upper() in ["MAC", "DARWIN"]:
                return cls.__firefox_driver_mac_path
            else:
                raise Exception("Not Supported Platform: " + platform)
        elif browser_name.upper() == "IE":
            if platform.upper() == "WINDOWS":
                return cls.__ie_driver_windows_path
            else:
                raise Exception("Not Supported Platform: " + platform)
        elif browser_name.upper() == "EDGE":
            if platform.upper() == "WINDOWS":
                return cls.__edge_driver_windows_path
            else:
                raise Exception("Not Supported Platform: " + platform)
        elif browser_name.upper() in ["PHANTOM", "PHANTOMJS"]:
            if platform.upper() == "WINDOWS":
                return cls.__phantomjs_driver_windows_path
            elif platform.upper() == "LINUX":
                return cls.__phantomjs_driver_linux_path
            elif platform.upper() == "DARWIN":
                return cls.__phantomjs_driver_mac_path
        else:
            raise Exception("Not Supported Browser: " + browser_name)

    @classmethod
    def create_chrome_options(cls, c_options):
        chrome_options = ChromeOptions()

        if c_options.get("goog:chromeOptions", {}).get("mobileEmulation", False):
            chrome_options.add_experimental_option(cls.__CHROME_MOBILE_EMULATION, c_options.get("mobileEmulation"))
            del c_options["mobileEmulation"]
        else:
            c_options = c_options.get("goog:chromeOptions").get("args")

        for o in c_options:
            chrome_options.add_argument(o)

        return chrome_options

    @classmethod
    def __get_firefox_options(cls, options_list: dict):

        firefox_options = FirefoxOptions()
        for o in options_list:
            firefox_options.add_argument(o)

        return firefox_options

    @classmethod
    def create_firefox_profile(cls, f_profile_options: dict):
        firefox_profile = webdriver.FirefoxProfile()
        for o in f_profile_options:
            firefox_profile.set_preference(o, f_profile_options[o])

        return firefox_profile

    @classmethod
    def get_firefox_driver(cls, driver_path, firefox_options=None, firefox_profile=None, desired_capabilities=None):
        try:
            driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=driver_path,
                                       firefox_options=firefox_options, desired_capabilities=desired_capabilities)

        except WebDriverException as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create an FIREFOX Webdriver instance."
                            + "\nERROR: "
                            + format(e)
                            + "\n")

        return driver

    @classmethod
    def get_edge_driver(cls):
        driver_path = cls.__get_driver_path("WINDOWS", "EDGE")
        try:
            driver = webdriver.Edge(executable_path=driver_path)
        except WebDriverException as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create an EDGE Webdriver instance."
                            + "\nERROR: "
                            + format(e)
                            + "\n")

        return driver

    @classmethod
    def get_ie_driver(cls):
        driver_path = cls.__get_driver_path("WINDOWS", "IE")
        try:
            driver = webdriver.Ie(driver_path)
        except (OSError, WebDriverException) as e:
            print(4 * "<" + "[ERROR]" + 4 * ">"
                  + "An error occurred when trying to create an IE Webdriver instance."
                  + "\nERROR: "
                  + format(e.strerror)
                  + "\n")
            raise Exception(e)

        return driver

    @classmethod
    def get_safari_driver(cls):
        try:
            driver = webdriver.Safari()

        except WebDriverException as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create an SAFARI Webdriver instance."
                            + "\nERROR: "
                            + format(e)
                            + "\n")
        return driver

    @classmethod
    def get_phantomjs_driver(cls, driver_path):
        try:
            driver = webdriver.PhantomJS(executable_path=driver_path)

        except WebDriverException as e:
            raise Exception(4 * "<" + "[ERROR]" + 4 * ">"
                            + "An error occurred when trying to create an PHANTOMJS Webdriver instance."
                            + "\nERROR: "
                            + format(e)
                            + "\n")
        return driver
