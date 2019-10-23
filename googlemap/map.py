#!/usr/bin/python
# -*- coding: utf-8 -*-  

import requests
import re
import configparser
import json
import sys
from bs4 import BeautifulSoup
import random
import time
sys.path.append("../include")
import inc
#|meal_deliveryrestaurant|
#type的設定:http://qwe81301-nuu.blogspot.com/2015/10/google-map-google-places-api.html

def search(addr):
    # 預設地址
    address = addr
    # 你的API_KEY
    GOOGLE_API_KEY = 'AIzaSyBcSLh7a-UmBO4Yj7P0Nlmi0ycb3k-oCB0'

    addurl = 'https://maps.googleapis.com/maps/api/geocode/json?key={}&address={}&sensor=false'.format(GOOGLE_API_KEY,address)

    # 經緯度轉換
    addressReq = requests.get(addurl)
    addressDoc = addressReq.json()
    lat = addressDoc['results'][0]['geometry']['location']['lat']
    lng = addressDoc['results'][0]['geometry']['location']['lng']
    pagetoken = None
    list = ''
    count = 0

    while True:

        # 取得店家資訊
        #foodStoreSearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={}&location={},{}&rankby=distance&type=restaurant&language=zh-TW".format(GOOGLE_API_KEY, lat, lng)
        foodStoreSearch = "https://maps.googleapis.com/maps/api/place/textsearch/json?key={}&location={},{}&rankby=distance&{type}&language=zh-TW&user_ratings_total&{pagetoken}".format(GOOGLE_API_KEY, lat, lng, type="&type="+"food " ,pagetoken = "&pagetoken="+pagetoken if pagetoken else "")
        foodReq = requests.get(foodStoreSearch)
        nearbyRestaurants_dict = foodReq.json()
        #不指定就只抓取20筆資料
        top20Restaurants = nearbyRestaurants_dict["results"]
        res_num = (len(top20Restaurants)) 

        # 取評分高於3.9的店家
        bravo=[]

        for i in range(res_num):
          try:
            if top20Restaurants[i]['rating'] > 3.9 and top20Restaurants[i]['user_ratings_total'] > 400:
              #print('rate:\n', top20Restaurants[i]['rating'])
              bravo.append(i)
          except:
            KeyError
        if len(bravo) < 0:
          print("沒東西可以吃")
          # restaurant = random.choice(top20Restaurants) 沒有的話隨便選一間

        #印出高於3.9的店家
        for j in range(len(bravo)):
            restaurant = top20Restaurants[bravo[j]]

            # 檢查餐廳有沒有照片
            if restaurant.get("photos") is None:
              thumbnailImageUrl = None
            else:
              # 取得照片
              photoReference = restaurant["photos"][0]["photo_reference"]
              photoWidth = restaurant["photos"][0]["width"]
              thumbnailImageUrl = "https://maps.googleapis.com/maps/api/place/photo?key={}&photoreference={}&maxwidth={}".format(GOOGLE_API_KEY, photoReference,photoWidth)
              
            # 餐廳詳細資訊
            rating = "無" if restaurant.get("rating") is None else restaurant["rating"]
            address = "沒有資料" if restaurant.get("vicinity") is None else restaurant["vicinity"]
            comments = "無" if restaurant.get("user_ratings_total") is None else restaurant["user_ratings_total"]
            details = "Google Map評分：{}\n地址：{}\n評論數：{}".format(rating, address,comments)

            #逐筆印出結果
            print(restaurant.get("name"))
            print(details)
            
            newline_name = restaurant.get("name")
            newline_detail = details

             # 取得餐廳的 Google map 網址
            mapUrl = "https://www.google.com/maps/search/?api=1&query={lat},{long}&query_place_id={place_id}".format(lat=restaurant["geometry"]["location"]["lat"],long=restaurant["geometry"]["location"]["lng"],place_id=restaurant["place_id"])
            #print(mapUrl)

            list += str(count)+"."+newline_name + "\n" + newline_detail+ "\n"
            count +=1
            
        pagetoken = nearbyRestaurants_dict.get("next_page_token")
        
        if not pagetoken:
            break
        else:
            time.sleep(5)  

    print(list)
    return list
