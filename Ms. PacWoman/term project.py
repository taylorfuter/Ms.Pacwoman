from tkinter import *
import random
import copy

#used barebones animation code

root=Tk()
highScores=[]
class Ghost(object):
    blueG=PhotoImage(file="Ms. PacWoman/images/blueG.gif")
    pinkG = PhotoImage(file="Ms. PacWoman/images/pinkG.gif")
    orangeG = PhotoImage(file="Ms. PacWoman/images/orangeG.gif")
    redG = PhotoImage(file="Ms. PacWoman/images/redG.gif")
    scared=PhotoImage(file="Ms. PacWoman/images/scared ghost.gif")

    def __init__(self,color,x,y,num,tarX,tarY):
        if color=="pink": self.image=Ghost.pinkG
        if color=="blue": self.image=Ghost.blueG
        if color=="orange": self.image=Ghost.orangeG
        if color=="red": self.image=Ghost.redG
        self.tar="spot" #first target is its "zone"
        self.x=x
        self.tarX=tarX
        self.tarY=tarY
        self.num=num
        self.temp=self.image
        self.y=y
        self.path=[]


    def getX(self):
        return self.x

    def setXY(self,x,y):
        self.x=x
        self.y=y

    def getY(self):
        return self.y

    def getImage(self):
        return self.image

    def setImage(self,img):
        self.image=img

    def sendHome(self,data): #when ghost is hit, send to box
        if len(data.ghostBox)==0:
            self.setXY(13,13)
        elif len(data.ghostBox)==1:
            self.setXY(13,11)
        else: self.setXY(13,15)
        self.path = []
        data.time[self.num - 5] = 0

    def rankDirs(self,x,y,targetX,targetY,scare):
        dirs=[] #sets direction order to better option for faster path
        if targetX<x or ((y==13 or y==14) and x==10):
            dirs.append((-1,0))
            dirs.append((1,0))
        else:
            dirs.append((1, 0))
            dirs.append((-1, 0))
        if targetY<y:
            dirs.insert(1,(0,-1))
            dirs.append((0,1))
        else:
            dirs.insert(1,(0, 1))
            dirs.append((0, -1))
        if scare:return dirs[::-1] #run away if scared
        return dirs

    #edited mazesolver as reference for validMove and moveGhost
    #used rankDirs in mazeSolver
    def validMove(self,data,x,y,): #if a ghost can move here
        if x>data.rows-1 or x<0 or y<0 or y>data.cols-1 \
                or data.board[x][y]==1 or (4<data.board[x][y]<9 \
                and data.board[x][y]!=self.num):
            return False
        return True

    def moveGhost(self,data,x,y,targetX,targetY,scare,count=0):
        if (x,y) in self.path: return False
        self.path.append((x,y))
        if x==targetX and targetY==y: return True
        if count==30:return True #prevents depth past 30, prevents huge lag if far
        directions=self.rankDirs(x,y,targetX,targetY,scare)
        if directions==[]:directions=[(0,1),(1,0),(0,-1),(-1,0)]
        for dir in directions:
            if self.validMove(data,x,y)==False:
                self.path.remove((x,y))
                return False
            if self.moveGhost(data,x+dir[0],y+dir[1],targetX,targetY,count+1):
                return True
        self.path.remove((x,y))
        return False

    def move(self,data,targetX=-1,targetY=-1,time=0):
        scare = data.countDown
        if targetX == -1 or targetY == -1: #set target to pacwoman
            targetX = data.pacX
            targetY = data.pacY
        x, y = self.x, self.y
        pre = data.board2[x][y]
        if time==0: #get the path to the target
            self.moveGhost(data,x,y,targetX,targetY,scare)
        if self.tar == "spot":
            self.tar= "pac"
        data.time[self.num-5]=1 #set  ghost's time to one
        if len(self.path)!=0:
            self.x,self.y=self.path.pop(0) #get next spot in path
        if len(self.path)==0: data.time[self.num-5]=0
        if scare==True: #if ghosts can die
            if data.board[self.x][self.y]==2:
                data.ghostBox.append(self) #put ghost in box
                self.sendHome(data)
                data.score+=200
                data.liveGhosts.remove(self)
        elif data.board[self.x][self.y] == 2:
            data.isGameOver = True #ghost killed pacwoman
        data.board[self.x][self.y] = self.num
        if pre==2: pre=-1
        if self.x!=x or self.y!=y:
            data.board[x][y]=pre


    def scare(self): #switch image to blue ghost
        self.image=Ghost.scared


