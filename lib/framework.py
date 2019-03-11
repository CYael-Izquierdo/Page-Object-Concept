import requests
from lib import json_cfg_reader as cfg_reader, util
import pytest
from retry import retry
import subprocess
from appium import webdriver as appium_webdriver
from lib.browser_factory import BrowserFactory as BF

COMMON_LIBRARIES = {"java": "java -version | head -1",
                    "node": "node --version",
                    "npm": "npm --version",
                    "appium": "npm view appium grep version",
                    "git": "brew info git | head -1",
                    "git-lfs": "brew info git-lfs | head -1"}
MAC_LIBRARIES = {"python": "python3 --version",
                 "libimobiledevice": "brew info libimobiledevice | head -1",
                 "ios-webkit-debug-proxy": "brew info ios-webkit-debug-proxy | head -1",
                 "ios-deploy": "npm list ios-deploy"}
WIN_LIBRARIES = {"python": "python --version"}

# ADB COMMANDS
ADB_COMMAND_PREFIX = 'adb'
ADB_COMMAND_SHELL = 'shell'
ADB_COMMAND_PULL = 'pull'
ADB_COMMAND_PUSH = 'push'
ADB_COMMAND_RM = 'rm -r'
ADB_COMMAND_CHMOD = 'chmod -R 777'
ADB_COMMAND_INSTALL = 'install'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_FORWARD = 'forward'
ADB_COMMAND_DEVICES = 'devices'
ADB_COMMAND_GETSERIALNO = 'get-serialno'
ADB_COMMAND_WAITFORDEVICE = 'wait-for-device'
ADB_COMMAND_KILL_SERVER = 'kill-server'
ADB_COMMAND_START_SERVER = 'start-server'
ADB_COMMAND_GET_STATE = 'get-state'
ADB_COMMAND_SYNC = 'sync'
ADB_COMMAND_VERSION = 'version'
ADB_COMMAND_BUGREPORT = 'bugreport'
ADB_COMMAND_TCPIP = 'tcpip'
ADB_COMMAND_CONNECT = 'connect'

# APPIUM COMMANDS
APPIUM_COMMAND = 'appium'
APPIUM_COMMAND_UDID = '-U'
APPIUM_COMMAND_PORT = '--port'
APPIUM_COMMAND_ADDRESS = '--address'
APPIUM_COMMAND_FULL_RESET = '--full-reset'
APPIUM_COMMAND_DEVICE_NAME = '--device-name'
APPIUM_COMMAND_PLATFORM_NAME = '--platform-name'
APPIUM_COMMAND_PLATFORM_VERSION = '--platform-version'
APPIUM_COMMAND_APP = '--app'
APPIUM_COMMAND_BROWSER_NAME = '--browser-name'
APPIUM_COMMAND_CHROME_DRIVER_PORT = '--chromedriver-port'
APPIUM_SELENDROID_PORT = '--selendroid-port'
APPIUM_SHOW_CONFIG = '--show-config'
APPIUM_NODE_CONFIG = '--nodeconfig'
APPIUM_TMP_DIR = '--tmp'
APPIUM_TRACE_DIR = '--trace-dir'
APPIUM_SUPPRESS_ADB_KILL_SERVER = '--suppress-adb-kill-server'
APPIUM_REBOOT = '--reboot'
APPIUM_WEBKIT_DEBUG_PROXY_PORT = '--webkit-debug-proxy-port'
APPIUM_ISOLATE_SIM_DEVICE = '--isolate-sim-device'
APPIUM_INSTRUMENTS = '--instruments'
APPIUM_DEFAULT_DEVICE = '--default-device'
APPIUM_FORCE_IPHONE = '--force-iphone'
APPIUM_FORCE_IPAD = '--force-ipad'

# APK PATHS
APK_BASE_PATH = "apks"
APK_ANDROID_DIR = "/android"
APK_ANDROID_X86 = "/x86/"
APK_ANDROID_ARM = "/arm/"
APK_ANDROID_CHROME = "/chrome"
APK_ANDROID_LATEST = "/latest"

