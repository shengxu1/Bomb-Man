import pygame
from GameObject import GameObject
from allGameData import allGameData



class Herotower(GameObject):
    #type 1 is green block, 2 is yellow block, 3 is bun, 4 is lamp, 5 is tree


 

    def __init__(self,row,col,team):

       teamindex=allGameData.colors.index(team)
       image=allGameData.homebaseImgs[teamindex]
       self.team=team
       self.numheros=0
       self.baselocation=(row,col)  #the location of the tower
       self.surroundinglocations=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),
       (row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
       super().__init__(row, col, image)
       self.y=self.y-30
       super().updateRect()
