#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2021/10/11 16:39
# @Author  : 
# @Desc    : 
# @File    : AppUtil.py
# *************************************
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException,TimeoutException,NoAlertPresentException,InvalidElementStateException
import time, traceback
from lib.common import *
import os,subprocess

appName = 'LMJZ-PE-V2.5.7-test-403.apk'
appInstallPath = r'C:\Users\rg_16\Downloads\%s' % appName


def open_desktop():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '8'
    desired_caps['deviceName'] = 'test'
    desired_caps['app'] = appInstallPath
    desired_caps['appPackage'] = 'com.miui.home'
    desired_caps['appActivity'] = '.launcher.Launcher'
    desired_caps['unicodeKeyboard'] = True
    desired_caps['noReset'] = True
    desired_caps['newCommandTimeout'] = 6000
    desired_caps['automationName'] = 'Uiautomator2'
    # 启动Remote RPC
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(10)
    GSTORE['global_appdriver'] = driver


def get_global_appdriver():
    return GSTORE['global_appdriver']


def app_is_installed(package):
    cmd = 'adb shell pm list packages %s' % package
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    if process.stdout.readlines():
        return True
    return False


def get_cmd_return(cmd):
    with os.popen(cmd) as op:
        ret = op.read().strip()
    return ret


def remove_installed_app():
    cmd = '''adb shell "pm list packages |egrep 'com.zcsmart.lmjz|appium'"'''
    result = get_cmd_return(cmd).strip().replace('package:', '')
    for one in map(lambda item: item.strip(), result.split('\n')):
        os.popen('adb uninstall %s' % one)


def usb_install(driver):
    seconds = 10
    driver.implicitly_wait(1)
    while seconds > 0:
        installBtnEles = driver.find_elements_by_xpath("//android.widget.Button[contains(@text,'继续安装')]")
        if installBtnEles:
            installBtnEles[0].click()
            break
        else:
            time.sleep(1)
            seconds -= 1


def is_exist(driver,expression):
    try:
        ele = driver.find_element_by_android_uiautomator(expression)
        ele.click()
        return True
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False


def scroll_into_view(driver,expression):
    timeout = 60
    while True:
        if timeout > 0:
            if is_exist(driver,expression):
                break
            else:
                start = driver.find_element_by_xpath('//android.view.View/*[last()-1]').location
                h = driver.get_window_size()['height']
                driver.swipe(0, 0.9 * h, 0, 0.1 * h, 5000)
                time.sleep(1)
                end = driver.find_element_by_xpath('//android.view.View/*[last()-1]').location
                timeout -= 1
                print(f'start:{start}end:{end}')

                if start == end:
                    break
        else:
            print('超时')
            break

# remove_installed_app()