IPA_IOS_DIR = "/ipas"

# APK Packages
ANDROID_CHROME_PKG_ACT = ("com.android.chrome", "com.google.android.apps.chrome.Main")
ANDROID_FF_PKG_ACT = ("org.mozilla.firefox", "org.mozilla.firefox.App")


def setup_appium_driver(config_name: str, capabilities_dict: dict = None):
    capabilities: dict = cfg_reader.get_appium_config(config_file_name=config_name)

    if capabilities_dict:
        capabilities.update(capabilities_dict)

    server_parameters = get_parameters_from_config_file("appium.local.server_flags")

    # UiAutomator2 port
    if capabilities.get("automationName", "N/A").lower() == "uiautomator2" and \
            capabilities.get("systemPort", False):
        capabilities["systemPort"] = is_port_available(server_parameters["address"],
                                                       str(capabilities.get("systemPort")))
        capabilities["systemPort"] = int(capabilities["systemPort"])
    else:
        if not hasattr(pytest, 'appium_data'):
            pytest.appium_data = {"appium_subprocess": None,
                                  "appium_server_url": None}

        if pytest.appium_data["appium_subprocess"] is None:
            pytest.appium_data["appium_subprocess"] = start_appium_server(server_parameters)
            pytest.appium_data["appium_server_url"] = "http://" + server_parameters[
                "address"] + ":" + str(appium_available_port) + "/wd/hub"

        driver = create_appium_webdriver_remote(server_url=pytest.appium_data["appium_server_url"],
                                            desired_capabilities=capabilities)

    if driver is None:
        pytest.skip("[Error] Exception occurs during appium initialization. Scenario Skipped.")

    return driver


def setup_desktop_browser(config_name):
    json_cfg = cfg_reader.get_browser_json_config(config_file_name=config_name)
    profile_options_dic = json_cfg.get("moz:firefoxOptions", {}).get("prefs", None)
    platform = pytest.execution_data["platform"]

    # LOCAL BROWSER

    browser_name = json_cfg.get("browserName", None)

    driver = BF.get_driver(browser_name=browser_name,
                           desired_capabilities=json_cfg,
                           firefox_profile=profile_options_dic,
                           platform=platform)

    # Check if Webdriver was correctly initialized. If not, skip test.
    if driver is None:
        pytest.skip("[Error] Exception occurs during browser initialization. Scenario Skipped.")

    return driver


def is_port_available(address, port):
    """
    Checks if appium url:port is available. If not, tries with the next port until it reaches an available one.
    :param address: address
    :param port: port
    :return: available port
    """
    attempts = 0
    max_attemps = 1000
    while True:
        url = "http://" + address + ":" + str(port)
        try:
            requests.get(url=url, timeout=1)
            attempts += 1
            port = str(int(port) + attempts)
        except requests.exceptions.ConnectionError as e:
            return port

        if attempts == max_attemps:
            raise Exception("No available port found. Max attempts " + str(max_attemps))


