from time import sleep, strftime
import os

class ScreenShots:
    def takeScreenshot(self, driver):
        """
        Takes screenshot of the current open web page
        """
        fileName = strftime('%m%d%Y_%H%M%S') + ".png"
        dirPath = os.getcwd()
        screenshotDirectory = f"{dirPath}\\screenshots\\"
        destinationFile = screenshotDirectory + fileName

        try:
            sleep(3)
            driver.save_screenshot(destinationFile)
            print("Screenshot saved to directory --> :: " + destinationFile)
        except NotADirectoryError:
            print("Issue: Directory not found" + screenshotDirectory)


ss = ScreenShots()
