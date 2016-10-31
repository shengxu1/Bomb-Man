import pygame
import math
from GameObject import GameObject
import random
from allGameData import allGameData



class Block(GameObject):
    #type 1 is green block, 2 is yellow block, 3 is bun, 4 is lamp, 5 is tree

    #type 1 is chest, 2 is darkblock, 3 is skull, 4 is flame, 5 is knight
 
    #type 1 is green block, 2 is white block, 3 is bun, 4 is door, 5 is tree, 
    # 10 is homebase 1, 11 is homebase 2

    #type 1 is bi, type 2 is wu, type 3 is noblock (essentially the background)
    def __init__(self,row,col,blocktype,item=None):

       self.canExplode=True if blocktype<=allGameData.explodableblocks else False
       self.hiddenItem=item 
       itemname=allGameData.blockimagenames[blocktype-1]
       image = allGameData.blockImgDict[itemname]
       self.blocktype=blocktype

       super().__init__(row, col, image)

       if itemname in allGameData.upperYShifts:
          self.y-=allGameData.upperYShifts[itemname]
       super().updateRect()

    def ispushed(self,drow,dcol):
       self.row+=drow
       self.col+=dcol
       super().updateRectWithRowCol(self.row,self.col)
       

    # def update(self):
    #   super().updateRect()


       
# #block that can be popped
# class EBlock(Block):
#   #color can be green, yellow
#      def __init__(self,row,col,color):
        
#         self.color=color
#         self.canExplode=True
#         self.imagename='images/%sblock.png'%self.color
#         self.image = pygame.image.load(self.imagename).convert_alpha()
#         self.image=pygame.transform.scale(
#               self.image.convert_alpha(),
#               self.scale)
#         super().__init__(row,col)
#         #item stuff..





# #block that can never be popped
# class NEBlock(Block):

#     def __init__(self,row,col,color):
        
#         self.color=color
#         self.canExplode=True
#         self.imagename='images/%sblock.png'%self.color
#         self.image = pygame.image.load(self.imagename).convert_alpha()
#         self.image=pygame.transform.scale(
#               self.image.convert_alpha(),
#               self.scale)
#         super().__init__(row,col)
