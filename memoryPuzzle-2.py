import pygame,sys,random
from pygame.locals import *

PADWIDTH=6
PADHEIGHT=5
BOXSIZE=60
GAPSIZE=10
ALLPOTO=15
WINX=600
WINY=500
TEXT='You Are Win!'
text='press esc to quit'
#-------红  绿  蓝
WHITE=(255,255,255)
BLUE =(  0,  0,255)
RED  =(255,  0,  0)
BLACK=(  0,  0,  0)
X=int((WINX-(BOXSIZE+GAPSIZE)*PADWIDTH)/2)
Y=int((WINY-(BOXSIZE+GAPSIZE)*PADHEIGHT)/2)
screen=pygame.display.set_mode((WINX,WINY))
pygame.display.set_caption('猜图案')

#-------------------------------------------------------------------------------------------------------------------------
#    主函数

def main():

    gameover=False
    pygame.init()
    mx,my=0,0
    imagePad=imageLoad()
    firstSelect=None
    startGameAnimation(imagePad)
    font=pygame.font.SysFont('arial',64)
    font1=pygame.font.SysFont('arial',32)
    font2=pygame.font.SysFont('arial',20)
    score=0
    p=0
    
    while True:
        drawGamePad()             
        mouseClick=False
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==MOUSEMOTION:
                mx,my=event.pos
            if event.type==MOUSEBUTTONUP:
                mx,my=event.pos
                mouseClick=True
        if isInBox(mx,my):                                 # 检验鼠标是否落在白色图标上，若在则使图标显示为蓝色。
            boxx,boxy=getBoxfromPixel(mx,my)
            left,top=xyTolefttop(mx,my)
            pygame.draw.rect(screen,BLUE,(left,top,BOXSIZE,BOXSIZE))
            if not imagePad[boxx][boxy][1] and mouseClick: # 当鼠标在该白色图标上，且该图标未被点击过，此时点击该图标
                                                           # 并将其属性设置为True
                imagePad[boxx][boxy][1]=True
                if firstSelect==None:                      #firstSelect值为空时代表此前未发生点击图标事件，
                                                           #当点击图标时将该图标坐标赋值给firstSelect.
                                                           #代表第一次点击图标，当第二次点击图标时，条件判断选择执行else。
                    
                    firstSelect=(boxx,boxy)
                else:
                    if imagePad[firstSelect[0]][firstSelect[1]][0]==imagePad[boxx][boxy][0]:
                        imagePad[firstSelect[0]][firstSelect[1]][2],imagePad[boxx][boxy][2]=True,True
                        p=10
                    elif imagePad[firstSelect[0]][firstSelect[1]][0]!=imagePad[boxx][boxy][0]:
                        imagePad[firstSelect[0]][firstSelect[1]][1],imagePad[boxx][boxy][1]=False,False
                        p=-1
                    firstSelect=None
                    score+=p           
                    pygame.draw.rect(screen,BLACK,(0,0,100,30))
                    screen.blit(font2.render('score:'+str(score),True,(255,255,255)),(0,0))
                    if score==-10:
                        gameover=True

                       
        for x in range(PADWIDTH):
            for y in range(PADHEIGHT):
                left,top=getlefttopfromBox(x,y)
                if imagePad[x][y][1] or imagePad[x][y][2]:
                    image=pygame.image.load(imagePad[x][y][0])
                    screen.blit(image,(left,top))
        
        
        
        if hasWon(imagePad):
            pygame.time.wait(1000)
            screen.fill(WHITE)
            screen.blit(font.render(TEXT,True,(0,0,0)),(WINX/2-180,WINY/2-30))
            screen.blit(font1.render(text,True,(0,0,0)),(WINX/2-100,WINY/2+50))
            screen.blit(font1.render('Score:'+str(score),True,(0,0,0)),(WINX/2-100,WINY/2+90))
            for event in pygame.event.get():
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        if gameover:
            screen.fill(WHITE)
            screen.blit(font1.render('press Q to quit.',True,(0,0,0)),(WINX/2-100,WINY/2+50))
            screen.blit(font.render('GAME OVER',True,(0,0,0)),(WINX/2-210,WINY/2-30))
            for event in pygame.event.get():
                if event.type==KEYUP:
                    if event.key==K_q:
                        pygame.quit()
                        sys.exit()
                        
        pygame.display.update()
                                
