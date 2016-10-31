
import pygame

from Player import Player
from pygamegame import PygameGame
import random
from Bubble import Bubble
from GameObject import GameObject
from Tile import Tile
from Block import Block
from Item import Item
from allGameData import allGameData
from Homebase import Homebase
from Herotower import Herotower
import random



class singleGame(PygameGame):

  #GridList:

    #can get in : 
    #            -1: capturetheflag: homebase  
    #             0: empty tile
    #             1:item
    
    #: can't get in:
    #             2: blocks
    #             3: bubble
    #             4:       captureflag: homebase 
    #             5: treasurehunt: pushable block
    


    def __init__(self):
        super().__init__()
        self.endgamecount=0
        self.gameends=False
        self.gamestarts=False
        self.playerPutItemDict=dict()
        #this dict records the location at which a player put a item, so that 
        #players would not get their own items right
        mydata=allGameData()
        self.gamemode=random.choice(allGameData.gamemodes)
        # self.gamemode="captureTheFlag"
        # self.gamemode=random.choice(allGameData.gamemodes)
        mydata.initmaps(self.gamemode)       
        # self.gamemap=random.choice(allGameData.maps)
        self.mapindex=random.randint(0,len(allGameData.maps)-1)
        self.gamemap=allGameData.maps[self.mapindex]
        mydata.gameinit(self.gamemode,self.gamemap,False)
        mydata.initImages()
        self.timecount=0   #used to slow down bubble explosion and other stuff
        self.bubbleExplosionCount=8 #used to extend bubble explosion time
        self.bubblePosListOfSets=[]
        character1,character2=random.choice(allGameData.characters),random.choice(allGameData.characters)
        mydata.initGameImages(["red","blue"],[character1,character2])
        
        self.itemGroup = pygame.sprite.Group()
        self.dartGroup = pygame.sprite.Group()
        self.blockGroup = pygame.sprite.Group()


        
        
        self.displayPlayer=1 #which player's attributes is displayed

        
        self.playerGroup = pygame.sprite.Group()

        self.bubbleGroupgroup=[] #a list of all the bubble 
        #groups. bubbles in the same bubble group explodes at the same time

        self.tileGroup = pygame.sprite.Group()
        if self.gamemode=="Kungfu":
           for row in range(allGameData.Rows):
                for col in range(allGameData.Cols):
                  if 4<=row<=11 and 1<=col<=13:
                    newtile=Tile(row,col)
                    self.tileGroup.add(newtile)
        else:
            for row in range(allGameData.Rows):
                for col in range(allGameData.Cols):
                    newtile=Tile(row,col)
                    self.tileGroup.add(newtile)
        if self.gamemode in ["captureTheFlag","Hero"]:
           self.homebaseGroup = pygame.sprite.Group()
        elif self.gamemode=="treasurehunt":
           self.totalpoints=0  #total points possible on the board, used to
           #detect endgame
           self.highestscoreplayers=[]  
           # a list of the players with the highest scores 
           self.highestscore=1 # so that at first, no player has highest score

           self.teamscoredict=dict()
              

        for brow in range(allGameData.Rows):
          for bcol in range(allGameData.Cols):
             blocktype=self.gamemap[brow][bcol]
             if self.gamemode=="treasurehunt":
                if blocktype==1: #treasure chest
                    chosenitem=self.chooserandomly(allGameData.gemItems,allGameData.gemfrequency)
                    self.totalpoints+=allGameData.gemScores[chosenitem]
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype==2:
                    chosenitem=self.chooserandomly(allGameData.itemNames,allGameData.itemfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=5
                elif blocktype>2:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
             elif self.gamemode=="Kungfu":
                if blocktype in [1,2]:
                    chosenitem=self.chooserandomly(allGameData.itemNames,allGameData.itemfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype==3:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
             elif self.gamemode=="Hero":
                if blocktype in [1,2]:
                    chosenitem=self.chooserandomly(allGameData.itemNames,allGameData.itemfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype==3:
                    chosenitem=self.chooserandomly(allGameData.bunNames,allGameData.bunfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif 3<blocktype<10:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype>=10:
                    team="red" if blocktype==10 else "blue"
                    self.homebaseGroup.add(Herotower(brow,bcol,team))
                    allGameData.GridList[brow][bcol]=2
                  
                
             elif self.gamemode=="captureTheFlag":
                if 0<blocktype<10:
                    chosenitem=self.chooserandomly(allGameData.itemNames,allGameData.itemfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype>=10:
                    team="red" if blocktype==10 else "blue"
                    self.homebaseGroup.add(Homebase(brow,bcol,team,1))
                    allGameData.GridList[brow][bcol]=-1
                    allGameData.GridList[brow-1][bcol-1]=4
                    allGameData.GridList[brow-1][bcol+1]=4
                    allGameData.GridList[brow+1][bcol-1]=4
                    allGameData.GridList[brow+1][bcol+1]=4


        
        newrow1,newcol1=random.choice(self.getEmptyTiles())
        newrow2,newcol2=random.choice(self.getEmptyTiles())

        if self.gamemode in "captureTheFlag":
           for homebase in self.homebaseGroup:
              if homebase.team=="red":
                 newrow1,newcol1=random.choice(allGameData.revivePositions[self.mapindex][0])
              elif homebase.team=="blue":
                 newrow2,newcol2=random.choice(allGameData.revivePositions[self.mapindex][1])
        elif self.gamemode=="Hero":
            for herotower in self.homebaseGroup:
                if herotower.team=="red":
                   newrow1,newcol1=random.choice(herotower.surroundinglocations)
                elif herotower.team=="blue":
                    newrow2,newcol2=random.choice(herotower.surroundinglocations)
        player1 = Player(newrow1-1,newcol1,character1
          ,1,"red")
        player2 = Player(newrow2-1,newcol2,character2
          ,2,"blue")
        self.playerGroup.add(player1)
        self.playerGroup.add(player2)

        pygame.mixer.Sound.play(allGameData.startgameSound)


        # if not self.isSingleComputer:
        #     for cID in self.clientele:
        #       self.clientele[cID].send(bytes(blockitemString+"\n", "UTF-8"))
                # self.clientele[cID].send(bytes("blockItem_%d_%d_%d_%s\n"%(brow,bcol,gamemap[brow][bcol],chosenitem), "UTF-8"))
    def chooserandomly(self,itemNames,itemfrequency):
         itemlist=[]
         for item in itemNames:
            freq=itemfrequency[item]
            itemlist+=[item]*freq
         return random.choice(itemlist)

    def keyPressed(self, code, mod):

        if code==pygame.K_m:
          for player in self.playerGroup :
           if player.playerno==1:
             self.playerPutBubble(player)

        if code==pygame.K_v:
          for player in self.playerGroup :
           if player.playerno==2:
               self.playerPutBubble(player)

        #test the results page
        if code==pygame.K_r:
           self.gameends=True
            
    def playerPutBubble(self,player):
            newBubble=player.putBubble()
            if newBubble!=None:
                pygame.mixer.Sound.play(allGameData.bubbleSound)
                self.reformBubbleLists(newBubble)


#check if the newly placed bubble is in the same bubble group
# (same row,same col with no blocks in between) as some other bubbles
#and put these into a new group (some of the old groups are combined if 
#linked together by the new bubble)
    def reformBubbleLists(self,newbubble):
         newrow,newcol=newbubble.row,newbubble.col
         newBubbleGroup=pygame.sprite.Group()
         for index in range(len(self.bubbleGroupgroup)):
           bubblegroup=self.bubbleGroupgroup[index]
           if bubblegroup!=None:
             isValid=False  #if some bubble in the bubble group 
             #is in the same row or same col as the new bubble
             isExploding=False
             for bubble in bubblegroup:
                if bubble.isExploding:
                    isExploding=True
    #two bubbles will belong to same group only if they are on the same
    #row or col, has distance smaller than the sum of their power, and 
    #has no obstacles between
                if ((bubble.row==newrow and 
                    self.noObstacleRow(newcol,bubble.col,newrow) and 
                    abs(bubble.col-newcol)<(bubble.power+newbubble.power)) or 
                (bubble.col==newcol and 
                    self.noObstableCol(newrow,bubble.row,newcol) and 
                    abs(bubble.row-newrow)<(bubble.power+newbubble.power))):
                    isValid=True
             if isValid and not isExploding:
                for bubble in bubblegroup:
                      newBubbleGroup.add(bubble)
                self.bubbleGroupgroup[index]=None
                #set to none to avoid loop crash
         for bubblegroup in self.bubbleGroupgroup:
            if bubblegroup==None:
                # print("hello")
                self.bubbleGroupgroup.remove(bubblegroup) 
                #remove the groups that are previously set to None
         newBubbleGroup.add(newbubble)
         lowestTime=None
         for bubble in newBubbleGroup:
            if lowestTime==None or bubble.timetillexp<lowestTime:
                lowestTime=bubble.timetillexp
         for bubble in newBubbleGroup:
             bubble.timetillexp=lowestTime
         self.bubbleGroupgroup.append(newBubbleGroup)

         






#see if two bubbles on the same row has obstacles between
    def noObstacleRow(self,col1,col2,row):
        lowercol=min(col1,col2)
        uppercol=max(col1,col2)
        for col in range(lowercol+1,uppercol):
            if allGameData.GridList[row][col] in [2,5] and (not self.isEmptyDirection(row,col,1)):
                return False
        return True

#see if two bubbles on the same col has obstacles between
    def noObstableCol(self,row1,row2,col):
        lowerrow=min(row1,row2)
        upperrow=max(row1,row2)
        for row in range(lowerrow+1,upperrow):
            if allGameData.GridList[row][col] in [2,5] and (not self.isEmptyDirection(row,col,0)):
                return False
        return True

    def timerFired(self, dt):
      
      if not self.gameends:
        self.timecount+=1
        if self.timecount>allGameData.maxPlayingTime:
           self.gameends=True
           if self.gamemode=="treasurehunt":
              highestscore=None
              highestteams=[]
              for team in self.teamscoredict:
                  if highestscore==None or self.teamscoredict[team]>highestscore:
                      highestscore=self.teamscoredict[team]
                      highestteams=[team]
                  elif self.teamscoredict[team]==highestscore:
                      highestteams.append(team)
              for player in self.playerGroup:
                  if player.team in highestteams and len(highestteams)==1:
                      player.isWin=True
                  elif player.team in highestteams:
                      pass
                  else:
                      player.isWin=False
           elif self.gamemode=="Kungfu":
              teamscoredict=dict()
              for player in self.playerGroup:
                 if player.team in teamscoredict:
                   teamscoredict[player.team]+=player.killcount
                 else:
                   teamscoredict[player.team]=player.killcount
              highestscore=None
              highestteams=[]
              for team in teamscoredict:
                  if highestscore==None or teamscoredict[team]>highestscore:
                      highestscore=teamscoredict[team]
                      highestteams=[team]
                  elif teamscoredict[team]==highestscore:
                      highestteams.append(team)
              for player in self.playerGroup:
                  if player.team in highestteams and len(highestteams)==1:
                      player.isWin=True
                  elif player.team in highestteams:
                      pass
                  else:
                      player.isWin=False

           elif self.gamemode=="Hero":
               numheros1=None
               for herotower in self.homebaseGroup:
                 if numheros1==None:
                     numheros1=herotower.numheros #first run
                 else: #second run
                  if herotower.numheros<numheros1: #first team wins
                    for player in self.playerGroup:
                        if player.team==herotower.team:
                            player.isWin=False
                        else:
                          player.isWin=True
                  elif herotower.numheros>numheros1:
                    for player in self.playerGroup:
                        if player.team==herotower.team:
                            player.isWin=True
                        else:
                          player.isWin=False
           elif self.gamemode=="captureTheFlag":
               numbuns1=None
               for homebase in self.homebaseGroup:
                 if numbuns1==None:
                     numbuns1=homebase.numbuns #first run
                 else: #second run
                  if homebase.numbuns<numbuns1: #first team wins
                    for player in self.playerGroup:
                        if player.team==homebase.team:
                            player.isWin=False
                        else:
                          player.isWin=True
                  elif homebase.numbuns>numbuns1:
                    for player in self.playerGroup:
                        if player.team==homebase.team:
                            player.isWin=True
                        else:
                          player.isWin=False
        for player in self.playerGroup:
          if player.isJelly: 
             player.jellyCount+=1
          if player.jellyCount>=allGameData.maxJellyCount:
              self.playerDie(player)
          if player.isDead: 
              player.deadCount+=1
          if player.deadCount>=allGameData.deadCount: 
              self.playerRevive(player)

        self.playerGroup.update()
        # print(len(self.bubbleGroupgroup))
        
        self.bubbleExplosions()
        self.checkKillSave()
        self.checkGetItems()

        for dart in self.dartGroup:

          dart.dartMove(allGameData.dartSpeed)
          # print(dart.row,dart.col)
          drow=dart.row if (dart.dartdir in [0,3]) else dart.row-1
          dcol=dart.col 
          origrow=dart.origrow if (dart.dartdir in [0,3]) else dart.origrow-1
          origcol=dart.origcol 
          #when the dart is horizontal, the row and col is over by 1
          if allGameData.GridList[drow][dcol]==3:
             for bubblegroup in self.bubbleGroupgroup:
                hasbubble=False 
              #if the bubblegroup contains the bubble that is hit by the dart
                for bubble in bubblegroup:
                  if not hasbubble: #stop checking after hasbubble=True
                   if (bubble.row,bubble.col)==(drow,dcol):
                       hasbubble=True
                if hasbubble:
                   for bubble in bubblegroup:
                       bubble.timetillexp=0
                   break #break after the correct bubblegroup is found
             self.dartGroup.remove(dart)
             self.itemGroup.remove(dart)
          # print(drow,dcol,allGameData.GridList[drow][dcol])
          if allGameData.GridList[drow][dcol]>=2 and not( 
            self.isEmptyDirection(drow,dcol,dart.dartdir)):
             self.dartGroup.remove(dart)
             self.itemGroup.remove(dart)
          elif ((dart.dartdir in [0,3] and ((drow==0 and origrow!=0) or 
                      (drow==allGameData.Rows-1 and origrow!=allGameData.Rows-1 )))
          or (dart.dartdir in [1,2] 
                    and ((dcol==0 and origcol!=0) or 
                      (dcol==allGameData.Cols-1 and origcol!=allGameData.Cols-1 )))):
             self.dartGroup.remove(dart)
             self.itemGroup.remove(dart)

          elif abs(dart.origrow-drow)>8 or abs(dart.origcol-dcol)>8:
             self.dartGroup.remove(dart)
             self.itemGroup.remove(dart)




         




        for player in self.playerGroup:

                if player.onBanana:
                    player.isSlow=False
                    player.bananaSlide()
                    prow,pcol=player.getPlayerGrid()
                    drow,dcol=allGameData.directiondrdc[player.direction]
                    if((player.direction in [0,3] and (prow==0 or 
                      prow==allGameData.Rows-1))or (player.direction in [1,2] 
                    and (pcol==0 or pcol==allGameData.Cols-1))):
                       player.onBanana=False
                    elif (allGameData.GridList[prow+drow]
                      [pcol+dcol]>1 and not (self.isEmptyDirection(prow+drow,pcol+dcol,player.direction) 
                        )):
                     
                       player.onBanana=False
                       player.reverseBananaSlide() #backtrack

                    self.renewPlayerItemDict(player)

                else:

                 if player.direction in [0,3]: #if the player is moving up or down originally, 
                 #the left and right keys can influence his direction
                    if self.isKeyPressed(player.keySet[1]):
                         pushresult=player.moveRight()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"right")
                            elif self.gamemode=="Kungfu": 
                              self.kickBubbles(pushresult)          

                    elif self.isKeyPressed(player.keySet[0]):
                         pushresult=player.moveLeft()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"left")
                            elif self.gamemode=="Kungfu":  
                               self.kickBubbles(pushresult)              
                      
                    elif self.isKeyPressed(player.keySet[2]):
                         pushresult=player.moveUp()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"up")
                            elif self.gamemode=="Kungfu":
                              self.kickBubbles(pushresult)          
                      
                    elif self.isKeyPressed(player.keySet[3]):
                         pushresult=player.moveDown()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"down")
                            elif self.gamemode=="Kungfu":
                               self.kickBubbles(pushresult)          

                    self.renewPlayerItemDict(player)

                 else:#if the player is moving left or right originally, 
                 #the up and down keys can influence his direction
                    if self.isKeyPressed(player.keySet[2]):
                         pushresult=player.moveUp()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"up")
                            elif self.gamemode=="Kungfu":
                              self.kickBubbles(pushresult)          
                      
                    elif self.isKeyPressed(player.keySet[3]):
                         pushresult=player.moveDown()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"down")
                            elif self.gamemode=="Kungfu":
                               self.kickBubbles(pushresult)   
                    elif self.isKeyPressed(player.keySet[1]):
                         pushresult=player.moveRight()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"right")
                            elif self.gamemode=="Kungfu": 
                              self.kickBubbles(pushresult)          

                    elif self.isKeyPressed(player.keySet[0]):
                         pushresult=player.moveLeft()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"left")
                            elif self.gamemode=="Kungfu":  
                               self.kickBubbles(pushresult)              
                      
                           

                    self.renewPlayerItemDict(player)


    def kickBubbles(self,kickresult):
       origrow,origcol,targetrow,targetcol=kickresult
       pygame.mixer.Sound.play(allGameData.kickbubbleSound)

       for bubblegroup in self.bubbleGroupgroup:
        if bubblegroup!=None: #thread safe
         for bubble in bubblegroup:
            if (bubble.row,bubble.col)==(origrow,origcol):
               bubble.row,bubble.col=targetrow,targetcol
               allGameData.GridList[origrow][origcol]=0
               allGameData.GridList[targetrow][targetcol]=3
               bubble.iskicked()
               self.reformBubbleLists(bubble)
               break


