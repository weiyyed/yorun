import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Session():
    '''get session of requests with cookies'''
    def __init__(self):
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }
        option = Options()
        option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=option)
    # def get_driver(self,url,name,password,login_type=1):
    #     option = Options()
    #     option.add_argument("--headless1")
    #     option.add_argument("--disable-gpu")
    #     self.driver = webdriver.Chrome(options=option)
    def login(self,url):
        pass
    @property
    def get_session(self):
        html_source = self.driver.page_source
        cookies = self.driver.get_cookies()
        sess = requests.session()
        sess.headers.update(self.headers)
        for cookie in cookies:
            sess.cookies.set(cookie["name"], cookie["value"])
        try:
            csrf = re.search("window.csrf = '(.*?)'", html_source).group(1)
            sess.headers.update({"csrf": csrf})
        except AttributeError:
            pass
        return sess
    def close(self):
        self.driver.close()

class HdProdSession(Session):
    # def __int__(self):
    #     super().__init__()
    def login(self,url,name,password,login_type=1):
        self.driver.get(url)
        if int(login_type) == 1:
            self.driver.find_element_by_id("name").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_xpath(r'//a[@onclick="login()"]').click()
        elif int(login_type) == 2:
            self.driver.find_element_by_id("username").send_keys(name)
            self.driver.find_element_by_id("pwd1").send_keys(password)
            self.driver.find_element_by_css_selector(r'input[value="立即登录"]').click()
        time.sleep(1)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/script")))
        return self.driver
