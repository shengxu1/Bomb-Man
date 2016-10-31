
import pygame
import math
from GameObject import GameObject
from Bubble import Bubble
from allGameData import allGameData
import copy


class Player(GameObject):
    

    

        

    def __init__(self, row, col , name, playernumber, team, itemindex=None):
        self.gamemode=allGameData.gamemode
        if self.gamemode=="captureTheFlag":
            self.hasBun=False
            self.bunshouldnotshow=False #sometimes bun should not show if in homebase
        elif self.gamemode=="Hero": 
            self.hashero=False
            self.ishidden=False
        elif self.gamemode=="Kungfu":
            self.killstreak=0
            self.streaklabel=False #if there is a streaklabel to be put on the screen
            self.streakcount=0 #records the time the streaklabel is on the screen

        elif self.gamemode=="treasurehunt":
            self.ishidden=False
            self.redgem=0
            self.yellowgem=0
            self.greengem=0
            self.gemscore=(self.redgem*allGameData.gemScores["redgem"]+
                self.yellowgem*allGameData.gemScores["yellowgem"]+
                self.greengem*allGameData.gemScores["greengem"])
        self.experience=None
        self.lagratio=1.0
        self.canMove=False
        self.hatindex,self.bubbleindex=None,1  #the default bubble type is 1
        if itemindex!=None:
            if itemindex<allGameData.numberofhats:
                 self.hatindex=itemindex
            else:
                 self.bubbleindex=itemindex-allGameData.numberofhats

        
        self.playerno=playernumber
        self.team=team
        self.walkingcount=0
        self.scale=(120,120) #scale of alive player
        self.scale2=70,90 #scale of jelly
        self.scale3=75,65  #scale of crying
        self.name=name
        self.isJelly=False
        self.isDead=False
        self.direction=0   #down
        self.images = []
        self.initiateImgList()
        # self.images=allGameData.transformcharacterImgs["devil"]
        self.image = self.updateImage()
        if self.gamemode=="Kungfu":
            self.origImg=self.images #keep a copy of the original images
            self.isTransformed=False
            self.newName=None
        self.speedItem=0
        self.powerItem=0
        self.bubbleItem=0

        self.initCharacter(self.name)

        
        self.maxBubbles=self.basicBubbles+self.bubbleItem
        self.speed=round((self.basicSpeed+self.speedItem)*self.lagratio)
        self.power=self.basicPower+self.powerItem

        self.currentBubbles=0
        self.collisionindex=0.3  #the higher this is, the harder for the player
                #to turn beside blocks
        self.isSlow=False
        self.slowcount=0
        self.onBanana=False
        self.isWin=None #start out as tie
        
        self.invincible=False
        self.invincibleCount=0

        self.bubbleHidden=False
        self.bubbleHiddenCount=0

        self.deadtimes=0
        self.killcount=0
        self.savecount=0

        self.jellyCount=0  #time in jelly
        self.deadCount=0  #time being dead
        self.layer=None  #layer of player being displayed
        self.basicitemlist=[]  
        self.itemKey=1 #which num key corresponds to which item
        self.usefulitemdict=dict()
        self.itemkeydict=dict()
        self.sex="male"


       #for single computer use
        if self.playerno==1:
           self.keySet=[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN,pygame.K_l]
           self.itemkeySet=[pygame.K_t,pygame.K_y,pygame.K_u,pygame.K_i,pygame.K_o,pygame.K_p]
        
           
        elif self.playerno==2:
           self.keySet=[pygame.K_a,pygame.K_d,pygame.K_w,pygame.K_s,pygame.K_t]
           self.itemkeySet=[pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6]
           
        


        super().__init__(row,col,self.image)

        if self.team=="red": self.color=allGameData.red
        elif self.team=="blue": self.color=allGameData.blue
        elif self.team=="green": self.color=allGameData.green
        elif self.team=="yellow": self.color=allGameData.yellow


    def initCharacter(self,name):
        if name=="ninja":
            self.basicSpeed=11
            self.basicPower=1
            self.basicBubbles=1
            self.maxPower=7
            self.maxSpeed=20
        elif name=="robot":
            self.basicSpeed=7
            self.basicPower=3
            self.basicBubbles=2
            self.maxPower=9
            self.maxSpeed=14
        elif name=="monkey":
            self.basicSpeed=9
            self.basicPower=1
            self.basicBubbles=2
            self.maxPower=8
            self.maxSpeed=17
        elif name=="cutegirl":
            self.basicSpeed=11
            self.basicPower=2
            self.basicBubbles=1
            self.maxPower=9
            self.maxSpeed=17


    def initiateImgList(self):
        if self.hatindex==None:
            imagename='images/characters/%s/%s%s.png'% (self.name,self.name,self.team)
            image = pygame.image.load(imagename).convert_alpha()
            self.rows, self.cols = 4, 4
            width, height = image.get_size()
            cellWidth, cellHeight = width/self.cols,(height)/self.rows

            for j in range(self.rows):
                for i in range(self.cols):
                    subImage = image.subsurface(
                        (i * cellWidth, j * cellHeight, 
                            cellWidth, cellHeight))
                    self.images.append(pygame.transform.scale(
                subImage.convert_alpha(),
                self.scale))
        else:
  
            imagename='images/characters/%s/%s%s.png'% (self.name,self.name,self.team)
            hatimagename='images/shoppableitems/hat%d.png'%self.hatindex
            image = pygame.image.load(imagename).convert_alpha()
            hatimage = pygame.image.load(hatimagename).convert_alpha()
            self.rows, self.cols = 4, 4


            self.hatscale=allGameData.hatscales[self.hatindex]
            self.hatxyposition=allGameData.hatxypositions[self.hatindex]


            width, height = image.get_size()
            cellWidth, cellHeight = width/self.cols,(height)/self.rows

            for j in range(self.rows):
                for i in range(self.cols):
                    subImage = image.subsurface(
                        (i * cellWidth, j * cellHeight, 
                            cellWidth, cellHeight))
                    subhatimage=hatimage.subsurface(
                        (i * cellWidth, j * cellHeight, 
                            cellWidth, cellHeight))
                    if self.hatindex<5 or (self.hatindex==5 and j>0):
                        if self.hatindex==5 and j==1:
                            origx,origy=self.hatxyposition
                            actualxypos=(origx+20,origy)
                        elif self.hatindex==5 and j==2:
                            origx,origy=self.hatxyposition
                            actualxypos=(origx-20,origy)
                        else:
                            actualxypos=self.hatxyposition
                        subhatimage=pygame.transform.scale(subhatimage,self.hatscale) 
                        subImage.blit(subhatimage,actualxypos)
                        self.images.append(pygame.transform.scale(
                    subImage.convert_alpha(),
                    self.scale))
                    else:
                        subhatimage=pygame.transform.scale(subhatimage,self.scale) 
                        subImage=pygame.transform.scale(subImage,self.scale) 
                        subhatimage.blit(subImage,(0,0))
                        self.images.append(pygame.transform.scale(
                    subhatimage.convert_alpha(),
                    self.scale))
        
        

        self.cryImgList=[pygame.transform.scale(pygame.image.load("images/malecry0.png").convert_alpha(),self.scale3),
        pygame.transform.scale(pygame.image.load("images/malecry1.png").convert_alpha(),self.scale3)]

        self.jellyImgList=[pygame.transform.scale(pygame.image.load("images/guodong0.png").convert_alpha(),self.scale2),
        pygame.transform.scale(pygame.image.load("images/guodong1.png").convert_alpha(),self.scale2),
        pygame.transform.scale(pygame.image.load("images/guodong2.png").convert_alpha(),self.scale2)]


    
    def updateImage(self):
     if self.isDead and self.deadCount<allGameData.cryCount:
        cryindex=0 if (self.deadCount//6)%3==2 else 1
        return self.cryImgList[cryindex]
        
        
     elif self.isJelly:
         jellyindex=(self.jellyCount//10)%3
         return self.jellyImgList[jellyindex]

     elif not self.isDead and not self.isJelly:
       if not (self.gamemode in ["treasurehunt","Hero"] and self.ishidden):
        imageindex=self.direction*4+(self.walkingcount//4)%4
        return self.images[imageindex]

    #returns None if is dead and pass crying time or if is hidden (can't see player on screen)
        
    def transformcharacter(self,character):
         self.images=allGameData.transformcharacterImgs[character]
         self.isTransformed=True
         self.resetCharacters()

         self.newName=character
         if self.newName=="pudding":
             self.bubbleHidden=True
         elif self.newName=="devil":
           try:
             temp=[None]*4
             temp[0],temp[1],temp[2],temp[3]=self.keySet[2],self.keySet[3],self.keySet[0],self.keySet[1]
             temp.append(self.keySet[4])
             self.keySet=temp
           except:
             pass

    def transformback(self):
        self.images=self.origImg
        self.isTransformed=False
        self.resetCharacters()
        self.newName=None
    
    def resetCharacters(self):
        if self.newName!=None and "pudding" in self.newName: #either pudding or transparent pudding
            self.bubbleHidden=False
        elif self.newName=="devil":
           try:
             temp=copy.copy(self.keySet)
             self.keySet[0],self.keySet[1],self.keySet[2],self.keySet[3]=temp[2],temp[3],temp[0],temp[1]
           except:
             pass

    def becomeInvisible(self):
        self.images=allGameData.transformcharacterImgs["transparentpudding"]
        self.newName="transparentpudding"

    def becomeVisible(self):
        self.images=allGameData.transformcharacterImgs["pudding"]
        self.newName="pudding"
    


    def getPlayerGrid(self):
            actualy=self.y
            if self.isJelly:
                 actualy=self.y-allGameData.Gridh//2
            prow=actualy//allGameData.Gridh
            pcol=self.x//allGameData.Gridw
            if prow>=allGameData.Rows:
                prow=allGameData.Rows-1
            if pcol>=allGameData.Cols:
                pcol=allGameData.Cols-1
            return prow,pcol

    def putBubble(self):
       if (self.currentBubbles<self.maxBubbles and not self.isJelly 
        and not self.isDead and not (self.gamemode=="captureTheFlag" and self.hasBun)
        and not (self.gamemode=="Hero" and self.hashero)):
              prow,pcol=self.getPlayerGrid()
              
              if allGameData.GridList[prow][pcol]<2 :
                     bubble=Bubble(prow,pcol,self.bubbleindex,self.power,self.playerno,self.bubbleHidden,False)
                     self.currentBubbles+=1
                     allGameData.GridList[prow][pcol]=3
                     # print("aduhasiu")
                     return bubble
              elif self.gamemode in ["treasurehunt","Hero"]:

                 if self.emptyBlock(prow,pcol) and (not 
                    (prow,pcol) in allGameData.emptyBlocksHaveBubbles):
                     allGameData.emptyBlocksHaveBubbles.add((prow,pcol))
                     bubble=Bubble(prow,pcol,self.bubbleindex,self.power,self.playerno,self.bubbleHidden,True)
                     self.currentBubbles+=1
                     allGameData.GridList[prow][pcol]=3
                     return bubble
    
    def update(self):
         if self.gamemode =="treasurehunt":
             self.ishidden=False
             prow,pcol=self.getPlayerGrid()
             if allGameData.map[prow][pcol]==3:
                 self.ishidden=True
         elif self.gamemode =="Hero":
             self.ishidden=False
             prow,pcol=self.getPlayerGrid()
             if allGameData.map[prow][pcol] in [4,10,11]:
                 self.ishidden=True
         self.image = self.updateImage() #update image even when blocked
         self.speed=round(3*self.lagratio) if self.isSlow else round((self.basicSpeed+self.speedItem)*self.lagratio)
         if self.gamemode=="captureTheFlag" and self.hasBun:
            self.speed=round(3*self.lagratio)
         if self.gamemode=="Hero" and self.hashero:
            self.speed=round(3*self.lagratio)
         if self.gamemode=="treasurehunt":
              self.gemscore=(self.redgem*allGameData.gemScores["redgem"]+
                self.yellowgem*allGameData.gemScores["yellowgem"]+
                self.greengem*allGameData.gemScores["greengem"])
         self.power=self.basicPower+self.powerItem
         self.maxBubbles=self.basicBubbles+self.bubbleItem
         if self.isSlow:
            self.slowcount+=1
            if self.slowcount>=allGameData.maxslowcount:
                self.isSlow=False
         if self.bubbleHidden:
            self.bubbleHiddenCount+=1
            if self.bubbleHiddenCount>=400:
                self.bubbleHidden=False
         if self.invincible:
            self.invincibleCount+=1
            if self.invincibleCount>=allGameData.invincibleCount:
                self.invincible=False
                self.invincibleCount=0
         if self.image!=None:  
            super().updateRect()
    
    def bananaSlide(self):
        if self.direction==1: self.x-=allGameData.bananaSpeed
        elif self.direction==2: self.x+=allGameData.bananaSpeed
        elif self.direction==3:  self.y-=allGameData.bananaSpeed
        elif self.direction==0: self.y+=allGameData.bananaSpeed

    def reverseBananaSlide(self):
        if self.direction==1: self.x+=allGameData.bananaSpeed
        elif self.direction==2: self.x-=allGameData.bananaSpeed
        elif self.direction==3:  self.y+=allGameData.bananaSpeed
        elif self.direction==0: self.y-=allGameData.bananaSpeed

#there are some changes made to compensate the fact that the player image 
#is larger than the player 

    def moveLeft(self):
        if not self.isJelly and not self.isDead:
            origrow,origcol=self.getPlayerGrid()
            if not self.emptyBlock(origrow,origcol) or self.isEmptyBlock(origrow,origcol,"left"):
              self.direction=1
              self.walkingcount+=1
              if (self.rect.left+allGameData.Gridh>0):
                  

                  if  self.x-origcol*allGameData.Gridw>allGameData.Gridw//2:
                       self.x-=self.speed
                  elif  allGameData.GridList[origrow][origcol-1]<2 or (self.isEmptyBlock(origrow,origcol-1,"left") 
                    and not (origrow,origcol-1) in allGameData.emptyBlocksHaveBubbles):

                      if (allGameData.GridList[origrow-1][origcol-1]>=2 and 
                          self.y-origrow*allGameData.Gridh<allGameData.Gridh*self.collisionindex):
                          self.y+=self.speed//2

                      elif (origrow<allGameData.Rows-1 and allGameData.GridList[origrow+1][origcol-1]>=2 and 
                          self.y-origrow*allGameData.Gridh>allGameData.Gridh*(1-self.collisionindex)):
                           self.y-=self.speed//2

                      else:
                          self.x-=self.speed
                  #push blocks
                  elif (self.gamemode=="treasurehunt" and 
                      allGameData.GridList[origrow][origcol-1]==5):                    
                  
                      
                      if (origcol-2>=0 and allGameData.GridList[origrow][origcol-2]==0 
                        and ((origrow,origcol-2) not in allGameData.cannotPushIntoSet)):

                               return (origrow,origcol-1)

                  elif (self.gamemode=="Kungfu" and self.newName=="panda" and 
                    allGameData.GridList[origrow][origcol-1]==3):
                     for kickdistance in allGameData.kickBubbleDistances:
                         targetcol=(origcol-1-kickdistance)%allGameData.Cols
                         if allGameData.GridList[origrow][targetcol]==0:

                             return (origrow,origcol-1,origrow,targetcol)
                             #ends the for loop
                    
    def emptyBlock(self,row,col):
        if self.gamemode=="treasurehunt":
            if allGameData.map[row][col]==3:
               return True
        elif self.gamemode=="Hero":
            if allGameData.map[row][col] in [4,10,11]: 
               return True
        return False

    def isEmptyBlock(self,row,col,playerdir):
        if self.gamemode=="treasurehunt":
            if allGameData.map[row][col]==3 and playerdir in ["left","right"]:
               return True
        elif self.gamemode=="Hero":
            if allGameData.map[row][col] in [4,10,11] and playerdir in ["up","down"]: #up and down
               return True
        return False

    def moveRight(self):
      if not self.isJelly and not self.isDead:
        origrow,origcol=self.getPlayerGrid()
        if not self.emptyBlock(origrow,origcol) or self.isEmptyBlock(origrow,origcol,"right"):
            self.direction=2
            self.walkingcount+=1
            if (self.rect.right-allGameData.Gridh<allGameData.Bwid):
                if  (origcol+1)*allGameData.Gridw-self.x>allGameData.Gridw//2 or origcol==allGameData.Cols-1:
                     self.x+=self.speed
                elif  allGameData.GridList[origrow][origcol+1]<2 or (self.isEmptyBlock(origrow,origcol+1,"right")
                    and not (origrow,origcol+1) in allGameData.emptyBlocksHaveBubbles):

                    if (allGameData.GridList[origrow-1][origcol+1]>=2 and 
                        self.y-origrow*allGameData.Gridh<allGameData.Gridh*self.collisionindex):
                        self.y+=self.speed//2

                    elif (origrow<allGameData.Rows-1 and allGameData.GridList[origrow+1][origcol+1]>=2 and 
                        self.y-origrow*allGameData.Gridh>allGameData.Gridh*(1-self.collisionindex)):
                         self.y-=self.speed//2

                    else:
                        self.x+=self.speed
                elif (self.gamemode=="treasurehunt" and 
                        allGameData.GridList[origrow][origcol+1]==5):                    
                    
                        if (origcol+2<allGameData.Cols and allGameData.GridList[origrow][origcol+2]==0 
                        and ((origrow,origcol+2) not in allGameData.cannotPushIntoSet)):
                                 return (origrow,origcol+1)

                elif (self.gamemode=="Kungfu" and self.newName=="panda" and 
                    allGameData.GridList[origrow][origcol+1]==3):
                     for kickdistance in allGameData.kickBubbleDistances:
                         targetcol=(origcol+1+kickdistance)%allGameData.Cols
                         if allGameData.GridList[origrow][targetcol]==0:

                             return (origrow,origcol+1,origrow,targetcol)
        

    def moveUp(self):
        if not self.isJelly and not self.isDead:
            origrow,origcol=self.getPlayerGrid()
            if not self.emptyBlock(origrow,origcol) or self.isEmptyBlock(origrow,origcol,"up"):
              self.direction=3
              self.walkingcount+=1
              if (self.rect.top+allGameData.Gridh*3//2>0):

                  if  self.y-origrow*allGameData.Gridh>allGameData.Gridh//2:
                       self.y-=self.speed
                  elif  allGameData.GridList[origrow-1][origcol]<2 or (self.isEmptyBlock(origrow-1,origcol,"up")
                    and not (origrow-1,origcol) in allGameData.emptyBlocksHaveBubbles):

                      if (allGameData.GridList[origrow-1][origcol-1]>=2 and 
                          self.x-origcol*allGameData.Gridw<allGameData.Gridw*self.collisionindex):
                          self.x+=self.speed//2

                      elif (origcol<allGameData.Cols-1 and allGameData.GridList[origrow-1][origcol+1]>=2 and 
                          self.x-origcol*allGameData.Gridw>allGameData.Gridw*(1-self.collisionindex)):
                           self.x-=self.speed//2

                      else:
                          self.y-=self.speed
                  elif (self.gamemode=="treasurehunt" and 
                      allGameData.GridList[origrow-1][origcol]==5):                    
                  
                      if (origrow-2>=0 and allGameData.GridList[origrow-2][origcol]==0 
                        and ((origrow-2,origcol) not in allGameData.cannotPushIntoSet)):
                               return (origrow-1,origcol)

                  elif (self.gamemode=="Kungfu" and self.newName=="panda" and 
                    allGameData.GridList[origrow-1][origcol]==3):
                     for kickdistance in allGameData.kickBubbleDistances:
                         targetrow=(origrow-1-kickdistance)%allGameData.Rows
                         if allGameData.GridList[targetrow][origcol]==0:

                             return (origrow-1,origcol,targetrow,origcol)
            

    def moveDown(self):
      if not self.isJelly and not self.isDead:
        origrow,origcol=self.getPlayerGrid()
        if not self.emptyBlock(origrow,origcol) or self.isEmptyBlock(origrow,origcol,"down"):
            self.direction=0
            self.walkingcount+=1
            if (self.rect.bottom<allGameData.Bhei):
                if  (origrow+1)*allGameData.Gridh-self.y>allGameData.Gridh//2 or origrow==allGameData.Rows-1:
                     self.y+=self.speed
                elif  allGameData.GridList[origrow+1][origcol]<2 or (self.isEmptyBlock(origrow+1,origcol,"down")
                    and not (origrow+1,origcol) in allGameData.emptyBlocksHaveBubbles):

                    if (allGameData.GridList[origrow+1][origcol-1]>=2 and 
                        self.x-origcol*allGameData.Gridw<allGameData.Gridw*self.collisionindex):
                        self.x+=self.speed//2

                    elif (origcol<allGameData.Cols-1 and allGameData.GridList[origrow+1][origcol+1]>=2 and 
                        self.x-origcol*allGameData.Gridw>allGameData.Gridw*(1-self.collisionindex)):
                         self.x-=self.speed//2

                    else:
                        self.y+=self.speed
                elif (self.gamemode=="treasurehunt" and 
                        allGameData.GridList[origrow+1][origcol]==5):                    
                    
                        if (origrow+2<allGameData.Rows and allGameData.GridList[origrow+2][origcol]==0 
                        and ((origrow+2,origcol) not in allGameData.cannotPushIntoSet)):
                                 return (origrow+1,origcol)
                elif (self.gamemode=="Kungfu" and self.newName=="panda" and 
                    allGameData.GridList[origrow+1][origcol]==3):
                     for kickdistance in allGameData.kickBubbleDistances:
                         targetrow=(origrow+1+kickdistance)%allGameData.Rows
                         if allGameData.GridList[targetrow][origcol]==0:

                             return (origrow+1,origcol,targetrow,origcol)
        




