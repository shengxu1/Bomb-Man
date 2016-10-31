'''
GameObject.py

implements the base GameObject class

'''
import pygame
from allGameData import allGameData



class GameObject(pygame.sprite.Sprite):
    # cryCount=150
    # Rows,Cols=13,15  #set up grid
    # Bwid,Bhei=750,650
    # Gridw,Gridh= 50, 50
    # GridList=[[0]*15 for row in range(13)]
    # BasicItems={"power","speed","bubble","question"}
    # UsefulItems={"slow","banana","fork","dart"}
    # OnetimeItems={"makeslow","bananapeel","hiddenbubble"}
    # timetillexp=60
    # deadCount=500
    # dropEverything=True
    # bananaSpeed=15
    # dartSpeed=30
    # directionList=["down","left","right","up"]

    #can get in : 0: empty tile
    #             1:item
    
    #: can't get in:
    #             2: blocks
    #             3: bubble
    #             4: homebase 



    def __init__(self, row, col, image):
        super().__init__()
        # x, y define the center of the object
        self.row,self.col=row,col
        self.x, self.y, self.image = (col*allGameData.Gridw+allGameData.Gridw//2, 
        row*allGameData.Gridh+allGameData.Gridh//2+allGameData.Gridh,  image)
        #the center of y needs to be shifted down to be in the grid
        w, h = image.get_size()
        self.updateRect()


    def updateRect(self):
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x-w//2, self.y-h//2-allGameData.Gridh, w, h)
         #center of objects needs to be shifted back up again
    
    def updateRectWithRowCol(self,row,col):
        self.x, self.y= (col*allGameData.Gridw+allGameData.Gridw//2, 
        row*allGameData.Gridh+allGameData.Gridh//2+allGameData.Gridh)
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x-w//2, self.y-h//2-allGameData.Gridh, w, h)

    def update(self):

        self.updateRect()

