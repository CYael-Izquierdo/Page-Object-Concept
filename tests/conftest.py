import pytest
from lib import util


def pytest_sessionstart(session):
    """ before session.main() is called. """
    filename = "pytest.ini"
    head = util.get_proyect_root_path()

    # Get behave ini config
    pytest.cfg = util.read_config_file(head + "/" + filename)

    sut_url = pytest.cfg.get('pytest.environment.local').get('sut_url')
    env_name = pytest.cfg.get('pytest.environment.local').get('env_name')

    import platform

    # TODO: Synchronize context "date_run" timestamp and screenshot timestamp
    pytest.execution_data = dict({
        "sut_url": sut_url,
        "environment": env_name,
        "project_root": head,
        "platform": platform.system().lower(),
        "driver": None,
        "video_recording": None,
        "run_id": None,
        "date_run": util.get_time_stamp(),
        "feature_name": None,
        "scenario_name": None,
        "window_size": None,
        "image_output_path": head + pytest.cfg.get('pytest').get('images_output_path'),
        "rest": {}
    })


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    kill_appium_process()


def kill_appium_process():
    if hasattr(pytest, 'appium_data'):
        pytest.appium_data['appium_subprocess'][2].kill()
        pytest.appium_data['appium_subprocess'][2].terminate()
        pytest.appium_data['appium_subprocess'] = None
