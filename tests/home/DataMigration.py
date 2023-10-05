import csv
import shutil
import pdb
import unittest
from datetime import datetime
from time import sleep
from tempfile import NamedTemporaryFile
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from utilities.home.seleniumDriver import SeleniumDriver

today = datetime.today()
tDate = today.strftime("%Y%m%d")


class DataMigration(SeleniumDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _signIn = "sign-in"
    _username = "signOnName"
    _password = "password"
    _new_password = 'oldPassword'
    _new_password2 = 'password'

    _contButton = "//input[@id='frmPreTermsandCondition_btnProceed']"
    _commandLine = "//input[@id='commandValue']"
    _basicDetail = "//a/span[text()='Basic Details']"
    _viewBasicDetail = "//img[@title='View Basic Details']"
    _btnCommit = "//img[@title='Commit the deal']"
    _btnValidt = "//img[@title='Validate a deal']"
    _btnGo = "//img[@id='cmdline_img']"
    # T24 URLs
    _url_sit1 = "https://t24sit1ag.cwb.local/BrowserWeb/servlet/BrowserServlet"
    _url_sit2 = 'https://arit24sit2.cwb.local/BrowserWeb/servlet/BrowserServlet'
    _url_sitdig = "https://t24sitdig.cwb.local/BrowserWeb/servlet/BrowserServlet"
    _url_diguat = "https://t24uatdig.cwb.local/BrowserWeb/servlet/BrowserServlet"
    _url_opsupport = "https://t24sptdig.cwb.local/BrowserWeb/"
    _url_dmmDIG = "https://t24ddmdig.cwb.local/BrowserWeb/servlet/BrowserServlet"

    def T24login(self, username, password, _url):
        self.driver.get(_url)

        self.sendKeys(username, self._username)
        self.sendKeys(password, self._password)
        self.elementClick(self._signIn)
        try:
            newPass = self.driver.find_element(By.ID, self._new_password)
            newPas2 = self.driver.find_element(By.ID, self._new_password2)
            newPass.send_keys(password)
            newPas2.send_keys(password)
            self.elementClick('goButton')
        except NoSuchElementException:
            print('No Need to Reset Password')

    def infinityLogin(self, loginID, passWrd):
        panField = self.driver.find_element(By.ID, "idp-discovery-username")
        nextButton = self.driver.find_element(By.ID, "idp-discovery-submit")
        panField.send_keys(loginID)
        nextButton.click()

        pacField = self.driver.find_element(By.ID, "okta-signin-password")
        loginButton = self.driver.find_element(By.ID, "okta-signin-submit")
        pacField.send_keys(passWrd)
        loginButton.click()
        sleep(2)

    def InfinityVerification(self, loginID, passWrd, accountType):
        # DigUAT
        url = "https://diguatr11.cwb.digital/apps/cwbDigital/#_frmLogin"
        # SITDIG
        # url = "https://cwb-qa04.temenoscloudna.com/apps/KonyOLB/#_frmLogin"
        # OP-SUPPORT
        # url = "https://opsupport.cwb.digital/apps/cwbDigital/"
        # DMM Environment
        # url = "https://cwb-dev03.temenoscloudna.com/apps/KonyOLB/#_frmLogin"

        if accountType == "Business":
            _frmNam = "frmBBAccountsLanding"
        else:
            _frmNam = "frmAccountsLanding"

        # pan = str(panNumber)[12:21]
        self.driver.get(url)
        sleep(5)
        self.infinityLogin(loginID, passWrd)

        headingText1 = self.driver.find_element(By.XPATH, '//div[@id="frmLogin_OktaLogin"]').text
        if "Set up multifactor authentication" in headingText1:
            if "cwb-qa04" in url:
                secText = self.driver.find_element(By.XPATH,
                                    '//*[starts-with(@id,"form")]/div/div[2]/div/ul/li[4]/div[2]/div/a')
                secText.click()

                secField = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'input')]")
                secField.send_keys("test")
            else:
                secText = self.driver.find_element(By.XPATH,
                                    '//*[starts-with(@id,"form")]/div/div[2]/div/ul/li[3]/div[2]/div/a')
                secText.click()
                # "input136")

                secField = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'input')]")
                secField.send_keys("test")

            saveButton = self.driver.find_element(By.XPATH, '//*[starts-with(@id, "form")]/div[2]/input')
            saveButton.click()
            sleep(5)
            finishButton = self.driver.find_element(By.XPATH, '//*[starts-with(@id, "form")]/div[2]/input')
            finishButton.click()
            sleep(5)

            # self.infinityLogin(pan)

        elif "Security Question" in headingText1:
            # headingText = self.driver.find_element(By.XPATH, '//*[@id="form79"]/div[1]/h2').text
            # if headingText == "Security Question":
            expectedSecQues = "What is the food you least liked as a child?"
            eleSecQues = self.driver.find_element(By.XPATH, '//label[starts-with(@for, "input")]').text
            secQues = eleSecQues.rstrip()
            if secQues != expectedSecQues:
                print("Security Question mismatched...")
            else:
                secField = self.driver.find_element(By.XPATH, "//input[starts-with(@id, 'input')]")
                verifyButton = self.driver.find_element(By.XPATH, '//*[starts-with(@id, "form")]/div[2]/input')
                secField.send_keys("test")
                verifyButton.click()
                sleep(5)
        try:
            agreeBox = self.driver.find_element(By.XPATH, '//*[@id="frmPreTermsandCondition_lblFavoriteEmailCheckBox"]')
            agreeBox.click()

            contButton = self.driver.find_element(By.XPATH, self._contButton)
            contButton.click()
            sleep(5)
        except NoSuchElementException:
            print("Terms and Conditions already Agreed. Page not displayed.")
        try:
            # phoneNo = self.driver.find_element(By.XPATH, f"//*[@id='{_frmNam}_tbxPhoneNum1']")
            # emailAd = self.driver.find_element(By.XPATH, f"//*[@id='{_frmNam}_tbxEmail1']")
            # phoneNo.send_keys("(780) 540-5400")
            # emailAd.send_keys("test.new@email.com")
            contBut = self.driver.find_element(By.XPATH, f"//input[@id='{_frmNam}_btnProceedCreate']")
            contBut.click()
            sleep(5)
            lblPhone = self.driver.find_element(By.XPATH, f"//div[@id='{_frmNam}_lblPhoneNo1']").text
            lblEmail = self.driver.find_element(By.XPATH, f"//div[@id='{_frmNam}_lblEmail1']").text
            # print("Phone#: ", lblPhone)
            # print("email Address: ", lblEmail)
            confirmButton = self.driver.find_element(By.XPATH, f"//input[@id='{_frmNam}_btnConfirm']")
            confirmButton.click()
        except ElementNotInteractableException:
            print("Contact Information already verified. Page not displayed.")

        # parentHandle = self.driver.current_window_handle
        # innerHandles = self.driver.window_handles
        # for innerHandle in innerHandles:
        #     if innerHandle not in innerHandles:
        #         self.driver.switch_to.window(innerHandle)
        #         try:
        #             # phoneNo = self.driver.find_element(By.XPATH, f"//*[@id='{_frmNam}_tbxPhoneNum1']")
        #             # emailAd = self.driver.find_element(By.XPATH, f"//*[@id='{_frmNam}_tbxEmail1']")
        #             # phoneNo.send_keys("(780) 540-5400")
        #             # emailAd.send_keys("test.new@email.com")
        #             contBut = self.driver.find_element(By.XPATH, f"//input[@id='{_frmNam}_btnProceedCreate']")
        #             contBut.click()
        #             sleep(10)
        #             lblPhone = self.driver.find_element(By.XPATH, f"//div[@id='{_frmNam}_lblPhoneNo1']").text
        #             lblEmail = self.driver.find_element(By.XPATH, f"//div[@id='{_frmNam}_lblEmail1']").text
        #             print("Phone#: ", lblPhone)
        #             print("email Address: ", lblEmail)
        #             confirmButton = self.driver.find_element(By.XPATH, f"//input[@id='{_frmNam}_btnConfirm']")
        #             confirmButton.click()
        #         except NoSuchElementException:
        #             print("Contact Information already verified. Page not displayed.")

        try:
            sQues = self.driver.find_element(By.ID, "frmOktaSecurityQuestions_lstBoxSelectSecurityQuestion")
            sel = Select(sQues)
            sel.select_by_index(1)

            sAns = self.driver.find_element(By.XPATH, "//input[@id='frmOktaSecurityQuestions_tbxSecurityQuestionAnswer']")
            sAns.send_keys("test")

            btnConfirm = self.driver.find_element(By.XPATH, "//input[@id='frmOktaSecurityQuestions_btnConfirm']")
            btnConfirm.click()
        except NoSuchElementException:
            print("Security Question/Answer already setup. Page not displayed.")

        rowData = []
        infData = []
        # if accountType == "Business":
        #     self.waitForElement("//div[@id='frmBBAccountsLanding_accountList']")
        #     eleList = self.driver.find_elements(By.XPATH, "//*[@id='frmBBAccountsLanding_accountList_segAccounts']")
        # else:
        #     self.waitForElement("//div[@id='frmAccountsLanding_accountList']")
        #     eleList = self.driver.find_elements(By.XPATH, "//*[@id='frmAccountsLanding_accountList_segAccounts']")
        self.waitForElement(f"//div[@id='{_frmNam}_accountList']")
        sleep(5)
        eleList = self.driver.find_elements(By.XPATH, f"//*[@id='{_frmNam}_accountList_segAccounts']")
        for each_ul in eleList:
            all_li = each_ul.find_elements(By.TAG_NAME, "li")
            for li in all_li:
                liText = li.text
                rowData.append(liText.splitlines())
        for r in range(len(rowData)):
            tmpData = []
            if rowData[r][0] == 'k':
                tmpData.append(rowData[r][1])
                tmpData.append(rowData[r][2][-12:])
                # print(rowData[r][3])
                amt = rowData[r][3].replace("$", "")
                if rowData[r][1][0:4] == "Line":
                    amt = amt.replace("-", "")
                amt = amt.replace("USD ", "")
                tmpData.append(amt)

                infData.append(tmpData)
        # Profile Information
        # if accountType == "Business":
        #     eleMenu = self.driver.find_element(By.ID, 'frmBBAccountsLanding_customheader_topmenu_imgMenu')
        # else:
        #     eleMenu = self.driver.find_element(By.ID, 'frmAccountsLanding_customheader_topmenu_imgMenu')
        # eleMenu.click()
        #
        # if accountType == "Business":
        #     eleSetting = self.driver.find_element(By.ID, 'frmBBAccountsLanding_customheader_customhamburger_SettingslblAccounts')
        # else:
        #     eleSetting = self.driver.find_element(By.ID, 'frmAccountsLanding_customheader_customhamburger_SettingslblAccounts')
        # eleSetting.click()
        #
        # if accountType == "Business":
        #     eleProfile = self.driver.find_element(By.ID, 'frmBBAccountsLanding_customheader_customhamburger_Settings0lblMyAccounts')
        # else:
        #     eleProfile = self.driver.find_element(By.ID, 'frmAccountsLanding_customheader_customhamburger_Settings0lblMyAccounts')
        # eleProfile.click()
        # sleep(10)

        eleMenu = self.driver.find_element(By.ID, f'{_frmNam}_customheader_topmenu_imgMenu')
        eleMenu.click()

        eleSetting = self.driver.find_element(By.ID, f'{_frmNam}_customheader_customhamburger_SettingslblAccounts')
        eleSetting.click()

        eleProfile = self.driver.find_element(By.ID, f'{_frmNam}_customheader_customhamburger_Settings0lblMyAccounts')
        eleProfile.click()
        sleep(5)

        eleName = self.driver.find_element(By.ID, 'frmProfileManagement_settings_lblNameValue').text
        eleMobile = self.driver.find_element(By.ID, 'frmProfileManagement_settings_lblMobileValue').text
        eleEmail = self.driver.find_element(By.ID, 'frmProfileManagement_settings_lblEmailIdValue').text
        # print("Name: ", eleName)
        # print("Mobile: ", eleMobile)
        # print("Email: ", eleEmail)
        infDetail = [eleName, eleMobile, eleEmail]
        infData.append(infDetail)

        return infData

    def accountsDetails(self):
        _acts = "//table[starts-with(@id,'datadisplay_AccountDetails')]/tbody"
        _tbl = "//table[starts-with(@id,'headtab_main')]/tbody/tr"
        AccountDetail = []
        # Accounts Tab
        r = 0
        xcpn = True
        while xcpn:
            try:
                acctDet0 = []
                rowData = {}
                r += 1
                accountsNo = self.driver.find_element(By.XPATH, f"{_acts}/tr[" + str(r) + "]/td[3]")
                shortTitle = self.driver.find_element(By.XPATH, f"{_acts}/tr[" + str(r) + "]/td[5]")
                workingBal = self.driver.find_element(By.XPATH, f"{_acts}/tr[" + str(r) + "]/td[11]")
                #
                # acctNo = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                 r) + ']/td[3]')
                # prodNm = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[4]')
                # shtTit = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[5]')
                # appRel = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[6]')
                # onrNam = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[7]')
                # ccyCod = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[10]')
                # wrkBal = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[11]')
                # lckAmt = self.driver.find_element(By.XPATH,
                #                             '//table[starts-with(@id,"datadisplay_AccountDetails")]/tbody/tr[' + str(
                #                                       r) + ']/td[13]')
                #
                # rowData = {"Product": prodNm.text, "Account": acctNo.text, "Relation": appRel.text, "Owner": onrNam.text,
                #            "Currency": ccyCod, "Working Bal": wrkBal.text, "Locked Amount": lckAmt.text}
                # 
                # AccountDetail.append(rowData)

                if workingBal.text == "":
                    wrkBalance = "0.00"
                else:
                    wrkBalance = workingBal.text.rstrip()
                acctDet0.append(shortTitle.text.rstrip())
                acctDet0.append(accountsNo.text.rstrip())
                acctDet0.append(wrkBalance)
                AccountDetail.append(acctDet0)

            except NoSuchElementException:
                xcpn = False

        # Deposits Tab
        depositTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[2]/a//span[text()='Deposits']")
        depositTab.click()
        # self.driver.maximize_window()
        tr = 0
        xcpn = True
        while xcpn:
            tr += 1
            tmpLst = []
            try:
                readAccNo = self.driver.find_element(By.XPATH,
                                                     f"//tr[starts-with(@id, 'r{tr}_DepositDetailEnquiry')]/td[3]")
                readPrdNm = self.driver.find_element(By.XPATH,
                                                     f"//tr[starts-with(@id, 'r{tr}_DepositDetailEnquiry')]/td[4]")
                readShtTl = self.driver.find_element(By.XPATH,
                                                     f"//tr[starts-with(@id, 'r{tr}_DepositDetailEnquiry')]/td[5]")
                readCrBal = self.driver.find_element(By.XPATH,
                                                     f"//tr[starts-with(@id, 'r{tr}_DepositDetailEnquiry')]/td[10]")
                tmpLst.append(readShtTl.text.rstrip())
                tmpLst.append(readAccNo.text.rstrip())
                tmpLst.append(readCrBal.text.rstrip())

                AccountDetail.append(tmpLst)
            except NoSuchElementException:
                xcpn = False

        # Loans Tab
        loanTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[3]/a//span[text()='Loans']")
        loanTab.click()
        # self.driver.maximize_window()
        tr = 0
        xcpn = True
        while xcpn:
            tr += 1
            tmpLst = []
            try:
                readStats = self.driver.find_element(By.XPATH,
                                                     f"//tr[starts-with(@id, 'r{tr}_LoanDetailsEnquiry')]/td[15]")
                if readStats.text == 'CURRENT' or readStats.text == 'AUTH':
                    readAccNo = self.driver.find_element(By.XPATH,
                                                         f"//tr[starts-with(@id, 'r{tr}_LoanDetailsEnquiry')]/td[3]")
                    readPrdNm = self.driver.find_element(By.XPATH,
                                                         f"//tr[starts-with(@id, 'r{tr}_LoanDetailsEnquiry')]/td[4]")
                    readShtTl = self.driver.find_element(By.XPATH,
                                                         f"//tr[starts-with(@id, 'r{tr}_LoanDetailsEnquiry')]/td[5]")
                    readPrBal = self.driver.find_element(By.XPATH,
                                                         f"//tr[starts-with(@id, 'r{tr}_LoanDetailsEnquiry')]/td[10]")
                    tmpLst.append(readShtTl.text.rstrip())
                    tmpLst.append(readAccNo.text.rstrip())
                    tmpLst.append(readPrBal.text.rstrip())

                    AccountDetail.append(tmpLst)
            except NoSuchElementException:
                xcpn = False

        # Registered Product Tab
        regProdTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[5]/a//span[text()='Registered Product']")
        regProdTab.click()
        # self.driver.maximize_window()

        # # Registered RSP
        regRSPTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[1]/a//span[text()='Registered RSP']")
        regRSPTab.click()

        tr = 0
        xcpn = True
        while xcpn:
            tr += 1
            tmpLst = []
            try:
                accountNos = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_FRAMEONE')]/td[6]")
                shortTitle = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_FRAMEONE')]/td[8]")
                accountVal = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_FRAMEONE')]/td[9]")
                tmpLst.append(shortTitle.text.rstrip())
                tmpLst.append(accountNos.text.rstrip())
                tmpLst.append(accountVal.text.rstrip())

                AccountDetail.append(tmpLst)
            except NoSuchElementException:
                xcpn = False

        # # Registered RIF
        regRIFTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[2]/a//span[text()='Registered RIF']")
        regRIFTab.click()

        tr = 0
        xcpn = True
        while xcpn:
            tr += 1
            tmpLst = []
            try:
                accountNos = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVRRIF')]/td[7]")
                shortTitle = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVRRIF')]/td[9]")
                accountVal = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVRRIF')]/td[10]")
                tmpLst.append(shortTitle.text.rstrip())
                tmpLst.append(accountNos.text.rstrip())
                tmpLst.append(accountVal.text.rstrip())

                AccountDetail.append(tmpLst)
            except NoSuchElementException:
                xcpn = False

        # # Registered TFSA
        regTFSTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[3]/a//span[text()='Registered TFSA']")
        regTFSTab.click()

        tr = 0
        xcpn = True
        while xcpn:
            tr += 1
            tmpLst = []
            try:
                accountNos = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVTFSA')]/td[4]")
                shortTitle = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVTFSA')]/td[6]")
                accountVal = self.driver.find_element(By.XPATH, f"//tr[starts-with(@id, 'r{tr}_SCVTFSA')]/td[7]")
                tmpLst.append(shortTitle.text.rstrip())
                tmpLst.append(accountNos.text.rstrip())
                tmpLst.append(accountVal.text.rstrip())

                AccountDetail.append(tmpLst)
            except NoSuchElementException:
                xcpn = False
        return AccountDetail

    def T24DataBusiness(self, panNumber, cifPersonal, cifBusiness):
        panNumber = str(panNumber)[12:21]
        global childHandle
        self.T24login("USMANIS3", "Sk!p2021", self._url_diguat)
        sleep(2)

        self.waitForElement("//frame[contains(@id,'banner')]", locatorType='xpath')
        iframe = self.driver.find_element(By.XPATH, "//frame[contains(@id,'banner')]")
        self.driver.switch_to.frame(iframe)

        cmdLine = self.driver.find_element(By.XPATH, "//*[@id='commandValue']")
        cmdLine.send_keys("CARD.ACCESS,DMI")
        btnGo = self.driver.find_element(By.XPATH, self._btnGo)
        btnGo.click()

        parentHandler = self.driver.current_window_handle
        handles = self.driver.window_handles
        for handle in handles:
            if handle not in parentHandler:
                self.driver.switch_to.window(handle)
                self.driver.maximize_window()
                try:
                    trnLine = self.driver.find_element(By.XPATH,
                            "/html/body/div[3]/div[2]/form[1]/div[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td[2]/input[1]")
                    trnLine.send_keys(panNumber)

                    btnGo = self.driver.find_element(By.XPATH, "//*[@id='goButton']/tbody/tr/td/table/tbody/tr/td[1]/a/img")
                    btnGo.click()

                    mdsbDt = self.driver.find_element(By.XPATH, "//*[@id='fieldName:MDSB.DISC.DATE']")
                    mdsbDt.send_keys(tDate)
                    self.driver.find_element(By.CSS_SELECTOR,
                                             "input[type='radio'][id='radio:tab1:MDSB.OPTED'][value='YES']").click()
                    self.driver.find_element(By.CSS_SELECTOR,
                                             "input[type='radio'][id='radio:tab1:MIGRT.TO.DBX'][value='Y']").click()
                    mdiOnline = self.driver.find_element(By.XPATH, "//*[@id='tab1']/tbody/tr[98]/td[3]/select")
                    selection = Select(mdiOnline)
                    selection.select_by_index(2)

                    btnCmt = self.driver.find_element(By.XPATH,
                                                      "//*[@id='goButton']/tbody/tr/td/table/tbody/tr/td[1]/a/img")
                    btnCmt.click()
                    self.takeScreenshot(self.driver, f"T24_DMX Update {panNumber}")
                    sleep(10)
                except NoSuchElementException:
                    errMsg = self.driver.find_element(By.XPATH, "//*[@id='messages']").text
                    print(f"\n{errMsg}\nError: Element not found")
        self.driver.close()
        self.driver.switch_to.window(parentHandler)

        # -----------------------------------------------------------------------------------
        # Accounts Detail
        # -----------------------------------------------------------------------------------
        self.performFind(cifBusiness, typ='b')
        accDetail = self.accountsDetails()
        # print(accDetail)

        # -----------------------------------------------------------------------------------
        # Update PAC
        # -----------------------------------------------------------------------------------
        # self.updatePAC(parentHandler, panNumber)
        # Did not test and complete as Malik advised that Prasanthi's got a code to reset the password in T24 before running DM
        #  Stopped working 2022-06-03
        # -----------------------------------------------------------------------------------
        innerHandles = self.driver.window_handles
        size = len(innerHandles) - 1
        for r in range(size, 0, -1):
            self.driver.switch_to.window(innerHandles[r])
            self.driver.close()
        # self.driver.switch_to.window(innerHandles[0])
        self.driver.switch_to.window(parentHandler)

        # -----------------------------------------------------------------------------------
        # Basic Details
        # -----------------------------------------------------------------------------------
        self.performFind(cifPersonal, typ='p')
        self.elementClick(self._basicDetail, locatorType='xpath')
        self.elementClick(self._viewBasicDetail, locatorType='xpath')

        innerHandles = self.driver.window_handles
        scrNo = len(innerHandles) - 1

        self.driver.switch_to.window(innerHandles[scrNo])
        self.driver.maximize_window()

        GBFullName = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[10]/td[3]/span").text
        fullName = GBFullName
        email = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[21]/td[4]/span").text
        contact = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[20]/td[7]/span").text
        phoneNo = contact[-10:]
        phoneNo = '+1 (' + phoneNo[:3] + ') ' + phoneNo[3:6] + '-' + phoneNo[6:10]

        basDetail = [fullName, phoneNo, email]
        # print(basDetail)

        accDetail.append(basDetail)

        innerHandles = self.driver.window_handles
        size = len(innerHandles) - 1
        for r in range(size, 0, -1):
            self.driver.switch_to.window(innerHandles[r])
            self.driver.close()
        self.driver.switch_to.window(innerHandles[0])

        return accDetail
        # -----------------------------------------------------------------------------------

    def T24DataRetail(self, panNumber):
        global accountDet
        try:
            # handles = self.customerCentricView('Customer number(CIF)', '805824')
            panNumber = str(panNumber)[12:21]
            # handles = self.customerCentricView('Card Number', panNumber)
            # self.T24login("USMANIS3", "Sk!p2021", self._url_sitdig)
            global childHandle
            self.T24login("USMANIS3", "Sk!p2021", self._url_diguat)
            sleep(2)

            # -----------------------------------------------------------------------------------
            self.waitForElement("//frame[contains(@id,'menu')]", locatorType='xpath')
            iframe = self.driver.find_element(By.XPATH, "//frame[contains(@id,'menu')]")
            self.driver.switch_to.frame(iframe)

            menuOptionPath = f"//div[@id='pane_']//span[text()='Full Service']"
            # print(f"Main Menu Path: {menuOptionPath}")
            menuOptionT24 = self.driver.find_element(By.XPATH, menuOptionPath)
            actions = ActionChains(self.driver)
            actions.move_to_element(menuOptionT24).perform()
            menuOptionT24.click()
            parentHandler = self.driver.current_window_handle

            sleep(2)
            targetPath = f"{menuOptionPath}//following-sibling::ul//a[contains(text(),'Customer Centric View')]"
            # print(f"Target Path: {targetPath}")
            subMenuLink = self.driver.find_element(By.XPATH, targetPath)
            subMenuLink.click()

            handles = self.driver.window_handles
            for handle in handles:
                if handle not in parentHandler:
                    childHandle = handle
            # -----------------------------------------------------------------------------------
            self.driver.switch_to.window(childHandle)
            sleep(2)

            clearForm = self.driver.find_element(By.XPATH,
            "//*[@id='enqsel']/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a")
            clearForm.click()

            searchField = self.driver.find_element(By.XPATH,
                                                   f"//table[@id='selectiondisplay']//span[text()='Card Number']"
                                                   f"//parent::td//following-sibling::td[2]//input")
            searchField.clear()

            searchField.send_keys(panNumber)
            self.elementClick("//a[text()='Find']", locatorType='xpath')

            self.elementClick("//img[@title='Customer Centric View']", locatorType='xpath')
            # -----------------------------------------------------------------------------------

            # Accounts Detail
            self.driver.maximize_window()
            accountDet = self.accountsDetails()

            # Basic Details
            self.elementClick(self._basicDetail, locatorType='xpath')
            self.elementClick(self._viewBasicDetail, locatorType='xpath')

            innerHandles = self.driver.window_handles
            scrNo = len(innerHandles) - 1

            self.driver.switch_to.window(innerHandles[scrNo])
            self.driver.maximize_window()

            fullName = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[10]/td[3]/span").text
            contact = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[20]/td[7]/span").text
            phoneNo = contact[-10:]
            phoneNo = '+1 (' + phoneNo[:3] + ') ' + phoneNo[3:6] + '-' + phoneNo[6:10]
            email = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[21]/td[4]/span").text
            basDetail = [fullName, phoneNo, email]
            accountDet.append(basDetail)
        except NoSuchElementException:
            print("Element Not Found")

        innerHandles = self.driver.window_handles
        size = len(innerHandles) - 1
        for r in range(size, 0, -1):
            self.driver.switch_to.window(innerHandles[r])
            self.driver.close()
        self.driver.switch_to.window(innerHandles[0])

        return accountDet

    def executeTest(self, panNumber, loginID, passWrd, cifPersonal, cifBusiness, accountType):
        filename = f"G:\\QA\\Automation Team\\Data Migration R-1.2\\DM_Data_T3.csv"
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        if accountType == "Business":
            T24Data = self.T24DataBusiness(panNumber, cifPersonal, cifBusiness)
        else:
            T24Data = self.T24DataRetail(panNumber)
        sleep(10)

        infinityData = self.InfinityVerification(loginID, passWrd, accountType)
        T24Data.sort()
        infinityData.sort()
        print("     T24 Data: ", T24Data)
        print("Infinity Data: ", infinityData)

        tstResult = 'PASSED'
        verification_errors = []
        dtaMismatch = []
        z = len(T24Data) - 1
        try:
            for i in range(len(T24Data)):
                for x in range(len(T24Data[i])):
                    if infinityData[i][x] != T24Data[i][x]:
                        if i != z:
                            if x == 0: dtaMismatch.append(' Account# Mismatched')
                            if x == 1: dtaMismatch.append(' Balance Amount Mismatched')
                            if x == 2: dtaMismatch.append(' Account Name Mismatched')
                        else:
                            if x == 0: dtaMismatch.append(' Contact Name Mismatched')
                            if x == 1: dtaMismatch.append(' Phone# Mismatched')
                            if x == 2: dtaMismatch.append(' eMail Mismatched')
                try:
                    if infinityData[i] == T24Data[i]:
                        verification_errors.append([panNumber, T24Data[i], infinityData[i]])

                    # assert infinityData[i] == T24Data[i], \
                    #     f"Check value in the list \nT24 Data: {T24Data[i]}\nInfinity Data: {infinityData[i]}"
                    # # self.verification_errors.append([T24Data[i], infinityData[i]])
                except AssertionError as exception:
                    print("Assertion failed.")
                    verification_errors.append([panNumber, T24Data[i], infinityData[i]])
                    tstResult = 'FAILED'
                    self.takeScreenshot(self.driver, f"FAILED_Verification {panNumber}")
        except IndexError:
            pass
        # ---------------------------------------------------------------------------
        fields = ['LoginID', 'AccountType', 'BCIF', 'PCIF', 'PAN', 'Password', 'Tested', 'Result', 'Comments']
        with open(filename, 'r') as csvfile, tempfile:
            reader = csv.DictReader(csvfile, fieldnames=fields)
            writer = csv.DictWriter(tempfile, fieldnames=fields)
            for row in reader:
                if row['LoginID'] == str(loginID):
                    print('updating row', row['LoginID'])
                    row['Tested'], row['Result'], row['Comments'] = 'Y', tstResult, dtaMismatch #verification_errors
                row = {
                        'LoginID': row['LoginID'],
                        'AccountType': row['AccountType'],
                        'BCIF': row['BCIF'],
                        'PCIF': row['PCIF'],
                        'PAN': row['PAN'],
                        'Password': row['Password'],
                        'Tested': row['Tested'],
                        'Result': row['Result'],
                        'Comments': row['Comments']
                       }
                writer.writerow(row)

        shutil.move(tempfile.name, filename)
        # ---------------------------------------------------------------------------
        print(accountType, " ", panNumber, " Completed")

        return

    def performFind(self, cifNumber, typ):
        global childHandle
        self.waitForElement("//frame[contains(@id,'menu')]", locatorType='xpath')
        iframe = self.driver.find_element(By.XPATH, "//frame[contains(@id,'menu')]")
        self.driver.switch_to.frame(iframe)
        menuOptionPath = f"//div[@id='pane_']//span[text()='Full Service']"
        # print(f"Main Menu Path: {menuOptionPath}")
        menuOptionT24 = self.driver.find_element(By.XPATH, menuOptionPath)
        actions = ActionChains(self.driver)
        actions.move_to_element(menuOptionT24).perform()
        if typ == 'b':
            menuOptionT24.click()

        parentHandler = self.driver.current_window_handle
        sleep(2)

        targetPath = f"{menuOptionPath}//following-sibling::ul//a[contains(text(),'Customer Centric View')]"
        # print(f"Target Path: {targetPath}")
        subMenuLink = self.driver.find_element(By.XPATH, targetPath)
        subMenuLink.click()

        handles = self.driver.window_handles
        for handle in handles:
            if handle not in parentHandler:
                childHandle = handle
        # -----------------------------------------------------------------------------------
        self.driver.switch_to.window(childHandle)
        sleep(2)

        clearForm = self.driver.find_element(By.XPATH,
            "//*[@id='enqsel']/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/a")
        clearForm.click()

        searchField = self.driver.find_element(By.XPATH,
             f"//table[@id='selectiondisplay']//span[text()='Customer number(CIF)']"
             f"//parent::td//following-sibling::td[2]//input")
        searchField.clear()

        searchField.send_keys(cifNumber)
        self.elementClick("//a[text()='Find']", locatorType='xpath')

        self.elementClick("//img[@title='Customer Centric View']", locatorType='xpath')
        # -----------------------------------------------------------------------------------

    def updatePAC(self, handles, panNumber):
        cmTab = self.driver.find_element(By.XPATH,
                                         '//table[contains(@id,"headtab_main")]//span[text()="Card Management"]')
        cmTab.click()
        sleep(1)
        checkImg = self.driver.find_element(By.XPATH,
                                            f'//tr[contains(@id,"ManageMemberCards")]//td[text()={panNumber[-8:]}]//following-sibling::td[10]//img')
        sleep(1)
        checkImg.click()
        innerHandles = self.driver.window_handles
        accountNos = []
        for innerHandle in innerHandles:
            if innerHandle not in innerHandles:
                self.driver.switch_to.window(innerHandle)
                # cardNumber = self.driver.find_element(By.XPATH,
                #                                       "//div[@id='toolBar']//span[contains(@class,'_CARDACCESS')]").text
                # print(cardNumber)
                # try:
                #     accountNames = self.driver.find_elements(By.XPATH,
                #                                              '//table[@id="tab1"]//span[contains(@id,"enri_ACCT.NO")]')
                #     for accountName in accountNames:
                #         print(accountName.text)
                #     accountnumbers = self.driver.find_elements(By.XPATH,
                #                                                '//table[@id="tab1"]//span[contains(@id,"disabled_ACCT.NO")]')
                #     for accountNumber in accountnumbers:
                #         accountNos.append(accountNumber.text)
                #         print(accountNumber.text)
                #
                #     self.driver.close()
                # except NoSuchElementException:
                #     print("Element Not Found")
                # self.driver.switch_to.window(childHandle)
                element = self.driver.find_element(By.XPATH,
                                                   f'//tr[contains(@id,"ManageMemberCards")]//td[text()={panNumber[-8:]}]'
                                                   f'//following-sibling::td[10]//select[contains(@id,"drillbox:")]')
                select = Select(element)
                # select by visible text
                select.select_by_visible_text("Update PAC")

                # checkImg = self.driver.find_element(By.XPATH, '//tr[contains(@id,"r1_ManageMemberCards")]//img')
                sleep(1)
                checkImg.click()
                innerHandles = self.driver.window_handles
                for handle in innerHandles:
                    if handle not in handles:
                        self.driver.switch_to.window(handle)
                        sleep(7)
                        clearPACnoRadioBtn = self.driver.find_element(By.XPATH,
                                                                      "//input[@id='radio:tab1:CA.CLR.PAC'][@value='NO']")
                        stateClearPAC = clearPACnoRadioBtn.get_attribute('selected')
                        # assert clearPACnoRadioBtn.get_attribute('selected') == 'true', \
                        #     f"CLear PAC? (Radio Btn)\nExpected: 'true' \nActual: {stateClearPAC}"

                        forcePACnoRadioBtn = self.driver.find_element(By.XPATH,
                                                                      "//input[@id='radio:tab1:FORCE.PAC.CHG'][@value='NO']")
                        stateForcePAC = forcePACnoRadioBtn.get_attribute('selected')
                        # assert forcePACnoRadioBtn.get_attribute('selected') == 'true', \
                        #     f"Force PAC Change(Radio Btn)\nExpected: 'true' \nActual: {stateForcePAC}"
                        self.takeScreenshot(self.driver, "Update PAC  ")

                        self.driver.close()
                        self.driver.switch_to.window(childHandle)

