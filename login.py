#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time
import random

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

"""
匯入欲搶購的連結、登入帳號、登入密碼及其他個資
"""
from settings import (
    DRIVER_PATH, CHROME_PATH, CHROME_DATA_PATH, ACC, PWD,   
)
from user_agent_list import(
    userAgent
)

def login():
    print("try to login")
    WebDriverWait(driver, 2).until(
        expected_conditions.presence_of_element_located((By.ID, 'loginAcc'))
    )

    elem = driver.find_element_by_id('loginAcc')
    time.sleep(1)
    elem.clear()
    elem.send_keys(ACC)
    elem = driver.find_element_by_id('loginPwd')
    time.sleep(1)
    elem.clear()
    elem.send_keys(PWD)
    print("pwd sended")

    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.ID, "btnLogin"))
    )
    time.sleep(0.5)
    driver.find_element_by_id('btnLogin').click()
    print('clicked login btn')


def click_button(xpath):
    print("try to click button")

    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, xpath))
    )

    driver.find_element_by_xpath(xpath).click()
    print('click_button funtion passed')




"""
集中管理需要的 xpath
"""
xpaths = {
    'add_to_cart': r"//li[@id='ButtonContainer']/button",
    'check_agree': r"//input[@name='chk_agree']",
    'BuyerSSN': r"//input[@id='BuyerSSN']",
    'BirthYear': r"//input[@name='BirthYear']",
    'BirthMonth': r"//input[@name='BirthMonth']",
    'BirthDay': r"//input[@name='BirthDay']",
    'multi_CVV2Num': r"//input[@name='multi_CVV2Num']",
    'BuyerMobile':r"//input[@name='BuyerMobile']",
    'invoice': r"//input[@name='invoice']"
    # 'pay_once': "//li[@class=CC]/a[@class='ui-btn']",
    # 'pay_line': "//li[@class=LIP]/a[@class='ui-btn line_pay']", 
    # 'submit': "//a[@id='btnSubmit']",
    # 'warning_msg': "//a[@id='warning-timelimit_btn_confirm']",  # 之後可能會有變動
}

"""
設定 option 可讓 chrome 記住已登入帳戶，成功後可以省去後續"登入帳戶"的程式碼
"""
options = webdriver.ChromeOptions()  
options.add_argument(CHROME_PATH)  

options.add_argument('--no-sandbox')

options.add_argument('--headless')

options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--allow-running-insecure-content')

user_agent= userAgent[random.randint(0,29)]
print(user_agent)
options.add_argument(f'user-agent={user_agent}')


options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')

###
options.add_argument(f'user-data-dir={CHROME_DATA_PATH}')
###



driver = webdriver.Chrome(
    executable_path=DRIVER_PATH, chrome_options=options)
driver.set_page_load_timeout(120)


"""
抓取商品開賣資訊，並嘗試搶購
"""

if __name__ == "__main__":
    driver.get("https://ecvip.pchome.com.tw/login/v3/login.htm?&rurl=https://24h.pchome.com.tw")
    try:
        login()
    except Exception as e:
        print("login_____error")
        print(e)
    print("\033[94mlogin success try to save logindata\033[0m")
    time.sleep(15)
    driver.get_screenshot_as_file("logindata_screenshot.png")
    driver.quit()
    exit()

