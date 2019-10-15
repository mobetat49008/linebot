#coding=utf-8
from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path="C:\Python34\Scripts\chromedriver.exe")
driver.get('https://www.yuanrenxue.com')
time.sleep(5)

driver.find_element_by_class_name('search-show').click()

search = driver.find_element_by_id("isearch")
search.send_keys(u'python教程')