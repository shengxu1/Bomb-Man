import pygame
from GameObject import GameObject
from allGameData import allGameData



class Homebase(GameObject):
    #type 1 is green block, 2 is yellow block, 3 is bun, 4 is lamp, 5 is tree


 

    def __init__(self,row,col,team,numbuns):

       teamindex=allGameData.colors.index(team)
       image=allGameData.homebaseImgs[teamindex]
       self.team=team
       self.cornerlist=[(row-1,col-1),(row-1,col+1),(row+1,col-1),(row+1,col+1)]
       self.twosides=[(row,col-2),(row,col-1),(row,col+1),(row,col+2)]
       self.allSides=[(row,col-1),(row,col+1),(row+1,col),(row-1,col),(row,col)]
       self.numbuns=numbuns
       self.baselocation=(row,col)#the location players can get buns from
       super().__init__(row, col, image)
       self.y=self.y-10
       super().updateRect()
