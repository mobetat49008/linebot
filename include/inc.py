result=False
str = ''
pttstr = []
boardnum = 0

def Setresult(res): 
    
    global result 
    result = res
 
def Getresult(): 

    #print("inc.py:",result)
    return result

def Setstr(res): 
    
    global str 
    str = res
 
def Getstr(): 

    #print("inc.py:",str)
    return str

def SetBoardNum(): 
    
    global boardnum 
    boardnum =  boardnum + 1
 
def GetBoardNum(): 
    global boardnum 
    #print("inc.py:",str)
    return boardnum

def Setpttstr(res): 
    
    global ptrstr 
    pttstr.append(res)
 
def Getpttstr(boardindex): 
    global ptrstr 
    #print("inc.py:",pttstr[boardindex])
    return pttstr[boardindex]

def Cleanpttstr(): 
    global ptrstr 
    pttstr.clear()

def CleanBoardNum(): 
    
    global boardnum 
    boardnum =  0
