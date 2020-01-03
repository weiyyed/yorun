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
from .session import HdProdSession
from .conf.changqing import *

# URL_PORTAL="http://p.51gxc.com/"
# URL_SY="http://sy.51gxc.com/"
# URL_HSE="http://hse.51gxc.com/"
# URL_EAM="http://eam.51gxc.com/"
# URL_PHD="http://phd.51gxc.com/"
# URL_CSC="http://csc.51gxc.com/"
# URL_RISK="http://risk.51gxc.com/"
# URL_HSM="http://hsm.51gxc.com/"
# URL_CBS="http://cbs.51gxc.com/"
# URL_TRN="http://trn.51gxc.com/"
# URL_MSG="http://msg.51gxc.com/"
# URL_WTASK="http://wtask.51gxc.com/"
# URL_PUB="http://pub-base.51gxc.com/"
# LOGIN_TYPE=1
# name="1031"
# password="1"
module="sy"

modules = [
    "sy", "hse", "eam", "phd", "risk", "hsm", "cbs", "trn", "portal", "msg", "wtask", "pub"
]

def sessions_dict():
    session_dic={}
    ses = HdProdSession()
    ses.login(URL_PORTAL, name, password, login_type=LOGIN_TYPE)
    for module in modules:
        url=__get_module_url(module)
        if url:
            ses.driver.get(url)
        else:
            continue
        session_dic[module]=ses.get_session
    ses.driver.close()
    return session_dic


def get_permissions_data(session=requests.session(),URL_SY=URL_SY):
    "获取权限的data数据"
    response=session.get(parse.urljoin(URL_SY,"/sy/SY_PERMISSON_PC/getPermissionTree"))
    data=response.json().get("data")
    return data
def __get_module_url(module):
    try:
        url = eval("URL_{}".format(module.upper()))
    except NameError:
        url = None
    return url

def gen_menu_urls(data,module):
    '''data字典'''
    urls=[]
    url_module=__get_module_url(module)
    if url_module:
        for fdic in data:
            funccode=fdic.get("funcode", "")
            if funccode:
                if funccode.startswith(module.upper()) and fdic.get("iconSkin")=="menu":
                    if module.lower()=="pub":
                        url=parse.urljoin(url_module,"/pub-base/{}/".format(funccode))
                    else:
                        url=parse.urljoin(url_module,"/{}/{}/".format(module,funccode))
                    urls.append(url)
    return urls


def gen_session_preurls(module_sessions,data,modules=modules):
    """获取模块-url元组列表"""
    urls=[]
    for m in modules:
        m=m.upper()
        session=module_sessions.get(m.lower())
        prefix_urls=gen_menu_urls(data,m)
        urls.extend([(session,url) for url in prefix_urls])
    return urls

module_sessions=sessions_dict()
permissions_data=get_permissions_data(module_sessions["sy"],URL_SY)
session_menu_urls=gen_session_preurls(module_sessions,data=permissions_data,modules=modules)
print()