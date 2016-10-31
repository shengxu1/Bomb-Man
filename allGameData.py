import pygame

#contains all the game variables and images
#customize according to game mode and the extra items player buy in the shop
#customize the team orders
class allGameData(object):

   def __init__(self):
     self.initiatlizeLevels()
     allGameData.numberofpinchecks=100
     allGameData.instructionImg=pygame.transform.scale(pygame.image.load(
      'images/instructionboard.png').convert_alpha(),(600,600))

     allGameData.screenSize=(980,735)
     allGameData.NumMaps={"captureTheFlag":5,"treasurehunt":2,"Hero":2,"Kungfu":3}
     self.cursorscale=20,30
     allGameData.loginImg=pygame.transform.scale(pygame.image.load(
      'images/login.png').convert_alpha(),allGameData.screenSize) 
     allGameData.accountImg=pygame.transform.scale(pygame.image.load
      ('images/accountbackground.png').convert_alpha(),allGameData.screenSize) 
     allGameData.cursorimage=pygame.transform.scale(pygame.image.load('images/cursor.png').convert_alpha(),self.cursorscale)      

     allGameData.smallFont = pygame.font.SysFont("chalkduster", 13)
     allGameData.largeFont = pygame.font.SysFont("chalkduster", 13)
     allGameData.superlargeFont = pygame.font.SysFont("chalkduster", 24)
     allGameData.slightlargeFont=pygame.font.SysFont("chalkduster", 15)
     allGameData.superlargeFont.set_bold(True)
     allGameData.supersuperlargeFont = pygame.font.SysFont("chalkduster", 29)
     allGameData.supersuperlargeFont.set_bold(True)
     allGameData.blue=(0,0,255)
     allGameData.red=(255,0,0)
     allGameData.black=(0,0,0)
     allGameData.yellow=(255,255,0)
     allGameData.green=(0,255,0)
     allGameData.white=(255,255,255)
     allGameData.azure=(137, 207, 240)
     allGameData.brown=(165,42,42)
     allGameData.colors=["red","blue","yellow","green"]
     allGameData.characters=["ninja","monkey","robot","cutegirl"]
     allGameData.transformcharacters=["devil","gentleman","panda","pudding","transparentpudding"]
     allGameData.gamemodes=["captureTheFlag","treasurehunt","Hero","Kungfu"]
     allGameData.gamemodemaxteams={"captureTheFlag":2,"treasurehunt":8,"Random":8,"Hero":2,"Kungfu":8}
     allGameData.chatMaxY=600
     allGameData.chatMinY=450
     allGameData.chatX=100

     allGameData.numberofdifferentbubbles=2
     allGameData.numberofhats=6
     allGameData.maxcanstartcount=500

     self.gamecharacterscale=40,50
     allGameData.kickBubbleDistances=[4,3,2]

     allGameData.numplayersonranking=8 #number of players on the ranking
     
     
     allGameData.hatscales=[(100,100),(100,100),(60,60),(50,50),(60,60),(80,80),(60,60),(60,60)]
     allGameData.hatxypositions=[(0,0),(0,0),(20,0),(25,10),(20,10),(10,30),(0,80),(0,80)]
     
     self.gamelogoscale=40,40
     allGameData.gamemodelogos=dict()
     for gamemode in allGameData.gamemodes:
        allGameData.gamemodelogos[gamemode]=pygame.transform.scale(pygame.image.load('images/logos/%s.png'%gamemode).convert_alpha(),self.gamelogoscale)   
     
   def initiatlizeLevels(self):
       allGameData.levelnames=["Rookie","Beginner","Bubble apprentice",
       "Bubble captain","Bubble master","Bubble lord","Bubble Demon",
       "Bubble warlord","Bubble king","Bubble god","???"]
       allGameData.levelexperiences=[0,10,50,100,200,400,600,800,1000,1300,1600]
       allGameData.basicExp=3  #the experience players get for completing each game
       allGameData.killExp=3
       allGameData.saveExp=2
       allGameData.winExp=10
       self.levellogoscale=20,20
       allGameData.levelImgs=[]
       

       for level in range(len(allGameData.levelexperiences)):
           allGameData.levelImgs.append(pygame.transform.scale(
            pygame.image.load('images/levels/level%d.png'%level).convert_alpha(),self.levellogoscale))
   def initmaps(self,gamemode):
       if gamemode=="captureTheFlag":
           allGameData.revivePositions=[[[(0,2),(0,3)],[(12,14),(11,14)]],
           [[(3,1),(3,2)],[(3,13),(3,14)]],[[(6,0),(5,0)],[(6,14),(5,14)]],
           [[(3,3),(9,3)],[(3,11),(9,11)]],[[(12,0),(12,1)],[(0,14),(0,13)]]
           ]
           allGameData.maps=[[[1,2,0,0,0,0,0,3,2,2,5,1,0,2,1],[1,2,0,0,0,0,0,3,2,2,1,1,0,2,1],
        [1,2,0,0,10,0,0,3,2,2,1,1,0,2,1],[1,2,0,0,0,0,0,0,2,2,1,1,0,2,1],
        [1,2,0,0,0,2,1,0,2,4,1,1,0,2,1],[1,2,0,1,1,2,1,3,2,4,1,1,0,2,1],
        [1,2,0,1,1,2,1,0,2,2,1,1,0,2,1],[1,2,0,1,1,2,1,1,2,2,1,1,0,2,1],
        [1,5,0,1,1,2,1,1,2,2,1,1,0,2,1],[1,2,0,1,1,2,1,0,2,2,1,2,0,0,0],
        [1,2,0,1,1,2,1,3,2,4,0,0,0,0,0],[1,2,0,5,1,2,1,3,2,2,0,0,11,0,0],
        [1,2,0,5,1,2,1,3,2,2,0,0,0,0,0]],
        [[1,2,0,1,1,2,1,3,2,2,1,1,0,2,2],[1,2,0,1,0,0,0,3,0,0,0,1,0,2,2],
        [0,0,0,1,0,10,0,3,0,11,0,1,0,0,0],[0,0,0,2,0,0,0,3,0,0,0,2,0,0,0],
        [0,2,0,4,0,0,0,4,0,0,0,4,0,2,0],[0,1,1,0,1,1,1,3,1,1,1,0,1,1,0],
        [0,1,1,0,1,2,2,3,2,2,2,0,1,1,0],[0,0,0,4,3,0,0,4,0,0,3,4,0,0,0],
        [0,4,3,3,2,3,3,2,3,3,3,2,3,4,0],[0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],[0,5,1,5,5,1,5,5,5,1,5,1,5,5,0],
        [5,5,5,5,1,1,5,5,1,1,5,1,1,5,5]],
        [[5,5,5,3,5,3,2,5,5,3,5,5,2,5,5],[0,0,0,0,0,2,2,2,2,2,0,0,0,0,0],
        [0,4,5,2,5,1,1,1,1,1,3,5,5,5,0],[1,1,2,2,2,4,2,2,2,4,2,2,2,1,0],
        [1,0,0,0,2,1,3,0,3,1,2,0,0,0,1],[0,0,0,0,0,0,1,3,3,0,0,0,0,0,0],
        [0,0,10,0,0,2,3,2,2,0,0,0,11,0,0],[0,0,0,0,0,0,1,3,3,0,0,0,0,0,0],
        [1,0,0,0,2,1,3,1,3,0,2,0,0,0,1],[1,1,2,2,2,4,2,2,2,4,2,2,2,1,1],
        [0,5,5,5,3,1,1,1,1,1,5,2,5,4,0],[0,0,0,0,0,2,2,2,2,2,0,0,0,0,0],
        [5,5,2,5,3,5,5,3,2,3,3,5,5,5,5]],
        [[2,0,0,0,0,0,0,0,0,0,0,0,0,0,2],[3,1,3,3,0,3,3,1,3,3,3,3,3,1,3],
        [3,2,3,0,3,2,1,2,1,2,0,1,3,2,3],[3,0,3,0,0,1,2,1,2,1,0,0,3,0,3],
        [4,0,4,1,0,2,1,2,1,2,3,0,4,0,4],[0,0,0,3,3,3,3,3,3,3,0,3,0,0,0],
        [0,10,0,0,1,2,1,2,1,2,1,0,0,11,0],[0,0,0,3,2,3,3,3,3,3,3,3,0,0,0],
        [4,0,4,0,3,1,2,1,2,1,0,2,3,0,4],[3,0,3,0,0,2,1,2,1,2,0,0,3,0,3],
        [3,2,3,1,0,1,2,1,2,1,3,0,3,2,3],[3,1,3,3,3,3,3,1,3,3,0,3,3,1,3],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,2]],
        [[2,0,0,0,0,2,2,2,1,1,1,1,0,0,0],[2,0,1,4,4,0,0,0,0,2,3,3,0,0,0],
        [2,0,1,4,2,1,0,0,0,0,1,1,0,11,0],[2,0,0,0,0,2,5,5,5,3,5,0,0,0,0],
        [0,0,3,3,3,1,1,1,1,1,1,2,0,0,2],[0,5,2,2,2,1,5,5,5,5,1,5,1,1,5],
        [1,5,5,0,0,4,5,5,5,2,1,5,0,1,2],[0,0,5,0,0,2,2,2,2,2,4,5,5,1,2],
        [1,0,5,5,1,0,0,0,0,2,5,3,3,3,2],[0,0,0,5,1,1,1,1,1,2,5,0,0,0,2],
        [0,10,0,2,2,2,3,3,0,1,4,1,5,5,5],[0,0,0,1,1,1,5,5,5,1,1,1,5,2,5],
        [0,0,0,0,3,3,0,0,0,0,0,2,2,2,5]]]



       elif gamemode=="treasurehunt":

            allGameData.maps=[[[4,1,1,1,1,0,0,0,0,0,1,1,1,1,4],[1,2,1,1,2,2,2,2,2,2,2,1,1,2,1],
        [1,1,1,2,2,0,0,0,0,0,2,2,1,1,1],[1,1,1,2,0,5,0,3,0,5,0,2,1,1,1],
        [1,1,2,2,0,0,0,3,0,0,0,2,2,1,1],
        [0,2,2,0,0,0,0,3,0,0,0,0,2,2,0],[0,2,0,0,0,0,3,1,3,0,0,0,0,2,0],
        [0,2,2,0,0,2,0,3,0,0,0,0,2,2,0],[1,1,1,2,2,0,0,3,0,0,2,2,1,1,1],
        [1,1,1,2,0,5,0,3,0,5,0,2,1,1,1],
        [1,1,1,2,2,2,0,0,0,2,2,2,1,1,1],[1,2,1,1,1,2,2,2,2,2,1,1,1,2,1],
        [4,1,1,1,0,0,0,0,0,0,0,1,1,1,4]],
        [[1,2,1,1,1,1,1,1,1,1,1,1,1,2,1],[2,5,2,0,0,0,2,0,2,0,0,0,2,5,2],
        [1,2,0,2,0,2,0,2,0,2,0,2,0,2,1],[1,0,2,0,0,0,2,0,2,0,0,0,2,0,1],
        [1,0,0,2,0,2,0,0,0,2,0,2,0,0,1],
        [1,0,0,0,2,0,0,2,0,0,2,0,0,0,1],[1,0,3,0,0,0,2,5,2,0,0,0,3,0,1],
        [1,0,0,0,2,0,0,2,0,0,2,0,0,0,1],[1,0,0,2,0,2,0,0,0,2,0,2,0,0,1],
        [1,0,2,0,0,0,2,0,2,0,0,0,2,0,1],
        [1,2,0,2,0,2,0,2,0,2,0,2,0,2,1],[2,5,2,0,0,0,2,0,2,0,0,0,2,5,2],
        [1,2,1,1,1,1,1,1,1,1,1,1,1,2,1]]]

       elif gamemode=="Hero":
            allGameData.maps=[[[3,1,0,1,3,3,3,3,3,3,3,1,0,1,3],[1,0,5,1,3,3,3,3,3,3,3,1,5,0,1],
        [0,1,1,5,3,3,3,4,3,3,3,5,1,1,0],[1,1,0,0,2,2,0,2,0,2,0,0,0,0,1],
        [0,0,4,0,2,0,2,2,2,0,2,0,4,0,0],
        [1,5,0,5,5,5,5,5,5,5,5,5,0,5,1],[1,5,1,0,0,0,0,5,0,0,0,0,1,5,1],
        [0,1,5,0,0,10,0,5,0,11,0,0,5,1,0],[0,0,1,0,0,0,0,5,0,0,0,0,0,0,0],
        [0,0,5,0,5,0,1,5,1,0,5,0,5,0,0],
        [0,5,5,0,5,5,1,5,1,5,5,0,5,5,0],[1,1,0,0,0,0,5,5,5,0,0,0,0,0,0],
        [1,1,0,0,0,0,0,3,0,0,0,0,0,0,1]],
        [[3,2,2,2,0,3,3,3,3,3,0,2,2,2,3],[3,0,2,0,2,3,3,3,3,3,2,0,2,0,3],
        [2,0,0,0,2,3,3,3,3,3,2,0,0,0,2],[2,2,0,2,2,2,2,2,2,2,2,2,0,2,2],
        [2,0,0,0,2,2,2,2,2,2,2,0,0,0,2],
        [1,1,1,1,5,5,4,5,4,5,5,1,1,1,1],[0,2,2,2,2,2,0,1,0,2,2,2,2,2,0],
        [1,0,2,2,0,0,0,1,0,0,0,2,2,0,1],[0,2,0,2,0,0,0,1,0,0,0,2,0,2,0],
        [0,0,2,5,2,0,0,1,0,0,2,5,2,0,0],
        [1,2,0,0,0,0,0,1,0,0,0,0,0,2,1],[0,2,0,10,0,0,0,1,0,0,0,11,0,2,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]]]

       elif gamemode=="Kungfu":
            allGameData.maps=[[[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,0,0,0,1,2,1,2,1,2,1,0,0,0,3],[3,0,0,0,1,2,1,2,1,2,1,0,0,0,3],
        [3,1,1,1,2,2,1,2,1,2,2,1,1,1,3],[3,2,2,2,2,1,2,1,2,1,2,2,2,2,3],
        [3,2,2,2,2,1,2,1,2,1,2,2,2,2,3],[3,1,1,1,2,2,1,2,1,2,2,1,1,1,3],
        [3,0,0,0,1,2,1,2,1,2,1,0,0,0,3],[3,0,0,0,1,2,1,2,1,2,1,0,0,0,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]],
        [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],[3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],
        [3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],[3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],
        [3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],[3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],
        [3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],[3,2,2,2,2,2,0,0,0,1,1,1,1,1,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]],
        [[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],[3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
        [3,0,1,2,1,0,1,2,1,0,1,2,1,0,3],[3,0,0,1,0,0,2,1,2,0,0,1,0,0,3],
        [3,0,1,1,1,0,1,2,1,0,1,1,1,0,3],[3,1,1,2,1,1,1,2,1,1,1,2,1,1,3],
        [3,1,1,2,1,1,1,2,1,1,1,2,1,1,3],[3,0,1,1,1,0,1,2,1,0,1,1,1,0,3],
        [3,0,0,1,0,0,2,1,2,0,0,1,0,0,3],[3,0,1,2,1,0,1,2,1,0,1,2,1,0,3],
        [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]]

   def roominit(self):
       allGameData.lockpositionImg=pygame.transform.scale(
        pygame.image.load('images/room/stopsign.png').convert_alpha(),(110,110))

       self.boardscale=800,600
       allGameData.rankingboardImg=pygame.transform.scale(
        pygame.image.load('images/room/rankingboard.png').convert_alpha(),self.boardscale)
       self.shopitemlogoscale=100,100
       allGameData.ymargin=50
       allGameData.shopx,allGameData.shopy=400,200
       allGameData.shophorizontallines=2
       allGameData.shopverticallines=len(allGameData.hatscales)//allGameData.shophorizontallines
       allGameData.shopItemImgs=[]
       for hatindex in range(allGameData.numberofhats):
          allGameData.shopItemImgs.append(pygame.transform.scale(
            pygame.image.load('images/shop/hat%d.png'%hatindex).convert_alpha(),
            self.shopitemlogoscale))
       for bubbleindex in range(allGameData.numberofdifferentbubbles):
           allGameData.shopItemImgs.append(pygame.transform.scale(
            pygame.image.load('images/shop/bubble%d.png'%bubbleindex).convert_alpha(),
            self.shopitemlogoscale))

       self.tickscale=50,50
       allGameData.gamewindowposition=(650,0)
       allGameData.roomcharacterscale=80,100
       allGameData.roomimage=pygame.transform.scale(pygame.image.load('images/room.png').convert_alpha(),allGameData.screenSize)
       allGameData.tickimage=pygame.transform.scale(pygame.image.load('images/tick.png').convert_alpha(),self.tickscale)    
       allGameData.choosegamemodeImg=pygame.image.load("images/room/gamemodes.png").convert_alpha()
       
       self.gamemapscale=200,250
       allGameData.gamemodemapdict=dict()

       for gamemode in allGameData.gamemodes:
           gamemodelist=[]
           for i in range(allGameData.NumMaps[gamemode]):
              gamemodelist.append(pygame.transform.scale(pygame.image.load('images/room/%s%d.png'%(gamemode,i)).convert_alpha(),self.gamemapscale))
           allGameData.gamemodemapdict[gamemode]=gamemodelist


   def gameinit(self,gamemode,gamemap,ismultigame):
      allGameData.gamemode=gamemode
      allGameData.map=gamemap
      allGameData.Rows,allGameData.Cols=len(gamemap),len(gamemap[0])

      allGameData.bubbleScale=110,110
      allGameData.bubbleyshift=5
      allGameData.itemScale=40,40  
      self.arrowscale=30,35 

      if ismultigame: #multi computer mode
           allGameData.gameendcount=300
           allGameData.maxPlayingTime=18000
           allGameData.deadCount=300
           allGameData.cryCount=150
           allGameData.invincibleCount=200
           allGameData.timetillexp=40
           allGameData.maxJellyCount=400
           allGameData.bananaSpeed=16
           allGameData.dartSpeed=20
           allGameData.maxslowcount=350
           allGameData.bubblechangingspeed=12   # how slow the bubble changes form
       
      else: #single computer mode
           allGameData.gameendcount=200
           allGameData.maxPlayingTime=18000
           allGameData.deadCount=150
           allGameData.cryCount=80
           allGameData.invincibleCount=200
           allGameData.timetillexp=80
           allGameData.maxJellyCount=200
           allGameData.bananaSpeed=20
           allGameData.dartSpeed=24
           allGameData.maxslowcount=350
           allGameData.bubblechangingspeed=8   # how slow the bubble changes form
         
            # allGameData.teamOrder=[red,blue]
     
      
      allGameData.Bwid,allGameData.Bhei=750,650
      allGameData.Gridw,allGameData.Gridh= 50, 50
      allGameData.GridList=[[0]*15 for row in range(13)]
      allGameData.BasicItems={"power","speed","bubble","question"}
      allGameData.UsefulItems={"slow","banana","fork","dart"}
      allGameData.OnetimeItems={"makeslow","bananapeel","hiddenbubble"} 
      #use sets for higher efficiency

      allGameData.directionList=["down","left","right","up"]
      allGameData.directiondrdc=[(1,0),(0,-1),(0,1),(-1,0)]
      if gamemode=="captureTheFlag":
          self.hbscale=int(allGameData.Gridw*3.1),int(allGameData.Gridh*3.6)
          self.bunscale=allGameData.Gridw,int(allGameData.Gridh*0.8)
          self.smallebunscale=13,13

      elif gamemode=="treasurehunt":
          allGameData.emptyBlocksHaveBubbles=set()
          allGameData.cannotPushIntoSet=set()

      elif gamemode=="Hero":
          self.hbscale=int(allGameData.Gridw*1.2),int(allGameData.Gridh*1.8)
          self.heroscale=int(allGameData.Gridw*1.2),int(allGameData.Gridh*0.8)
          allGameData.emptyBlocksHaveBubbles=set()

      elif gamemode=="Kungfu":
         allGameData.maxstreakcount=100
         allGameData.transformcharacterImgs=dict()
         for character in allGameData.transformcharacters:

              imagename='images/transformcharacters/%s.png'% (character)
              image = pygame.image.load(imagename).convert_alpha()
              self.rows, self.cols = 4, 4
              width, height = image.get_size()
              cellWidth, cellHeight = width/self.cols,(height)/self.rows

              characterlist=[]

              for j in range(self.rows):
                  for i in range(self.cols):
                      subImage = image.subsurface(
                          (i * cellWidth, j * cellHeight, 
                              cellWidth, cellHeight))
                      characterlist.append(pygame.transform.scale(
                  subImage.convert_alpha(),
                  (120,120)))
              allGameData.transformcharacterImgs[character]=characterlist



   def initGameImages(self,teamlist,characterlist):
          allGameData.gameImgDict=dict()
       
          for index in range(len(teamlist)):
            try: #thread safe
              if teamlist[index]!=None and characterlist[index]!=None:
                 team,character=teamlist[index],characterlist[index]
                 allGameData.gameImgDict[index]=(pygame.transform.scale(
                  pygame.image.load('images/room/%s%s.png'%(team,character)).convert_alpha(),
                    self.gamecharacterscale))
            except:
               pass
  
    
#load all images (so we don't have to reload every time) according to gamemode
#also init sounds
   def initImages(self):
       self.fillBubbleList()

       allGameData.gamewindowimage=pygame.image.load("images/gamewindow.png").convert_alpha()
       allGameData.resultsimage=pygame.image.load("images/resultspage.png").convert_alpha()
       allGameData.arrowimage=pygame.transform.scale(pygame.image.load("images/arrow.png").convert_alpha(),self.arrowscale)



       #explosion images
       self.tilescale=allGameData.Gridw,allGameData.Gridh
       allGameData.explosionImgList=[pygame.transform.scale(pygame.image.load('images/explosiondown.png').convert_alpha(),self.tilescale),
       pygame.transform.scale(pygame.image.load('images/explosionleft.png').convert_alpha(),self.tilescale),
       pygame.transform.scale(pygame.image.load('images/explosionmid.png').convert_alpha(),self.tilescale),
       pygame.transform.scale(pygame.image.load('images/explosionright.png').convert_alpha(),self.tilescale),
       pygame.transform.scale(pygame.image.load('images/explosionup.png').convert_alpha(),self.tilescale)]


       
       allGameData.malecryImgs= [ pygame.transform.scale(pygame.image.load(
        'images/malecry0.png').convert_alpha(),self.gamecharacterscale),
       pygame.transform.scale(pygame.image.load(
        'images/malecry1.png').convert_alpha(),self.gamecharacterscale)]

   
       allGameData.explodeSound=pygame.mixer.Sound("sounds/explosion.wav")
       allGameData.itemSound=pygame.mixer.Sound("sounds/getitem.wav")
       allGameData.bubbleSound=pygame.mixer.Sound("sounds/putbubble.wav")
       allGameData.killSound=pygame.mixer.Sound("sounds/kill.wav")
       allGameData.thankyouSound=pygame.mixer.Sound("sounds/thankyou.wav")
       allGameData.startgameSound=pygame.mixer.Sound("sounds/startgame.wav")
       allGameData.pushblockSound=pygame.mixer.Sound("sounds/pushblock.wav")
       if allGameData.gamemode=="Kungfu":
           allGameData.doublekillSound=pygame.mixer.Sound("sounds/doublekill.wav")
           allGameData.triplekillSound=pygame.mixer.Sound("sounds/triplekill.wav")
           allGameData.dominatingSound=pygame.mixer.Sound("sounds/dominating.wav")
           allGameData.rampageSound=pygame.mixer.Sound("sounds/rampage.wav")
           allGameData.kickbubbleSound=pygame.mixer.Sound("sounds/kickbubble.wav")
           allGameData.doublekillSound.set_volume(1)
           allGameData.triplekillSound.set_volume(1)
           allGameData.dominatingSound.set_volume(1)
           allGameData.rampageSound.set_volume(1)
       allGameData.explodeSound.set_volume(1)
       allGameData.thankyouSound.set_volume(1)
       allGameData.startgameSound.set_volume(1)
       
       # allGameData.bubbleImgList=[pygame.transform.scale(pygame.image.load('images/bubbles/bubble1_0.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/bubble1_1.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/bubble1_2.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/bubble1_3.png').convert_alpha(),allGameData.bubbleScale)]
       # allGameData.transbubbleImgList=[pygame.transform.scale(pygame.image.load('images/bubbles/transbubble1_0.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/transbubble1_1.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/transbubble1_2.png').convert_alpha(),allGameData.bubbleScale),
       # pygame.transform.scale(pygame.image.load('images/bubbles/transbubble1_3.png').convert_alpha(),allGameData.bubbleScale)]

       if allGameData.gamemode=="captureTheFlag":
       #tile image
             allGameData.tileImg= pygame.transform.scale(pygame.image.load(
              'images/captureTheFlag/tile.png').convert_alpha(),self.tilescale)

             allGameData.homebaseImgs=[]
             for color in allGameData.colors:
                allGameData.homebaseImgs.append(pygame.transform.scale(pygame.image.load(
              'images/%s/homebase%s.png'%(allGameData.gamemode,color)).convert_alpha(),self.hbscale))

             allGameData.bunitemImg=pygame.transform.scale(pygame.image.load(
              'images/%s/bunitem.png'%allGameData.gamemode).convert_alpha(),self.bunscale)
             allGameData.smallbunitemImg=pygame.transform.scale(pygame.image.load(
              'images/%s/bunitem.png'%allGameData.gamemode).convert_alpha(),self.smallebunscale)
           
            #block images
             allGameData.blockImgDict=dict()
             allGameData.blockimagenames=["greenblock","yellowblock","bun","lamp","tree"]
             allGameData.blockimageheights={"greenblock":60,"yellowblock":60,"bun":75,"lamp":78,"tree":75}
             allGameData.upperYShifts={"bun":10,"lamp":10,"tree":10}
             allGameData.explodableblocks=2
             for block in allGameData.blockimageheights:
                  imagename='images/%s/%s.png'%(allGameData.gamemode,block)
                  allGameData.blockImgDict[block]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),
                    (allGameData.Gridw,allGameData.blockimageheights[block]))


             #item images
             allGameData.itemNames=["power","speed","bubble","question","slow",
             "banana","fork","dart","hiddenbubble","empty"]
             allGameData.itemfrequency={"power":10,"speed":12,"bubble":15,"question":4,"slow":8,
             "banana":6,"fork":4,"dart":2,"hiddenbubble":2,"empty":15}
             allGameData.allItemNames=["bun","power","speed","bubble","question","slow","banana","fork","dart","hiddenbubble","makeslow","bananapeel","leftdart","rightdart","updart","downdart"]
             allGameData.itemImgDict=dict()
             for itemname in allGameData.allItemNames:
                imagename='images/items/%sitem.png'%itemname
                allGameData.itemImgDict[itemname]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),allGameData.itemScale)

       elif allGameData.gamemode=="treasurehunt":
             allGameData.tileImgs= [pygame.transform.scale(pygame.image.load(
              'images/treasurehunt/tile1.png').convert_alpha(),self.tilescale),
             pygame.transform.scale(pygame.image.load(
              'images/treasurehunt/tile2.png').convert_alpha(),self.tilescale)]
            #block images
             allGameData.blockImgDict=dict()
             allGameData.blockimagenames=["chest","darkblock","skull","flame","knight"]
             allGameData.blockimageheights={"chest":60,"darkblock":60,"skull":90,"flame":65,"knight":90}
             allGameData.explodableblocks=2
             allGameData.upperYShifts={"flame":15,"knight":30,"skull":20}
             for block in allGameData.blockimageheights:
                  imagename='images/%s/%s.png'%(allGameData.gamemode,block)
                  allGameData.blockImgDict[block]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),
                    (allGameData.Gridw,allGameData.blockimageheights[block]))

             allGameData.gemScales=[(15,35),(20,40),(30,30)]
             #item images
             allGameData.itemNames=["power","speed","bubble","question","slow",
             "banana","fork","dart","hiddenbubble","empty"]
             allGameData.gemItems=["redgem","yellowgem","greengem"]
             allGameData.gemScores={"redgem":1,"yellowgem":2,"greengem":3}
             allGameData.gemfrequency={"redgem":5,"yellowgem":3,"greengem":1,"empty":3}
             allGameData.itemfrequency={"power":10,"speed":12,"bubble":15,"question":3,"slow":6,
             "banana":3,"fork":3,"dart":2,"hiddenbubble":5,"empty":8}
             allGameData.allItemNames=["power","speed","bubble","question","redgem","yellowgem","greengem","slow","banana","fork","dart","hiddenbubble","makeslow","bananapeel","leftdart","rightdart","updart","downdart"]
             allGameData.itemImgDict=dict()
             for itemname in allGameData.allItemNames:
                imagename='images/items/%sitem.png'%itemname
                if "gem" in itemname:
                   allGameData.itemImgDict[itemname]=pygame.transform.scale(
                    pygame.image.load(imagename).convert_alpha(),allGameData.gemScales[allGameData.gemItems.index(itemname)])
                else:
                   allGameData.itemImgDict[itemname]=pygame.transform.scale(
                    pygame.image.load(imagename).convert_alpha(),allGameData.itemScale)


       elif allGameData.gamemode=="Hero":
             self.statuescale=50,25
       #tile image
             allGameData.tileImg= pygame.transform.scale(pygame.image.load(
              'images/Hero/tile.png').convert_alpha(),self.tilescale)
             allGameData.statueImg=pygame.transform.scale(pygame.image.load(
              'images/Hero/basicstatue.png').convert_alpha(),self.statuescale)

             allGameData.homebaseImgs=[]
             for color in allGameData.colors:
                allGameData.homebaseImgs.append(pygame.transform.scale(pygame.image.load(
              'images/Hero/%shome.png'%(color)).convert_alpha(),self.hbscale))
            #block images
             allGameData.explodableblocks=3
             allGameData.blockImgDict=dict()
             allGameData.blockimagenames=["greenblock","whiteblock","bun","door","tree"]
             allGameData.blockimageheights={"greenblock":60,"whiteblock":60,"bun":60,"door":85,"tree":70}
             allGameData.upperYShifts={"door":20,"tree":10}
             for block in allGameData.blockimageheights:
                  imagename='images/%s/%s.png'%(allGameData.gamemode,block)
                  allGameData.blockImgDict[block]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),
                    (allGameData.Gridw,allGameData.blockimageheights[block]))
             allGameData.heroitemImg=pygame.transform.scale(pygame.image.load(
              'images/items/heroitem.png').convert_alpha(),self.heroscale)
             allGameData.bunNames=["hero","empty"]
             allGameData.bunfrequency={"hero":1,"empty":2}
             #added the bomb item
             allGameData.itemNames=["power","speed","bubble","question","slow",
             "banana","fork","dart","hiddenbubble","bomb","empty"]
             allGameData.UsefulItems={"slow","banana","fork","dart","bomb","hero"}
             allGameData.itemfrequency={"power":10,"speed":12,"bubble":15,"question":2,"slow":4,
             "banana":6,"fork":2,"dart":2,"bomb":5,"hiddenbubble":2,"empty":3}
             allGameData.allItemNames=["hero","power","speed","bubble","question","bomb","slow","banana","fork","dart","hiddenbubble","makeslow","bananapeel","leftdart","rightdart","updart","downdart"]
             allGameData.itemImgDict=dict()
             for itemname in allGameData.allItemNames:
                imagename='images/items/%sitem.png'%itemname
                allGameData.itemImgDict[itemname]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),allGameData.itemScale)

       elif allGameData.gamemode=="Kungfu":

             self.backgroundscale=750,628
       #tile image
             allGameData.tileImg= pygame.transform.scale(pygame.image.load(
              'images/Kungfu/tile.png').convert_alpha(),self.tilescale)

             allGameData.backgroundImg= pygame.transform.scale(pygame.image.load(
              'images/Kungfu/background.png').convert_alpha(),self.backgroundscale)
           
            #block images
             allGameData.blockImgDict=dict()
             allGameData.blockimagenames=["bi","wu","noblock"]
             allGameData.blockimageheights={"bi":60,"wu":60,"noblock":60}
             allGameData.upperYShifts={}
             allGameData.explodableblocks=2
             for block in allGameData.blockimageheights:
                  imagename='images/%s/%s.png'%(allGameData.gamemode,block)
                  allGameData.blockImgDict[block]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),
                    (allGameData.Gridw,allGameData.blockimageheights[block]))


             #item images
             allGameData.itemNames=["power","speed","bubble","question","slow",
             "banana","fork","dart","hiddenbubble","devil","gentleman","panda","pudding","empty"]
             allGameData.itemfrequency={"power":11,"speed":11,"bubble":15,"question":2,"slow":2,
             "banana":2,"fork":2,"dart":3,"hiddenbubble":2,"devil":1,"gentleman":2,"panda":3,"pudding":2,"empty":7}
             allGameData.allItemNames=["power","speed","bubble","question","slow",
             "banana","fork","dart","hiddenbubble","makeslow","bananapeel",
             "leftdart","rightdart","updart","downdart","devil","gentleman","panda","pudding"]
             allGameData.itemImgDict=dict()
             for itemname in allGameData.allItemNames:
                imagename='images/items/%sitem.png'%itemname
                allGameData.itemImgDict[itemname]=pygame.transform.scale(pygame.image.load(imagename).convert_alpha(),allGameData.itemScale)
   
   def fillBubbleList(self):
           #standard bubble images (bubbletype 1)
       
       allGameData.bubbleImgList,allGameData.transbubbleImgList=list(),list()
       

       for bubbletype in range(allGameData.numberofdifferentbubbles):
           innerbubblelist,innertransbubblelist=[],[]
           for index in range(4):
              innerbubblelist.append(pygame.transform.scale(
                  pygame.image.load('images/bubbles/bubble%d_%d.png'%(bubbletype,index)).convert_alpha(),
                  allGameData.bubbleScale))
              innertransbubblelist.append(pygame.transform.scale(
                  pygame.image.load('images/bubbles/transbubble%d_%d.png'%(bubbletype,index)).convert_alpha(),
                  allGameData.bubbleScale))
           allGameData.bubbleImgList.append(innerbubblelist)
           allGameData.transbubbleImgList.append(innertransbubblelist)

          





       
