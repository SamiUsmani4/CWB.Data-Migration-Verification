"""
@package base

WebDriver Factory class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriverFactory(browser)
    wdf.getWebDriverInstance()
"""
import traceback
from time import sleep

from selenium import webdriver


class WebDriverFactory:
    def __init__(self, browser):
        """
        Inits WebDriverFactory class

        Returns:
            None
        """
        self.browser = browser
    """
        Set chrome driver and iexplorer environment based on OS

        chromedriver = "C:/.../chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver
        self.driver = webdriver.Chrome(chromedriver)

        PREFERRED: Set the path on the machine where browser will be executed
    """

    def getWebDriverInstance(self):
        """
       Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """

        # Personal DCO Skip ALL (PIN, AML, CC, Fraud)
        # baseURL = "https://staging.cwb.avoka-transact.com/cwbank/servlet/SmartForm.html?formCode=cwb-pers-dco&testConfigProfile=skipPinFraudAmlCreditMock"

        # Motive DCO Skip ALL (PIN, AML, CC, Fraud)
        baseURL = "https://staging.cwb.avoka-transact.com/motivebank/servlet/SmartForm.html?formCode=dcompmotive&testConfigProfile=skipPinFraudAmlCreditMock"

        if self.browser == "ie":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            profile = webdriver.FirefoxProfile()
            profile.set_preference('network.http.phishy-userpass-length', 255)
            driver = webdriver.Firefox(firefox_profile=profile)
        elif self.browser == "edge":
            # Set chrome driver
            driver = webdriver.Edge()
        else:
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(options=options)

        # Setting Driver Implicit Time out for An Element
        driver.implicitly_wait(5)
        # Maximize the window
        driver.maximize_window()
        # Loading browser with App URL
        # driver.get(baseURL)
        sleep(2)
        return driver