#push result is the original position of the box being pushed
    def pushBlocks(self,pushresult,direction):
            # print("canpush")  
            if direction=="left": drow,dcol=0,-1
            elif direction=="right": drow,dcol=0,1
            elif direction=="up": drow,dcol=-1,0
            elif direction=="down": drow,dcol=1,0
            canpush=True
            brow,bcol=pushresult
            for player in self.playerGroup:
              if player.getPlayerGrid()==(brow+drow,bcol+dcol):
                  canpush=False
            if canpush: 
                pygame.mixer.Sound.play(allGameData.pushblockSound)                              
                for block in self.blockGroup:
                    if (block.row,block.col)==(brow,bcol):
                       block.ispushed(drow,dcol)
                       allGameData.GridList[brow][bcol]=0
                       allGameData.GridList[block.row][block.col]=5
                       break


    def renewPlayerItemDict(self,player):
         if len(self.playerPutItemDict)>0:
                newrow,newcol=player.getPlayerGrid()
                try:
                   origrow,origcol=self.playerPutItemDict[player.playerno]
                   if (origrow,origcol)!=(newrow,newcol):
                       del self.playerPutItemDict[player.playerno]
                except: 
                  pass       

    def keyReleased(self, keyCode, modifier):

          if keyCode==pygame.K_SPACE:
              if self.displayPlayer==1:
                 self.displayPlayer=2
              else:
                self.displayPlayer=1

          for player in self.playerGroup:
              if (not player.isDead) :
                 row,col=player.getPlayerGrid()
                 if keyCode==player.itemkeySet[0] and player.itemKey>1:
                     self.useItem(1,row,col,player)
                 elif keyCode==player.itemkeySet[1] and player.itemKey>2:
                     self.useItem(2,row,col,player)
                 elif keyCode==player.itemkeySet[2] and player.itemKey>3:
                     self.useItem(3,row,col,player)
                 elif keyCode==player.itemkeySet[3] and player.itemKey>4:
                     self.useItem(4,row,col,player)
                 elif keyCode==player.itemkeySet[4] and player.itemKey>5:
                     self.useItem(5,row,col,player)
                 elif keyCode==player.itemkeySet[5] and player.itemKey>6:
                     self.useItem(6,row,col,player)

                 elif self.gamemode=="Kungfu":
                   if keyCode==player.keySet[4]:
                     if player.newName=="pudding":
                         player.becomeInvisible()
                     elif player.newName=="transparentpudding":
                         player.becomeVisible()
                    
                 



    # def travelItems(self):
    #   for item in self.itemGroup:
    #     if item.isMoving:
    #       print(item.getItemGrid())
    #       print(item.targetLocation)
    #       if (item.x,item.y)==item.targetLocation:
    #           item.isMoving=False
    #           item.xtravelspeed,item.ytravelspeed=0,0
    #           item.targetLocation=None

    #       else:
    #         item.itemTravel()