def init(data): # load data as appropriate
        data.mode="MAIN"
        data.r, data.bigR= 3,10
        data.posX = 0
        data.rows, data.cols = 31, 28
        data.score=0
        data.isGameOver,data.isPaused=False,False
        data.pink=Ghost("pink",10,12,5,4,1)
        data.red = Ghost("red", 13, 11,6,4,data.cols-2)
        data.blue = Ghost("blue", 13, 13,7,22,1)
        data.orange = Ghost("orange", 13, 15,8,22,data.cols-2)
        data.dir,data.ghostMove = (0, 1),0
        data.ghostRelease,data.added=500,False
        data.pacX,data.pacY=data.rows//2,data.cols//2
        data.board2, data.delay, data.countDown = [], 700, False
        data.board = [([0] * data.cols) for row in range(data.rows)]
        boardOne(data)
        data.dotsLeft=countDots(data.board)-155
        data.level=1
        data.ghostSpeed=300//data.level
        data.time=[0,0,0,0]
        data.ghostBox=[data.blue,data.red,data.orange]
        data.liveGhosts,data.isPaused=[data.pink],True



def initC(canvas): #downloads all images
    canvas.name = PhotoImage(file="Ms. PacWoman/images/pacwoman name.gif")  # title
    canvas.pinkR = PhotoImage(file="Ms. PacWoman/images/pink R.gif")
    canvas.blueR = PhotoImage(file="Ms. PacWoman/images/blue R.gif")
    canvas.orangeR = PhotoImage(file="Ms. PacWoman/images/orange R.gif")
    canvas.pac = PhotoImage(file="Ms. PacWoman/images/pacman.gif")  # frame one of gif
    canvas.frame2 = PhotoImage(file="Ms. PacWoman/images/pacman.gif",
                        format="gif -index 2")  # frame 2 of gif
    canvas.pacR=PhotoImage(file="Ms. PacWoman/images/Pac left.gif") #frame 1
    canvas.pacR2 = PhotoImage(file="Ms. PacWoman/images/Pac left.gif",
                    format="gif -index 2")  # frame 2 of gif
    canvas.pacD = PhotoImage(file="Ms. PacWoman/images/PacD.gif")  # frame 1
    canvas.pacD2 = PhotoImage(file="Ms. PacWoman/images/PacD.gif",
                    format="gif -index 2")  # frame 2 of gif
    canvas.pacL = PhotoImage(file="Ms. PacWoman/images/PacL.gif")  # frame 1
    canvas.pacL2 = PhotoImage(file="Ms. PacWoman/images/PacL.gif",
                              format="gif -index 2")  # frame 2 of gif
    canvas.pacU = PhotoImage(file="Ms. PacWoman/images/PacU.gif")  # frame 1
    canvas.pacU2 = PhotoImage(file="Ms. PacWoman/images/PacU.gif",
                              format="gif -index 2")  # frame 2 of gif
    canvas.redR = PhotoImage(file="Ms. PacWoman/images/red R.gif")
    canvas.ins = PhotoImage(file="Ms. PacWoman/images/ins.gif")
    canvas.label = PhotoImage(file="Ms. PacWoman/images/instructions label.gif")
    canvas.scoreLabel=PhotoImage(file="Ms. PacWoman/images/score label.gif")
    canvas.gameOver=PhotoImage(file="Ms. PacWoman/images/GAME OVER .gif")
    canvas.image=canvas.pacR
    canvas.image2=canvas.pacR2

def countDots(arr):
    count=0 #return dots in board
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j]==0 or arr[i][j]==10:
                count+=1
    return count

