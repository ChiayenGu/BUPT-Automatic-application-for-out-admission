# -*- coding:utf-8 -*-
#  Copyright (c) 2022 by Chiayen

import datetime
import json
import time

import chinese_calendar
import requests
import msvcrt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings


# 等待加载
def wait_target_loacated(target, timeout=30, poll_frequency=0.5, model=None):
    try:
        start = datetime.datetime.now()
        WebDriverWait(driver, timeout, poll_frequency).until(target)
        end = datetime.datetime.now()
        print(f'登陆成功 用时:{end - start}')
    except:
        print('等待失败，即将刷新页面')
        raise


# 获取日期
def get_tomorrow():
    day = datetime.timedelta(days=1)
    tomorrow = (datetime.datetime.today() + day).date()
    weekday = tomorrow.weekday()
    weekday_arr = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日',]

    return str(tomorrow),weekday_arr[weekday]
tomorrow,weekday = get_tomorrow()


def set_driver():
    options = webdriver.ChromeOptions()
    # 处理SSL证书错误问题
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    # 忽略无用的日志
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

    # 处理无头
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

# 登陆 自动跳转页面
login_url = "https://auth.bupt.edu.cn/authserver/login?service=https%3A%2F%2Fservice.bupt.edu.cn%2Fsite%2Flogin%2Fcas-login%3Fredirect_url%3Dhttps%253A%252F%252Fservice.bupt.edu.cn%252Fv2%252Fmatter%252Fstart%253Fid%253D578"


def auth_login(login_url):
    driver.get(login_url)

    driver.switch_to.frame('loginIframe')
    driver.find_element_by_id('username').send_keys(student_id)
    driver.find_element_by_id('password').send_keys(password)

    button = driver.find_element_by_class_name('submit-btn')
    button.click()
    return True
    # 访问新网页

def redirect(login_url):
    current_url = driver.current_url
    while (current_url == login_url):
        time.sleep(1)
        current_url = driver.current_url
    driver.get(current_url)
    return current_url

# 等待表格加载完毕 加载cookie
def get_cookie(retry=3):
    current_url = redirect(login_url)
    target = EC.element_to_be_clickable((By.CLASS_NAME, 'dradiostyle'))
    while (retry):
        try:
            wait_target_loacated(target)
            cookies_temp = driver.get_cookies()
            cookies = {}
            for cookie in cookies_temp:
                cookies[cookie['name']] = cookie['value']
            return cookies
        except:
            retry = retry - 1
            print("等待失败，即将刷新网页，剩余尝试次数{retry}".format(retry))
            driver.get(current_url)
    raise