#check if a player in a jelly is killed or saved and process the kill

    def useItem(self,itemkey,row,col,player):
            successfullyPut=False
            itemname=player.itemkeydict[itemkey]
            # print(itemname)
            if (not player.isJelly) or itemname=="fork":
                if itemname=="slow":
                        self.itemGroup.add(Item(row,col,"makeslow",None))
                        allGameData.GridList[row][col]=1
                        successfullyPut=True
                elif itemname=="banana":
                    self.itemGroup.add(Item(row,col,"bananapeel",None))
                    allGameData.GridList[row][col]=1
                    successfullyPut=True
                elif itemname=="fork":
                    if player.isJelly:
                        self.playerSaved(player)
                        successfullyPut=True
                    else:
                        successfullyPut=False

                elif itemname=="dart":
                    dirname=allGameData.directionList[player.direction]
                    newDart=Item(row,col,"%sdart"%dirname,None)
                    newDart.dartdir=player.direction
                    newDart.origrow,newDart.origcol=newDart.row,newDart.col
                    self.itemGroup.add(newDart)
                    self.dartGroup.add(newDart)
                    successfullyPut=True
                elif self.gamemode=="Hero" and itemname=="hero":
                    player.hashero=False
                    prow,pcol=player.getPlayerGrid()
                    self.itemGroup.add(Item(prow,pcol,"hero"))
                    allGameData.GridList[prow][pcol]=1
                    successfullyPut=True
                elif self.gamemode=="Hero" and itemname=="bomb":
                    prow,pcol=player.getPlayerGrid()
                    for herotower in self.homebaseGroup:
                       if herotower.team!=player.team:
                          if (prow,pcol)==(herotower.row,herotower.col) and herotower.numheros>0:
                             herotower.numheros-=1
                             pygame.mixer.Sound.play(allGameData.explodeSound)
                             successfullyPut=True
                          else:
                            successfullyPut=False
                          break

            if successfullyPut:
                  self.playerPutItemDict[player.playerno]=(row,col)
                  if player.usefulitemdict[itemname]>0:
                      player.usefulitemdict[itemname]-=1
                  if player.usefulitemdict[itemname]==0:
                     player.itemKey-=1
                     newitemkeydict=dict()
                     for newitemkey in player.itemkeydict:
                        if newitemkey<itemkey:
                           newitemkeydict[newitemkey]=player.itemkeydict[newitemkey]
                           #don't change smaller items
                        
                        elif newitemkey>=itemkey and newitemkey<len(player.itemkeydict):
                          newitemkeydict[newitemkey]=player.itemkeydict[newitemkey+1]
                     player.itemkeydict=newitemkeydict
              # print(player.itemkeydict)
               





    def playerSaved(self,player):
           player.isJelly=False
           player.y-=allGameData.Gridh//2
           pygame.mixer.Sound.play(allGameData.thankyouSound)


    def checkKillSave(self):
      for player in self.playerGroup:
         if player.isJelly:
            jellypos=player.getPlayerGrid()
            for otherplayer in self.playerGroup:
              if (not otherplayer.isJelly and not otherplayer.isDead and 
                otherplayer.playerno!=player.playerno 
                and singleGame.isIntersecting(player,otherplayer)):

                  if otherplayer.team==player.team:
                       otherplayer.savecount+=1
                       self.playerSaved(player)
                  else:
                      otherplayer.killcount+=1
                      if self.gamemode=="Kungfu":
                         otherplayer.killstreak+=1
                         if otherplayer.killstreak>=2:
                            otherplayer.streaklabel=True
                         if otherplayer.killstreak==2:
                            pygame.mixer.Sound.play(allGameData.doublekillSound)
                         elif otherplayer.killstreak==3:
                            pygame.mixer.Sound.play(allGameData.triplekillSound)
                         elif otherplayer.killstreak==4:
                            pygame.mixer.Sound.play(allGameData.dominatingSound)
                         elif otherplayer.killstreak==5:
                            pygame.mixer.Sound.play(allGameData.rampageSound)
                      self.playerDie(player)

    def playerRevive(self,player):
            player.isDead=False
            player.deadCount=0
            player.invincible=True
            player.invincibleCount=0
            teamindex=0 if player.team=="red" else 1
            
            if self.gamemode =="captureTheFlag":
                newrow,newcol=random.choice(allGameData.revivePositions[self.mapindex][teamindex])
            elif self.gamemode=="Hero":
                for herotower in self.homebaseGroup:
                    if herotower.team==player.team:
                       newrow,newcol=random.choice(herotower.surroundinglocations)
  
            else:
                newrow,newcol=random.choice(self.getEmptyTiles())
            newrow-=1
            player.x, player.y= (newcol*allGameData.Gridw+allGameData.Gridw//2, 
                  newrow*allGameData.Gridh+allGameData.Gridh//2+allGameData.Gridh)
            player.direction=0
            player.walkingcount=0


    def playerDie(self,player):
          if allGameData.gamemode=="captureTheFlag" and player.hasBun:
              player.hasBun=False
              prow,pcol=player.getPlayerGrid()
              self.itemGroup.add(Item(prow,pcol,"bun"))
              allGameData.GridList[prow][pcol]=1
          elif allGameData.gamemode=="Hero" and player.hashero:
              player.hashero=False
              prow,pcol=player.getPlayerGrid()
              self.itemGroup.add(Item(prow,pcol,"hero"))
              allGameData.GridList[prow][pcol]=1
          elif self.gamemode=="Kungfu":
             player.killstreak=0
          pygame.mixer.Sound.play(allGameData.killSound)
          player.deadtimes+=1
          player.isJelly=False
          player.jellyCount=0
          player.isSlow=False
          player.bubbleHidden=False
          player.isDead=True
          self.playerDropItems(player)


    def playerDropItems(self,player):
        if self.gamemode=="Kungfu":
           shouldnotDrop=True if len(player.usefulitemdict)>0 else False
           
        player.usefulitemdict=dict() #clear all useful items
        player.itemkeydict=dict()
        player.itemKey=1
        prow,pcol=player.getPlayerGrid()

        if allGameData.gamemode=="treasurehunt" and player.gemscore>0:
             self.teamscoredict[player.team]-=player.gemscore
             player.gemlist=(["redgem"]*player.redgem+["greengem"]*player.greengem+
              ["yellowgem"]*player.yellowgem)
             
             for drop in range(len(player.gemlist)):
               popItem=random.choice(player.gemlist)
               if popItem=="redgem": player.redgem-=1
               elif popItem=="yellowgem": player.yellowgem-=1
               elif popItem=="greengem": player.greengem-=1
               newrow,newcol=random.choice(self.getEmptyTiles())
               newItem=Item(newrow,newcol,popItem,None)
               self.itemGroup.add(newItem)
               player.gemlist.remove(popItem)
               allGameData.GridList[newrow][newcol]=1
             player.update()
             self.highestscore,self.highestscoreplayers=self.updateScores()

        else:
            if self.gamemode!="Kungfu":
                 dropCount=len(player.basicitemlist) 
            else:
               if shouldnotDrop or len(player.basicitemlist)==0:
                 dropCount=0
               else:
                 dropCount=len(player.basicitemlist)//2+1
            for drop in range(dropCount):
                popItem=random.choice(player.basicitemlist)
                if popItem=="power": player.powerItem-=1
                elif popItem=="bubble": player.bubbleItem-=1
                elif popItem=="speed": player.speedItem-=1
                newrow,newcol=random.choice(self.getEmptyTiles())
                newItem=Item(newrow,newcol,popItem,None)
                self.itemGroup.add(newItem)
                # newItem.isMoving=True
                # newItem.row,newItem.col=newrow,newcol
                # targetx,targety=newcol*allGameData.Gridw+allGameData.Gridw//2,newrow*allGameData.Gridh+allGameData.Gridh//2
                # newItem.xtravelspeed,newItem.ytravelspeed=targetx-newItem.x,targety-newItem.y
                # newItem.targetLocation=targetx,targety
                # print(newItem.xtravelspeed,newItem.ytravelspeed)
                allGameData.GridList[newrow][newcol]=1
                player.basicitemlist.remove(popItem)

    def updateScores(self):
        highestscore=1
        highestlist=[]
        for player in self.playerGroup:
            if player.gemscore>highestscore:
                highestscore=player.gemscore
                highestlist=[player.playerno]
            elif player.gemscore==highestscore:
                highestlist.append(player.playerno)
        return highestscore,highestlist
        
    #returns a set of empty tile positions in tuples
    def getEmptyTiles(self):
      emptylist=[]
      for row in range(allGameData.Rows):
          for col in range(allGameData.Cols):
              if allGameData.GridList[row][col]==0:
                emptylist.append((row,col))
      return emptylist


    @staticmethod
    def isIntersecting(player,otherplayer):
       pstartx,pstarty=player.x-allGameData.Gridw//2,player.y-allGameData.Gridh
       pwid,phei=allGameData.Gridw,allGameData.Gridh
       ostartx,ostarty=otherplayer.x-allGameData.Gridw//2,otherplayer.y-allGameData.Gridh
       return (pstartx-int(0.75*pwid)<=ostartx<=pstartx+int(0.75*pwid) and 
        pstarty-int(phei*1.25)<=ostarty<=pstarty+int(phei*0.25))


    def checkGetItems(self):
         for player in self.playerGroup:
           if (not player.isDead) and (not player.isJelly):
               prow,pcol=player.getPlayerGrid()
               if allGameData.GridList[prow][pcol]==1: 
      #increase efficiency of function by only checking grids that have items
                   for item in self.itemGroup:
                        if (prow,pcol)==(item.row,item.col):
                          isValid=True
                          try:
                            if (prow,pcol)==self.playerPutItemDict[player.playerno]:
                              isValid=False
                          except:
                            pass
                          if self.gamemode=="captureTheFlag" and item.chosenname=="bun" and player.hasBun:
                             isValid=False
                          elif self.gamemode=="Hero" and item.chosenname=="hero" and player.hashero:
                             isValid=False
                          
                          if isValid:
                            self.getItem(player,item)
                            pygame.mixer.Sound.play(allGameData.itemSound)
                            allGameData.GridList[item.row][item.col]=0
                            self.itemGroup.remove(item)
               
               if self.gamemode=="captureTheFlag":
                   for homebase in self.homebaseGroup:
                      if homebase.baselocation==(prow,pcol): 
                           if (homebase.team != player.team) and (not player.hasBun):
                                  player.hasBun=True
                                  homebase.numbuns-=1
                           elif (homebase.team == player.team) and player.hasBun:
                                  player.hasBun=False
                                  homebase.numbuns+=1
                                  if homebase.numbuns==2:
                                     self.gameends=True 
                                     for player in self.playerGroup:
                                       if player.team==homebase.team:
                                          player.isWin=True
                                       else:
                                          player.isWin=False
                                #end game when one team gets all the buns
               elif self.gamemode=="Hero":
                   for herotower in self.homebaseGroup:
                      if herotower.baselocation==(prow,pcol) and player.hashero: 
                           if (herotower.team == player.team):
                              herotower.numheros+=1
                              player.hashero=False
                              for key in player.itemkeydict:
                                 if player.itemkeydict[key]=="hero":
                                   itemkey=key
                                   break
                              player.itemKey-=1
                              player.usefulitemdict["hero"]-=1
                              newitemkeydict=dict()
                              for newitemkey in player.itemkeydict:
                                if newitemkey<itemkey:
                                   newitemkeydict[newitemkey]=player.itemkeydict[newitemkey]
                                   #don't change items corresponding to smaller keys
                                elif newitemkey>=itemkey and newitemkey<len(player.itemkeydict):
                                  newitemkeydict[newitemkey]=player.itemkeydict[newitemkey+1]
                              player.itemkeydict=newitemkeydict
                              if herotower.numheros==4:
                                  self.gameends=True
                                  for player in self.playerGroup:
                                       if player.team==herotower.team:
                                          player.isWin=True
                                       else:
                                          player.isWin=False


                              


    def getItem(self,player,item):
      if item.chosenname in allGameData.BasicItems:
        isminus=False
        questionname=None
        if item.chosenname=="question":
           questionname=random.choice(["speed","power","bubble"])
           isminus=random.choice([True,False])

        if (item.chosenname=="power" or questionname=="power")  and player.power<=player.maxPower:
          if isminus:
             if player.powerItem>0:
                player.powerItem-=1
                player.basicitemlist.remove("power")
          else:
            player.powerItem+=1
            player.basicitemlist.append("power")
          #only append if not over the limit power

        elif (item.chosenname=="speed" or questionname=="speed") and player.speed<=player.maxSpeed:
          if isminus:
             if player.speedItem>0:
                player.speedItem-=1
                player.basicitemlist.remove("speed")
          else:
              player.speedItem+=1
              player.basicitemlist.append("speed")

        elif (item.chosenname=="bubble" or questionname=="bubble"):
          if isminus:
             if player.bubbleItem>0:
                player.bubbleItem-=1
                player.basicitemlist.remove("bubble")
          else:
              player.bubbleItem+=1
              player.basicitemlist.append("bubble")
        

      elif item.chosenname in allGameData.UsefulItems:
            if self.gamemode=="Hero" and item.chosenname=="hero":
                player.hashero=True
            player.usefulitemdict[item.chosenname]=player.usefulitemdict.get(item.chosenname,0)+1
            if player.usefulitemdict[item.chosenname]<=1:
              player.itemkeydict[player.itemKey]=item.chosenname
              player.itemKey+=1
        

      elif item.chosenname in allGameData.OnetimeItems:
        if item.chosenname=="makeslow":
          player.isSlow=True
          player.onBanana=False
          player.slowcount=0 #if player is already on slow, slowcount restarts
        elif item.chosenname=="bananapeel":
          player.onBanana=True
        elif item.chosenname=="hiddenbubble":
          player.bubbleHidden=True
          player.bubbleHiddenCount=0

      elif self.gamemode=="captureTheFlag" and item.chosenname=="bun":
          player.hasBun=True

      elif self.gamemode=="Kungfu":
          if item.chosenname in allGameData.transformcharacters:
             player.transformcharacter(item.chosenname)
          if player.newName=="gentleman":
              if not ("dart" in player.usefulitemdict) or player.usefulitemdict["dart"]==0:
                player.itemkeydict[player.itemKey]="dart"
                player.itemKey+=1
              player.usefulitemdict["dart"]=player.usefulitemdict.get("dart",0)+4
              

      elif self.gamemode=="treasurehunt":
          if item.chosenname=="redgem":
              player.redgem+=1
          elif item.chosenname=="yellowgem":
              player.yellowgem+=1
          elif item.chosenname=="greengem":
              player.greengem+=1
          player.update()
                       
              
          if player.team in self.teamscoredict:
           self.teamscoredict[player.team]+=allGameData.gemScores[item.chosenname]
          else:
           self.teamscoredict[player.team]=allGameData.gemScores[item.chosenname]
          if self.teamscoredict[player.team]==self.totalpoints:
              self.gameends=True
              winningteam=player.team
              for allplayers in self.playerGroup:
                 if allplayers.team==winningteam:
                    allplayers.isWin=True
                 else:
                    allplayers.isWin=False
          if player.gemscore>self.highestscore:
            self.highestscoreplayers=[player.playerno]
            self.highestscore=player.gemscore
          elif player.gemscore==self.highestscore:
            self.highestscoreplayers.append(player.playerno)




    def bubbleExplosions(self):
        for bubblegroup in self.bubbleGroupgroup:
          if bubblegroup!=None:
            isExploding=False
            for bubble in bubblegroup:
                bubble.timetillexp-=1
                bubble.bubbleChangeForm()
                if bubble.timetillexp<0: 
                    isExploding=True

                    bubble.isExploding=True
                    break
            if isExploding:
                explosioncontinues=False #check if is exploding or recovering
                shouldPlaySound=False
                for bubble in bubblegroup: #only check 1 bubble for efficiency 
                    if bubble.hasPlayedSound==False:
                       shouldPlaySound=True
                    break
                if shouldPlaySound: #only enters here once for each bubble explosion
                    pygame.mixer.Sound.play(allGameData.explodeSound)
                    tempset=set()
                    for bubble in bubblegroup:
                        bubble.hasPlayedSound=True
                        tempset.add((bubble.row,bubble.col))
                        if self.gamemode=="treasurehunt":
                          allGameData.cannotPushIntoSet.add((bubble.row,bubble.col))
                        if not self.isEmptyBlock(bubble.row,bubble.col):
                            allGameData.GridList[bubble.row][bubble.col]=0
                    self.bubblePosListOfSets.append(tempset)
                    
                       # print("hello")

                  
                for bubble in bubblegroup:
                     for player in self.playerGroup:
                          if (player.playerno==bubble.playerno and 
                            not bubble.hasDeducted):
                               player.currentBubbles-=1
                               bubble.hasDeducted=True

                       
                     
            #clear the grid of the bubbles in this exploding bubblegroup
                     if bubble.power>=0: #the bubbles that are still exploding
                        explosioncontinues=True
                        brow,bcol=bubble.row,bubble.col
                        bubble.power-=1
                        # (lefttile,righttile,uptile,downtile)=((brow,bcol-
                        #     bubble.explodeDistList[0]),
                        # (brow,bcol+bubble.explodeDistList[1]),
                        # (brow-bubble.explodeDistList[2],bcol),
                        # (brow+bubble.explodeDistList[3],bcol))
                        (downtile,lefttile,righttile,uptile)=((brow+
                          bubble.explodeDistList[0],bcol),
                        (brow,bcol-bubble.explodeDistList[1]),
                        (brow,bcol+bubble.explodeDistList[2]),
                        (brow-bubble.explodeDistList[3],bcol))
                        # print(lefttile,righttile,uptile,downtile)
                        backtracklist=self.collision([downtile,lefttile,righttile,uptile],bubble,bubblegroup)
                        # print(backtracklist)
                        # print(backtracklist)
                        if backtracklist!=None:
                          # for backtrackindex in backtracklist:
                          #    if backtrackindex==0: 
                          #        lefttile=(brow,bcol-bubble.explodeDistList[0]+1)
                          #    elif backtrackindex==1:
                          #        righttile=(brow,bcol+bubble.explodeDistList[1]-1)
                          #    elif backtrackindex==2:
                          #        uptile=(brow-bubble.explodeDistList[2]+1,bcol)
                          #    elif backtrackindex==3:
                          #        downtile=(brow+bubble.explodeDistList[3]-1,bcol)
                            for backtrackindex in backtracklist:
                             if backtrackindex==0: 
                                 downtile=(brow+bubble.explodeDistList[0]-1,bcol)
                                 
                             elif backtrackindex==1:
                                 lefttile=(brow,bcol-bubble.explodeDistList[1]+1)
                                 
                             elif backtrackindex==2:
                                 righttile=(brow,bcol+bubble.explodeDistList[2]-1)
                                 
                             elif backtrackindex==3:
                                 uptile=(brow-bubble.explodeDistList[3]+1,bcol)

                        for tile in self.tileGroup:
                            tpos=(tile.row,tile.col)
                            num=None
                            if tpos==(brow,bcol): num=3
                            elif tpos==lefttile: num=2
                            elif tpos==righttile: num=4
                            elif tpos==uptile: num=5
                            elif tpos==downtile: num=1
                            if num!=None:

                                tile.updateTile(num)
                        #only the directions that are still true keep expanding
                        for index in range(4):
                          if bubble.directionList[index]:
                            bubble.explodeDistList[index]+=1

                                
                
                if not explosioncontinues:
                    self.bubbleExplosionCount-=1 #timechecker
                    if self.bubbleExplosionCount<max(bubble.explodeDistList):
                          recoverList=[]
                          for bubble in bubblegroup:
                             recoverList+=self.endExplosion(bubble)

                          for tile in self.tileGroup:
                               tpos=(tile.row,tile.col)
                               if tpos in recoverList:
                                   tile.updateTile(0)
                          if self.gamemode in ["treasurehunt","Hero"]:
                             for bubble in bubblegroup:
                                if (bubble.row,bubble.col) in allGameData.emptyBlocksHaveBubbles:
                                   allGameData.emptyBlocksHaveBubbles.remove((bubble.row,bubble.col))
                          if self.gamemode=="treasurehunt":
                             for bubble in bubblegroup:
                                if (bubble.row,bubble.col) in allGameData.cannotPushIntoSet:
                                   allGameData.cannotPushIntoSet.remove((bubble.row,bubble.col))
                                print(bubble.row,bubble.col)
                                   
                          self.bubbleGroupgroup.remove(bubblegroup)  
                          for bubble in bubblegroup:
                            for bubblepossets in self.bubblePosListOfSets:
                                 if (bubble.row,bubble.col) in bubblepossets: 
                                    self.bubblePosListOfSets.remove(bubblepossets)
                                    break                      
                          self.bubbleExplosionCount=8
    def isEmptyBlock(self,row,col):
        if self.gamemode=="treasurehunt":
            if allGameData.map[row][col]==3:
               return True
        elif self.gamemode=="Hero":
            if allGameData.map[row][col] in [4,10,11]:
               return True
        return False  

    def isEmptyBlockDirection(self,row,col,directionindex):
          return not self.isEmptyBlock(row,col) or self.isEmptyDirection(row,col,directionindex)
    
    def isEmptyDirection(self,row,col,directionindex):
        if self.gamemode=="treasurehunt":
            if allGameData.map[row][col]==3 and directionindex in [1,2]: #left and right
               return True
        elif self.gamemode=="Hero":
            if allGameData.map[row][col] in [4,10,11] and (directionindex in [0,3]): #up and down
               return True
        return False  

    def endExplosion(self,bubble):
          # ld,rd,ud,dd=tuple(bubble.explodeDistList)
          # brow,bcol=bubble.row,bubble.col
          # recoverTileList=[]
          # for row in range(brow-ud,brow+dd+1):
          #       recoverTileList.append((row,bcol))
          # for col in range(bcol-ld,bcol+rd+1):
          #       recoverTileList.append((brow,col))
          # return recoverTileList
          dd,ld,rd,ud=tuple(bubble.explodeDistList)
          brow,bcol=bubble.row,bubble.col
          recoverTileList=[]
          for row in range(brow-ud,brow+dd+1):
                recoverTileList.append((row,bcol))
          for col in range(bcol-ld,bcol+rd+1):
                recoverTileList.append((brow,col))
          return recoverTileList
          
    def collision(self,explodedTileList,bubble,bubblelist):
       backtracklist=[]
       cancellist=[]
       for bubblepossets in self.bubblePosListOfSets:
           if (bubble.row,bubble.col) in bubblepossets:
              for epos in explodedTileList:
                 if epos!=(bubble.row,bubble.col) and epos in bubblepossets:
                    directionindex=explodedTileList.index(epos)
                    bubble.directionList[directionindex]=False
              break
          
       for block in self.blockGroup:
          row,col=block.row,block.col       
            
          if ((row,col) in explodedTileList): #explosion in a direction stops if hit a block
            directionindex=explodedTileList.index((row,col))


            if not ( self.isEmptyDirection(row,col,directionindex)):
     
              #if it is an empty block, bubbles exploding in the left and right (or up and down 
              #depending on gamemode) positions
              #will not be stopped but those in the up and down positions will be stopped 
                  bubble.directionList[directionindex]=False

                  #left,right,up,down
                  if block.canExplode:
                    self.blockGroup.remove(block)
                    if block.hiddenItem!="empty":
                        allGameData.GridList[row][col]=1
                        self.itemGroup.add(Item(row,col,block.hiddenItem,bubble))

                    elif block.hiddenItem=="empty":
                         allGameData.GridList[row][col]=0
                  else:
                     
                     if self.isEmptyBlockDirection(bubble.row,bubble.col,directionindex):
                        backtracklist.append(directionindex)
                     cancellist.append(explodedTileList[directionindex])
       for player in self.playerGroup:
        if not player.isDead and not player.invincible:
          ppos=player.getPlayerGrid()
          if ppos in explodedTileList and ppos not in cancellist:
            if self.gamemode=="Kungfu" and player.isTransformed:
                 player.transformback()
            else:
                     
                original=player.isJelly
                player.isJelly=True
                player.onBanana=False
                if original!=player.isJelly: 
    #move the player jelly down a bit in the first run to keep position the same
                  player.y+=allGameData.Gridh//2
        
       for item in self.itemGroup:
            itempos=(item.row,item.col)
            if itempos in explodedTileList and (item.fromBubble==None or item.fromBubble not in bubblelist): 
            #bubblelist is the list of bubbles in the same explosion
              if item.chosenname != "bun":
                if self.gamemode=="treasurehunt" and item.chosenname in allGameData.gemItems:
                    self.totalpoints-=allGameData.gemScores[item.chosenname]
                    # print(self.totalpoints)
                self.itemGroup.remove(item)



        #backtrack the explosion by one block since the block cannot explode
       if self.gamemode=="captureTheFlag":
           for homebase in self.homebaseGroup:
               hrow,hcol=homebase.row,homebase.col
               rowcolset=set(homebase.cornerlist)#use set for higher efficiency
               for epos in explodedTileList:
                  if epos in rowcolset:
                      directionindex=explodedTileList.index(epos)
                      bubble.directionList[directionindex]=False
                      backtracklist.append(directionindex) #backtrack the explosion by one block
       elif self.gamemode=="Hero":
           for herotower in self.homebaseGroup:
               hpos=(herotower.row,herotower.col)
               for epos in explodedTileList:
                  if epos == hpos:
                      directionindex=explodedTileList.index(epos)
                      if directionindex in [1,2] and not hpos==(bubble.row,bubble.col):
                        bubble.directionList[directionindex]=False
                        backtracklist.append(directionindex) #backtrack the explosion by one block
       return backtracklist if len(backtracklist)>0 else None


#has a a/b chance of returning True
    @staticmethod
    def randomChance(a,b):
        b=random.randint(1,b)
        if b<=a: return True  
    def mysort(self,player):
      return player.y

    def findPlayerWithID(self,playerid):
       for player in self.playerGroup:
          if player.playerno==playerid:
              return player


    def redrawAll(self, screen):


        one_surface=pygame.Surface((980,735))

        #Fill color to surface
        one_surface.blit(allGameData.gamewindowimage,(0,0)) #white

        #Blitting surface in to window
        screen.blit(one_surface,(0,0))

        if self.gamemode=="Kungfu":
           screen.blit(allGameData.backgroundImg,(0,0))


        for player in self.playerGroup:
              if player.playerno==self.displayPlayer:
                index=0
                for basicitem in [player.bubbleItem,player.powerItem,player.speedItem]:

                    label = allGameData.smallFont.render(str(basicitem), 1, (0,0,0))
                    screen.blit(label, (62+index*65, 697))
                    index+=1

        for player in self.playerGroup:
              if player.playerno==self.displayPlayer:
                index=0
                for key in player.itemkeydict:
                  usefulitem=player.itemkeydict[key]
                  if player.usefulitemdict[usefulitem]>0:
                    self.itemimage = allGameData.itemImgDict[usefulitem]
                    self.itemimage=pygame.transform.scale( self.itemimage.convert_alpha(),(50,50))
                    screen.blit(self.itemimage,(248+index*62,655))
                    # render text
                    label = allGameData.smallFont.render(str(player.usefulitemdict[usefulitem]), 1, (0,0,0))
                    screen.blit(label, (289+index*62, 694))
                    index+=1
                break
        

        
            

        allgroup = pygame.sprite.LayeredUpdates()
        for tile in self.tileGroup:
          allgroup.add(tile) #tile has default layer 0 (lowest layer)

#the other layers are based on row. We draw from top to bottom
        for block in self.blockGroup:
          allgroup.add(block)
          allgroup.change_layer(block,block.row*10)
        for item in self.itemGroup:
          allgroup.add(item)
          allgroup.change_layer(item,item.row*10)
          
               # print("item position: x:%d  y:%d  width:%d  height:%d"% (item.x,item.y,item.width,item.height))
        for bubbleGroup in self.bubbleGroupgroup:
          if bubbleGroup!=None:
            drawBubble=True
            for bubble in bubbleGroup:
                if bubble.isExploding:
                    drawBubble=False
            if drawBubble:
               for bubble in bubbleGroup:
                   allgroup.add(bubble)
                   allgroup.change_layer(bubble,bubble.row*10)
        playerSameRowDict=dict()
        for player in self.playerGroup:
          if player.image!=None: #in case player is dead or is in empty block
            allgroup.add(player)
            player.row=player.getPlayerGrid()[0]
            if player.row not in playerSameRowDict:
               playerSameRowDict[player.row]=[]
               playerSameRowDict[player.row].append(player)
            else:
               playerSameRowDict[player.row].append(player)
            allgroup.change_layer(player,player.row*10)
        for keyrow in playerSameRowDict:
           sameRowPlayerList=playerSameRowDict[keyrow]
           sameRowPlayerList=sorted(sameRowPlayerList,key=self.mysort) 
        #sort by the y positions of players for 2.5 D
           for player in sameRowPlayerList:
                allgroup.change_layer(player,player.row*10+sameRowPlayerList.index(player))
        if self.gamemode=="Hero":
            for homebase in self.homebaseGroup:
             allgroup.add(homebase)
             allgroup.change_layer(homebase,homebase.row*10) 
        elif self.gamemode=="captureTheFlag":
          for player in self.playerGroup:
                player.bunshouldnotshow=False
          for homebase in self.homebaseGroup:
             allgroup.add(homebase)
             allgroup.change_layer(homebase,(homebase.row+1)*10+1) 
             #higher layer than everything on top of the bottom row of homebase
            
             #so that the player gets hidden when entering the homebase from the side
             for player in self.playerGroup:
               
               prow,pcol=player.getPlayerGrid()
               if (prow,pcol) in homebase.twosides:
                  if player.x<allGameData.Gridw*(homebase.col)-40 or player.x>allGameData.Gridw*(homebase.col+1)+40:
                    origlayer=allgroup.get_layer_of_sprite(player)
                    allgroup.change_layer(player,origlayer+13)
                  else:
                    allgroup.change_layer(player,-1)

               if (prow,pcol) in homebase.allSides:
                    player.bunshouldnotshow=True #player is in homebase, so bun should not show   
       
           
              # print("player position: x:%d  y:%d  width:%d  height:%d"% (player.x,player.y,player.width,player.height))
        allgroup.draw(screen)

        lefttime=(allGameData.maxPlayingTime-self.timecount)//80
        if lefttime>=0:
          minute=lefttime//60
          second=lefttime-60*minute
          if second<10: second="0%d"%second
          mylabel = allGameData.superlargeFont.render("%d:%s"%(minute,second), 1, allGameData.yellow)
        else:
           mylabel = allGameData.superlargeFont.render("0:00", 1, allGameData.yellow)
        screen.blit(mylabel, (820,60))

        #draw arrow and invincible mark, this is the topmost layer
        for player in self.playerGroup: 
              if player.playerno==self.displayPlayer and not player.isDead:
                 screen.blit(allGameData.arrowimage,(player.x-17,player.y-105))

              if player.invincible:
                 label = allGameData.largeFont.render("INV", 1, (255,0,0))
                 screen.blit(label, (player.x-17, player.y-95))
              if self.gamemode=="treasurehunt" and player.playerno in self.highestscoreplayers:
                  label = allGameData.largeFont.render("Leading", 1, player.color)
                  screen.blit(label, (player.x-27, player.y-95))
              elif (self.gamemode=="captureTheFlag"):  
                 if player.hasBun and (not player.isJelly) and (not player.bunshouldnotshow):
                       screen.blit(allGameData.bunitemImg,(player.x-25,player.y-80))
                 
              elif self.gamemode=="Hero":
                  if player.hashero and not player.isJelly:
                      screen.blit(allGameData.heroitemImg,(player.x-29,player.y-80))

        if self.gamemode=="captureTheFlag":
          for homebase in self.homebaseGroup:
                   for bunindex in range(homebase.numbuns):
                     screen.blit(allGameData.smallbunitemImg,(homebase.x-23+12*bunindex,homebase.y-122))

        elif self.gamemode=="Hero":
          for herotower in self.homebaseGroup:
                   for heroindex in range(herotower.numheros):
                     screen.blit(allGameData.statueImg,(herotower.x-25,herotower.y-90-heroindex*20))

        quitlabel=allGameData.smallFont.render("Click left top to quit", 1, allGameData.red)
        screen.blit(quitlabel,(780,650))
        
        playerstr="Player %d"%(self.displayPlayer)
        player=self.findPlayerWithID(self.displayPlayer)
        teamcolor=allGameData.red if player.team=="red" else allGameData.blue
        playerlabel=allGameData.superlargeFont.render(playerstr,1,teamcolor)
        screen.blit(playerlabel,(0,0))
        
        try:
          for player in self.playerGroup:
              xpos=890
              ypos=130+60*player.playerno
              playerstr="Player %d:"%(player.playerno)
              playerlabel=allGameData.largeFont.render(playerstr,1,allGameData.yellow)
              screen.blit(playerlabel,(800,ypos+20))
              if player.isDead or player.isWin==False:
                  cryindex=(self.timecount//4)%2
                  playerimage=allGameData.malecryImgs[cryindex]
              else:
                  playerimage=allGameData.gameImgDict[player.playerno-1]
              screen.blit(playerimage,(xpos,ypos))

              if allGameData.gamemode=="treasurehunt":
                  gemlabel=allGameData.superlargeFont.render(str(player.gemscore),1,allGameData.yellow)
                  screen.blit(gemlabel,(xpos-135,ypos+5))
              elif allGameData.gamemode=="Kungfu":
                  killcountlabel=allGameData.superlargeFont.render(str(player.killcount),1,allGameData.yellow)
                  screen.blit(killcountlabel,(xpos-135,ypos+5))
                  if player.streaklabel:
                      player.streakcount+=1
                      if player.streakcount>allGameData.maxstreakcount:
                         player.streaklabel=False
                         player.streakcount=0
                      killstreaklabel=allGameData.superlargeFont.render(str(player.killstreak)+" in a row!",1,allGameData.yellow)
                      screen.blit(killstreaklabel,(player.x-50,player.y-90))
        except: pass

        if self.gameends:
          self.endgamecount+=1
          if self.endgamecount>allGameData.gameendcount:
              self.playing=False
          screen.blit(allGameData.resultsimage,(100,100))
          rowindex=0
          displaytitle=["P.No","Kill","Save","Die","W\\L"]
          for index in range(len(displaytitle)): 
                self.displayLabels(screen,displaytitle[index],index*100,-50,allGameData.yellow)
          for player in self.playerGroup:
             if player.isWin==None:
                isWin="Tie"
             elif player.isWin==True:
                isWin="Win"
             elif player.isWin==False:
                isWin="Lost"
             displaylist=[player.playerno,player.killcount,player.savecount,player.deadtimes,isWin]

             for index in range(len(displaylist)): 
                self.displayLabels(screen,str(displaylist[index]),index*100,rowindex*30,player.color)
             rowindex+=1  



    def displayLabels(self,screen,str1,x,y,color):
        mylabel = allGameData.superlargeFont.render(str1, 1, color)
        screen.blit(mylabel,(200+x,215+y))
        
# def main():
#     game1 = singleGame()
#     game1.run()

# if __name__ == '__main__':
#     main()

