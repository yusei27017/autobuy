#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import json
import time
import requests
import random
import sys
import datetime

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

"""
匯入欲搶購的連結、登入帳號、登入密碼及其他個資
"""
from settings import (
    target_URL, DRIVER_PATH, CHROME_DATA_PATH, CHROME_PATH, ACC, PWD,
    BuyerMobile    
)
from user_agent_list import(
    userAgent
)


def input_info(xpath, info):  # info = 個資
    WebDriverWait(driver, 1).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, xpath))
    )
    elem = driver.find_element_by_xpath(xpath)
    elem.clear()
    elem.send_keys(info)

def click_button(xpath):
    print("try to click button")

    WebDriverWait(driver, 20).until(
        expected_conditions.element_to_be_clickable(
            (By.XPATH, xpath))
    )

    driver.find_element_by_xpath(xpath).click()
    print('click_button funtion passed')

def input_flow():
    """
    填入個資，若無法填入則直接填入信用卡背面安全碼 3 碼 (multi_CVV2Num)
    """
    print('try to input_info')
    try:
        input_info(xpaths['BuyerMobile'], BuyerMobile)
    except:
        print("info already filled in!")

    finally:
        print('input_info entered')

def get_product_id(url):
    pattern = '(?<=prod/)(\w+-\w+)'
    try:
        product_id = re.findall(pattern, url)[0]
        print(product_id)
        return product_id
    except Exception as e:
        print(e.__class__.__name__, ': 取得商品 ID 錯誤！')

def get_product_status(product_id):
    api_url = f'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id={product_id}'
    # DGBJG9-A900B51SM
    #'https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/button&id=DGBJG9-A900B51SM'

    print(api_url)
    resp = requests.get(api_url)
    status = json.loads(resp.text)[0]['ButtonType']
    return status

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

def main():
    print("try to get prod url")
    try:
        driver.get(target_URL)
    except:
        print("prod url get fail")
        print(sys.exc_info()[0])
        driver.quit()
        exit()


    """
    放入購物車
    """
    print('try to add shopping car')
    click_button(xpaths['add_to_cart'])

    """
    前往購物車
    """
    time.sleep(0.5)
    driver.get("https://ecssl.pchome.com.tw/sys/cflow/fsindex/BigCar/BIGCAR/ItemList")
    driver.get_screenshot_as_file("car_screenshot.png")

    """
    前往結帳 (一次付清) (要使用 JS 的方式 execute_script 點擊)
    """

    try:
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//li[@class='ATM']/a[@class='ui-btn']"))
        )
        
        button = driver.find_element_by_xpath(
            "//li[@class='ATM']/a[@class='ui-btn']")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.5)


        print("\033[94mlogin success try to pay\033[0m")
        button2 = driver.find_element_by_xpath(
            "//ul[@class='bar_tool']/li/a[@class='ui-btn']")
        driver.execute_script("arguments[0].click();", button2)
    except Exception as e:
        print(e)
        print('\033[1;31m login error please try again later\033[0m')
        driver.get_screenshot_as_file("bnt_screenshot.png")
        driver.quit()
        exit()
        

    """
    點擊提示訊息確定 (有些商品可能不需要)
    """
    try:
        WebDriverWait(driver, 1).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//a[@id='warning-timelimit_btn_confirm']"))
        )
        button = driver.find_element_by_xpath("//a[@id='warning-timelimit_btn_confirm']")
        driver.execute_script("arguments[0].click();", button)

    except:
        print('Warning message passed!')

    """
    填入個資
    """

    input_flow()

    """
    勾選同意（注意！若帳號有儲存付款資訊的話，不需要再次勾選，請註解掉！）
    """
    click_button(xpaths['check_agree'])
    click_button(xpaths['invoice'])

    """
    test run end
    """
    driver.get_screenshot_as_file("fianl_screenshot.png")
    end = datetime.datetime.now()
    run_time = end - start
    print(f"run time:{run_time}")

    """
    送出訂單 (要使用 JS 的方式 execute_script 點擊)
    """
    try:
        WebDriverWait(driver, 20).until(
            expected_conditions.element_to_be_clickable(
                (By.XPATH, "//a[@id='btnSubmit']"))
        )
        button = driver.find_element_by_xpath("//a[@id='btnSubmit']")
        driver.execute_script("arguments[0].click();", button)
        print("order btn clicked")
        time.sleep(7)
        driver.get_screenshot_as_file("order_btn.png")
        # driver.quit()
        print("order over plz check status!!!")

    except:
        print('order send failed')
        driver.get_screenshot_as_file("order_failed.png")
        driver.quit()
        exit()

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
curr_retry = 0
max_retry = 5   # 重試達 5 次就結束程式，可自行調整
wait_sec = 1    # 1 秒後重試，可自行調整秒數
wait_count = 0

if __name__ == "__main__":
    product_id = get_product_id(target_URL)
    start = datetime.datetime.now()

    while curr_retry <= max_retry:
        try:
            status = get_product_status(product_id)
            if status != 'ForSale':
                print('商品尚未開賣！')
                curr_retry += 1
                time.sleep(wait_sec)
                driver.quit()
            else:
                time.sleep(1)
                print('商品已開賣！')
                main()
                break
        except Exception as e:
            wait_count += 1
            if wait_count == 5:
                driver.quit()
                exit()
            print(f"plz wait a minute: {wait_count}")
            print(e)