def copyArr(arr): #deep copy of board
    copy=[]
    for i in range (len(arr)):
        row=[]
        for j in range(len(arr[i])):
            row.append(arr[i][j])
        copy.append(row)
    return copy

def placeGhosts(data):
    data.board[data.pink.getX()][data.pink.getY()] = 5  # pink ghost
    data.board[data.red.getX()][data.red.getY()] = 6  # red ghost
    data.board[data.blue.getX()][data.blue.getY()] = 7  # blue ghost
    data.board[data.orange.getX()][data.orange.getY()] = 8  # orange ghost


def boardOne(data): #sets up walls for board
    data.board[data.pacX][data.pacY]=2 #pacwoman
    for i in range(data.cols): #top and bottom
        data.board[0][i]=1
        data.board[24][i]=1
    for i in range(data.rows): #left and right
        if i==13: data.board[i][0],data.board[i][data.cols-1]=-1,-1
        else:data.board[i][0],data.board[i][data.cols-1]=1,1
    for i in range(3): #vertical line on top
        data.board[i+1][13],data.board[i+1][14]=1,1
    for i in range(2,4): #first/last block on top
        for j in range(2,5):
            data.board[i][j]=1
            data.board[i][data.cols-j-1]=1
    for i in range(2,4):#second/third block on top
        for j in range(5,11):
            data.board[i][j+1]=1
            data.board[i][data.cols-j-2]=1
    for i in range(2,6): #first/last block on 2nd row
        data.board[5][i],data.board[6][i]=1,1
        data.board[5][data.cols-1-i], data.board[6][data.cols-1-i] = 1, 1
    for i in range(10,18): #horizontalTop T
        data.board[6][i],data.board[5][i]=1,1
    for i in range(5,10): #vertical top T
        data.board[i][14],data.board[i][13]=1,1
    for i in range(5,13): #vertical part of horizontal T's
        data.board[i][8],data.board[i][7]=1,1
        data.board[i][data.cols-8], data.board[i][data.cols-9] = 1, 1
    for i in range(9,12): #horizontal of horizontal T
        data.board[9][i],data.board[8][i]=1,1
        data.board[9][data.cols-1-i],data.board[8][data.cols-1-i]=1,1
    for i in range(8,13): #blocks on side
        for j in range(6):
            if i!=8 and i!=12 and j!=5:
                data.board[i][j], data.board[i][data.cols - 1 - j] = -1, -1
            else:data.board[i][j],data.board[i][data.cols-1-j]=1,1
    for i in range(16,20): #lower blocks on side
        for j in range(4):
            if i!=16 and i!=19 and j!=3:
                data.board[i][j], data.board[i][data.cols - 1 - j] = -1, -1
            else:data.board[i][j],data.board[i][data.cols-1-j]=1,1
    for i in range(14,17): #boxes in middle
        for j in range(7,9):
            data.board[i][j],data.board[i][data.cols-j-1]=1,1
    for i in range(10,18): #top of ghost box
        if i==13 or i==14:
            data.board[11][i]=3
        else: data.board[11][i]=1
    for i in range(14,20): #vertical L
        data.board[i][5],data.board[i][data.cols-6]=1,1
    for i in range(2,5): #horizontal L
        data.board[14][i],data.board[14][data.cols-1-i]=1,1
    for i in range(2,12): #bottom weird T horizontal
        data.board[22][i],data.board[22][data.cols-1-i]=1,1
        data.board[21][i], data.board[21][data.cols - 1 - i] = 1, 1
    for i in range(18,22): #bottom weird T vertical
        data.board[i][8],data.board[i][data.cols-9]=1,1
        data.board[i][7],data.board[i][data.cols-8]=1,1
    for i in range(12,14): #empty ghost box
        for j in range(11,17):
            data.board[i][j]=-1
    for row in range(14,20):
        for i in range(10,18): #bottom T horizontal and bottom box
            if row==15 or row==17: continue
            if row==16 and (i==14 or i==13):continue #gap in bar
            data.board[row][i],data.board[row][i]=1,1
            data.board[row][i],data.board[row][i]=1,1
    for i in range(11,15): #box sides
        data.board[i][10],data.board[i][17]=1,1
    for i in range(19,23):#bottom T vertical
        data.board[i][13],data.board[i][14]=1,1
    data.board[4][1],data.board[4][data.cols-2]=10,10 #power up
    data.board[22][1],data.board[22][data.cols-2]=10,10 #power up
    data.board2=copyArr(data.board)
    placeGhosts(data)

# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.
def mousePressed(event, data):
    if data.mode=="MAIN": #toggle modes
        if 408<=event.x<=465 and 706<=event.y<=723:
            data.mode="HIGH SCORES"
    if data.mode=="HELP" or data.mode=="HIGH SCORES":
        if 506<=event.x<=571 and 717<=event.y<=737:
            data.mode="MAIN"

def keyPressed(event, data,canvas):
    if data.mode=="MAIN":
        if event.keysym=="p":
            data.mode="PLAY"
        if event.keysym=="h":
            data.mode="HELP"
    if data.mode=="PLAY":
        if event.keysym == "Up":
            data.dir = (-1, 0)
            canvas.image, canvas.image2 = canvas.pacU, canvas.pacU2
        if event.keysym == "Down":
            data.dir = (1, 0)
            canvas.image, canvas.image2 = canvas.pacD, canvas.pacD2
        if event.keysym == "Left":
            data.dir = (0, -1)
            canvas.image, canvas.image2 = canvas.pacL, canvas.pacL2
        if event.keysym == "Right":
            data.dir = (0, 1)
            canvas.image, canvas.image2 = canvas.pacR, canvas.pacR2
        if event.keysym=="p":
            data.isPaused=not data.isPaused
        if event.keysym=="r":
            init(data)
            canvas.image = canvas.pacR
            canvas.image2 = canvas.pacR2


def releaseGhost(data): #get ghost out of box
    if len(data.ghostBox)>0:
        ghost=data.ghostBox.pop(0)
        ghost.move(data,ghost.tarX,ghost.tarY,0)
        data.liveGhosts.append(ghost)


