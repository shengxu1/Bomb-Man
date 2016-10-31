import pygame
import math
from GameObject import GameObject
from allGameData import allGameData

class Bubble(GameObject):


    
    def __init__(self,brow,bcol,bubbletype,bubblepower,playernumber,bubblehidden,bubblenotshown):
       self.timetillexp=allGameData.timetillexp
       self.isExploding=False #so that bubble is not displayed when exploding
       self.type=bubbletype
       self.power=bubblepower
       self.bubbleform=(self.timetillexp//allGameData.bubblechangingspeed)%4
       self.bubblehidden=bubblehidden
       self.bubblenotshown=bubblenotshown
       if self.bubblenotshown:
          self.image=pygame.transform.scale(pygame.image.load(
              'images/bubbles/emptybubble.png').convert_alpha(),(10,10))
       else:
           if not self.bubblehidden:
               self.image=allGameData.bubbleImgList[self.type][self.bubbleform]
           else:
               self.image=allGameData.transbubbleImgList[self.type][self.bubbleform]
       self.playerno=playernumber
       self.hasDeducted=False #has deducted the bubble count from player's 
       #max bubble
       if self.bubblenotshown:
          if allGameData.gamemode=="treasurehunt":
             self.directionList=[False,True,True,False]
          elif allGameData.gamemode=="Hero":
             self.directionList=[True,False,False,True]
       else:
          self.directionList=[True,True,True,True]   #down,left,right,up
       self.explodeDistList=[0,0,0,0]

       self.hasPlayedSound=False

       super().__init__(brow, bcol, self.image)
       self.y-=allGameData.bubbleyshift
       super().updateRect()
    #the x and y values are not impacted here b/c they are already set above
       

       
    def bubbleChangeForm(self):
       self.bubbleform=(self.timetillexp//allGameData.bubblechangingspeed)%4
       if self.bubblenotshown:
          pass
       else:
         if not self.bubblehidden:
             self.image=allGameData.bubbleImgList[self.type][self.bubbleform]
         else:
             self.image=allGameData.transbubbleImgList[self.type][self.bubbleform]
         super().updateRect()

    def iskicked(self):
        super().updateRectWithRowCol(self.row,self.col)
