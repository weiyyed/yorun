# -*- coding: utf-8 -*-
import re

import pytest
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url="http://sy.51gxc.com/hd#eyJtYyI6InN5IiwiZmMiOiJTWV9PUkciLCJ1YyI6IjAxNzAwMDIwIn0="
LOGIN_TYPE=1
name="1031"
password="1"
module="sy"

option=Options()
option.add_argument("--headless1")
option.add_argument("--disable-gpu")
driver=webdriver.Chrome(chrome_options=option)
@pytest.fixture()
def login_session(gen_session):
    driver.get(url)
    if int(LOGIN_TYPE) == 1:
        driver.find_element_by_id("name").send_keys(name)
        driver.find_element_by_id("pwd1").send_keys(password)
        driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
    elif int(LOGIN_TYPE) == 2:
        driver.find_element_by_id("username").send_keys(name)
        driver.find_element_by_id("pwd1").send_keys(password)
        driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
    time.sleep(1)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/script")))
    if module == "sy":
        driver.get(url + "#eyJtYyI6InN5IiwiZmMiOiJTWV9QRVJNSVNTT05fUEMiLCJ1YyI6IjAxNzAwMDQ1MDAxMCJ9")
    time.sleep(1)
    html_source = driver.page_source
    csrf = re.search("window.csrf = '(.*?)'", html_source).group(1)
    driver.get(url)
    cookies = driver.get_cookies()
    driver.close()
    sess = gen_session
    for cookie in cookies:
        sess.cookies.set(cookie["name"], cookie["value"])
    sess.headers.update({"csrf": csrf})
    return sess
@pytest.fixture()
def gen_session():
    """genenate general requests session"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    sess = requests.session()
    sess.headers.update(headers)
    return sess