def timerFired(data,canvas):
    if data.mode=="MAIN":
        data.posX+=5
        if data.posX%2==0:
            data.frame="canvas.pacman"
        else: data.frame="canvas.frame2"
        if data.posX-550>=data.width:
            data.posX=0
    if data.mode=="PLAY":
        if data.isGameOver:return
        data.posX+=5
        if data.isPaused: return
        takeStep(data,canvas) #move forward
        if data.isPaused==False:
            if data.ghostSpeed%(5//data.level)==0: #speed of ghost
                data.ghostRelease-=100 #speed to release from box
                for ghost in data.liveGhosts: #target spot or ghost
                    if ghost.tar=="spot":ghost.move(data,ghost.tarX,ghost.tarY,data.time[ghost.num-5])
                    else:ghost.move(data,-1,-1,data.time[ghost.num-5])
            data.ghostSpeed-=3
            if data.ghostSpeed==0: data.ghostSpeed=300//data.level
            if data.ghostRelease==0: #release next ghost
                releaseGhost(data)
                data.ghostRelease=500
            if data.countDown: #turn ghosts blue
                data.delay-=20
            if data.delay==0:
                data.delay=700
                data.countDown=False
                data.pink.setImage(Ghost.pinkG)
                data.blue.setImage(Ghost.blueG)
                data.red.setImage(Ghost.redG)
                data.orange.setImage(Ghost.orangeG)


def nextLevel(data,canvas): #begin next level; speeds up ghosts
    score=data.score
    level=data.level+1
    init(data)
    data.score=score
    data.mode="PLAY"
    data.level=level
    data.isGameOver,data.isPaused=False,False
    canvas.image=canvas.pacR
    canvas.image2=canvas.pacR2


#used from snake code
def hitFood(data,newHeadRow,newHeadCol,canvas):
    # hit food
    data.board[newHeadRow][newHeadCol]-= 1
    data.board2[newHeadRow][newHeadCol] -= 1
    data.board[data.pacX][data.pacY] = -1
    data.board2[data.pacX][data.pacY] = -1
    data.pacX = newHeadRow
    data.pacY = newHeadCol
    data.score+=10
    data.dotsLeft-=1
    if data.dotsLeft==0:
        nextLevel(data,canvas)

def powerUp(data,newHeadRow,newHeadCol):
    # hit food
    data.board[newHeadRow][newHeadCol]-= 1
    data.board[data.pacX][data.pacY] = -1
    data.board2[data.pacX][data.pacY] = -1
    data.pacX = newHeadRow
    data.pacY = newHeadCol
    data.countDown,data.delay=True,700 #scare ghosts
    data.score+=50
    data.dotsLeft-=1
    data.pink.scare()
    data.red.scare()
    data.orange.scare()
    data.blue.scare()

#used from snake code
def takeStep(data,canvas):
    if data.isGameOver: return
    drow, dcol = data.dir[0],data.dir[1]
    newHeadRow = data.pacX + drow
    newHeadCol = data.pacY + dcol
    if newHeadCol<0:newHeadCol=data.cols-1
    if newHeadCol==data.cols: newHeadCol=0
    if (data.board[newHeadRow][newHeadCol] == 1): #hits wall
        newHeadRow-=drow
        newHeadCol-=dcol
    elif (data.board[newHeadRow][newHeadCol] == 0):
        hitFood(data,newHeadRow,newHeadCol,canvas)
    elif data.board[newHeadRow][newHeadCol]==10:
        powerUp(data,newHeadRow,newHeadCol)
    if (data.board[newHeadRow][newHeadCol] == -1): #forwards
        data.board[data.pacX][data.pacY]=-1
        data.board[newHeadRow][newHeadCol] = 2
        data.pacX = newHeadRow
        data.pacY = newHeadCol

#from snake
def getScores():
    st="\n\t"
    highScores.sort()
    for i in range(len(highScores)-1,len(highScores)-4,-1): #last 3
        if i<0: continue
        st+=str(highScores[i])+"\n\t" #formatting
    return st

def displayAll(canvas,data): #ghosts walk on title page
    if data.posX%2==0: #which frame of pacman
        canvas.create_image(data.posX, data.height / 2, image=canvas.pac)
    else: canvas.create_image(data.posX,data.height/2,image=canvas.frame2)
    canvas.create_image(data.posX-200,data.height/2,image=canvas.pinkR)
    canvas.create_image(data.posX-300,data.height/2,image=canvas.blueR)
    canvas.create_image(data.posX-400,data.height/2,image=canvas.redR)
    canvas.create_image(data.posX - 500, data.height / 2, image=canvas.orangeR)

def highScoresScreen(canvas,data):
    canvas.create_image(data.width / 2, 20, anchor=N, image=canvas.scoreLabel)
    canvas.create_text(data.width / 1.5, data.height / 1.35, anchor=S,
    text="CLICK 'HERE' TO RETURN TO MAIN MENU", font=("System", "24", "bold")
    , fill="white")
    canvas.create_text(data.width / 2, data.height / 2.5,
    font=("Times", "34", "bold"),fill="white", text="TODAY'S TOP SCORES ARE: " + getScores())


def helpSplashScreen(canvas,data):
    canvas.create_image(data.width/2,20,anchor=N,image=canvas.label)
    canvas.create_image(data.width/2,data.height/2.5,image=canvas.ins)
    canvas.create_text(data.width/1.5,data.height/1.35, anchor=S,
    text="CLICK 'HERE' TO RETURN TO MAIN MENU",font=("System","24","bold")
    ,fill="white")


def mainSplashScreen(canvas,data):
    canvas.create_image(data.width/2,20,anchor=N,image=canvas.name)
    displayAll(canvas,data) #ghosts loop
    canvas.create_text(data.width / 2, data.height / 1.5, font=("System", "20", "bold")
    , fill="white", text="PRESS 'P' TO START\n\nPRESS 'H' FOR HELP\n\n\
CLICK 'HERE' FOR HIGH SCORES")

# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.

def redrawAll(canvas, data):
    # draw in canvas
    if data.isGameOver:
        #lines 397-401 from snake
        if data.added==False: #didn't add score yet
         highScores.append(data.score)
         data.added=True
        canvas.create_text(data.width / 2, data.height / 2.5,
        font=("Times", "34", "bold"),fill="white",text="TODAY'S TOP SCORES ARE: " + getScores())
        canvas.create_text(data.width / 2, data.height / 1.75,
        font=("Times", "34", "bold"), fill="white", text="YOUR SCORE: " + str(data.score))
        canvas.create_image(data.width/2,20,anchor=N,image=canvas.gameOver)
        canvas.create_text(data.width / 2, data.height / 1.35, anchor=S,
        text="PRESS R TO RESTART", font=("System", "24", "bold"), fill="white")
        return
    if data.mode=="MAIN":
        mainSplashScreen(canvas,data)
        return
    if data.mode=="PLAY":
        drawBoard(canvas, data)
        canvas.create_text(data.width/4,20,text="SCORE: "+str(data.score),
        font=("System", "14", "bold"), fill="white")
        canvas.create_text(data.width *3/ 4, 20, text="DOTS LEFT: " + str(data.dotsLeft),
            font=("System", "14", "bold"), fill="white")
    if data.mode=="HELP":
        helpSplashScreen(canvas,data)
    if data.mode=="HIGH SCORES":
        highScoresScreen(canvas,data)


#used from snake code
def drawBoard(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col)

#used from snake code
def drawCell(canvas, data, row, col):
    w = data.width
    h = data.height
    cellW = w / data.cols
    cellH = h / data.rows
    x0 = cellW * col
    y0 = cellH * row
    x1 = cellW * (col + 1)
    y1 = cellH * (row + 1)
    ovalX=(x0+x1)/2
    ovalY=(y1+y0)/2
    #set appropriate colors based on object
    if (data.board[row][col] ==1): #wall
        canvas.create_rectangle(x0, y0, x1, y1, fill="hot pink", width=0)
    elif (data.board[row][col] == 0): #food
        canvas.create_rectangle(x0, y0, x1, y1, width=0)
        canvas.create_oval(ovalX - data.r, ovalY - data.r, ovalX + data.r, ovalY + data.r, fill="white")
    elif (data.board[row][col] == -1): #eaten food
        canvas.create_rectangle(x0, y0, x1, y1, width=0)
    elif data.board[row][col]==3: #ghost box door
        canvas.create_rectangle(x0,y0,x1,y1,width=0,fill="gray72")
    elif (data.board[row][col]==2): #pacwoman
        if data.posX%2==0:
           canvas.create_image((x0+x1)//2,(y0+y1)/2,image=canvas.image)
        else:
            canvas.create_image((x0+x1)//2,(y0+y1)/2,image=canvas.image2)
    elif data.board[row][col]==5: #pink ghost
        canvas.create_image((x0+x1)/2,(y0+y1)/2,image=data.pink.image)
    elif data.board[row][col]==6: #red ghost
        canvas.create_image((x0+x1)/2,(y0+y1)/2,image=data.red.getImage())
    elif data.board[row][col]==7: #blue ghost
        canvas.create_image((x0+x1)/2,(y0+y1)/2,image=data.blue.image)
    elif data.board[row][col]==8: #orange ghost
        canvas.create_image((x0+x1)/2,(y0+y1)/2,image=data.orange.image)
    elif data.board[row][col]==10:
        canvas.create_rectangle(x0, y0, x1, y1, width=0)
        canvas.create_oval(ovalX - data.bigR, ovalY - data.bigR, ovalX + data.bigR, ovalY + data.bigR, fill="white")


####################################
####################################
# use the run function as-is
####################################
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data,canvas)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data,canvas)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 80  # milliseconds
    init(data)
    # create the root and the canvas
    #root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    canvas.configure(background="black")
    initC(canvas)
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1000, 1000)
