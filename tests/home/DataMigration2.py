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


class DataMigration2(SeleniumDriver):
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
    _url_sit2 = 'https://t24sit2.cwb.local/BrowserWeb/servlet/BrowserServlet'
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
        #
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
                # if rowData[r][1][0:4] == "Line":
                #     amt = amt.replace("-", "")
                amt = amt.replace("USD ", "")
                tmpData.append(amt)

                infData.append(tmpData)

        return infData

    def accountsDetails(self, typ):
        global allAccounts
        try:
            _tbl = "//table[starts-with(@id,'headtab_main')]/tbody/tr"
            customerTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[1]/a//span[text()='Customer Details']")
            customerTab.click()

            cHoldingTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[6]/a//span[text()='Client Holdings']")
            cHoldingTab.click()

            if typ == 'r':
                personalTab = self.driver.find_element(By.XPATH, f"{_tbl}/td[1]/a//span[text()='Personal']")
                personalTab.click()

                namTab = "CAD"
                cadTabP = self.driver.find_element(By.XPATH, f"{_tbl}/td[1]/a//span[text()='CAD']")
                cadTabP.click()
                cadAccounts = self.persAccounts(namTab)

                namTab = "USD"
                usdTabP = self.driver.find_element(By.XPATH, f"{_tbl}/td[2]/a//span[text()='USD']")
                usdTabP.click()
                usdAccounts = self.persAccounts(namTab)
            else:
                nonPersonal = self.driver.find_element(By.XPATH, f"{_tbl}/td[2]/a//span[text()='Non Personal']")
                nonPersonal.click()

                namTab = "CAD"
                cadTabP = self.driver.find_element(By.XPATH, f"{_tbl}/td[1]/a//span[text()='CAD']")
                cadTabP.click()
                cadAccounts = self.bussAccounts(namTab)

                namTab = "USD"
                usdTabP = self.driver.find_element(By.XPATH, f"{_tbl}/td[2]/a//span[text()='USD']")
                usdTabP.click()
                usdAccounts = self.bussAccounts(namTab)

            allAccounts = [cadAccounts, usdAccounts]

        except NoSuchElementException:
            msgBox = self.driver.find_element(By.XPATH, f"//table[@id='message']/tbody/tr[2]/td/table/tbody/tr/td").text
            print(f"Error Msg: {msgBox}")
        return allAccounts

    def persAccounts(self, namTab):
        print(f"Started...{namTab}, {datetime.now()}")
        global acctDim, acctTrn
        AccountDetail = []
        r = 0
        d = 1
        xcpn = True
        while xcpn:
            try:
                acctTrn = []
                r += 1
                d += 1
                for d in range(2, 9):
                    info = self.driver.find_element(By.XPATH, f"//table[starts-with(@id, 'r" + str(r) + "_workarea')]/td[" + str(d) + "]")
                    txt = info.text.rstrip()
                    if d == 7:
                        txt = namTab
                    if d == 8:
                        if info.text == "":
                            info = self.driver.find_element(By.XPATH, f"//table[starts-with(@id, 'r" + str(r) + "_workarea')]/td[" + str(d + 1) + "]")
                            if info.text == "":
                                txt = '0.00'
                            else:
                                txt = info.text
                    acctTrn.append(txt)
                if acctTrn[0] != "":
                    AccountDetail.append(acctTrn)
            except NoSuchElementException:
                xcpn = False
        # print(AccountDetail)
        return AccountDetail

    def bussAccounts(self, namTab):
        print(f"Started...{namTab}, {datetime.now()}")
        global acctDim, acctTrn
        AccountDetail = []
        r = 0
        d = 1
        xcpn = True
        while xcpn:
            try:
                acctTrn = []
                r += 1
                d += 1
                for d in range(2, 8):
                    info = self.driver.find_element(By.XPATH,
                                            f"//*[starts-with(@id, 'r" + str(r) + "_workarea')]/td[" + str(d) + "]")
                    txt = info.text.rstrip()
                    if d == 6:
                        acctTrn.append("")     # inserting an extra element for 'Joint' to match with retail
                        txt = namTab
                    if d == 7:
                        if info.text == "":
                            info = self.driver.find_element(By.XPATH,
                                            f"//*[starts-with(@id, 'r" + str(r) + "_workarea')]/td[" + str(d + 1) + "]")
                            if info.text == "":
                                txt = '0.00'
                            else:
                                txt = info.text
                    acctTrn.append(txt)
                if acctTrn[0] != "":
                    AccountDetail.append(acctTrn)
            except NoSuchElementException:
                xcpn = False
        # print(AccountDetail)
        return AccountDetail

    def T24DataBusiness(self, panNumber, cifPersonal, cifBusiness):
        panNumber = str(panNumber)[12:21]
        global childHandle
        self.T24login("USMANIS3", "Sk!p2021", self._url_dmmDIG)
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
        accDetail = self.accountsDetails(typ='b')
        # print(accDetail)

        # -----------------------------------------------------------------------------------
        # Update PAC
        # -----------------------------------------------------------------------------------
        # self.updatePAC(parentHandler, panNumber)
        # Did not test and complete as Malik advised that Prasanthi's got a code to reset the password in T24 before running DM
        #  Stopped further working 2022-06-03
        # -----------------------------------------------------------------------------------

        #No need of Personal data
        # innerHandles = self.driver.window_handles
        # size = len(innerHandles) - 1
        # for r in range(size, 0, -1):
        #     self.driver.switch_to.window(innerHandles[r])
        #     self.driver.close()
        # # self.driver.switch_to.window(innerHandles[0])
        # self.driver.switch_to.window(parentHandler)
        #
        # # -----------------------------------------------------------------------------------
        # # Basic Details
        # # -----------------------------------------------------------------------------------
        # self.performFind(cifPersonal, typ='p')
        # self.elementClick(self._basicDetail, locatorType='xpath')
        # self.elementClick(self._viewBasicDetail, locatorType='xpath')
        #
        # innerHandles = self.driver.window_handles
        # scrNo = len(innerHandles) - 1
        #
        # self.driver.switch_to.window(innerHandles[scrNo])
        # self.driver.maximize_window()
        #
        # GBFullName = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[10]/td[3]/span").text
        # fullName = GBFullName
        # email = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[21]/td[4]/span").text
        # contact = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[20]/td[7]/span").text
        # phoneNo = contact[-10:]
        # phoneNo = '+1 (' + phoneNo[:3] + ') ' + phoneNo[3:6] + '-' + phoneNo[6:10]
        #
        # basDetail = [fullName, phoneNo, email]
        # # print(basDetail)
        #
        # accDetail.append(basDetail)
        #
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
            panNumber = str(panNumber)[-8:]
            # handles = self.customerCentricView('Card Number', panNumber)
            # self.T24login("USMANIS3", "Sk!p2020", self._url_sitdig)
            global childHandle
            self.T24login("USMANIS3", "Sk!p2020", self._url_dmmDIG)
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
            accountDet = self.accountsDetails(typ='r')

            # # Basic Details
            # self.elementClick(self._basicDetail, locatorType='xpath')
            # self.elementClick(self._viewBasicDetail, locatorType='xpath')
            #
            # innerHandles = self.driver.window_handles
            # scrNo = len(innerHandles) - 1
            #
            # self.driver.switch_to.window(innerHandles[scrNo])
            # self.driver.maximize_window()
            #
            # fullName = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[10]/td[3]/span").text
            # contact = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[20]/td[7]/span").text
            # phoneNo = contact[-10:]
            # phoneNo = '+1 (' + phoneNo[:3] + ') ' + phoneNo[3:6] + '-' + phoneNo[6:10]
            # email = self.driver.find_element(By.XPATH, "//table[@id='mainTab']/tbody/tr[21]/td[4]/span").text
            # basDetail = [fullName, phoneNo, email]
            # accountDet.append(basDetail)
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
        filename = f"G:\\QA\\Automation Team\\Data Migration R-1.2\\DM_Data.csv"
        tempfile = NamedTemporaryFile(mode='w', delete=False)
        if accountType == "Business":
            T24Data = self.T24DataBusiness(panNumber, cifPersonal, cifBusiness)
        else:
            T24Data = self.T24DataRetail(panNumber)
        sleep(10)

        infinityData = self.InfinityVerification(loginID, passWrd, accountType)

        tstResult = 'PASSED'
        inf = []
        t24 = []
        mAct = []
        dtaMismatch = []
        for a in T24Data:
            for b in a:
                t24Temp = [b[2], b[0], b[6]]
                t24.append(t24Temp)
                mAct.append(b[0])
        for a in infinityData:
            inf.append(a)
        for a in inf:
            if a[1] not in mAct:
                dtaMismatch.append(f"{a} Not Found in T24")
                tstResult = 'FAILED'
            else:
                ctr = 0
                try:
                    while ctr <= len(t24):
                        if a[1] in t24[ctr]:
                            if a[0] != t24[ctr][0]:
                                dtaMismatch.append(f"Account Name Mismatched: {a[1]} > Inf: {a[0]}, T24: {t24[ctr][0]}")
                                tstResult = 'VERIFY'
                            if a[2] != t24[ctr][2]:
                                dtaMismatch.append(f"Amount Not Matched: {a[1]} > Inf: {a[2]}, T24: {t24[ctr][2]}")
                                tstResult = 'FAILED'
                        ctr += 1
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
                    row['Tested'], row['Result'], row['Comments'] = 'Y', tstResult, dtaMismatch
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
        print(f"{accountType} {panNumber} Completed")

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

    def T24DataBusiness2(self, panNumber):
        # panNumber = str(panNumber)[12:21]
        global childHandle

        # self.T24login("USMANIS3", "Sk!p2021", self._url_sit2)
        # sleep(2)
        #
        self.waitForElement("//frame[contains(@id,'banner')]", locatorType='xpath')
        iframe = self.driver.find_element(By.XPATH, "//frame[contains(@id,'banner')]")
        self.driver.switch_to.frame(iframe)

        cmdLine = self.driver.find_element(By.XPATH, "//*[@id='commandValue']")
        cmdLine.clear()
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
                    # self.takeScreenshot(self.driver, f"T24_DMX Update {panNumber}")
                    sleep(10)
                except NoSuchElementException:
                    errMsg = self.driver.find_element(By.XPATH, "//*[@id='messages']").text
                    print(f"\n{errMsg}\nError: Element not found")
        self.driver.close()
        self.driver.switch_to.window(parentHandler)

        self.waitForElement("//frame[contains(@id,'banner')]", locatorType='xpath')
        iframe = self.driver.find_element(By.XPATH, "//frame[contains(@id,'banner')]")
        self.driver.switch_to.frame(iframe)

        cmdLine = self.driver.find_element(By.XPATH, "//*[@id='commandValue']")
        cmdLine.clear()
        cmdLine.send_keys("CARD.ISSUE,DMI")
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

                    self.driver.find_element(By.CSS_SELECTOR,
                                             "input[type='radio'][id='radio:tab1:MIGRT.TO.DBX'][value='Y']").click()

                    btnCmt = self.driver.find_element(By.XPATH,
                                                      "//*[@id='goButton']/tbody/tr/td/table/tbody/tr/td[1]/a/img")
                    btnCmt.click()
                    # self.takeScreenshot(self.driver, f"T24_DMX Update {panNumber}")
                    sleep(10)
                except NoSuchElementException:
                    errMsg = self.driver.find_element(By.XPATH, "//*[@id='messages']").text
                    print(f"\n{errMsg}\nError: Element not found")

        self.driver.close()
        self.driver.switch_to.window(parentHandler)
        innerHandles = self.driver.window_handles
        size = len(innerHandles) - 1
        for r in range(size, 0, -1):
            self.driver.switch_to.window(innerHandles[r])
            self.driver.close()
        self.driver.switch_to.window(innerHandles[0])

        return

    def InfinityVerification2(self, loginID, passWrd, accountType):
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
        #

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

        _topMenu = "//*[@id='frmAccountsLanding_customheader_topmenu_imgMenu']"
        _accMenu = "//*[@id='frmAccountsLanding_customheader_customhamburger_FASTTRANSFERSlblAccounts']"
        _myAccounts = "//*[@id='frmAccountsLanding_customheader_customhamburger_FASTTRANSFERS3flxMyAccounts']"
        _addReciept = "//*[@id='frmFastManagePayee_flxAddReciepient']"

        _Logout = "//*[@id='frmeTransferAddRecipientAcknowledgement_customheadernew_btnLogout']"
        pdb.set_trace()

        topMenu = self.driver.find_element(By.XPATH, _topMenu)
        topMenu.click()

        accMenu = self.driver.find_element(By.XPATH, _accMenu)
        accMenu.click()

        myAccounts = self.driver.find_element(By.XPATH, _myAccounts)
        myAccounts.click()

        addReciept = self.driver.find_element(By.XPATH, _addReciept)
        addReciept.click()
        _profHeader = "//div[contains(@id, 'flxCreateSenderProfileHeader')]"
        hdrText = self.driver.find_element(By.XPATH, _profHeader).text
        print(hdrText)
        # if hdrText == "Add New Recipient":
        #     print("Hello")
        try:
            self.add_Sender()
            self.add_Recepient()
        except NoSuchElementException:
            self.add_Recepient()

        Logout = self.driver.find_element(By.XPATH, _Logout)
        Logout.click()
        _btnYesNo = "//*[@id='frmeTransferAddRecipientAcknowledgement_CustomPopup_btnYes']"
        btnYesNo = self.driver.find_element(By.XPATH, _btnYesNo)
        btnYesNo.click()
        self.driver.close()

        return

    def add_Sender(self):
        _profileHdr = "//*[@id='frmeTransferCreateSenderProfile_lblCreateSenderProfileHeader']"
        # _sndrCMthd = "//*[@id='frmeTransferCreateSenderProfile_flxContactMethodListBox']"
        _sndrCMthd = "//*[@id='frmeTransferCreateSenderProfile_lbxContactMethod']"
        _sndrEmail = "//*[@id='frmeTransferCreateSenderProfile_tbxEmailAddress']"
        _btnCon1 = "//*[@id='frmeTransferCreateSenderProfile_btnContinue']"
        _btnCon2 = "//*[@id='frmeTransferSenderProfileConfirm_btnConfirm']"
        pdb.set_trace()

        profileHdr = self.driver.find_element(By.XPATH, _profileHdr).text
        if profileHdr == "Create Your Sender Profile":
            sndrCMthd = self.driver.find_element(By.XPATH, _sndrCMthd)
            sel = Select(sndrCMthd)
            sel.select_by_index(1)

            sndrEmail = self.driver.find_element(By.XPATH, _sndrEmail)
            sndrEmail.send_keys("test@cwbank.com")

            btnCon1 = self.driver.find_element(By.XPATH, _btnCon1)
            btnCon1.click()

            btnCon2 = self.driver.find_element(By.XPATH, _btnCon2)
            btnCon2.click()

    def add_Recepient(self):
        _recName = "//*[@id='frmeTransferAddRecipient_tbxRecipientName']"
        _recEmail = "//*[@id='frmeTransferAddRecipient_tbxEmailAddress']"
        _recMobile = "//*[@id='frmeTransferAddRecipient_tbxMobileNumber']"
        _recMethod = "//*[@id='frmeTransferAddRecipient_lbxSendTransferByMethod']"
        _btnCont = "//*[@id='frmeTransferAddRecipient_btnAddRecipientContinue']"

        _secQue = "//*[@id='frmeTransferAddRecipientSecurityInfo_tbxSecurityQuestion']"
        _secAns = "//*[@id='frmeTransferAddRecipientSecurityInfo_tbxAnswer']"
        _secAn2 = "//*[@id='frmeTransferAddRecipientSecurityInfo_tbxConfirmAnswer']"
        _btnUpd = "//*[@id='frmeTransferAddRecipientSecurityInfo_btnUpdateSecurityInfo']"

        _btnCnf = "//*[@id='frmeTransferAddRecipientConfirm_btnConfirm']"
        pdb.set_trace()

        recName = self.driver.find_element(By.XPATH, _recName)
        recName.send_keys("Test Recipient")

        recEmail = self.driver.find_element(By.XPATH, _recEmail)
        recEmail.send_keys("test@cwbank.com")

        recMobile = self.driver.find_element(By.XPATH, _recMobile)
        recMobile.send_keys("647-999-9999")

        recMethod = self.driver.find_element(By.XPATH, _recMethod)
        sel = Select(recMethod)
        sel.select_by_index(1)

        btnCont = self.driver.find_element(By.XPATH, _btnCont)
        btnCont.click()

        secQue = self.driver.find_element(By.XPATH, _secQue)
        secQue.send_keys("Security question to verify")

        secAns = self.driver.find_element(By.XPATH, _secAns)
        secAns.send_keys("test")

        secAn2 = self.driver.find_element(By.XPATH, _secAn2)
        secAn2.send_keys("test")

        btnUpd = self.driver.find_element(By.XPATH, _btnUpd)
        btnUpd.click()

        try:
            _errorMsg = "// *[ @ id = 'frmeTransferAddRecipient_flxAddRecipientError']"
            errMsg = self.driver.find_element(By.XPATH, _errorMsg).text
            if errMsg == "A Recipient/Contact with the specified name already exists for this Sender":
                recName.send_keys("Test Recipient New")
                btnCont.click()
                btnUpd.click()
        except NoSuchElementException:
            pass

        btnCnf = self.driver.find_element(By.XPATH, _btnCnf)
        btnCnf.click()