#（1）------------------------------------------------------------------------------------------------------------------------

def gamePad(val):
    '''函数创建存储游戏板数据的二维列表，由 imageLoad函数调用，用于加载图片使用'''
    padlist=[]
    for i in range(PADWIDTH):
        padlist.append([val]*PADHEIGHT)
    return padlist

#（2）------------------------------------------------------------------------------------------------------------------------

def potoArray():
    '''函数返回存储有游戏图片的列表，由imageLoad函数调用，用于加载图片使用。'''
    potolist=[]
    for i in range(ALLPOTO):
        potolist.append('%d.png'%(i+1))
    potolist*=2
    random.shuffle(potolist)
    return potolist

#（3）------------------------------------------------------------------------------------------------------------------------

def imageLoad():
    '''把图片数据加载到游戏板数据列表中,函数返回一个二维列表，该列表存储图片信息和bool值的元组'''
    p=potoArray()
    g=gamePad(False)
    for x in range(PADWIDTH):
        for y in range(PADHEIGHT):
            g[x][y]=[p[0],False,False]
            del p[0]
    return g  # 存储图片信息和状态信息的三维列表['i.png',False,False]。第二个元素是检验数据项是否被点击的
              # 状态，若被点击则为真，否则为假。第三个元素是检验两个图标是否相同的状态，若相同则为真，否则为假。

#（4）------------------------------------------------------------------------------------------------------------------------

def getlefttopfromBox(boxx,boxy):
    '''从方块坐标中获取像素坐标'''
    left=X+boxx*(BOXSIZE+GAPSIZE)
    top=Y+boxy*(BOXSIZE+GAPSIZE)
    return (left,top)

#（5）------------------------------------------------------------------------------------------------------------------------

def isInBox(x,y):
    '''判断像素坐标是否在方块坐标内，若在返回真，若不在返回假'''
    for boxx in range(PADWIDTH):
        for boxy in range(PADHEIGHT):
            p=getlefttopfromBox(boxx,boxy)
            if x in range(p[0],p[0]+BOXSIZE) and y in range(p[1],p[1]+BOXSIZE):
                return True
    return False

#（6）------------------------------------------------------------------------------------------------------------------------

def getBoxfromPixel(x,y):
    '''获取像素坐标所在位置的方块坐标'''
    for boxx in range(PADWIDTH):
        for boxy in range(PADHEIGHT):
            p=getlefttopfromBox(boxx,boxy)
            if x in range(p[0],p[0]+BOXSIZE) and y in range(p[1],p[1]+BOXSIZE):
                return (boxx,boxy)
    return (None,None)

#（7）------------------------------------------------------------------------------------------------------------------------
            
def drawGamePad():
    '''绘制游戏板'''
    for boxx in range(PADWIDTH):
        for boxy in range(PADHEIGHT):
            p=getlefttopfromBox(boxx,boxy)
            pygame.draw.rect(screen,WHITE,(p[0],p[1],BOXSIZE,BOXSIZE))
                           
#(8)--------------------------------------------------------------------------------------------------------------------------

def xyTolefttop(x,y):
    '''从鼠标当前坐标中获取方块所在位置的像素坐标'''
    boxx,boxy=0,0
    boxx,boxy=getBoxfromPixel(x,y)
    left,top=getlefttopfromBox(boxx,boxy)
    return (left,top)
        
#(9)--------------------------------------------------------------------------------------------------------------------------

def startGameAnimation(imageload):  #所接受参数应为存储游戏数据板数据的三维列表，是函数imageLoad的返回值。
    
    drawGamePad()
    for x in range(PADWIDTH):
        for y in range(PADHEIGHT):
            left,top=getlefttopfromBox(x,y)
            image=pygame.image.load(imageload[x][y][0])
            screen.blit(image,(left,top))
    pygame.display.update()
    pygame.time.wait(3000) 
        
#（10）-----------------------------------------------------------------------------------------------------------------------

def hasWon(imageload):              #参数类型同函数（9）
    for x in range(PADWIDTH):
        for y in range(PADHEIGHT):
            if not imageload[x][y][2]:
                return False
    else:
        return True  
#-----------------------------------------------------------------------------------------------------------------------------
    
if __name__=='__main__':
    main()
