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
msgsend = u'午安 台北30夜景純粹喝大叔'
#msgsend = u'台北女'

class Wootalk():
    def setUp(self,responseTime):
        self.driver = webdriver.Chrome(executable_path="C:\Python34\Scripts\chromedriver.exe")
        self.driver.implicitly_wait(10)
        self.base_url = "https://knock.tw/"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.responseTime = responseTime
        self.driver.get(self.base_url)
    
    def launch(self):

        #selenium usage
        driver = self.driver
        driver.get(self.base_url)
               
        #selenium start to click button
        #driver.find_element_by_class_name('start').click()
        #Record init array
        msg_init= []
        msg_receive = ''
        message_sent = False

        try:
            WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[@class="start"]'))).click()
            message=driver.find_element_by_class_name('main-input')
        except:
            print("Can't find start button")
            #Can't find start button so try to press exit button
            try:
                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
            except:
                print("Can't find start button-->Quit")
                return False
            
        time.sleep(3)
        
        try:
            #有時候來不及送訊息對方就斷開連接
            WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
            print("Connection is disconnected before sending the msg")
            return False
        except:
            pass

        for msg in driver.find_elements_by_xpath("//div[@class=\"message-content\"]"):
            if msgquit[0] in msg.text:

                #driver.find_element_by_xpath("//button[text()=\"對話已結束，請點我重新配對聊天\"]").click()
                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
                print("對方斷開聊天-0")
                return False
            else:
                if message_sent==False:
                
                    #也會發生無法發送訊息就斷開的情形
                    try:
                        message.send_keys(msgsend)
                    except:
                        driver.find_element_by_xpath("//button[text()=\"對話已結束，請點我重新配對聊天\"]").click()
                    driver.find_element_by_class_name('send').click()
                    message_sent=True

        msg_init= msg.text
        #print("msg_init=",msg_init)
        #print("msg_init長度=",len(msg_init))#73
        #print("msg_send長度=",len(msgsend)) #18

        i = 0
        while 1:
            print("===START====")
        
            texts = len(driver.find_elements_by_xpath("//div[@class=\"message-content\"]"))
            
            #for msg in driver.find_elements_by_xpath("//div[@class=\"message-content\"]"):
            #    print("0=====訊息=",msg.text)
            #    print("0=====訊息自元長度=",len(msg.text))
            
            msglist = []

            print("loop time=",i)
            print("Quit loop times = ",self.responseTime) 
            print("總訊息長度=",texts)
            
            if i == self.responseTime :
                #print("超過時間,換人!")
                driver.find_element_by_xpath("//i[@title=\"顯示更多操作\"]").click()
                time.sleep(1)
                driver.find_element_by_xpath("//i[@title=\"離開對話\"]").click()
                time.sleep(1)

                #有時候會有按不到的情形
                #try:                               
                driver.find_element_by_xpath("//button[@class='modal-default-button confirm']").click()
                #except:
                #    WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[@class="start"]'))).click()  
                i = 0
                message_sent = False
                print("對方斷開聊天-1")
                return False
            else :
                #print(find_elements_by_xpath("//span[contains(text())]") )
                #print("Test content")
                #print(driver.find_elements_by_xpath("//div[@class=\"message-content\"]/span"))
                
               
                #對方有訊息 
                #print("等待對方發訊") 

                if texts > 2:
                    #print("對方有訊息") 

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
                        #print("1=====訊息=",msg.text)
                        #print("訊息自元長度=",len(msg.text))
                        for j in range(len(msgban)):
                            #print("檢查是否有ban的字串...")
                            if msgban[j] in msg.text and msg.text != msgquit[0]: 

                                driver.find_element_by_xpath("//i[@title=\"顯示更多操作\"]").click()
                                time.sleep(1)
                                driver.find_element_by_xpath("//i[@title=\"離開對話\"]").click()
                                time.sleep(1)
                                
                                #有時候會有按不到的情形
                                try:                               
                                    driver.find_element_by_xpath("//button[@class='modal-default-button confirm']").click()
                                except:
                                    WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[@class="start"]'))).click()    
                                i = 0
                                message_sent = False
                                print("符合跳出關鍵字")
                                return False
                            elif msgquit[0] in msg.text: 

                                #print("對方離開")
                                #driver.find_element_by_xpath("//button[text()=\"對話已結束，請點我重新配對聊天\"]").click()
                                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
                                print("對方斷開聊天-2")
                                return False
                            #else :
                                #例外1.len(msg.text)!= len(msg_init)*2 : 初始字串重複兩次
                                #例外2.len(msg.text)!=len(msg_init)+len(msgsend) : 初始字串+自帶字串 
                                #例外3.len(msg.text)!=len(msg_init) : 抓到初始字串
                                #例外4.len(msg.text)!=len(msgsend) : 抓到自帶字串

                        if  msg.text != msgquit[0] and len(msg.text)!= len(msg_init)*2 and len(msg.text)!=len(msg_init)+len(msgsend):
                            #print("2=====訊息:",msg.text) 
                            #print("訊息長度=",texts)
                            #print("訊息自元長度=",len(msg.text))
                            
                            if len(msg.text)!=len(msg_init) and len(msg.text)!=len(msgsend):
                                #print("3=====訊息:",msg.text) 
                                #print("訊息長度=",texts)
                                #print("訊息自元長度=",len(msg.text))
                                if msg_receive.find(msg.text)<0:
                                    msg_receive = msg_receive + msg.text + "\n"
                                    #print("測試回傳訊息")
                                    #print(msg.text)
                                    #print(msg_receive)
                                    inc.Setstr(msg_receive)
                                    #print("4=====訊息:",msg_receive) 
                                #print(inc.Getstr())

                    if i>=2:
                        print("通知介入")
                        #print("2=====msg_receive:",msg_receive)
                        #print(inc.Getstr())
                        return True

                #if texts == 2:
                 #   for msg in driver.find_elements_by_xpath("//div[@class=\"message-content\"]"):
                 #       print("3=====訊息:",msg.text) 
                 #       print("訊息自元長度=",len(msg.text))
            i=i+1

            try:
                #對方斷開聊天
                #print("對方斷開聊天-3-1")
                WebDriverWait(driver,1).until(EC.presence_of_element_located((By.XPATH, '//button[text()="對話已結束，請點我重新配對聊天"]'))).click()
                print("對方斷開聊天-3-2")
                return False

            except:
                #print("Continue")
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
