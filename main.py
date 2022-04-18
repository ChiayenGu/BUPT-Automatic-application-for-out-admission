from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
from datetime import datetime
import re
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def wait_target_loacated(target, timeout=30, poll_frequency=0.5, model=None):
    try:
        start = datetime.now()
        WebDriverWait(driver, timeout, poll_frequency).until(target)
        end = datetime.now()
        print(f'等待"{model}"时长:{end - start}')
    except:
        print('等待失败，即将刷新页面')
        raise


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


driver.get(current_url)

# 等待表格加载完毕
target = EC.element_to_be_clickable((By.CLASS_NAME,'dradiostyle'))
wait_target_loacated(target)
cookies = driver.get_cookies()
print(cookies)
# 获取元素
# mobile = driver.find_element_by_xpath('.//div[@data-key="User_11"]//input')
# campus = driver.find_element_by_xpath('.//div[@data-key="SelectV2_58"]//input')
# instructor = driver.find_element_by_xpath('.//div[@data-key="UserSearch_60"]//input')
# # mentor = driver.find_element_by_xpath('.//div[@data-key="UserSearch_84""]//input')
# mobile.send_keys('18810100529')
# campus.send_keys('西土城校区')
# # instructor.send_keys('王宁')
# # mentor.send_keys('双锴')
