#!/usr/bin/python
# -*- coding: utf-8 -*-  
from web import Wootalk
import time,os


def knock():
    result = False
    w = Wootalk()
    
    w.setUp(3) # 30秒無人回應，自動離開換人/驗證時間
    while 1:
        print("迴圈重新開始")
        result=w.launch()
        print("判斷ing...")
        if result == True:
            print("準備通知介入")
            return True