def start_appium_server(param):
    appium_options = []

    # Available port for appium
    global appium_available_port
    appium_available_port = is_port_available(param.get("address", "127.0.0.1"), param["port"])

    # Launching Appium Server by CONSOLE COMMANDS:
    # ALL MOBILE PLATFORM
    if param.get("udid", False):
        appium_options.append(APPIUM_COMMAND_UDID)
        appium_options.append(param.get("udid"))
    appium_options.append(APPIUM_COMMAND_PORT)
    appium_options.append(appium_available_port)
    appium_options.append(APPIUM_COMMAND_ADDRESS)
    appium_options.append(param.get("address", "127.0.0.1"))

    if param.get("chromedriver_port", False):
        appium_options.append(APPIUM_COMMAND_CHROME_DRIVER_PORT)
        appium_options.append(param.get("chromedriver_port"))
    if param.get("selendroid_port", False):
        appium_options.append(APPIUM_SELENDROID_PORT)
        appium_options.append(param.get("selendroid_port"))
    if param.get("show_config", False):
        appium_options.append(APPIUM_SHOW_CONFIG)
        appium_options.append(param.get("show_config"))
    if param.get("nodeconfig", False):
        appium_options.append(APPIUM_NODE_CONFIG)
        appium_options.append(param.get("nodeconfig"))
    if param.get("tmp_dir", False):
        appium_options.append(APPIUM_TMP_DIR)
        appium_options.append(param.get("tmp_dir"))
    if param.get("trace_dir", False):
        appium_options.append(APPIUM_TRACE_DIR)
        appium_options.append(param.get("trace_dir"))
    # ANDROID ONLY
    if param.get("suppress_adb_kill_server", False):
        appium_options.append(APPIUM_SUPPRESS_ADB_KILL_SERVER)
        appium_options.append(param.get("suppress_adb_kill_server"))
    if param.get("reboot", False):
        appium_options.append(APPIUM_REBOOT)
        appium_options.append(param.get("reboot"))
    # IOS ONLY
    if param.get("default_device", False):
        appium_options.append(APPIUM_DEFAULT_DEVICE)
        appium_options.append(param.get("default_device"))
    if param.get("instruments", False):
        appium_options.append(APPIUM_INSTRUMENTS)
        appium_options.append(param.get("instruments"))
    if param.get("isolate_sim_device", False):
        appium_options.append(APPIUM_ISOLATE_SIM_DEVICE)
        appium_options.append(param.get("isolate_sim_device"))
    if param.get("webkit_debug_proxy_port", False):
        appium_options.append(APPIUM_WEBKIT_DEBUG_PROXY_PORT)
        appium_options.append(param.get("webkit_debug_proxy_port"))
    if param.get("force_iphone", False):
        appium_options.append(APPIUM_FORCE_IPHONE)
        appium_options.append(param.get("force_iphone"))
    if param.get("force_ipad", False):
        appium_options.append(APPIUM_FORCE_IPAD)
        appium_options.append(param.get("force_ipad"))

    return call_command_line(APPIUM_COMMAND, appium_options)


def call_command_line(command_string: str, options_list=None):
    if options_list is not None:
        for i in range(0, len(options_list)):
            options_list[i] = str(options_list[i])

        options_list.insert(0, command_string)

        command_args = " ".join(options_list)
        # print("[SUB-PROCESS] " + command_args)
        # p = subprocess.Popen(command_args, shell=True)
        p = subprocess.Popen(command_args, shell=True)
        sub_process_info = [command_string, options_list[1::], p]
        return sub_process_info

    else:
        process = subprocess.Popen(command_string, shell=True, stderr=subprocess.STDOUT)
        output, error = process.communicate()


@retry(exceptions=Exception, tries=30, delay=1)
def create_appium_webdriver_remote(server_url: str, desired_capabilities: dict):
    return appium_webdriver.Remote(command_executor=server_url,
                                   desired_capabilities=desired_capabilities)


def get_parameters_from_config_file(section):
    # Get Global Server Flags from behave.ini file
    parameters = pytest.cfg.get(section)

    # Filtering key/values parameters which don't have values in behave.ini file
    parameters = filter_config_dict(parameters)
    return parameters


def filter_config_dict(var_dict):
    to_be_removed = ["", "no", "None"]
    """
    Filter dictionary removing values in to_be_removed list.
    :param var_dict: var dictionary
    :return: Filtered dictionary
    """
    # Filtering key/values parameters which don't have values in behave.ini file
    var_dict_filtered = []
    # # Getting keys of the parameter which have values distinct than "" (Empty)
    keys = [k for k in var_dict if var_dict[k] not in to_be_removed]
    # # Using the resulting keys to re create the dict
    var_dict_filtered = {k: var_dict[k] for k in keys}

    return var_dict_filtered

