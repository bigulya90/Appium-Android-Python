import sys
import os
import random
import signal
import string
import subprocess
import time
import unittest
import zipfile
from subprocess import check_output, CalledProcessError
from datetime import datetime
import requests
from appium import webdriver


class AndroidTestBase(unittest.TestCase):
    device_name = 'device_name'
    os_version = 'os_version'
    API_Level = 'API_Level'
    proc_video = None
    global lastSeenFailureCount

    #Checking device's ID
    try:
        adb_result = check_output(["adb", "devices"])
        lines = adb_result.split('\n')[1:]
        device_name = lines[0].split('\t')[0]
        print('Device name is: ')
        print(device_name)
    except CalledProcessError as e:
        print e.returncode

    #Checking android's version
    try:
        adb_result = check_output(["adb", "shell", "getprop", "ro.build.version.release"])
        lines = adb_result.split('\r\n')
        os_version = lines[0]
        print("Android version: " + os_version)
    except CalledProcessError as e:
        print e.returncode

    #Checking API level
    try:
         API_Level= check_output(["adb", "shell", "getprop", "ro.build.version.sdk "])
         print("API Level: " + API_Level)
    except CalledProcessError as e:
         print e.returncode

    def take_screenshot(self):
        directory = 'Test_results/'
        file_name = self._testMethodName + HorizonTestBase.device_name + '.png'
        self.driver.save_screenshot(directory + file_name)

    def setUp(self):
        desired_caps = {
            'noSign': 'true',
            'platformName': 'Android',
            'platformVersion': self.os_version,
            'deviceName': self.device_name,
            'automationName': 'Appium',
            'appPackage': 'xxx',
            'app': 'xxx.apk',
            'newCommandTimeout': 180,
            'appActivity': 'xxx'
        }

        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(100)

        clean_logs = subprocess.Popen('adb logcat -c', shell=True, universal_newlines=True)

    def tearDown(self):
        # end the session
        if sys.exc_info():
            f = open('./Test_results/{}.txt'.format(self.device_name + self._testMethodName), "w")
            proc = subprocess.Popen('adb logcat -v time', shell=True, universal_newlines=True, stdout=f)
        self.driver.quit()
