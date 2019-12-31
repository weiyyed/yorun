# -*- coding: utf-8 -*-
import re
import pytest
import time
from urllib import parse
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

URL_SY="http://sy.51gxc.com/"
URL_HSE="http://hse.51gxc.com/"
URL_EAM="http://eam.51gxc.com/"
URL_PHD="http://phd.51gxc.com/"
URL_CSC="http://csc.51gxc.com/"
URL_RISK="http://risk.51gxc.com/"
URL_HSM="http://hsm.51gxc.com/"
URL_CBS="http://cbs.51gxc.com/"
URL_TRN="http://trn.51gxc.com/"
URL_PORTAL="http://portal.51gxc.com/"
URL_MSG="http://msg.51gxc.com/"
URL_WTASK="http://wtask.51gxc.com/"
URL_PUB="http://pub.51gxc.com/"
LOGIN_TYPE=1
name="1031"
password="1"
module="sy"

modules = [
    "sy", "hse", "eam", "phd", "risk", "hsm", "cbs", "trn", "portal", "msg", "wtask", "rqreport", "pub"
]

# @pytest.fixture(scope="class")
# def login_sy():
#     return login_session(URL_SY)
# @pytest.fixture(scope="class")
# def login_hse():
#     return login_session(URL_HSE)
# @pytest.fixture(scope="class")
# def login_eam():
#     return login_session(URL_EAM)
# @pytest.fixture(scope="class")
# def login_phd():
#     return login_session(URL_PHD)
# @pytest.fixture(scope="class")
# def login_csc():
#     return login_session(URL_CSC)
# @pytest.fixture(scope="class")
# def login_trn():
#     return login_session(URL_TRN)
# @pytest.fixture(scope="class")
# def login_msg():
#     return login_session(URL_MSG)
# @pytest.fixture(scope="class")
# def login_wtask():
#     return login_session(URL_WTASK)
# @pytest.fixture(scope="class")
# def login_pub():
#     return login_session(URL_PUB)
class LoginDriver():
    """登录后的driver"""
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--disable-gpu")
    def __int__(self,url=URL_PORTAL):
        self.driver=webdriver.Chrome(options=option)
        self.url=url
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()
    def __call__(self, *args, **kwargs):
        self.driver.get(self.url)
        if int(LOGIN_TYPE) == 1:
            self.driver.find_element_by_id("name").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
        elif int(LOGIN_TYPE) == 2:
            self.driver.find_element_by_id("username").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
        time.sleep(1)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/script")))
        return self.driver
def login_sessions(modules=modules):
    # option = Options()
    # option.add_argument("--headless")
    # option.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(options=option)


    # driver.get(url)
    # if int(LOGIN_TYPE) == 1:
    #     driver.find_element_by_id("name").send_keys(name)
    #     driver.find_element_by_id("pwd1").send_keys(password)
    #     driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
    # elif int(LOGIN_TYPE) == 2:
    #     driver.find_element_by_id("username").send_keys(name)
    #     driver.find_element_by_id("pwd1").send_keys(password)
    #     driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
    # time.sleep(1)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/script")))
    # driver.get(url)
    # time.sleep(1)
    sessions=[]
    with LoginDriver() as driver:
        html_source = driver.page_source
        csrf = re.search("window.csrf = '(.*?)'", html_source).group(1)
        for module in modules:
            session_dic={}
            driver.get(eval("URL_{}".format(module.upper())))
            cookies = driver.get_cookies()
            sess = gen_session()
            for cookie in cookies:
                sess.cookies.set(cookie["name"], cookie["value"])
            sess.headers.update({"csrf": csrf})
            session_dic[module]=sess
            sessions.append(session_dic)
        return sessions

def gen_session():
    """genenate general requests session"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    sess = requests.session()
    sess.headers.update(headers)
    return sess

# def get_permissions():
#     "获取权限的data数据"
#     login_sy=login_session(URL_SY)
#     response=login_sy.get(parse.urljoin(URL_SY,"/sy/SY_PERMISSON_PC/getPermissionTree"))
#     data=response.json().get("data")
#     return data

def gen_prefix_urls(data,module):
    '''daat:data字典'''
    urls=[]
    url_module=eval("URL_{}".format(module))
    for fdic in data:
        funccode=fdic.get("funcode", "")
        if funccode:
            if funccode.startswith(module.upper()) and fdic.get("iconSkin")=="menu":
                url=parse.urljoin(url_module,"/{}/{}/".format(module,funccode))
                urls.append(url)
    return urls


def get_module_urls(data):
    """获取模块-url元组列表"""
    urls=[]
    for m in modules:
        m=m.upper()
        session=login_session(eval("URL_{}".format(m)))
        prefix_urls=gen_prefix_urls(data,m)
        # urls_dic[m]=[(session,url) for url in prefix_urls]
        urls.extend([(session,url) for url in prefix_urls])
    return urls

data=get_permissions()
prefix_urls=get_module_urls(data)
print()
# SY_PREFIX_URLS=gen_prefix_urls(data,"sy")
# HSE_PREFIX_URLS=gen_prefix_urls(data,"hse")
# EAM_PREFIX_URLS=gen_prefix_urls(data,"eam")
# PHD_PREFIX_URLS=gen_prefix_urls(data,"phd")
# CSC_PREFIX_URLS=gen_prefix_urls(data,"csc")
# RISK_PREFIX_URLS=gen_prefix_urls(data,"risk")
# HSM_PREFIX_URLS=gen_prefix_urls(data,"hsm")
# CBC_PREFIX_URLS=gen_prefix_urls(data,"cbs")
# TRN_PREFIX_URLS=gen_prefix_urls(data,"trn")
# PORTAL_PREFIX_URLS=gen_prefix_urls(data,"portal")
# MSG_PREFIX_URLS=gen_prefix_urls(data,"msg")
# WTASK_PREFIX_URLS=gen_prefix_urls(data,"wtask")
# RQREPORT_PREFIX_URLS=gen_prefix_urls(data,"rqreport")
# PUB_PREFIX_URLS=gen_prefix_urls(data,"pub")