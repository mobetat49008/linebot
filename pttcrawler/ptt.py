import requests
from bs4 import BeautifulSoup
import time
import sys
sys.path.append("../PTTLibrary")
from PTTLibrary import PTT
import numpy as np
sys.path.append("../include")
import inc
import json

ID=["pppla","dddddddd","zeen3033"]
Password="2b58aaj2"
Query = True
str1=''
str2=''

FirstRange = 20

FastInit = True
InitControl = [True,True,True]
everread = [False,False,False]
contents = None

O2Author = []
TestAuthor = ['pppla','dddddddd','donotworryok']
MailTitle = u'如果你也喜歡說走就走'
removestr = "("
removestr1 = ")"
whiteOptionAuthor = ['kevin5','bluesky2','CrazyR']
whiteStockAuthor = ['zesonpso']
LastFloor = 0
SaveIndex={}

from enum import Enum
 
class InputType(Enum):
    Board = 0
    Index = 1
    Condition = 2


SlowList = [
    #('Wanted', PTT.PostSearchType.Keyword, '[公告]'),
    #('Wanted', PTT.PostSearchType.Author, 'gogin'),
    #('Wanted', PTT.PostSearchType.Push, '10'),
    #('Wanted', PTT.PostSearchType.Mark, 'm'),
    #('Wanted', PTT.PostSearchType.Money, '5'),
    ('Gossiping', PTT.PostSearchType.Keyword, '韓'),
    #('Gossiping', PTT.PostSearchType.Keyword, '李佳芬'),
    #('Gossiping', PTT.PostSearchType.Author, 'tsukiyomi157'),
    #('Gossiping', PTT.PostSearchType.Push, '10'),
    #('Gossiping', PTT.PostSearchType.Mark, 'm'),
    #('Gossiping', PTT.PostSearchType.Money, '5'),
    #('Gossiping', PTT.PostSearchType.Push, '-100'),
    #('Gossiping', PTT.PostSearchType.Push, '100'),
    ('Alltogether', PTT.PostSearchType.Keyword, '徵男'),
]

FastList = [
    ('Option', PTT.PostSearchType.Keyword, '閒聊'),
]

DayList = [
    ('Stock', PTT.PostSearchType.Author, 'NG1999'),
    #('Stock', PTT.PostSearchType.Author, 'zesonpso'),
    ('Stock', PTT.PostSearchType.Push, '20'),
]

#建立一個寬度為3,高度為2的陣列, 後面表示高度
# Row1 - Slow 
# Row2 - Fast
# Row3 - Day
LastIndex =  [([0] * len(SlowList)) for i in range(3)]
StartIndex = [([0] * len(SlowList)) for i in range(3)]

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
    global str2
    global LastFloor

    PushCount = 0
    BooCount = 0
    ArrowCount = 0

    Buffer = ''
    SpecificAuthor = ''

    positionleft=0
    
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
        #print("進入爬蟲,內容為:")
        #print(f'[推:{str(PushCount)}][噓:{str(BooCount)}][{Post.getWebUrl()}][{Post.getAID()}][{Post.getTitle()}]')
        str1 = str1+ f'[推:{str(PushCount)}][噓:{str(BooCount)}]' +f'{Post.getTitle()}' + "\n" + f'{Post.getWebUrl()}' + "\n"

    if Post.getBoard() == "Alltogether":

        O2Author.append(f'{Post.getAuthor()}')

    if Post.getBoard() == "Stock":

        if Post.getDeleteStatus() != PTT.PostDeleteStatus.NotDeleted:
            if Post.getDeleteStatus() == PTT.PostDeleteStatus.ByModerator:
                print(f'[板主刪除][{Post.getAuthor()}]')
            elif Post.getDeleteStatus() == PTT.PostDeleteStatus.ByAuthor:
                print(f'[作者刪除][{Post.getAuthor()}]')
            elif Post.getDeleteStatus() == PTT.PostDeleteStatus.ByUnknow:
                print(f'[不明刪除]')
            return

        SpecificAuthor = Post.getAuthor()
        positionleft = SpecificAuthor.find(removestr)

        #Noted that rstrip() is necessnary to remove the space
        if SpecificAuthor[:positionleft].rstrip() == 'zesonpso' or SpecificAuthor[:positionleft].rstrip() == 'NG1999':
            str1 = str1 +f'{Post.getTitle()}' + "\n" + f'{Post.getWebUrl()}' + "\n"
        else :

            for Push in Post.getPushList():

                if Push.getAuthor() == 'zesonpso' or Push.getAuthor() == 'NG1999':
                    Author = Push.getAuthor()
                    Content = Push.getContent()
                    Buffer += f'{Author} 說 {Content}' +"\n"

            str1 = str1 + Buffer

    #To avoid length too long
    if len(Buffer) > 2000:
        str1 = str1[:1999]
    else:
        str1 = str1

    
