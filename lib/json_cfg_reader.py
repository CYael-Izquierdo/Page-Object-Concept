from lib import util
import os

head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))


def get_browser_json_config(config_file_name: str):
    json_file_config_path = head + "/webdriver_configs/" + config_file_name+".json"
    return get_config(json_file_config_path)


def get_appium_config(config_file_name: str):
    json_file_config_path = head + "/appium_configs/" + config_file_name + ".json"
    return get_config(json_file_config_path)


def get_config(config_file_path: str):
    return util.read_json_file(config_file_path)


def get_appium_sever_local_flags(file_name: str):
    json_file_config_path = head + "/appium_flags/" + file_name+".json"
    return get_config(json_file_config_path)
