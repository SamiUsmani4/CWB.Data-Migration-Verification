import os
import unittest
import pandas as pd
import pytest
from time import sleep
from datetime import datetime
from tests.home.DataMigration2 import DataMigration2
from utilities.home.seleniumDriver import SeleniumDriver


@pytest.mark.filterwarnings("ignore::RuntimeWarning")
@pytest.mark.usefixtures("setUp")
class Sandbox(unittest.TestCase, SeleniumDriver):
    @pytest.fixture(autouse=True)
    def classSetup(self, setUp):
        self.md = DataMigration2(self.driver)

    _url_sit2 = 'https://t24sit2.cwb.local/BrowserWeb/servlet/BrowserServlet'
    _url_sitdig = "https://t24sitdig.cwb.local/BrowserWeb/servlet/BrowserServlet"
    _url_uatdig = "https://t24uatdig.cwb.local/BrowserWeb/servlet/BrowserServlet"

    def testing11(self):
        filePath = f"G:\\QA\\Automation Team\\Data Migration R-1.2\\dataBusiness.csv"
        df = pd.read_csv(filePath, encoding='utf-8')
        for n in range(len(df)):
            if df['Tested'][n] != 'Y':
                currTime = datetime.now()
                print(f'\n', df['PAN'][n], 'Started at:  ', currTime)
                accountType = str(df['AccountType'][n])
                panNumber = str(df['PAN'][n])
                loginID = str(df['PAN'][n])[-8:]
                passWrd = str(df['Password'][n])
                cifPersonal = str(df['PCIF'][n])
                cifBusiness = str(df['BCIF'][n])
                self.md.executeTest(panNumber, loginID, passWrd, cifPersonal, cifBusiness, accountType)

    def testing12(self):
        panNumber = "5858311010124223"
        t24AccountDet = self.md.T24DataRetail(panNumber)
        print(f"t24AccountDet= {t24AccountDet}")

    def testing13(self):
        panNumber = "CWB.5858311011175273"
        cifBusiness = "816065"
        cifPersonal = "816063"
        t24AccountDet = self.md.T24DataBusiness(panNumber, cifPersonal, cifBusiness)
        print(f"t24AccountDet= {t24AccountDet}")

    def testing14(self):
        loginID = "11175273"
        accountType = "Business"
        passWrd = "Cwb@1234"
        infAccountDet = self.md.InfinityVerification(loginID, passWrd, accountType)
        print(f"infAccountDet= {infAccountDet}")

    # testing15 is set up to update 'Mgt to DBX' in 'CARD.ACCESS, DMI' and 'CARD.ISSUE, DMI' of T24
    # PAN must be complete number with .000 (eg: CWB.5858311010125105.000)
    # pytest tests\home\DMProject.py::Sandbox::testing15 -v -s
    def testing15(self):
        # filePath = f"C:\\Data Migration R-1.2\\DBX_Landon_05152023.csv"
        filePath = f"C:\\Data Migration R-1.2\\DBX_Harish_05172023.csv"
        df = pd.read_csv(filePath, encoding='utf-8')

        # self.md.T24login("USMANIS3", "Sk!p2020", self._url_uatdig)
        self.md.T24login("USMANIS3", "Sk!p2020", self._url_sitdig)
        # self.md.T24login("USMANIS3", "Sk!p2021", self._url_sit2)
        sleep(2)

        for n in range(len(df)):
            if df['Tested'][n] != 'Y':
                currTime = datetime.now()
                print(f'\n', df['PAN'][n], 'Started at:  ', currTime)
                panNumber = str(df['PAN'][n])
                self.md.T24DataBusiness2(panNumber)

    def testing16(self):
        filePath = f"C:\\Data Migration R-1.2\\Sahil_inf.csv"
        df = pd.read_csv(filePath, encoding='utf-8')
        for n in range(len(df)):
            loginID = str(df['username'][n])
            passWrd = str(df['password'][n])
            accType = "Retail"

            self.md.InfinityVerification2(loginID, passWrd, accType)
