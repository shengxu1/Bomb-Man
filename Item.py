import pygame
import math
from GameObject import GameObject
import random
from allGameData import allGameData


class Item(GameObject):


            

    def __init__(self,row,col,itemtype=None,bubble=None):
       self.fromBubble=bubble
       self.chosenname=random.choice(allGameData.itemNames) if itemtype==None else itemtype
       self.image=allGameData.itemImgDict[self.chosenname]
       super().__init__(row, col, self.image)
       self.dartdir=None
       self.origrow=None
       self.origcol=None
       self.dartno=None #helps us find the same dart in multiplayer mode
       # self.imagename='images/items/%sitem.png'%self.chosenname
       # self.scale=40,40
       # # self.image = pygame.image.load(self.imagename).convert_alpha()
       # self.image=pygame.transform.scale(
       #      self.image.convert_alpha(),
       #      self.scale)



       # self.isMoving=False  
       # self.xtravelspeed,self.ytravelspeed=0,0
       # self.targetLocation=None
#when an item is released from a dead player, it travels to its target location
       
    def dartMove(self,speed):
       if self.dartdir==2: self.x+=speed
       elif self.dartdir==1: self.x-=speed
       elif self.dartdir==0: self.y+=speed
       elif self.dartdir==3: self.y-=speed
       super().updateRect()
       self.row,self.col=self.getItemGrid()
    # def itemTravel(self):
    #     self.x+=self.xtravelspeed
    #     self.y+=self.ytravelspeed
    def getItemGrid(self):
            irow=self.y//allGameData.Gridh
            icol=self.x//allGameData.Gridw
            if irow>=allGameData.Rows:
                irow=allGameData.Rows-1
            if icol>=allGameData.Cols:
                icol=allGameData.Cols-1
            return irow,icol
