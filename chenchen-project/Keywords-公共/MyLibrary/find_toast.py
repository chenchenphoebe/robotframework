# -*- coding:utf-8 -*-
# _author_ = 'phoebe'
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from AppiumLibrary import *


class find_toast(AppiumLibrary):

    def __init__(self):
        AppiumLibrary.__init__(self, timeout=5, run_on_failure='ExtendAppniumLibrary.Capture Page Screenshot')

    def find_toast(self, message):
        application = self._current_application()
        try:
            toast_loc = ("xpath", "//*[contains(@text,'%s')]" % message)
            WebDriverWait(application, 6, 0.5).until(expected_conditions.presence_of_element_located(toast_loc))
            self._info("Toast has been found: %s ." % message)
        except:
            self._info("Not found toast")
