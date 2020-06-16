#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys  
from shopping import Wootalk
import time,os
import threading,queue

#w = Wootalk()


result = False
w = Wootalk()

w.setUp(3) # 30秒無人回應，自動離開換人/驗證時間

try:
    result=w.launch()
except:
    print("except")
#print("判斷ing...,result=",result)
#if result == True:
 #   print("準備通知介入")
    #return True

def open():
    
    w.setUp(3) # 30秒無人回應，自動離開換人/驗證時間

    
