import pygame
import math
from GameObject import GameObject
from allGameData import allGameData

class Tile(GameObject):


    
    def __init__(self,row,col):
       self.status=0  #0 is tile, 1 is explosion
       if allGameData.gamemode=="treasurehunt":
          if (row+col)%2==0:
              image=allGameData.tileImgs[0]
          else:
              image=allGameData.tileImgs[1]
       else:
          image=allGameData.tileImg
       super().__init__(row, col, image)

    def updateTile(self,newstatus):
        self.status=newstatus
        # if self.status==0:  self.imagename='images/tile.png'
        # elif self.status==1: self.imagename='images/explosiondown.png'
        # elif self.status==2: self.imagename='images/explosionleft.png'
        # elif self.status==3: self.imagename='images/explosionmid.png'
        # elif self.status==4: self.imagename='images/explosionright.png'
        # elif self.status==5: self.imagename='images/explosionup.png'
        if self.status==0:
           if allGameData.gamemode=="treasurehunt":
                if (self.row+self.col)%2==0:
                     self.image=allGameData.tileImgs[0]
                else:
                    self.image=allGameData.tileImgs[1]
           else:
             self.image=allGameData.tileImg
        else:
          self.image = allGameData.explosionImgList[self.status-1]
        super().updateRect()


