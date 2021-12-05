#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2021/5/13 20:52
# @Author  : 
# @Desc    : 
# @File    : WebOpEnterprise.py
# *************************************
from lib.WebUtil import *
from lib.common import *
import time, re, os
from lib.EnterpriseOpApi import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from pprint import pprint
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, \
    NoAlertPresentException, InvalidElementStateException


class WebOpEnterprise:
    def __init__(self):
        if 'global_webdriver' not in GSTORE.keys():
            open_browser()
        self.wd = get_global_webdriver()

    def _print_qrcode(self):
        self.wd.find_element_by_xpath('//button/span[contains(text(),"生成溯码")]').click()
        catch_error_info(self.wd, By.CSS_SELECTOR, 'div[role="alert"].el-message--warning p,.el-message--error p')
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys('1')
        self.wd.find_element_by_css_selector(
            '.el-dialog__body .is-required:nth-child(2) .el-input__suffix-inner').click()
        self.wd.find_element_by_xpath(
            '//li[contains(@class,"el-select-dropdown__item")]/span[contains(text(),"txt")]').click()
        self.wd.find_element_by_xpath(
            '//div[@aria-label="生成溯码"]//div[@class="el-form-item__content"]/button/span[contains(text(),"确 定")]').click()
        time.sleep(2)
        batchNo = self.wd.find_element_by_css_selector(
            'tbody tr:nth-child(1) td:nth-child(2) span,.main-page>:not(.product_qrcode) tbody tr:nth-child(1) td:nth-child(3) div').text
        # eleText = self.wd.find_element_by_css_selector('.main-page>:not(.packCode-mangement):not(.product-code):not(.code-circulate) .el-pagination__total').text
        # print(int(eleText.replace(' ','')[1:-1]))
        print(batchNo)
        return batchNo

    def _print_rfid(self):
        self.wd.find_element_by_xpath('//button/span[contains(text(),"生成唯码")]').click()
        catch_error_info(self.wd, By.CSS_SELECTOR, 'div[role="alert"].el-message--warning p,.el-message--error p')
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys(1)
        self.wd.find_element_by_xpath('//div[@aria-label="生成唯码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(1)
        okBtnXpath = '//div[@aria-label="提示"]//button/span[contains(text(),"确 定")]'
        self.wd.find_element_by_xpath(okBtnXpath).click()
        time.sleep(1)
        catch_error_info(self.wd, By.CSS_SELECTOR, 'div[role="alert"].el-message--warning p,.el-message--error p')
        self.wd.find_element_by_xpath(okBtnXpath).click()
        time.sleep(1)
        self.wd.refresh()
        batchNo = self.wd.find_element_by_css_selector(
            '#pad_none[style] tbody tr:nth-child(1) td:nth-child(2) div,tbody tr:nth-child(1) td:nth-child(3) div').text
        print(batchNo)
        return batchNo

    def _multi_print_qrcode(self):
        # self.wd.find_element_by_xpath('//button/span[contains(text(),"批量生成码")]').click()
        self.wd.find_element_by_xpath('//div[contains(@class,"operator")]//div/button[last()-1]/span').click()
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys('1')
        self.wd.find_element_by_xpath('//div[@aria-label="批量生成txt格式溯码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(2)
        batchNo = self.wd.find_element_by_css_selector(
            'tbody tr:nth-child(1) td:nth-child(2) span,.main-page>:not(.product_qrcode) tbody tr:nth-child(1) td:nth-child(3) div').text
        seconds = 5
        while True:
            if seconds > 0:
                self.wd.refresh()
                time.sleep(1)
                opEle = self.wd.find_element_by_css_selector(
                    '.main-page>.product_qrcode tbody tr:nth-child(1) td:nth-child(9),.main-page>:not(.product_qrcode) tbody tr:nth-child(1) td:nth-child(10)')
                if '下载' == opEle.text:
                    opEle.click()
                    break
                seconds -= 1
            else:
                raise Exception('批量生成码超时！')
        print(batchNo)
        return batchNo

    def _service_decode_qrcode(self, filePath):
        self.wd.find_element_by_xpath('//button/span[contains(text(),"批量解码")]').click()
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys(filePath)
        self.wd.find_element_by_xpath('//div[@aria-label="服务端解码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(0.5)

    def get_notification_info(self):
        ele = self.wd.find_element_by_class_name('el-message__content')
        print(ele.text)
        return ele.text

    def operator_login(self, username, password):
        self.wd.get(f'https://{g_ops_host}/#/login')
        self.wd.find_element_by_css_selector('input[placeholder="用户名"]').send_keys(username)
        self.wd.find_element_by_css_selector('input[placeholder="密码"]').send_keys(password)
        self.wd.find_element_by_xpath('//span[contains(text(),"登录")]').click()
        self.get_notification_info()
        self.wd.find_element_by_css_selector('header[class="el-header header"]')
        # self.wd.find_element_by_class_name('icon-ecode')
        token = self.wd.execute_script('return localStorage.getItem("jwt");')
        GSTORE['enterpriseOpToken'] = token

    def operator_logout(self):
        ele = self.wd.find_element_by_xpath('//button/span[contains(text(),"退出")]')
        self.wd.execute_script("arguments[0].click()", ele)

    def get_operator_homepage_info(self):
        self.wd.find_element_by_class_name('fl-lt').click()
        self.wd.find_element_by_class_name('el-icon-bell').click()
        time.sleep(0.5)
        companyName = self.wd.find_element_by_id('companyName').text
        qrcode = self.wd.find_element_by_class_name('qrcode').get_attribute('title')
        userName = self.wd.find_element_by_css_selector('[class="user-info"] span[style]').text
        boxEles = self.wd.find_elements_by_class_name('box-container')
        cardEles = self.wd.find_elements_by_css_selector('ul[class*="card_info"]>li')
        p = re.compile(r'(\d+)/(\d+)')
        m = p.findall(''.join([cardEle.text for cardEle in cardEles]))
        (SMLeft, SMPurchased), (WMLeft, WMPurchased), (MWLeft, MWPurchased) = m
        ret = {
            'companyName': companyName,
            'qrcode': qrcode,
            'userName': userName,
            'accountInfo': boxEles[0].text,
            'SMLeft': SMLeft,
            'SMPurchased': SMPurchased,
            'WMLeft': WMLeft,
            'WMPurchased': WMPurchased,
            'MWLeft': MWLeft,
            'MWPurchased': MWPurchased
        }
        self.wd.find_element_by_class_name('el-icon-bell').click()
        print(ret)
        return ret

    def add_product_by_product_template(self):
        self.wd.find_element_by_xpath('//li[contains(text(),"产品管理")]').click()
        self.wd.find_element_by_xpath('//button//span[contains(text(),"新建产品")]').click()
        self.wd.find_element_by_css_selector('div[class="select-operation"] input[type="text"]').send_keys('jmeter')
        self.wd.find_element_by_class_name('el-icon-search').click()
        useTemplateXpath = '//span[contains(text(),"jmeter")]/../../../td[last()]//button[position()=2]'
        retrying_find_click(self.wd, By.XPATH, useTemplateXpath)
        # self.wd.find_element_by_css_selector('tbody tr:nth-of-type(1) i[class*="icon-fuzhi2"]').click()
        self.wd.find_element_by_id('file').send_keys(imgPath)
        time.sleep(1)
        # originEle = self.wd.find_element_by_class_name('el-popup-parent--hidden')
        # print(originEle)
        self.wd.find_element_by_xpath(
            '//div[@aria-label="裁剪图片"]/div[@class="el-dialog__footer"]//button[last()]').click()
        time_stamp = int(round(time.time() * 1000))
        self.wd.find_element_by_xpath('//label[contains(text(),"产品名称")]/following-sibling::div//input').send_keys(
            f'cpmbproduct{time_stamp}')
        save_button = '//span[contains(text(),"保存并下一步")]'
        WebDriverWait(self.wd, 10).until(EC.element_to_be_clickable((By.XPATH, save_button)))
        self.wd.find_element_by_xpath(save_button).click()
        self.wd.find_element_by_xpath('//div[@class="oper-button"]//span[contains(text(),"保 存")]').click()
        self.get_notification_info()
        self.wd.find_element_by_class_name('operation-successful')

    def delete_product(self):
        self.wd.find_element_by_xpath('//li[contains(text(),"产品管理")]').click()
        self.wd.find_element_by_css_selector('[class="el-table__row"]:nth-child(1) i[class*="icon-lajitong"]').click()
        self.wd.find_element_by_css_selector('div[aria-label="提示"] button[class*="primary"]').click()

    def choice_code_type(self, menu, name, codeType):
        self.wd.find_element_by_xpath('//li[contains(text(),"%s")]' % menu).click()
        inputEle = self.wd.find_element_by_css_selector(
            '.product-code input[placeholder="请输入名称"],[placeholder="请输入包装码名称"],[placeholder="请输入流通码名称"]')
        inputEle.clear()
        inputEle.send_keys(name)
        self.wd.find_element_by_css_selector('#operator .el-button--primary').click()
        time.sleep(1)
        choiceXpath = '//span[contains(text(),"%s")]/../../../td[last()]//button[position()=%s]' % (name, codeType)
        retrying_find_click(self.wd, By.XPATH, choiceXpath)
        time.sleep(2)
        self.wd.find_element_by_xpath('//div[contains(text(),"批次")]')

    def print_product_qrcode(self, name):
        self.choice_code_type('产品打码', name, 1)
        return self._print_qrcode()

    def multi_print_product_qrcode(self, name):
        self.choice_code_type('产品打码', name, 1)
        return self._multi_print_qrcode()

    def service_decode_product_qrcode(self, filePath, name):
        self.choice_code_type('产品打码', name, 1)
        self._service_decode_qrcode(filePath)

    def print_qrcodeplusrfid(self, name):
        self.choice_code_type('产品打码', name, 3)
        self.wd.find_element_by_xpath('//button/span[contains(text(),"生成密唯码")]').click()
        self.wd.find_element_by_xpath('//i[@class="el-icon-upload"]/..').click()
        update_uid_file(uidPath)
        upload_file(uidPath)
        self.wd.find_element_by_xpath('//div[@aria-label="生成密唯码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(0.5)
        catch_error_info(self.wd, By.CSS_SELECTOR, 'div[role="alert"].el-message--warning p,.el-message--error p')
        batchNo = self.wd.find_element_by_css_selector('tbody tr:nth-child(1) td:nth-child(2) span').text
        seconds = 5
        while True:
            if seconds > 0:
                time.sleep(1)
                opEle = self.wd.find_element_by_xpath('//tbody/tr[position()=1]/td[last()]')
                if '下载' == opEle.text:
                    opEle.click()
                    break
                seconds -= 1
            else:
                raise Exception('密唯码生成超时！')
        time.sleep(2)
        print(batchNo)
        return batchNo

    def print_product_rfid(self, name):
        self.choice_code_type('产品打码', name, 2)
        return self._print_rfid()

    def print_pack_qrcode(self, name):
        self.choice_code_type('包装码信息管理', name, 4)
        return self._print_qrcode()

    def multi_print_pack_qrcode(self, name):
        self.choice_code_type('包装码信息管理', name, 4)
        return self._multi_print_qrcode()

    def service_decode_pack_qrcode(self, filePath, name):
        self.choice_code_type('包装码信息管理', name, 4)
        self._service_decode_qrcode(filePath)

    def print_pack_rfid(self, name):
        self.choice_code_type('包装码信息管理', name, 5)
        return self._print_rfid()

    def print_process_qrcode(self, name):
        self.choice_code_type('流通码信息管理', name, 4)
        return self._print_qrcode()

    def multi_print_process_qrcode(self, name):
        self.choice_code_type('流通码信息管理', name, 4)
        return self._multi_print_qrcode()

    def service_decode_process_qrcode(self, filePath, name):
        self.choice_code_type('流通码信息管理', name, 4)
        self._service_decode_qrcode(filePath)

    def print_process_rfid(self, name):
        self.choice_code_type('流通码信息管理', name, 5)
        return self._print_rfid()

    def print_multi_root(self, mailAddressPlusName):
        self.wd.find_element_by_xpath('//li[contains(text(),"主体码管理")]').click()
        self.wd.find_element_by_xpath(
            '//span[contains(text(),"主体码")]/../../../td[last()]//button[position()=1]').click()
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys(2)
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(2) .el-input__suffix').click()
        time.sleep(1)
        ele = self.wd.find_element_by_xpath('//span[contains(text(),"%s")]' % mailAddressPlusName)
        self.wd.execute_script("arguments[0].scrollIntoView()", ele)
        ele.click()
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(3) .el-input__suffix').click()
        time.sleep(0.5)
        self.wd.find_element_by_xpath('//span[contains(text(),"txt")]').click()
        self.wd.find_element_by_xpath('//div[@aria-label="生成溯码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(0.5)
        batchNo = self.wd.find_element_by_css_selector('tbody tr:nth-child(1) td:nth-child(1) span').text
        return batchNo

    def send_records(self):
        self.wd.find_element_by_xpath('//li[contains(text(),"主体码管理")]').click()
        self.wd.find_element_by_xpath(
            '//span[contains(text(),"主体码")]/../../../td[last()]//button[position()=3]').click()
        # time.sleep(0.5)
        self.wd.find_element_by_css_selector(
            'tbody tr:nth-child(1) td:nth-child(7) button:nth-child(2)').click()
        time.sleep(1)
        attempts = 0
        self.wd.implicitly_wait(1)
        while attempts < 10:
            try:
                decryptPwd = self.wd.find_element_by_xpath('//div[@aria-label="发送记录"]//td[last()]//span').text
                self.wd.implicitly_wait(10)
                self.wd.find_element_by_css_selector('div[aria-label="发送记录"] .el-dialog__headerbtn').click()
                return decryptPwd
            except NoSuchElementException:
                attempts += 1
                self.wd.find_element_by_css_selector('div[aria-label="发送记录"] .el-dialog__headerbtn').click()
                self.wd.find_element_by_css_selector(
                    'tbody tr:nth-child(1) td:nth-child(7) button:nth-child(2)').click()
                time.sleep(1)

    def print_root_rfid(self):
        self.wd.find_element_by_xpath('//li[contains(text(),"主体码管理")]').click()
        self.wd.find_element_by_xpath(
            '//span[contains(text(),"主体码")]/../../../td[last()]//button[position()=2]').click()
        self.wd.find_element_by_css_selector('.el-dialog__body .is-required:nth-child(1) input').send_keys(1)
        self.wd.find_element_by_xpath('//div[@aria-label="生成唯码"]//button/span[contains(text(),"确 定")]').click()
        time.sleep(1)
        okBtnXpath = '//div[@aria-label="dialog"]//button/span[contains(text(),"确 定")]'
        self.wd.find_element_by_xpath(okBtnXpath).click()
        time.sleep(1)
        catch_error_info(self.wd, By.CSS_SELECTOR, 'div[role="alert"].el-message--warning p,.el-message--error p')
        batchNo = self.wd.find_element_by_css_selector('tbody tr:nth-child(1) td:nth-child(1) span').text
        print(batchNo)
        return batchNo


webOpEnterprise = WebOpEnterprise()
if __name__ == '__main__':
    # for fp in list_files(exp='code.txt'):
    #     os.remove(fp)

    # webOpEnterprise.operator_login(g_enterprise_operator_username_universal, g_enterprise_operator_password_universal)
    # webOpEnterprise.operator_logout()
    # time.sleep(2)
    # webOpEnterprise.operator_login(g_enterprise_operator_username_pharmaceutical, g_enterprise_operator_password_pharmaceutical)
    webOpEnterprise.operator_login(g_enterprise_operator_username_salt, g_enterprise_operator_password_salt)
    webOpEnterprise.print_process_qrcode(processNameSalt)
    # webOpEnterprise.print_multi_root(mailAddressPlusName)
    # webOpEnterprise.get_notification_info()
    # webOpEnterprise.get_operator_homepage_info()
    # webOpEnterprise.add_product_by_product_template()
    # webOpEnterprise.delete_product()