def crawlone(Post):

    global Query
    global str1
    global str2
    global LastFloor

    PushCount = 0
    BooCount = 0
    ArrowCount = 0
    Buffer = ''
    startfloor = 0

    if Post.getBoard() == 'Option':
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

            Author = Push.getAuthor()
            Content = Push.getContent()

            for j in range(len(whiteOptionAuthor)):
                
                if whiteOptionAuthor[j] == Author :
                    startfloor +=1
                    if startfloor > LastFloor:
                        LastFloor += 1
                        Buffer += f'{Author} 說 {Content}' +"\n"

                #print(Buffer)
        #print("起始樓層:",startfloor)
        #print("終止樓層:",LastFloor)
        #Buffer += f'時間是 {Push.getTime()}'
        #line limitation
        if len(Buffer) > 2000:
            str1 = str1+ Buffer[:1999]
        else:
            str1 = str1+ Buffer
    

def pttgrab(rowindex):

    global str1
    global str2
    global SlowInit
    global DayInit
    global LastIndex
    global contents
    global O2Author
    global InitControl
    global SaveIndex
    global everread
    returnstr=''
    PTTBot = PTT.Library()
    boardindex=0
    positionleft=0
    positionright=0
    ColumeIndex=1
    Author = ''
    f=[{'Init':False}]
    data = {}
   
    #print("=======SaveIndex1============",everread[rowindex])

    if everread[rowindex] == False:
        with open("pttrecord.json","r", encoding='utf-8') as file:
            data = json.load(file)

            #if python file is destoryed, mark this line to rebuild
            try:
                InitControl[rowindex] = data[str(rowindex)][0]['Init']
                if InitControl[rowindex] == True:
                    #print("=======SaveIndex0============",SaveIndex)
                    SaveIndex[rowindex] = f
                else:
                    #SaveIndex = data
                    #print("=======SaveIndex1============",SaveIndex)
                    SaveIndex[rowindex] = data[str(rowindex)]
                    InitControl[rowindex] = False
                    #print("=======SaveIndex2============",SaveIndex[rowindex][ColumeIndex]['ArticleIndex'])
                #print("=======TEST1:",data["0"][2]["ArticleIndex"])
   
            except:
                print("=======SaveIndex3============",SaveIndex)
                SaveIndex[rowindex] = f    

            everread[rowindex] = True 

    try:
        PTTBot.login(ID[rowindex], Password,KickOtherLogin=True)
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

    if rowindex==0:
        grablist = SlowList
    elif rowindex==1:
        grablist = FastList
    elif rowindex==2:
        grablist = DayList 

    for (Board, SearchType, Condition) in grablist:

        showCondition(Board, SearchType, Condition)
        NewestIndex = PTTBot.getNewestIndex(
            PTT.IndexType.BBS,
            Board,
            SearchType=SearchType,
            SearchCondition=Condition,
        )
        print(f'{Board} 最新文章編號 {NewestIndex}')
        print("是否已初始化",InitControl[rowindex])

        if InitControl[rowindex] == True:
            StartIndex[rowindex][boardindex] = NewestIndex - FirstRange + 1
            if NewestIndex - FirstRange + 1 <=0 :
                StartIndex[rowindex][boardindex] = 1
            rowArray = []
            rowArray.append({'Board':Board, 'ArticleIndex':StartIndex[rowindex][boardindex], 'Condition':Condition})
            #print("飛驢=======SaveIndex1========>",SaveIndex)
            SaveIndex[rowindex] += rowArray

        else :
            #print("ColumeIndex=",ColumeIndex)
            LastIndex[rowindex][boardindex] = SaveIndex[rowindex][ColumeIndex]['ArticleIndex']
            StartIndex[rowindex][boardindex] = LastIndex[rowindex][boardindex]+1
            #print("飛驢=======SaveIndex2========>",SaveIndex)
            #SaveIndex[rowindex][ColumeIndex]['ArticleIndex'] = StartIndex[rowindex][boardindex]
            SaveIndex[rowindex][ColumeIndex]['ArticleIndex'] = NewestIndex

        #Update the NewestIndex
        #LastIndex[rowindex][boardindex] = NewestIndex 

        if StartIndex[rowindex][boardindex] > NewestIndex :
            StartIndex[rowindex][boardindex] = NewestIndex

        print("START:",StartIndex[rowindex][boardindex])
        print("LAST:",LastIndex[rowindex][boardindex])
        print("Value:",StartIndex)
        print("boardindex:",boardindex)

        if Board != 'Option':
            if StartIndex[rowindex][boardindex] != NewestIndex:
                ErrorPostList, DelPostList = PTTBot.crawlBoard(
                    crawlHandler,
                    PTT.CrawlType.BBS,
                    Board,
                    StartIndex=StartIndex[rowindex][boardindex],
                    EndIndex=NewestIndex,
                    SearchType=SearchType,
                    SearchCondition=Condition,
                    #Query=True,
                )
    
        else :
            
            if StartIndex[rowindex][boardindex] != NewestIndex:
                LastFloor = 0
        
            Post = PTTBot.getPost(
                Board,
                PostIndex=NewestIndex,
                SearchType=SearchType,
                SearchCondition=Condition,
            )
            crawlone(Post)

        boardindex=boardindex+1
        print('=' * 50)    

       
        returnstr = str1
        str1 =''

        if len(returnstr)!=0:
            inc.Setpttstr(returnstr)
            inc.SetBoardNum()

        ColumeIndex +=1


    #print("return長度:",len(returnstr))
    #print("SaveIndex:",SaveIndex)

    with open("pttrecord.json","r", encoding='utf-8') as r_file:
        data = json.load(r_file)
        #print("data:",data)
        #print("Final SaveIndex1:",SaveIndex)
        #print("Final SaveIndex2:",SaveIndex[rowindex])
        data[str(rowindex)] = SaveIndex[rowindex]
        #print("Final data[str(rowindex)]:",data[str(rowindex)])
        #print("data:",data)
        
        with open("pttrecord.json","w", encoding='utf8') as w_file:
            json.dump(data,w_file,ensure_ascii=False,indent=4)

    #with open("pttrecord.json","r", encoding='utf-8') as f:
    #    data = json.load(f)
    #print("=======TEST:",data)
    #print("=======TEST1:",data["0"][1]['ArticleIndex'])
    
    #InitControl[rowindex] = False

    print(O2Author)

    if O2Author:
        try:
            f = open('C:\linebot\pttcrawler\mailmsg.txt', 'r' , encoding='utf8', newline='')    # 打开文件
            contents = f.read()
            f.close()

            for i in range(len(O2Author)):
                Author = O2Author[i]
                positionleft = O2Author[i].find(removestr)
                positionright = O2Author[i].find(removestr1)
                #print(Author[:positionleft])

                try:
                    
                    PTTBot.mail(
                        # 寄信對象
                        Author[:positionleft],
                        # 標題
                        MailTitle,
                        # 內文
                        contents,
                        # 簽名檔
                        0
                    )
                    
                    print("寄信給:",Author[:positionleft])
                except PTT.Exceptions.NoSuchUser:   
                    print('No Such User')
        except:
            print("Unexpected error:", sys.exc_info()[0])
        finally:
            O2Author = []

    #PTT logout
    #print(SaveIndex)
    #print(SaveIndex[0])
    #print(SaveIndex[0][0])
    #print(SaveIndex[0][0]['ArticleIndex'])
    #print(SaveIndex[0][1]['ArticleIndex'])
    #print(SaveIndex[0][2]['ArticleIndex'])
    
    PTTBot.logout()
