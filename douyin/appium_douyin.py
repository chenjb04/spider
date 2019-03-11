# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/9 21:11'
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


cap = {
    "platformName": "Android",
    "platformVersion": "5.1.1",
    "deviceName": "127.0.0.1:62025",
    "appPackage": "com.ss.android.ugc.aweme",
    "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
    "noReset": True,
    'unicodekeyboard': True,
    'resetkeyboard': True
}

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", cap)


def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


try:
    if WebDriverWait(driver, 3).until(lambda x: x.tap([(670, 75)], 100)):
        driver.tap([(670, 75)], 100)
except Exception as e:
    pass

if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']")):
    driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']").click()
    driver.find_element_by_xpath("//android.widget.EditText[@resource-id='com.ss.android.ugc.aweme:id/adj']").send_keys("191433445")

# 点击搜索
while True:
    if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/adm']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/adm']").click()


    # 点击用户
    if WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='用户']")):
            driver.find_element_by_xpath("//android.widget.TextView[@text='用户']").click()

    # 点击头像
    if WebDriverWait(driver, 3).until(lambda x: x.tap([(24, 198), (108, 282)], 100)):
        driver.tap([(24, 198), (108, 282)], 100)

    # 点击粉丝
    if WebDriverWait(driver, 3).until(lambda x: x.tap([(372, 665), (418, 700)], 100)):
        driver.tap([(372, 665), (418, 700)], 100)


    time.sleep(1)
    l = get_size()

    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.9)
    y2 = int(l[1] * 0.15)

    # 滑动操作
    while True:
        if '没有更多了' in driver.page_source:
            break
        elif 'TA还没有粉丝' in driver.page_source:
            break
        else:
            driver.swipe(x1, y1, x1, y2)
            time.sleep(0.5)
    driver.find_element_by_id("com.ss.android.ugc.aweme:id/jk").click()
    driver.find_element_by_id("com.ss.android.ugc.aweme:id/jk").click()
    driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.ss.android.ugc.aweme:id/adm']").clear()