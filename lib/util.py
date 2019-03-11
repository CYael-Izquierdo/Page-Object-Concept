import configparser
import time
from datetime import datetime, timedelta
# from arrow import arrow
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
# from lib.mock_data import Generator


def convert_string_to_float(str_value, num_of_decimals=2):
    """
    Convert Money values like $1000.0 to 1000.0 as float
    :param str_value: value to be c
    :param num_of_decimals: Number of decimals required.
    :return: float value with the accuracy required.
    """
    float_value = str_value.replace("$", "")

    if num_of_decimals == 0:
        float_value = "{0:.0f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 1:
        float_value = "{0:.1f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 2:
        float_value = "{0:.2f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 3:
        float_value = "{0:.3f}".format((float(float_value.replace(',', ''))))

    return float(float_value)


def convert_empty_values_to_string(value):
    """
    Convert "" empty string values to "0"
    :param value: Value to be checked
    :return: 0 if value == "" or value instead.
    """
    if value in ["", " "]:
        return "0"
    else:
        return value


def table_to_dict(table, transposed=False):
    """
    Convert Step Table to Dictionary
    :param table: Behave feature table data format
    :param transposed: If step data table is transposed.
    :return: dictionary when the table is not transposed and tuple when it is transposed
    """
    test_data = []
    if not transposed:
        for row in table:
            test_data.append([str(row[0]), str(row[1])])
        return dict(test_data)
    else:
        heading = table.headings
        for r in table.rows:
            for i, v in enumerate(r):
                test_data.append((heading[i], v))
        return tuple(test_data)


# TODO: Check if model can be changed to contex or to the table itself"""
def table_to_list(model):
    """
    Convert Step Table to LIST
    :param model:
    :return: List with model rows
    """
    list_temp = []
    for i, r in enumerate(model.rows):
        list_temp.append(r[1])
    return list_temp


def read_config_file(ini_path):
    """
    Reads the ini config file.
    :ini_path: is the path of the file.
    :param ini_path: .ini file path
    :return: Dictionary with section:option keys/values.
    """
    config_file = configparser.RawConfigParser()
    config_file.optionxform = str
    config_file.read(ini_path)

    # Create dict for config file information.
    config_info = {}

    # Iterate config file sections.
    for section in config_file.sections():
        config_info[section] = {}

        # Iterate options for each section and append_values into the dict.
        for option in config_file.options(section):
            config_info[section][option] = config_file.get(section, option)

    return config_info


# TODO: Check
def get_time(occurrence=None):
    """
    Get date or/and time depending on occurrence parameter
    :param occurrence: Part of the date time you want to get.
    :return:
    """
    import datetime

    if occurrence is None or occurrence == "today":
        """Returns today's date and time"""
        current_time = datetime.datetime.now().time()
        hour, minutes, seconds = str(current_time).split(":")
        seconds = seconds.split(".")[0]
        return hour + ":" + minutes + ":" + seconds
    elif occurrence.lower() == "month":
        """Returns today's month name"""
        month = datetime.datetime.now().month
        return month
    # TODO: Find the way to get the month Name
    # elif occurrence.lower() == "month_name":
    #     month_name = datetime.datetime.now()
    #     return month_name
    elif occurrence.lower() == "month_number":
        """Returns today's month"""
        month_number = datetime.datetime.now().month
        return month_number
    elif occurrence.lower() == "year":
        """Returns today's year"""
        year = datetime.datetime.now().year
        return year


def get_time_stamp():
    """
    Returns time stamp
    :return: Time stamp format mdY-HMS
    """
    timestr = time.strftime("%m%d%Y-%H%M%S")
    time_stamp = ""
    for i, t in enumerate(timestr):
        if i == 2 or i == 4:
            time_stamp = time_stamp + "-"
        time_stamp = time_stamp + t
    return time_stamp


