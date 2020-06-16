#!/usr/bin/python
# -*- coding: utf-8 -*-  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, re
from msg import msg
import requests as rq
import sys
from bs4 import BeautifulSoup
sys.path.append("../include")
import inc

msgban = ["嗨", "我男", "男", "不是女" , "大叔", "line", "私"]
#msgban = ["私"]
msgquit = ["對方已離開聊天"]
msgsend = u'午安 台北30粗公'
#msgsend = u'台北女'
count =u'0952597567'
pwd = u'Pigwu0822'

class Wootalk():
    def setUp(self,responseTime):
        self.driver = webdriver.Chrome(executable_path="C:\Python34\Scripts\chromedriver.exe")
        self.driver.implicitly_wait(10)
        #self.base_url = "https://www.myfone.com.tw/buy/index.php?action=event20191001"
        self.base_url = "https://www.myfone.com.tw/buy/main.php?action=supersale_list"
        #self.base_url = "https://www.catch.net.tw/auth/myfoneshopping_login_full.jsp?return_url=https%3A%2F%2Fwww.myfone.com.tw%2Fbuy%2Fbackground%2Fbg.sso_receiver.php&from_ch=NEWEC&cancel_return_url=https%3A%2F%2Fwww.myfone.com.tw%2Fbuy%2Fmain.php%3Faction%3Dsupersale_cart%26fm%3Dpf&google_login_url=https%3A%2F%2Fwww.myfone.com.tw%2Fbuy%2Fgoogle%2Fopenid%2Flogin%2Fw%2F%3Forigin_url%3Dhttps%3A%2F%2Fwww.myfone.com.tw%2Fbuy%2Fmain.php%3Faction%3Dsupersale_cart%26fm%3Dpf"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.responseTime = responseTime
        self.driver.get(self.base_url)

    def launch(self):

        #selenium usage
        driver = self.driver
        driver.get(self.base_url)
        
        print("Test")
        #WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[@class="搶購GO"]'))).click()   
        try:
            #/a/div[@class='btnGo']
            #WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[@class="btnGo"]'))).click()  
            #driver.find_element_by_xpath("//div[@class=\"btnGo\"]").click()
            #/div[@class=\"btnGo\"]"
            #driver.find_element_by_xpath("//a[@href='https://www.myfone.com.tw/buy/main.php?action=supersale_list']/div[@class='btnGo'").click()
            #//*[@class='myclass' and contains(text(),'qwerty')]
            #driver.find_element_by_xpath("//a[@href='https://www.myfone.com.tw/buy/main.php?action=supersale_list']/div[@class='btnGo' and contains(text(),'搶購GO')").click()
            driver.find_element_by_xpath("//button[@class='btn btn-default' and contains(text(),'立即搶購') ]").click()
            #driver.find_elements_by_xpath("//div[@class=\"message-content\"]"
            #windows=driver.window_handles
            #driver.switch_to.window(windows[-1])
            #print(driver.current_url)
            driver.get(driver.current_url)
            #time.sleep(3)
            #print(driver.find_element_by_xpath("//div[@class='a1']/input[1]"))
            message_count=driver.find_element_by_xpath("//div[@class='a1']/input[@id='loginAccount']")
            message_count.send_keys(count)
            message_pwd=driver.find_element_by_xpath("//div[@id='login_box']/div[7]/input[@id='loginPW']")
            #message_count = driver.find_element_by_class_name("a1")
            #print(message_count.text)
            message_pwd.send_keys(pwd)
            message_count=driver.find_element_by_xpath("//div[@id='login_box']/a[2]/div[@class='bt1']").click()

        except:
            print("Unexpected error:", sys.exc_info()[0])
           


def is_element_present(self, how, what):
    try: self.driver.find_element(by=how, value=what)
    except NoSuchElementException as e: return False
    return True

def is_alert_present(self):
    try: self.driver.switch_to_alert()
    except NoAlertPresentException as e: return False
    return True

def close_alert_and_get_its_text(self):
    try:
        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        if self.accept_next_alert:
            alert.accept()
        else:
            alert.dismiss()
        return alert_text
    finally: self.accept_next_alert = True

def close(self):
    self.driver.quit()
