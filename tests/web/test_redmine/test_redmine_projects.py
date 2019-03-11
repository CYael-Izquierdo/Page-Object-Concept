import pytest
from lib import framework
from page_objects.web.redmine.redmine_login_page import RedmineLoginPage
from page_objects.web.redmine.redmine_homepage_page import RedmineHomePage
from page_objects.web.redmine.redmine_projects_page import RedmineProjectsPage
from assertpy import soft_assertions, assert_that
from tests.web.test_redmine import helper_redmine_project as helper

# -------------------------------------------------------------------------------

browser_list = [
                'chrome_default_config',
                'chrome_mac_config_1',
                'chrome_mac_headless_config'
                ]


@pytest.fixture(params=browser_list)
def driver(request):
    driver = framework.setup_desktop_browser(request.param)
    yield driver
    driver.quit()

# -------------------------------------------------------------------------------


class TestRedmineProject:
    @pytest.mark.Working
    @pytest.mark.usefixtures('clean_project_list')
    @pytest.mark.parametrize("project_name, description, identifier, homepage", [
        ('Quantum', 'This project is about...', 'quantum', 'https://www.quantum.com'),
        ('Quantum123', 'This project is about...', 'quantum', 'https://www.quantum.com')
        ])
    def test_create_project(self, driver, project_name, description, identifier, homepage):
        projects_po = RedmineProjectsPage(driver, user='admin')
        project_dict = helper.create_project_dict(project_name, description, identifier, homepage)
        projects_po.create_project(project_dict)
        helper.verify_project_successfully_created(projects_po.get_ui_message())
        projects_po.homepage_po.click_on_link('projects')
        project = projects_po.find_project(project_dict.get('project_name'))
        helper.verify_project(project, project_dict)