def seconds_to_hh_mm_ss(seconds):
    """
    Converts seconds to hours/minutes/seconds
    :param seconds:
    :return: [hours, minutes, seconds]
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


# TODO: Check
def compare_two_dates(date_1, date_2, operator=">"):
    """ CHANGE TO GE, GT, LT, LE, etc convention """
    from datetime import datetime
    date_1 = date_1.replace("/", "-")
    date_2 = date_2.replace("/", "-")
    mm, dd, yyyy = date_1.split("-")
    d1 = datetime(int(yyyy), int(mm), int(dd))
    mm, dd, yyyy = date_2.split("-")
    d2 = datetime(int(yyyy), int(mm), int(dd))

    if operator == ">=":
        if d1 >= d2:
            return True
        else:
            return False
    if operator == "<=":
        if d1 <= d2:
            return True
        else:
            return False
    elif operator == ">":
        if d1 > d2:
            return True
        else:
            return False
    elif operator == "<":
        if d1 < d2:
            return True
        else:
            return False


# TODO: Check
def sum_dates(date_1, date_2):
    """
    Sums two dates
    :param date_1: first date to be sum
    :param date_2: second date in format of year or months. eg. 2 years
    :return: The sum of a date plus a year or a month.
    """
    date_1 = date_1.replace("/", "-")
    if date_2.endswith("year") or date_2.endswith("years"):
        date_2.replace("year", "").replace(" ", "")
        mm, dd, yyyy = date_1.split("-")
        result_date = arrow.get(yyyy + "-" + mm + "-" + dd).replace(year=int(date_2)).format(
            'MM/DD/YYYY')
        return result_date
    elif date_2.endswith("month") or date_2.endswith("months"):
        if date_2.endswith("months"):
            date_2 = date_2.replace("months", "").replace(" ", "")
        if date_2.endswith("month"):
            date_2 = date_2.replace("month", "").replace(" ", "")
        mm, dd, yyyy = date_1.split("-")
        result_date = arrow.get(yyyy + "-" + mm + "-" + dd).replace(months=int(date_2)).format('MM/DD/YYYY')
        return result_date


# TODO: Check
def get_dob_by_age(age, reference_date):
    """
    Calculates the dob based on a specific DATE and AGE
    :param age: The standard age
    :param reference_date:
    :return: date of birth according to the age.
    """
    date = reference_date.replace("/", "-")
    mm, dd, yyyy = date.split("-")
    dob = arrow.get(yyyy + "-" + mm + "-" + dd).replace(years=int(-age)).format('MM/DD/YYYY')

    return dob


def get_address(by, criteria):
    """
    Get address according to the city, state or zip_code.
    :param by: Address from city, state or zip code.
    :param criteria: could be a zip code number, state or city name.
    :return: Returns a dictionary with the person data generated
    """
    g = Generator()
    if by == "city":
        return g.get_person_by_city(criteria).__as_dict()
    elif by == "state":
        return g.get_person_by_state(criteria).__as_dict()
    elif by == "zip_code":
        return g.get_person_by_zip_code(criteria).__as_dict()


def get_numbers_from_string(str_var):
    """
    Cleans a numeric string like $30,000.00 to 30000.00
    :param str_var:
    :return:
    """
    result = ""
    for s in str_var:
        if s.isdigit() or s == ",":
            result = result + s
        else:
            continue
    return result


def is_field_in_blank(self, web_element):
    """
    Verifies if a field is in blank or is 0
    :param self:
    :param web_element:
    :return:
    """
    text = self.web_element_text(web_element)
    text = text.replace(".", "")

    if text.isdigit():
        float_var = float(text)
        print("float_var: ", float_var)

        if float_var == 0:
            return True

    elif text == "":
        return True

    else:
        return False


def select_first_valid_element(web_element):
    """
    Selects a valid first dropdown element
    :param web_element: Webelement reference
    :return: None
    """
    dd_values_list = get_dropdown_options_list(web_element)
    if dd_values_list[0] == "- Select -":
        select_item_dropdown_by_index(web_element, 2)
    else:
        select_item_dropdown_by_index(web_element, 1)


def select_item_dropdown_by_index(web_element, item_index):
    """
    Selects option by index
    :param web_element: Webelement: Webelement reference
    :param item_index:
    :return: None
    """
    sel = web_element.find_elements_by_tag_name("option")
    try:
        sel[item_index].click()
    except IndexError:
        sel[0].click()


# Returns the dropdown selected option.
def get_dropdown_selected_option(web_element):
    sel_option = ""
    try:
        select = Select(web_element)
        sel_option = select.first_selected_option

    except Exception as e:
        print("Exception occurred!", format(e))

    return sel_option.text


# Returns a list of options
def get_dropdown_options_list(web_element):
    item_list = []
    for option in web_element.find_elements_by_tag_name("option"):
        item_list.append(option.text)

    if "- Select -" in item_list:
        item_list.remove("- Select -")

    return item_list


def select_highest_dropdown_option(web_element):
    """
    Selects the highest numeric value from a dropdown.
    :param web_element:
    :return:
    """
    option_list = get_dropdown_options_list(web_element)

    filtered_list = []
    for o in option_list:
        if o != "No Coverage":
            filtered_list.append(o)

    last_option = filtered_list[-1]

    select = Select(web_element)
    select.select_by_visible_text(last_option)


def select_any_value(rows, selection="any"):
    """
    Selects Any value from a list of dropdowns.
    :param rows: Rows containing dropdowns
    :param selection: Any/Combi. Any means the first valid value. Combi means a combination of selected options.
    :return: None
    """
    for r in rows:
        cols = r.find_elements_by_tag_name("td")
        for i, c in enumerate(cols):
            field = c.find_elements_by_tag_name("select")
            if len(field) != 0:
                if field[0].is_displayed():
                    if selection.lower() == "any":
                        try:
                            Select(field[0]).select_by_index(1)
                        except NoSuchElementException:
                            pass
                    elif selection.lower() == "combi":
                        if (i + 1) % 2 != 0:
                            Select(field[0]).select_by_index(1)
                        else:
                            select_highest_dropdown_option(field[0])


def get_dropdown(driver, locator):
    web_element = driver.find_element(*locator)
    select_component = Select(web_element)
    return select_component


# Verifies if an standard options list are in a dropdown options.
def check_dropdown_contains_an_option(web_element, options):
    options_to_verify = []
    options_found = []
    options_list = get_dropdown_options_list(web_element)

    options_to_verify.append(options)

    for o in options_list:
        if o in options_to_verify:
            options_found.append(o)
            options_to_verify.remove(o)

            if len(options_to_verify) == 0 and options_found != 0:
                return True

    return False


# TODO: Locator needs to be changed according to the SUT's loading icon.
def wait_until_page_is_loaded(driver, locator=None, wait_time=20):
    """
    Wait until the page loads and the "loading" icon disappears
    :param driver:
    :param locator:
    :param wait_time:
    :return:
    """
    if locator is None:
        locator = "//*[@id='processing']"
    elif locator == "obtain_operators_and_vehicles":
        locator = "//li[contains(.,'Your operator/vehicle information request is being processed...')]"

    wait = WebDriverWait(driver, wait_time, 1, TimeoutException)
    wait.until(ec.invisibility_of_element_located((By.XPATH, locator)))


def get_element(driver, locator):
    """
    Return the VISIBLE element starting from the TOP of the list of weblements.
    This is useful when there are many web elements which fetchs for the same XPATH
    :param driver:
    :param locator:
    :return:
    """
    web_elements = driver.find_elements(*locator)

    for w in reversed(web_elements):
        if w.is_displayed():
            return w

    assert False is True, "get_element() - Visible WebElement NOT FOUND."


def generate_web_element_dic(web_element_list):
    """
    Generates a web element dictionary based on key: web_element_title and webelement instance
    :param web_element_list:
    :return: dictionary of webelements
    """
    we_dict = {}
    for w in web_element_list:
        if w.is_enabled and w.is_displayed:
            we_title = w.get_attribute("title")
            we_dict.update({we_title: w})

    return we_dict


def print_feature_duration(feature_name, duration_in_hh_mm_ss):
    print("\n" + 50 * "*")
    print("Feature: " + feature_name)
    print("Time: " + "%d:%02d:%02d" % (duration_in_hh_mm_ss[0], duration_in_hh_mm_ss[1], duration_in_hh_mm_ss[2]))
    print("\n" + 50 * "*")


def read_json_file(file_path):
    import json
    try:
        with open(file_path, "r") as file:
            file = json.load(file)
    except FileNotFoundError as e:
        raise Exception(
            4 * "<" + "[ERROR]" + 4 * ">" + "An error occurred when trying to read  "
            + file_path
            + " file"
            + "\nERROR: "
            + format(e)
            + "\n")
    return file


def get_proyect_root_path():
    import os
    head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))

    return head


def get_current_branch_name(repo_path=None):
    """
    Returns the name of the active Git branch as a string.
    :param repo_path:
    :return: Current Branch name as String
    """
    from git import Repo

    # By default gets proyect repo path.
    if repo_path is None:
        repo_path = get_proyect_root_path()

    repo = Repo(repo_path)
    try:
        branch = repo.active_branch
        branch_name = branch.name
    except Exception as e:
        print(
            4 * "<" + "[WARNING]" + 4 * ">" + "Not able to get branch name."
            + " file"
            + "\nERROR: "
            + format(e)
            + "\n")
        branch_name = None
    finally:
        repo.close()

    return branch_name


def get_revision_number(repo_path=None):
    """
    Returns the revision name of the active Git branch as a string.
    :param repo_path:
    :return:
    """

    repo = __get_repo_instance(repo_path)

    branch = repo.active_branch
    return branch.commit.name_rev


def get_revision_last_commit_date_time(repo_path=None):
    """
    Returns the datetime of the last commit of the active Git branch as a string.
    :param repo_path:
    :return:
    """
    repo = __get_repo_instance(repo_path)
    branch = repo.active_branch
    return branch.commit.committed_datetime


def __get_repo_instance(repo_path):
    from git import Repo

    # By default gets proyect repo path.
    if repo_path is None:
        repo_path = get_proyect_root_path()

    return Repo(repo_path)


def convert_slash_path(f_path):
    """
        Checks platform and performs conversion from windows path to mac & linux ones if needed.
        :param f_path:
        :return:
    """
    import platform

    if platform.system().lower() != "windows":
        f_path = f_path.replace("\\", "/")

    return f_path


def create_folder(file_path):
    import os
    import errno

    # Check platform and convert \ to / in file path
    file_path = convert_slash_path(file_path)

    try:
        os.mkdir(file_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise Exception("Error when creating a folder in " + file_path + "\n")


def delete_folder(folder_path):
    """
    Delete a folder. If it is not empty, checks the 2nd level. Delete inner folders without checking if they are empty 
    or not. Is not a recursive method.
    :param folder_path: Folder path to be deleted
    :return: 
    """
    import os

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        if len(os.listdir(folder_path)) == 0:
            os.rmdir(folder_path)
        else:
            for d in os.listdir(folder_path):
                os.rmdir(folder_path + "/" + d)

        os.rmdir(folder_path)
    # else:
    #     print(folder_path + " does NOT exist or is NOT a folder.")


def validate_list_content(expected_values: list, result_values: list) -> dict:
    """
    Check if two lists has exactly the same content. Compares the expected_values list with the result_values list.
    :param expected_values: a list of expected values willing to be found in result_values.
    :param result_values: The list to be compared to.
    :return: Return a result dictionary with:
    # are_equal: True if both lists have exactly the same values. False otherwise.
    # missing_values: a list of missing values from expected_values list not found in result_values list.
    # unexpected_values: a list of values found in result_values list that are not in expected_values
    """

    result = {"are_equal": True, "missing_values": [], "unexpected_values": []}

    if not expected_values:
        raise Exception(
            4 * "<" + "[ERROR]" + 4 * ">" +
            "Expected Test Test Data cannot have leght = 0"
            "\n")

    # Empty Error List
    if not result_values:
        result["are_equal"] = False
        result["missing_values"] = expected_values

        return result

    # Missing Loop
    for expected in expected_values:
        if not expected in result_values:
            result["are_equal"] = False
            result["missing_values"].append(expected)

    # Unexpected Loop
    for response_err in result_values:
        if not response_err in expected_values:
            result["are_equal"] = False
            result["unexpected_values"].append(response_err)

    return result
