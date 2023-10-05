import pytest
from utilities.home.webdriverFactory import WebDriverFactory


# @pytest.yield_fixture()
# def setUp():
#     print("Running method level setUp")
#     yield
#     print("Running method level tearDown")

@pytest.fixture()
def setUp(request, browser):
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def oneTimeSetUp(request, browser):
    # print("Running one time setUp")
    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    # print("Running one time tearDown")


def pytest_addoption(parser):
    parser.addoption('--browser', '--repeat', action='store')


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

def pytest_generate_tests(metafunc):
    if metafunc.config.option.repeat is not None:
        count = int(metafunc.config.option.repeat)

        # We're going to duplicate these tests by parametrizing them,
        # which requires that each test has a fixture to accept the parameter.
        # We can add a new fixture like so:
        metafunc.fixturenames.append('tmp_ct')

        # Now we parametrize. This is what happens when we do e.g.,
        # @pytest.mark.parametrize('tmp_ct', range(count))
        # def test_foo(): pass
        metafunc.parametrize('tmp_ct', range(count))