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
from bs4 import BeautifulSoup

#msgban = ["嗨", "嗎", "您好", "在" , "hello", "hi"];
msgban = ["嗨", "我男", "男", "不是女" , "大叔", "line", "私"];
msgquit = ["對方已離開聊天"]

class Wootalk():
    def setUp(self,responseTime):
        self.driver = webdriver.Chrome(executable_path="C:\Python34\Scripts\chromedriver.exe")
        self.driver.implicitly_wait(10)
        self.base_url = "https://knock.tw/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.responseTime = responseTime  
    
    def launch(self):

        #selenium usage
        driver = self.driver
        driver.get(self.base_url)
               
        #selenium start to click button
        driver.find_element_by_class_name('start').click()
        message=driver.find_element_by_class_name('main-input')
        time.sleep(3)
        for msg in driver.find_elements_by_xpath("//div[@class=\"message-content\"]"):
            if msgquit[0] in msg.text:
                print("對方離開")
                driver.find_element_by_xpath("//button[text()=\"對話已結束，請點我重新配對聊天\"]").click()
            else:
                message.send_keys(u'早安 台北30喝酒小雞男')
                driver.find_element_by_class_name('send').click()

        message_sent = False
        i = 0
        while 1:
            print("===START====")
        
            texts = len(driver.find_elements_by_xpath("//div[@class=\"message-content\"]"))
            
            #print("text=",texts)
            
            msglist = []

            print("loop time=",i)
            print("Quit loop times = ",self.responseTime) 

            
            if i == self.responseTime :
                driver.find_element_by_xpath("//i[@title=\"顯示更多操作\"]").click()
                time.sleep(1)
                driver.find_element_by_xpath("//i[@title=\"離開對話\"]").click()
                time.sleep(1)
                driver.find_element_by_xpath("//button[@class='modal-default-button confirm']").click()
                i = 0
                message_sent = False
                print("超過時間,換人!")
                return False
            else :
                #print(find_elements_by_xpath("//span[contains(text())]") )
                #print("Test content")
                #print(driver.find_elements_by_xpath("//div[@class=\"message-content\"]/span"))
                
               
                #對方有訊息 

                if texts > 2:
                    print("對方有訊息") 

                    #BeautifulSoup usage
                    #Noted soup is not suit for chat , 解析不出對話
                    '''
                    response = rq.get(self.base_url) # 用 requests 的 get 方法把網頁抓下來
                    html_doc = response.text # text 屬性就是 html 檔案
                    soup = BeautifulSoup(response.text , "html.parser") # 指定 lxml 作為解析器


                    recommendations = soup.find_all('div', class_ = 'message-content')
                    print("recommendations") 
                    print(recommendations)

                    for recommendation in recommendations:
                        #try:
                        print("extract") 
                        print(recommendation)
                        msg = recommendation.find('span').get_text()
                        print(msg)
                            #except:
                    '''
                    for msg in driver.find_elements_by_xpath("//div[@class=\"message-content\"]"):
                        #print(msg.text)
                        for j in range(len(msgban)):
                            if msgban[j] in msg.text and msg.text is not msgquit[0]: 
                                print("符合跳出關鍵字")

                                driver.find_element_by_xpath("//i[@title=\"顯示更多操作\"]").click()
                                time.sleep(1)
                                driver.find_element_by_xpath("//i[@title=\"離開對話\"]").click()
                                time.sleep(1)
                                driver.find_element_by_xpath("//button[@class='modal-default-button confirm']").click()
                                i = 0
                                message_sent = False
                                return False
                            elif msgquit[0] in msg.text: 
                                print("對方離開")
                                driver.find_element_by_xpath("//button[text()=\"對話已結束，請點我重新配對聊天\"]").click()
                            else :
                                if i==2:
                                    print("通知介入")
                                    return True
            i=i+1
            try:
                #對方斷開聊天
                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
                return False

            except:
                continue

    
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