def get_headers():
    headers = {
        "authority": "service.bupt.edu.cn",
        "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
        "sec-ch-ua-platform": "\"Windows\"",
        "origin": "https://service.bupt.edu.cn",
        "referer": "https://service.bupt.edu.cn/v2/matter/start?id=578",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    return headers

def send_apply_for_out_school(out_time, back_time):
    data = {
        "data":
            {"app_id": "578", "node_id": "", "form_data": {
                "1716": {"User_5": base_user_info['User_5'], "User_7": base_user_info['User_7'],
                         "User_9": base_user_info['User_9'],
                         "User_11": mobile_number,
                         "User_75": base_user_info['User_75'], "Alert_65": "", "Alert_67": "",
                         "Input_28": destination,
                         "Input_80": menter_info['number'],
                         "Input_81": counselor_info['number'], "Radio_52": {"value": "1", "name": "本人已阅读并承诺"},
                         "Calendar_47": "{day}T{back}:00:00.000Z".format(day=tomorrow, back=back_time - 8),
                         "Calendar_50": "{day}T{out}:00:00.000Z".format(day=tomorrow, out=out_time - 8),
                         "Calendar_62": "{day}T00:00:00+08:00".format(day=tomorrow),
                         "SelectV2_58": [{"name": "西土城校区", "value": "2", "default": 0, "imgdata": ""}],
                         "ShowHide_79": "",
                         "Validate_63": "", "Validate_66": "", "DataSource_85": "", "DataSource_86": "",
                         "MultiInput_30": reason,
                         "UserSearch_60": {"uid": counselor_info['id'], "name": counselor_info['name'],
                                           "college": counselor_info['college'], "number": counselor_info['number']},
                         "UserSearch_84": {"uid": menter_info['id'], "name": menter_info['name'],
                                           "college": menter_info['college'], "number": menter_info['number']}}},
             "userview": 1,
             "special_approver": [{"node_key": "UserTask_0dvqsya", "uids": [197765], "subprocessIndex": ""}]},
        "step": "0",
        "agent_uid": "",
        "starter_depart_id": "181789",
        "test_uid": "0"
    }
    data['data'] = json.dumps(data['data'], ensure_ascii=False, separators=(',', ':'))

    url = "https://service.bupt.edu.cn/site/apps/launch"
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    response.encoding = "utf-8"
    print(response.text)
    # print(response)
    if response.status_code == 200:
        return True
    else:
        raise

# 查询学生基本信息
def fetch_base_user_info():
    # headers = get_headers()
    # cookies = get_cookie(current_url)
    url = "https://service.bupt.edu.cn/site/form/start-data"
    params = {
        "app_id": "578",
        "node_id": "",
        "userview": "1",
        "agent_uid": "",
        "starter_depart_id": "181789",
        "test_uid": "0"
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    base_user_data = response.json()['d']['data']
    base_user_data = list(base_user_data.values())[0]
    # pprint.pprint(base_user_data)
    print('学生基本信息: {name} {id}'.format(name=base_user_data['User_5'],id=base_user_data['User_7']))
    return base_user_data


# 查询辅导员和导师信息
def fetch_admin_user_info(name, type='counselor'):
    tag_id = [231546, 227839] if type == 'counselor' else [193258, 200083, 195969, 227839]
    url = "https://service.bupt.edu.cn/site/user/form-search-user"
    data = {
        "param": {"keyword": name, "search_field": ["name", "number"], "depart_id": [],
                  "job_id": [184900, 193053, 227839], "tag_id": tag_id, "uids": [], "relation": [], "default": {}},
        "agent_uid": "",
        "starter_depart_id": "181789",
        "test_uid": "0"
    }
    data['param'] = json.dumps(data['param'], ensure_ascii=False, separators=(',', ':'))
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    admin_user_info = response.json()['d']['data']
    if (len(admin_user_info) > 1):
        for item in admin_user_info:
            if base_user_info['User_9'] == item.collage:
                # pprint.pprint(item)
                print('查询信息: {name} {id}'.format(name=item['name'],id=item['number']))
                return item
    else:
        # pprint.pprint(admin_user_info[0])
        print('查询信息: {name} {id}'.format(name=admin_user_info[0]['name'], id=admin_user_info[0]['number']))
        return admin_user_info[0]

def are_you_outing_tomorrow(want_out_weekday):
    day = datetime.timedelta(1)
    today = datetime.datetime.today()
    tomorrow = today+day

    if(chinese_calendar.is_holiday(tomorrow+day) and (chinese_calendar.is_workday(tomorrow))):
        # 节假日前一天（明天）要出门，于是大前天发请求
        return True
    elif(chinese_calendar.is_holiday(tomorrow) and (chinese_calendar.is_workday(tomorrow+day))):
        # 节假日最后一天（明天）要回校，于是节假日倒数第二天发送请求
        return True
    elif(chinese_calendar.is_holiday(today) and (chinese_calendar.is_workday(tomorrow))):
        # 节假日结束的工作日（明天）要回校，于是节假日最后一天发送请求
        return True
    elif(tomorrow.weekday() in want_out_weekday and (chinese_calendar.is_workday(tomorrow))):
        # 如果明天是预定出校，明天还是工作日
        return True
    else:
        return False

if __name__ == "__main__":
    student_id = settings.STUDENT_ID  # 学号
    password = settings.PASSWORD  # 密码
    mobile_number = settings.MOBILE_NUMBER  # 手机号
    counselor_name = settings.COUNSELOR_NAME  # 辅导员姓名
    menter_name = settings.MENTER_NAME  # 导师姓名
    destination = settings.DESTINATION  # 外出去向
    reason = settings.REASON  # 外出原因
    out_time = settings.OUT_TIME  # 出校时间 只支持整数 24小时制
    back_time = settings.BACK_TIME  # 入校时间 只支持整数 24小时制

    want_out_weekday = settings.WANT_OUT_WEEKDAY # 星期几出入校？0=星期一 4=星期五 5=星期六 6=星期日

    if(are_you_outing_tomorrow(want_out_weekday)):
        print('按照预定计划，明天{tomorrow} {weekday} 出校 开始发送请求'.format(tomorrow=tomorrow,weekday=weekday))
        driver = set_driver()
        if (auth_login(login_url)):
            try:
                cookies = get_cookie()
                headers = get_headers()
                base_user_info = fetch_base_user_info()
                counselor_info = fetch_admin_user_info(counselor_name)
                menter_info = fetch_admin_user_info(menter_name, type="menter")
                if (send_apply_for_out_school(out_time,back_time)):
                    print("自动发送出入校请求成功")
            except Exception as e:
                print('自动发送出入校请求失败')
            finally:
                driver.close()
    else:
        print('按照预定计划，明天{tomorrow} {weekday} 不出校'.format(tomorrow=tomorrow,weekday=weekday))