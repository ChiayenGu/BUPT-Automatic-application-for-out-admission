from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import re
import os
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

# 处理SSL证书错误问题
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# 忽略无用的日志
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(options=options)

login_url = "https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fservice.bupt.edu.cn%2Fsite%2Flogin%2Fcas-login%3Fredirect_url%3Dhttps%253A%252F%252Fservice.bupt.edu.cn%252Fv2%252Fmatter%252Fstart%253Fid%253D578"
driver.get(login_url)

driver.switch_to.frame('loginIframe')
driver.find_element_by_id('username').send_keys('2019118022')
driver.find_element_by_id('password').send_keys('03143124')

button = driver.find_element_by_class_name('submit-btn')
button.click()
current_url = driver.current_url
while(current_url == login_url):
    time.sleep(1)
    current_url = driver.current_url

# cookie = driver.get_cookies()
driver.get(current_url)
# print(cookie)

