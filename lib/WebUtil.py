#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/4/15 21:37
# @Author  : 
# @Desc    : 
# @File    : WebUtil.py
# *************************************
from selenium import webdriver
from lib.common import *
import win32com.client, win32gui, win32con, win32api
from selenium.common.exceptions import StaleElementReferenceException,ElementClickInterceptedException
import time, zipfile, json, email, imaplib, os,subprocess


def open_browser():
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_path}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_extension(extension_path)
    wd = webdriver.Chrome(chrome_options=chrome_options)
    # wd = webdriver.Chrome(executable_path=driver_path)
    wd.maximize_window()
    wd.implicitly_wait(10)
    GSTORE['global_webdriver'] = wd
    return wd


def get_global_webdriver():
    return GSTORE['global_webdriver']


def retrying_find_click(driver, by, value):
    result = False
    attempts = 0
    while attempts < 2:
        try:
            driver.find_element(by, value).click()
            result = True
            break
        except (StaleElementReferenceException,ElementClickInterceptedException):
            attempts += 1
    return result


def catch_error_info(driver, by, value):
    driver.implicitly_wait(1)
    try:
        ele = driver.find_element(by, value)
        print(ele.text)
        time.sleep(0.5)
        driver.get_screenshot_as_file(f'{now}.png')
        time.sleep(0.5)
    except:
        pass
    driver.implicitly_wait(10)


def upload_file(path):
    result = False
    win32com.client.Dispatch("WScript.shell")
    second = 10
    edit_text = 0
    window_state = 0
    while second > 0:
        window_state = win32gui.FindWindow(None, '打开')
        edit_text = win32gui.FindWindowEx(window_state, 0, 'ComboBoxEx32', None)
        if edit_text != 0:
            break
        time.sleep(1)
        second -= 1
        if second == 0:
            print('超时1')
    timeout = 10
    while timeout > 0:
        time.sleep(1)
        win32api.SendMessage(edit_text, win32con.WM_SETTEXT, 0, path)
        length = 4
        buf = win32gui.PyMakeBuffer(length)
        win32api.SendMessage(edit_text, win32con.WM_GETTEXT, length, buf)
        address, length = win32gui.PyGetBufferAddressAndLen(buf)
        text = win32gui.PyGetString(address, length)
        timeout = timeout - 1
        if text[0:2] == os.getcwd().split('\\')[0]:
            result = True
            break
    save_btn = win32gui.FindWindowEx(window_state, 0, 'Button', '打开(&O)')
    win32api.SendMessage(save_btn, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    win32api.SendMessage(save_btn, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
    time.sleep(2)
    return result


def list_files(dir=download_path, exp=None):
    ret = []
    for root, dirs, files in os.walk(dir, topdown=False):
        targetFiles = filter(lambda file: exp in file, files) if exp else files
        for file in targetFiles:
            if file.endswith('.crdownload'):
                continue
            ret.append(os.path.join(root, file))
    return ret


def get_recent_file(dir=download_path, exp=None):
    fileMap = {}
    ret = []
    if exp:
        seconds = 10
        while True:
            if seconds > 0:
                ret = list_files(dir, exp)
                if ret:
                    break
                time.sleep(1)
                seconds -= 1
            else:
                break
    else:
        ret = list_files(dir)
    for filePath in ret:
        modifyTime = os.path.getmtime(filePath)
        fileMap.update({filePath: modifyTime})
    retlist = sorted(fileMap.items(), key=lambda d: d[1], reverse=True)
    if not retlist:
        raise Exception("找不到符合条件的文件!")
    return retlist[0][0]


def get_qrcode_by_file(position, filePath, lineNo=1):
    with open(filePath, 'r', encoding='utf-8') as f:
        contents = f.read().splitlines()
        if contents:
            qrcode = contents[lineNo - 1].split(',')[position]
            return qrcode
        else:
            raise Exception("空文件！")


def unzip_file(filePath, pwd=None):
    if pwd:
        pwd = bytes(pwd, encoding='utf-8')
    dir = os.path.split(filePath)[0]
    fileZip = zipfile.ZipFile(filePath, 'r')
    for file in fileZip.namelist():
        fileZip.extract(file, dir, pwd)
    fileZip.close()
    filePathList = [os.path.join(dir, file) for file in fileZip.namelist()]
    return filePathList


def update_uid_file(filePath):
    with open(filePath, 'r+', encoding='utf-8') as f:
        content = '%x' % (int(f.read(), 16) + 1,)
        f.seek(0)
        f.write(content)


def decode(header: str):
    value, charset = email.header.decode_header(header)[0]
    if charset:
        return str(value, encoding=charset)
    else:
        return value


def download_attachment():
    attachment_file_path = None
    mail = imaplib.IMAP4_SSL('imap.126.com')
    mail.login(mailAddress, authCode)
    imaplib.Commands['ID'] = ('AUTH')
    args = ("name", "XXXX", "contact", "XXXX@126.com", "version", "1.0.0", "vendor", "myclient")
    typ, dat = mail._simple_command('ID', '("' + '" "'.join(args) + '")')
    status, msgs = mail.select('INBOX')
    unseen = mail.search(None, 'UNSEEN')
    for num in unseen[1][0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        content = data[0][1]
        msg = email.message_from_bytes(content)
        for part in msg.walk():
            if 'attachment' == part.get_content_disposition():
                attachment_name = decode(part.get_filename())
                attachment_content = part.get_payload(decode=True)
                if not os.path.isdir(download_path):
                    os.mkdir(download_path)
                attachment_file_path = os.path.join(download_path, attachment_name)
                attachment_file = open(attachment_file_path, 'wb')
                attachment_file.write(attachment_content)
                attachment_file.close()
                break
    return attachment_file_path


def retry_download_attachment():
    attempts = 0
    while attempts < 2:
        attachment_file_path = download_attachment()
        if not attachment_file_path:
            time.sleep(5)
        else:
            return attachment_file_path
    raise Exception('邮件接收超时！')


# def filling_ukey(packFile):
#     os.environ["PYTHONUNBUFFERED"] = "1"
#     arg1 = os.path.join(ukeyImporterDir,'ukey-importer.exe')
#     arg2 = os.path.join(ukeyImporterDir,packFile)
#     cmd = rf"{arg1} {arg2}"
#     process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
#     for stdout_line in iter(process.stdout.readline, b''):
#         INFO(stdout_line)
#         if b'import ccks domain done.\r\n' in stdout_line:
#             INFO('import ccks domain done')
#             return
#     raise Exception('ukey灌装失败！')
def filling_ukey(packFile):
    os.environ["PYTHONUNBUFFERED"] = "1"
    arg1 = os.path.join(ukeyImporterDir,'ukey-importer.exe')
    arg2 = os.path.join(ukeyImporterDir,packFile)
    cmd = 'cmd.exe /C ' + rf'{arg1} {arg2}'
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    for stdout_line in out.splitlines():
        INFO(stdout_line)
        if b'import ccks domain done' in stdout_line:
            INFO('import ccks domain done')
            return
    raise Exception('ukey灌装失败！')
