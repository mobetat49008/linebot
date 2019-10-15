#!/usr/bin/python
# -*- coding: utf-8 -*-  
from web import Wootalk
import time,os


def knock():
    result = False
    w = Wootalk()
    print("====")
    w.setUp(3) # 30秒無人回應，自動離開換人/驗證時間
    while 1:
        result=w.launch()
        
        if result == True:
            return True
