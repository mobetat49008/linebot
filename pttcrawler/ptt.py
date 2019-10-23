import requests
from bs4 import BeautifulSoup
import time
import sys
sys.path.append("../PTTLibrary")
from PTTLibrary import PTT
import numpy as np

ID="pppla"
Password="123456"
Query = True
str1=''

FirstRange = 20

Init = True
contents = None
boardnum =2
LastIndex = [0,0]
StartIndex = [0,0]
O2Author = []
TestAuthor = ['pppla','dddddddd','donotworryok']
MailTitle = u'如果你也喜歡說走就走'

TestList = [
    #('Wanted', PTT.PostSearchType.Keyword, '[公告]'),
    #('Wanted', PTT.PostSearchType.Author, 'gogin'),
    #('Wanted', PTT.PostSearchType.Push, '10'),
    #('Wanted', PTT.PostSearchType.Mark, 'm'),
    #('Wanted', PTT.PostSearchType.Money, '5'),
    ('Gossiping', PTT.PostSearchType.Keyword, '韓'),
    #('Gossiping', PTT.PostSearchType.Author, 'ReDmango'),
    #('Gossiping', PTT.PostSearchType.Push, '10'),
    #('Gossiping', PTT.PostSearchType.Mark, 'm'),
    #('Gossiping', PTT.PostSearchType.Money, '5'),
    #('Gossiping', PTT.PostSearchType.Push, '-100'),
    #('Gossiping', PTT.PostSearchType.Push, '150'),
    ('Alltogether', PTT.PostSearchType.Keyword, '徵男'),
]


def showCondition(Board, SearchType, Condition):
    if SearchType == PTT.PostSearchType.Keyword:
        Type = '關鍵字'
    if SearchType == PTT.PostSearchType.Author:
        Type = '作者'
    if SearchType == PTT.PostSearchType.Push:
        Type = '推文數'
    if SearchType == PTT.PostSearchType.Mark:
        Type = '標記'
    if SearchType == PTT.PostSearchType.Money:
        Type = '稿酬'

    print(f'{Board} 使用 {Type} 搜尋 {Condition}')

def crawlHandler(Post):

    global Query
    global str1

    PushCount = 0
    BooCount = 0
    ArrowCount = 0
    
    if Post.getBoard() == 'Gossiping':
        if Post.getDeleteStatus() != PTT.PostDeleteStatus.NotDeleted:
            if Post.getDeleteStatus() == PTT.PostDeleteStatus.ByModerator:
                print(f'[板主刪除][{Post.getAuthor()}]')
            elif Post.getDeleteStatus() == PTT.PostDeleteStatus.ByAuthor:
                print(f'[作者刪除][{Post.getAuthor()}]')
            elif Post.getDeleteStatus() == PTT.PostDeleteStatus.ByUnknow:
                print(f'[不明刪除]')
            return

        for Push in Post.getPushList():
            PushType = Push.getType()

            if PushType == PTT.PushType.Push:
                PushCount += 1
            elif PushType == PTT.PushType.Boo:
                BooCount += 1
            elif PushType == PTT.PushType.Arrow:
                ArrowCount += 1
        
        #print(f'[推:{str(PushCount)}][噓:{str(BooCount)}][{Post.getWebUrl()}][{Post.getAID()}][{Post.getTitle()}]')
        str1 = str1+ f'[推:{str(PushCount)}][噓:{str(BooCount)}]' +f'{Post.getTitle()}' + "\n" + f'{Post.getWebUrl()}' + "\n"

    if Post.getBoard() == "Alltogether":

        O2Author.append(f'{Post.getAuthor()}')
    



def pttgrab():

    global str1
    global Init
    global LastIndex
    global contents
    global O2Author
    returnstr=''
    PTTBot = PTT.Library()
    i=0

    try:
        PTTBot.login(ID, Password)
    except PTT.Exceptions.LoginError:
        PTTBot.log('登入失敗')
        sys.exit()
    except PTT.Exceptions.WrongIDorPassword:
        PTTBot.log('帳號密碼錯誤')
        sys.exit()
    except PTT.Exceptions.LoginTooOften:
        PTTBot.log('請稍等一下再登入')
        sys.exit()
    PTTBot.log('登入成功')

    for (Board, SearchType, Condition) in TestList:

        showCondition(Board, SearchType, Condition)
        NewestIndex = PTTBot.getNewestIndex(
            PTT.IndexType.BBS,
            Board,
            SearchType=SearchType,
            SearchCondition=Condition,
        )
        print(f'{Board} 最新文章編號 {NewestIndex}')
        print(Init)
        if Init == True:
            StartIndex[i] = NewestIndex - FirstRange + 1
            LastIndex[i] = NewestIndex
            
        else :
            #StartIndex = NewestIndex - LastIndex + 1
            StartIndex[i] = LastIndex[i]
        print(StartIndex[i])
        if StartIndex[i] != NewestIndex:
            ErrorPostList, DelPostList = PTTBot.crawlBoard(
                crawlHandler,
                PTT.CrawlType.BBS,
                Board,
                StartIndex=StartIndex[i],
                EndIndex=NewestIndex,
                SearchType=SearchType,
                SearchCondition=Condition,
                #Query=True,
            )

        i=i+1
        print('=' * 50)        
       
        returnstr = str1
    if len(returnstr)==0:
        returnstr = "無更新"
    str1 =''
    print("return長度:",len(returnstr))
    Init = False

    print(O2Author)
    #print(len(O2Author))
    try:
        f = open('C:\linebot\pttcrawler\mailmsg.txt', 'r' , encoding='utf8', newline='')    # 打开文件
        contents = f.read()
        f.close()

        for i in range(len(O2Author)):
            try:
                PTTBot.mail(
                    # 寄信對象
                    O2Author[i],
                    # 標題
                    MailTitle,
                    # 內文
                    contents,
                    # 簽名檔
                    0
                )
            except PTT.Exceptions.NoSuchUser:   
                print('No Such User')
    except:
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        O2Author = []
        return returnstr