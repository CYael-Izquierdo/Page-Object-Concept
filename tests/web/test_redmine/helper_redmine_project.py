from lib.mock_data import Generator
from page_objects.web.redmine.redmine_login_page import RedmineLoginPage
from page_objects.web.redmine.redmine_projects_page import RedmineProjectsPage
from page_objects.web.redmine.redmine_admin_projects_page import RedmineAdminProjectsPage
from page_objects.web.redmine.redmine_administration_page import RedmineAdministrationPage
import pytest
from assertpy import assert_that, soft_assertions


def connect_to_redmine(driver, environment):
    if environment.upper() == "REDMINE":
        sut_url = pytest.cfg.get('pytest.environment.redmine').get('sut_url')
    else:
        raise Exception("NOT SUPPORTED ENVIRONMENT: " + environment)

    pytest.execution_data["sut_url"] = sut_url
    pytest.execution_data["environment"] = environment
    driver.get(sut_url)


def login_into_redmine(driver, user: str = 'admin'):
    user_name_cred, password_cred = pytest.cfg.get('pytest.environment.redmine').get(user).split("/")
    login_page = RedmineLoginPage(driver)
    login_page.login(user)


def create_project_dict(project_name, description, identifier, homepage):

    project = {}

    if project_name == "mock_data":
        project_name = Generator.generate_sentence(nb_words=6)
    else:
        from random import randint
        project_name = project_name + "-" + str(randint(0, 9999999))
    project['project_name'] = project_name

    if description.lower() == "mock_data":
        description = Generator.generate_text(max_nb_chars=100)
    project["description"] = description

    if identifier.lower() == "mock_data":
        identifier = project["identifier"] + Generator.generate_license_plate_number()
    else:
        from random import randint
        identifier = identifier + "-" + str(randint(0, 9999999))
    project['identifier'] = identifier

    if homepage.lower() == "mock_data":
        homepage = Generator.generate_profile().get("website")[0]
    project["homepage"] = homepage

    return project


def create_project(driver, project_info):
    project_po = RedmineProjectsPage(driver)
    project_po.create_project(project_info)


def verify_project_successfully_created(driver):
    project_po = RedmineProjectsPage(driver)
    ui_message = project_po.get_ui_message()
    with soft_assertions():
        assert_that(ui_message). \
            is_equal_to("Successful creation."). \
            described_as("The message was not found or was incorrect.")


def find_project_in_project_list(driver, project_name):
    project_po = RedmineProjectsPage(driver)
    project = project_po.find_project(project_name)

    return project


def verify_project(project, td):
    with soft_assertions():
        assert_that(project.text). \
            described_as('The created project was no found.'). \
            is_equal_to(td["project_name"])


def verify_that_project_is_in_projects_list(driver, td):
    project = find_project_in_project_list(driver, td["project_name"])

    with soft_assertions():
        assert_that(project.text). \
            described_as('The created project was no found.'). \
            is_equal_to(td["project_name"])


def delete_all_projects(driver):
    admin_po = RedmineAdministrationPage(driver=driver)

    admin_po.homepage_po.click_on_link("administration")
    admin_po.navigate_to("projects")

    admin_projects_po = RedmineAdminProjectsPage(driver=driver)
    admin_projects_po.delete_all_projects()


def verify_project_successfully_created(ui_message):
    with soft_assertions():
        assert_that(ui_message). \
            is_equal_to("Successful creation."). \
            described_as("The message was not found or was incorrect.")
