import pytest
from pytest import Item

# ======================================================================================================================

# CUSTOM REPORTER

# Agregar verctor con mark a ejecutar y a skipear.

tests_list = []
markers_to_run = ['Working']
markers_to_skip = ['NotImplementedYet', 'Broken']

mark_counter = {}
# mark_counter example
# mark_counter = {'Working':
#                     {'total': 0,
#                      'tests': []},
#                 'NotImplementedYet':
#                     {'total': 0,
#                      'tests': []},
#                 'Broken':
#                     {'total': 0,
#                      'tests': []},
#                 }

wrong_marked_tests = {}
# wrong_marked_tests example
# wrong_marked_tests = {'test_name': ['Working', 'NotImplementedYet']}

unmarked_tests = []


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--mark-metrics', action='store_true', dest='mark metrics')


def pytest_runtest_setup(item: Item):

    def _sum_test_to_mark_counter(mark_name, item):
        """Add test info to mark_counter"""
        mark_counter[mark_name]['total'] += 1
        mark_counter[mark_name]['tests'].append(item.nodeid)

    def _create_mark_counter(mark_list: list):
        """Initialize mark_counter like a dict"""
        if not mark_counter:
            for mark in mark_list:
                mark_counter[mark] = {}
                mark_counter[mark]['total'] = 0
                mark_counter[mark]['tests'] = []

    def _add_wrong_test_marked(item, marks):
        """Add test info to wrong_marked_tests"""
        wrong_marked_tests[item.nodeid] = {}
        wrong_marked_tests[item.nodeid]['Marks'] = marks

    def _get_my_custom_marks(item: Item):
        """:return list with the marks of the test that are included in marks_to_run or marks_to_skip """
        marks = []
        for mark in item.own_markers:
            if mark.name in markers_to_skip + markers_to_run:
                marks.append(mark.name)
        return marks

    tests_list.append(item.nodeid)

    _create_mark_counter(markers_to_run + markers_to_skip)

    test_marks = _get_my_custom_marks(item)

    if not test_marks:
        unmarked_tests.append(item.nodeid)
        pytest.skip()
    elif len(test_marks) >= 2:
        _add_wrong_test_marked(item, test_marks)
        pytest.skip()
    else:
        _sum_test_to_mark_counter(test_marks[0], item)
        if test_marks[0] in markers_to_skip:
            pytest.skip()


def pytest_sessionfinish(session, exitstatus):
    print_report()


def print_report():
    print('')
    print('\33[0m' + '-------------------------------------------------------------------------')
    print('Total: {}'.format(len(tests_list)))
    print('\33[0m' + '-------------------------------------------------------------------------')

    # Print marked tests
    for mark_name in mark_counter.keys():
        if mark_name in markers_to_run:
            colour = '\33[92m'
        elif mark_name in markers_to_skip:
            colour = '\33[91m'
        print('{}{}: {}'.format(colour, mark_name, mark_counter[mark_name]['total']))
        print('     Tests: ')
        for test in mark_counter[mark_name]['tests']:
            print('         - {}'.format(test))
    print('\33[0m' + '-------------------------------------------------------------------------')

    # Print wronly marked tests
    print('\33[91m' + 'Wrongly marked tests: {}'.format(len(wrong_marked_tests)))
    for test_name in wrong_marked_tests.keys():
        print('     - {}:'.format(test_name))
        for mark in wrong_marked_tests[test_name]['Marks']:
            print('         - {}'.format(mark))
    print('\33[0m' + '-------------------------------------------------------------------------')

    # Print unmarked tests
    print('\33[91m' + 'Unmarked tests: {}'.format(len(unmarked_tests)))
    for test in unmarked_tests:
        print('     - {}'.format(test))
    print('\33[0m' + '-------------------------------------------------------------------------')

# ======================================================================================================================