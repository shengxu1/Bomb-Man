


import pygame

from Player import Player
from pygamegame import PygameGame
import random
from Bubble import Bubble
from allGameData import allGameData
from GameObject import GameObject
from Tile import Tile
from Block import Block
from Item import Item
from Homebase import Homebase
import socket
from _thread import *
from queue import Queue
from Herotower import Herotower
import copy
import select
from singleGame import singleGame
import subprocess
import os


import urllib.request




class GamePlayer(PygameGame):
    def __init__(self):
       self.owntimecount=0
       self.lostconnectioncount=0
       self.replayfilename="replayvideo.txt"

       

       super().__init__()
       self.name="ninja"
       self.team="blue"


       self.mydata=allGameData()
 

       
      


       
       self.multiKeySet=[pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_DOWN]
       self.maininit()

    def maininit(self):
        self.cursorx=0
        self.cursory=0
        self.showinstruction=False
        pygame.mouse.set_visible(False)
        self.failedconnection=False
        self.isreplaying=False
        self.buttonleft=575
        self.buttonright=925
        self.buttonwidth=self.buttonright-self.buttonleft
        self.buttonheight=100
        self.starty=100
        self.buttonmargin=50
        self.topdownmargin=self.buttonmargin+self.buttonheight
        self.numbuttons=4
        self.buttoncolor=allGameData.white
        self.buttonrects=[]
        self.replayrect=(825,670,100,40)
        self.replaytext=allGameData.slightlargeFont.render("Replay",1,allGameData.blue)
        for i in range(self.numbuttons):
            self.buttonrects.append((self.buttonleft,
              self.starty+i*self.topdownmargin,self.buttonwidth,self.buttonheight))
        self.text1=allGameData.supersuperlargeFont.render("Create an account",1,allGameData.blue)
        self.text2=allGameData.supersuperlargeFont.render("Online Play",1,allGameData.blue)
        self.text3=allGameData.supersuperlargeFont.render("Single Computer",1,allGameData.blue)
        self.text4=allGameData.supersuperlargeFont.render("Instructions",1,allGameData.blue)
        self.text5=allGameData.largeFont.render(
          "Multi Server is not currently open or server is full or a game is going on",1,allGameData.red)
        self.text6=allGameData.largeFont.render(
          "Lost connection to server",1,allGameData.red)
        self.mode="main"

    def mainredrawAll(self,screen):

        screen.blit(allGameData.loginImg,(0,0))
        
        for i in range(self.numbuttons):
            pygame.draw.rect(screen,self.buttoncolor,self.buttonrects[i])
        pygame.draw.rect(screen,allGameData.yellow,self.replayrect)

        screen.blit(self.replaytext,(845,678))
                
        screen.blit(self.text1,(583,120))
        
        screen.blit(self.text2,(634,270))
     
        screen.blit(self.text3,(597,420))
    
        screen.blit(self.text4,(627,570))
        
        if self.showinstruction:
           screen.blit(allGameData.instructionImg,(0,50))

        screen.blit(allGameData.cursorimage,(self.cursorx,self.cursory))

        if self.failedconnection:
          screen.blit(self.text5,(300,20))
        try:
          if self.lostconnection:
             screen.blit(self.text6,(300,20))
        except:
           pass
    def accountmousepressed(self,x,y):
        if 380<=x<=680 and 220<=y<=270:
            self.isclickingusername=True
            self.isclickingpassword=False
        elif 380<=x<=680 and 470<=y<=520:
            self.isclickingusername=False
            self.isclickingpassword=True
        else:
            self.isclickingusername=False
            self.isclickingpassword=False

    def changeAccountStuff(self,mymsg):
        if mymsg.startswith("successfullyCreatedAccount"):
             self.errorindex=None
             self.issuccessful=True
        elif mymsg.startswith("usernameTaken"):
           self.errorindex=2
           self.issuccessful=False
        elif mymsg.startswith("successfullyLoggedIn"):
           self.errorindex=None
           self.roominit()
        elif mymsg.startswith("invalidLogIn"):
           self.errorindex=2

    def tryServerConnection(self):
        with urllib.request.urlopen('http://www.contrib.andrew.cmu.edu/~shengx/myip.txt') as response:
         self.HOST = response.read().decode("UTF-8")
       
        # print(self.HOST)
        for port in range(6110,6121):
          if self.connectToServer(port):
               # print("Successfully Connected, waiting for server confirmation!")
               start_new_thread(self.handleServerMsg, (self.server,))
               # self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
               # succesfullyconnected=True
               break

#islogin=True: login window     islogin=False: create account window
    def accountinit(self):
        

            


            self.accounttimecount=0
           
            self.textfont = pygame.font.SysFont("comicsansms", 30)

            self.flashing=self.textfont.render("|",1,allGameData.black)

            self.usernametext=allGameData.largeFont.render("User Name (>3 characters):",1,allGameData.red)

            self.passwordtext=allGameData.largeFont.render("Password (>3 characters):",1,allGameData.red)

            self.infotext=allGameData.largeFont.render("Press escape to go back, press return to confirm",
              1,allGameData.red)

            if self.islogin:
                self.errorindex=None
                self.firstRun=True

                self.titletext=allGameData.supersuperlargeFont.render("Login",
              1,allGameData.yellow)

                self.errortexts=[allGameData.largeFont.render("Username too short",
                  1,allGameData.red),allGameData.largeFont.render("Password too short",
                  1,allGameData.red),allGameData.largeFont.render("Wrong username or password",
                  1,allGameData.red)]                

            else:
                self.errorindex=None

                self.issuccessful=False #has successfully created an account

                self.successtext=allGameData.largeFont.render("Successfully Created Account! You can login now!",
                  1,allGameData.blue)

                self.errortexts=[allGameData.largeFont.render("Username too short",
                  1,allGameData.red),allGameData.largeFont.render("Password too short",
                  1,allGameData.red),allGameData.largeFont.render("Username already taken",
                  1,allGameData.red)]

                self.titletext=allGameData.supersuperlargeFont.render("Create Account",
              1,allGameData.yellow)

            self.textbox1=(380,220,300,50)

            self.textbox2=(380,470,300,50)

            self.accountImg=allGameData.accountImg

            self.isclickingusername=False

            self.isclickingpassword=False

            self.usernamestring=""

            self.passwordstring=""

            self.mode="account"

    def accountredrawAll(self,screen):
       usernametext=self.textfont.render(self.usernamestring,1,allGameData.black)

       passwordtext=self.textfont.render(self.passwordstring,1,allGameData.black)

       screen.blit(self.accountImg,(0,0))
       
       screen.blit(self.usernametext,(365,190))

       screen.blit(self.passwordtext,(365,440))

       pygame.draw.rect(screen,allGameData.black,self.textbox1,5)

       pygame.draw.rect(screen,allGameData.black,self.textbox2,5)

       screen.blit(usernametext,(385,220))

       screen.blit(passwordtext,(385,470))

       screen.blit(self.infotext,(300,100))

       if self.isclickingusername and (self.accounttimecount//40)%2==0:
          screen.blit(self.flashing,(380+16*len(self.usernamestring),220))
       elif self.isclickingpassword and (self.accounttimecount//40)%2==0:
          screen.blit(self.flashing,(380+16*len(self.passwordstring),470))
       
       if self.islogin:
           if self.errorindex!=None:
               screen.blit(self.errortexts[self.errorindex],(300,700))
           screen.blit(self.titletext,(430,20))

       else:
           if self.errorindex!=None:
               screen.blit(self.errortexts[self.errorindex],(300,700))
           elif self.issuccessful:
              screen.blit(self.successtext,(300,700))
           screen.blit(self.titletext,(390,20))

       screen.blit(allGameData.cursorimage,(self.cursorx,self.cursory))

    def accountTimerFired(self):
        self.accounttimecount+=1

    def keyPressed(self, keyCode, modifier):
        if self.mode=="account":
           self.accountKeyPressed(keyCode, modifier)

    def accountKeyPressed(self,keyCode, modifier):
        if keyCode==pygame.K_ESCAPE:
           self.server.send(bytes("outsidequit\n", "UTF-8"))
           self.server.shutdown(2)
           self.maininit()
        elif keyCode==pygame.K_RETURN:
           if self.islogin:
              self.attemptLogin(self.usernamestring,self.passwordstring)
           else:
              self.createAccount(self.usernamestring,self.passwordstring)
        elif keyCode==95 or keyCode==42: #the _ and * key, which we are using as delimiters, are not allowed
          pass
        elif self.isclickingusername:
           self.presskey(keyCode,"username")
        elif self.isclickingpassword:
           self.presskey(keyCode,"password")

    def attemptLogin(self,usernamestring,passwordstring):
       if len(usernamestring)<3:
          self.errorindex=0
          self.issuccessful=False
       elif len(passwordstring)<3:
          self.errorindex=1
          self.issuccessful=False
       else:
          self.server.send(bytes("attemptlogin_%s_%s\n"%(usernamestring,passwordstring), "UTF-8"))

    def createAccount(self,usernamestring,passwordstring):
       if len(usernamestring)<3:
          self.errorindex=0
          self.issuccessful=False
       elif len(passwordstring)<3:
          self.errorindex=1
          self.issuccessful=False
       else:
          self.server.send(bytes("createaccount_%s_%s\n"%(usernamestring,passwordstring), "UTF-8"))


    def presskey(self,keyCode,identifer):
        if keyCode==pygame.K_BACKSPACE:
           if identifer=="username" and len(self.usernamestring)>0:
             self.usernamestring=self.usernamestring[:-1]
           elif identifer=="password" and len(self.passwordstring)>0:
             self.passwordstring=self.passwordstring[:-1]

        elif keyCode<=127:
           if identifer=="username" and len(self.usernamestring)<=17:
              self.usernamestring+=(chr(keyCode))
           elif identifer=="password" and len(self.passwordstring)<=17:
              self.passwordstring+=(chr(keyCode))

    def mainTimerFired(self):
      try:
        if self.lostconnection:
           self.lostconnectioncount+=1
           if self.lostconnectioncount>=300:
             self.lostconnection=False
      except:
         pass

    def mainmousepressed(self,x,y):
        self.showinstruction=False #if you click anywhere else, the instruction goes away
        if self.buttonleft<=x<=self.buttonright:

            if 100<=y<=200:
                self.islogin=False
                self.tryServerConnection()   #create account
            elif 250<=y<=350:
                self.islogin=True
                self.tryServerConnection()  #login

            elif 400<=y<=500:
                game1 = singleGame()
                game1.runSinglePlayer()
                self.failedconnection=False
            elif 550<=y<=650:
                self.showinstruction=True

        if 825<=x<=925 and 670<=y<=710:
            self.replaymaterial=self.readFile(self.replayfilename)
            if len(self.replaymaterial)>0:
                 self.startReplayGame()
    
    def startReplayGame(self):
        self.isreplaying=True
        self.replaytimecount=0
        self.replaymateriallist=self.replaymaterial.splitlines() #very important
        playerteamlist,playerchrlist=[],[]
        msg,playerteamstr,playercharacterstr,playernamestr=(self.replaymateriallist[1],
          self.replaymateriallist[2],self.replaymateriallist[3],self.replaymateriallist[4])
        
        for team in playerteamstr.split("_"):
           if team=="None": team=None
           playerteamlist.append(team)
        for char in playercharacterstr.split("_"):
           if char=="None": char=None
           playerchrlist.append(char)
        self.usernameinplay=[None]*8
        playernamelist=playernamestr.split("_")
        for i in range(len(playernamelist)):
            temp=playernamelist[i]
            self.usernameinplay[i]=temp if temp!="None" else None
        msg=msg.split("_")
        mapindex=int(msg[1])
        gamemode=msg[2]
        self.mydata.initmaps(gamemode)
        self.mydata.initGameImages(playerteamlist,playerchrlist)
        actualmap=allGameData.maps[mapindex]
        numplayers=int(msg[3])
        teamstr=msg[4]
        teams=teamstr.split("*")
        teamlist=[]
        for team in teams:
            teamlist.append(team)
        self.gameinit(actualmap,gamemode,numplayers,teamlist)
        
        
        
        self.useritemlist=[None]*8
        # self.usernameinplay=["hello"]*8
        self.userlevelsinplay=[0]*8
        self.myid=int(self.replaymateriallist[0])
        goon=True
        newlineindex=5
        while goon:
           newline=self.replaymateriallist[newlineindex]
           if newline.startswith("newPlayer"):
              msg=newline.split("_")           
              (pr,pc,pn,pid,pt)=(int(msg[1]),int(msg[2]),msg[3],
              int(msg[4]),msg[5])
              try:
                item=int(msg[6])
              except:
                item=None
              newPlayer=Player(pr,pc,pn,pid,pt,item)
              self.playerGroup.add(newPlayer)
              newlineindex+=1
              
           else:
             goon=False
        self.replayloopindex=newlineindex
        self.replaymaxindex=len(self.replaymateriallist)

        self.nextreplaytime=int(self.replaymateriallist[self.replayloopindex].split("_")[0])
        print(self.nextreplaytime)
        self.mode="game"

    def findintlen(self,a):
       if a==0: 
          return 1
       else:
          num=1
          while a>10**num:
            num+=1
          return num

    def processreplayloop(self):
         previoustime=self.nextreplaytime

         while previoustime==self.nextreplaytime:
             currentcommandline=self.replaymateriallist[self.replayloopindex]

             currentcommandlist=currentcommandline.split("_")

             realcommandline=currentcommandline[self.findintlen(self.nextreplaytime)+1:]

             
             self.changeStuff(realcommandline)
             

             self.replayloopindex+=1

            

             if self.replayloopindex>=self.replaymaxindex-1: #we do not want the back to room command
               self.endreplay()
             self.nextreplaytime=int(self.replaymateriallist[self.replayloopindex].split("_")[0])
             # print(self.nextreplaytime)

    def endreplay(self):
       self.isreplaying=False
       self.replaytimecount=0
       self.nextreplaytime=0
       self.maininit()

    def readFile(self,path):
       with open(path, "rt") as f:
           return f.read()   

    def roominit(self):
        
        # succesfullyconnected=False
        # for port in range(6110,6121):
        #   if self.connectToServer(port):
               # print("Successfully Connected!")
        #        self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        #        succesfullyconnected=True
        #        break
        # if succesfullyconnected:
          self.replaytimecount=0
          self.mydata.roominit()
          self.mode="room"
          self.isReady=False
          self.gameends=False
          self.canstart=False
          self.canstartcount=0
          self.replaystring=""

          
          self.gamemodelabel=allGameData.slightlargeFont.render("Gamemodes",1,allGameData.red)
          self.gamemaplabel=allGameData.slightlargeFont.render("Gamemaps",1,allGameData.red)
          self.gobacklabel=allGameData.superlargeFont.render("Back",1,allGameData.red)
          self.unavailablelabel=allGameData.largeFont.render("Currently unavailable",1,allGameData.green)
          
          
          #each player is assigned a number when entering the room. This number
          #is used to identify the player in the room and in the game

          self.isReadyList=[False]*8
          self.otheruserinfolist=[None]*8

          if self.firstRun:
              self.playerteams=[None]*8 #the teams of players
              self.playercharacters=[None]*8
              self.useritemlist=[None]*8
              self.usernameinplay=[None]*8
              self.userlevelsinplay=[None]*8
              self.ownerID=None
              # start_new_thread(self.handleServerMsg, (self.server,))
              self.firstRun=False
              self.userhasleveledup=[None]*8
              self.lockedpositionlist=[]

          self.gamemodeWindow=False
          self.gamemapWindow=False
          self.gamesettingsWindow=False
          self.checkUserInfoWindow=False
          self.opensShop=False
          self.rankingWindow=False
          self.worldRankingInfo=None
        # else:
        #    self.failedconnection=True

    def connectToServer(self,port):
      try:    
         
         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
         self.server.connect((self.HOST,port))
         return True
      except:
        # print("failed connection: port "+str(port))
        return False

    

       

    def gameinit(self,gamemap,gamemode,numplayers,teamlist):
        self.userhasleveledup=[None]*8 #renew the user level up list
        self.numberOfPlayers=numplayers
        self.gamemode=gamemode
        self.gameends=False
        self.gamemap=gamemap  
        self.mydata.gameinit(self.gamemode,self.gamemap,True)
        self.mydata.initImages()
        self.timecount=0   #count of the server
        self.bubbleExplosionCount=8 #used to extend bubble explosion time
        self.gamemap=gamemap
        self.maxJellyCount=250

        self.isSpeaking=False
        self.speakString=""
        self.speaklist=[] # a list of all the spoken stuff 

        self.itemGroup = pygame.sprite.Group()
        self.blockGroup = pygame.sprite.Group()
        if self.gamemode in ["captureTheFlag","Hero"]:
           self.homebaseGroup = pygame.sprite.Group()
        elif self.gamemode=="treasurehunt":
           self.highestscoreplayers=[]  
           # a list of the players with the highest scoresroommousepressed 
           self.highestscore=1 # so that at first, no player has highest score

        self.teamlist=teamlist

        # blockitemString="blockItem"
        for brow in range(allGameData.Rows):
          for bcol in range(allGameData.Cols):
             blocktype=self.gamemap[brow][bcol]
             if self.gamemode=="treasurehunt":
               if blocktype>0:
                  block=Block(brow,bcol,blocktype)
                  self.blockGroup.add(block)
             elif self.gamemode=="Hero":
                if 0<blocktype<10:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                elif blocktype>=10:
                    team=teamlist[0] if blocktype==10 else teamlist[1]
                    self.homebaseGroup.add(Herotower(brow,bcol,team))   
             elif self.gamemode=="Kungfu":
                if blocktype in [1,2]:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                elif blocktype==3:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)        
             elif self.gamemode=="captureTheFlag":
                if 0<blocktype<10:
                    block=Block(brow,bcol,blocktype)
                    self.blockGroup.add(block)
                elif blocktype>=10:
                    team=teamlist[0] if blocktype==10 else teamlist[1]
                    self.homebaseGroup.add(Homebase(brow,bcol,team,self.numberOfPlayers//2))

        self.playerGroup = pygame.sprite.Group()
        self.bubbleGroup = pygame.sprite.Group() #a list of all the bubbles
        self.dartGroup = pygame.sprite.Group()


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
        
        pygame.mixer.Sound.play(allGameData.startgameSound)


    def handleServerMsg(self,server):
      server.setblocking(0)
      msg = ""
      command = ""
      while True:
          rlist,wlist,xlist=select.select([server],[],[])
          if len(rlist)>0:
            msg += server.recv(1024).decode("UTF-8")
            # print("msg:"+msg)
            command = msg.split("\n")
            while (len(command) > 1): #use a while loop here to be faster
              readyMsg = command[0]
              # print("readyMsg:"+readyMsg)
              msg = "".join(command[1:])
              # serverMsg.put(readyMsg)
              self.changeStuff(readyMsg)
              command=command[1:]

    def redrawAll(self,screen):
       if self.mode=="game":
          self.gameredrawAll(screen)
       elif self.mode=="room":
           self.roomredrawAll(screen)
       elif self.mode=="main":
          self.mainredrawAll(screen)
       elif self.mode=="account":
          self.accountredrawAll(screen)

    def mousePressed(self,x,y):
         if self.mode=="room":
            self.roommousePressed(x,y)
         elif self.mode=="main":
            self.mainmousepressed(x,y)
         elif self.mode=="account":
            self.accountmousepressed(x,y)
         elif self.mode=="game":
             pass

    def roommousePressed(self,x,y):
        # print(x,y)
        if self.opensShop:
           shopwidth=allGameData.shophorizontallines*100
           shopheight=allGameData.shopverticallines*100+allGameData.ymargin
           if (allGameData.shopx<x<allGameData.shopx+shopwidth and 
            allGameData.shopy<y<allGameData.shopy+shopheight):
               colindex=(x-allGameData.shopx)//100
               rowindex=(y-allGameData.shopy-allGameData.ymargin)//100
               itemindex=rowindex*allGameData.shophorizontallines+colindex
               self.server.send(bytes("getshopitem_%d\n"%itemindex, "UTF-8"))
           else:
              self.opensShop=False
        elif self.rankingWindow:
            self.rankingWindow=False
        else:
          if self.myid==self.ownerID: #owner specific actions
              if self.gamemodeWindow==True:
                 if 650<=x<=950 and 0<=y<=500:
                    if 0<=y<=100:
                       self.server.send(bytes("changeGameMode_captureTheFlag\n", "UTF-8"))
                    elif 100<=y<=200:
                       self.server.send(bytes("changeGameMode_Hero\n", "UTF-8"))
                    elif 200<=y<=300:
                       self.server.send(bytes("changeGameMode_Kungfu\n", "UTF-8"))
                    elif 300<=y<=400:
                       self.server.send(bytes("changeGameMode_treasurehunt\n", "UTF-8"))
                    elif 400<=y<=500:
                        self.server.send(bytes("changeGameMode_Random\n", "UTF-8"))
                 else: #if owner  clicks somewhere else then the screen disappears
                     self.gamemodeWindow=False
              elif self.gamemapWindow==True:
                  numberofmaps=allGameData.NumMaps[self.gamemode] 
                  if 650<=x<=950 and 0<=y<numberofmaps*100:
                     mapindex=y//100
                     self.server.send(bytes("changeMap_%d\n"%mapindex, "UTF-8"))
                  else:
                    self.gamemapWindow=False
                    
              else:
                  if 646<=x<=760 and 50<=y<=100:
                     self.gamemodeWindow=True
                     self.gamesettingsWindow=False
                     self.gamemapWindow=False

                  elif 646<=x<=760 and 112<=y<=162:
                     self.gamemodeWindow=False
                     self.gamesettingsWindow=True
                     self.gamemapWindow=False
                  elif 646<=x<=760 and 171<=y<=221 and self.gamemode!="Random":
                     self.gamemodeWindow=False
                     self.gamesettingsWindow=False
                     self.gamemapWindow=True
                  


          charwid,charhei=63,80
          if 650<=x<=850 and 600<=y<=700 : 
             if (self.myid==self.ownerID):
                 if self.canstart:
                    #game starts
                    self.server.send(bytes("gamestarts\n", "UTF-8"))
                    self.canstart=False
             else:
              #owner can not change ready status
           
                  msg="changeReady_%d\n"%(self.myid)
                  self.server.send(bytes(msg, "UTF-8"))

          elif 860<=x<=960 and 650<=y<=700:
              self.server.send(bytes("iquit\n", "UTF-8"))
              self.server.shutdown(2)
              self.maininit()

          if self.checkUserInfoWindow: #when the user clicks, 
          #the user info window goes away unless the owner is kicking out a user

            if (self.myid==self.ownerID and 
              self.otherplayerroomid!=self.myid and not
              (self.isReadyList[self.otherplayerroomid])):
               ydist=30
               leftx=130+(self.otherplayerroomid%4)*150+30
               upy=120+(self.otherplayerroomid//4)*420+ydist*6
               if leftx<=x<=leftx+170 and upy<=y<=upy+30:
                  self.server.send(bytes("kickoutplayer_%d\n"%(self.otherplayerroomid),
                     "UTF-8"))
               
            else:
             self.checkUserInfoWindow=False
             self.otheruserinfolist=[None]*8


          
          if not self.isReady: #once ready, a player cannot change character 
          #or color or check info of other players or check the shop
              if 880<=x<=960 and 580<=y<=630:
                self.opensShop=True
          #if the user clicked to see another user's info
              elif 240<=x<=400 and 25<=y<=50:
                 self.rankingWindow=True
                 self.server.send(bytes("wantRankingInfo\n",
                     "UTF-8"))
              if 120<=y<=280:
                 if 30<=x<=150:
                   if self.usernameinplay[0]!=None:
                      otherplayerusername=self.usernameinplay[0]
                      self.otherplayerroomid=0
                      self.checkUserInfoWindow=True
                      self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                       "UTF-8"))
                   elif (self.usernameinplay[0]==None) and (self.ownerID==self.myid):
                        self.server.send(bytes("changeRoomPositionStatus_0\n",
                     "UTF-8"))
                    
                 elif 180<=x<=300:
                  if self.usernameinplay[1]!=None:
                    otherplayerusername=self.usernameinplay[1]
                    self.otherplayerroomid=1
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[1]==None and self.ownerID==self.myid:
                     self.server.send(bytes("changeRoomPositionStatus_1\n",
                     "UTF-8"))
                 elif 330<=x<=450:
                  if self.usernameinplay[2]!=None:
                    otherplayerusername=self.usernameinplay[2]
                    self.otherplayerroomid=2
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[2]==None and self.ownerID==self.myid:
                      self.server.send(bytes("changeRoomPositionStatus_2\n",
                     "UTF-8"))
                 elif 480<=x<=600:
                  if self.usernameinplay[3]!=None:
                    otherplayerusername=self.usernameinplay[3]
                    self.otherplayerroomid=3
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[3]==None and self.ownerID==self.myid:
                      self.server.send(bytes("changeRoomPositionStatus_3\n",
                     "UTF-8"))
              elif 540<=y<=700:
                 if 30<=x<=150:
                  if self.usernameinplay[4]!=None:
                    otherplayerusername=self.usernameinplay[4]
                    self.otherplayerroomid=4
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[4]==None and self.ownerID==self.myid:
                    self.server.send(bytes("changeRoomPositionStatus_4\n",
                     "UTF-8"))
                 elif 180<=x<=300:
                  if self.usernameinplay[5]!=None:
                    otherplayerusername=self.usernameinplay[5]
                    self.otherplayerroomid=5
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[5]==None and self.ownerID==self.myid:
                    self.server.send(bytes("changeRoomPositionStatus_5\n",
                     "UTF-8"))
                 elif 330<=x<=450:
                  if self.usernameinplay[6]!=None:
                    otherplayerusername=self.usernameinplay[6]
                    self.otherplayerroomid=6
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[6]==None and self.ownerID==self.myid:
                    self.server.send(bytes("changeRoomPositionStatus_6\n",
                     "UTF-8"))
                 elif 480<=x<=600:
                  if self.usernameinplay[7]!=None:
                    otherplayerusername=self.usernameinplay[7]
                    self.otherplayerroomid=7
                    self.checkUserInfoWindow=True
                    self.server.send(bytes("wantToSeeUserInfo_%s\n"%(otherplayerusername),
                     "UTF-8"))
                  elif self.usernameinplay[7]==None and self.ownerID==self.myid:
                    self.server.send(bytes("changeRoomPositionStatus_7\n",
                     "UTF-8"))
              if 648<=x<=800 and 486<=y<=546:
                  xover=(x-648)//38
                  color=allGameData.colors[xover]
                  msg="changeColor_%d_%s\n"%(self.myid,color)
                  self.server.send(bytes(msg, "UTF-8"))
              elif 677<=x<=944 and 305<=y<=471:
                  if 677<=x<=677+charwid and 305<=y<=305+charhei:
                      self.playercharacters[self.myid]=random.choice(allGameData.characters)
                  elif 743<=x<=743+charwid and 305<=y<=305+charhei:
                     self.playercharacters[self.myid]="ninja"

                  elif 809<=x<=809+charwid and 305<=y<=305+charhei:
                     self.playercharacters[self.myid]="monkey"

                  elif 877<=x<=877+charwid and 305<=y<=305+charhei:
                     self.playercharacters[self.myid]="robot"
                  if 677<=x<=677+charwid and 394<=y<=394+charhei:
                      self.playercharacters[self.myid]="cutegirl"
                  
                  msg="changeCharacter_%d_%s\n"%(self.myid,self.playercharacters[self.myid])
                  self.server.send(bytes(msg, "UTF-8"))
         


            

    def roomredrawAll(self,screen):
            screen.blit(allGameData.roomimage,(0,0))
            try:
              gamemodelabel=allGameData.superlargeFont.render(self.gamemode,1,allGameData.green)
              screen.blit(gamemodelabel,(400,0))

              if self.gamemode!="Random" and self.mapindex!="random":
                  screen.blit(allGameData.gamemodemapdict[self.gamemode][self.mapindex],(780,30))
            except: 
               pass


            screen.blit(self.gamemodelabel,(655,65))
            screen.blit(self.gamemaplabel,(655,185))
            screen.blit(self.gobacklabel,(880,655))
            screen.blit(self.unavailablelabel,(815,500))


            shoplabel=allGameData.superlargeFont.render("Shop",1,allGameData.red)
            screen.blit(shoplabel,(880,580))
            
            rankinglabel=allGameData.largeFont.render("World Ranking",1,allGameData.yellow)
            screen.blit(rankinglabel,(250,30))
                        
            for index in range(8):
              team=self.playerteams[index]
              character=self.playercharacters[index]
              username=self.usernameinplay[index]
              userlevel=self.userlevelsinplay[index]
              leveledup=self.userhasleveledup[index]
              useritem=self.useritemlist[index]
              xpos=50+(index%4)*150
              ypos=140+(index//4)*420
              if team!=None and character!=None and username!=None: #check all to be sure
                  
                  userImg=pygame.transform.scale(pygame.image.load(
                    'images/room/%s%s.png'%(team,character)).convert_alpha(),
                    allGameData.roomcharacterscale)
                  screen.blit(userImg,(xpos,ypos))
                  player="Player %d"%(index+1)
                  playerlabel=allGameData.superlargeFont.render(player,1,allGameData.yellow)
                  usernamelabel=allGameData.largeFont.render(username,1,allGameData.green)
                  screen.blit(playerlabel,(xpos-10,ypos-40))
                  screen.blit(usernamelabel,(xpos+10,ypos+140))
                  if type(useritem)==int:
                     itemImg=allGameData.shopItemImgs[useritem]
                     dx,dy=allGameData.hatxypositions[useritem]
                     if useritem in [2,5]:
                       dx-=20
                     if useritem<6:
                       dy-=50
                     if useritem in [0,1,2]:
                       dx-=10
                     if useritem in [3,4]:
                       dx-=30
                     if useritem in [0,1]:
                       dy+=15
                     if useritem==5:
                        dy+=40
                     screen.blit(itemImg,(xpos+dx,ypos+dy))
                  userlevelImg=allGameData.levelImgs[userlevel]
                  screen.blit(userlevelImg,(xpos-15,ypos+140))
                  if leveledup:
                      leveleduplabel=allGameData.superlargeFont.render("Leveled Up!!",1,allGameData.red)
                      screen.blit(leveleduplabel,(xpos+30,ypos+140))
                  if self.ownerID==index:
                     ownerlabel=allGameData.superlargeFont.render("Owner",1,allGameData.red)
                     screen.blit(ownerlabel,(xpos-10,ypos+90))
                  if self.isReadyList[index]:
                      isreadylabel=allGameData.superlargeFont.render("Ready",1,allGameData.blue)
                      screen.blit(isreadylabel,(xpos,ypos+125))
                  if index==self.myid:
                      melabel=allGameData.superlargeFont.render("Me",1,allGameData.yellow)
                      screen.blit(melabel,(xpos+10,ypos-70))

              elif index in self.lockedpositionlist:
                screen.blit(allGameData.lockpositionImg,(xpos-10,ypos))
            try:
               if self.myid==self.ownerID:
                    start="Start" if self.canstart else "Wait"
                    startlabel=allGameData.superlargeFont.render(start,1,allGameData.black)
                    screen.blit(startlabel,(695,635))

                    if self.gamemodeWindow:

                      screen.blit(allGameData.choosegamemodeImg,allGameData.gamewindowposition)
                    elif self.gamesettingsWindow:
                      pass
                      
                    elif self.gamemapWindow:
                      numberofmaps=allGameData.NumMaps[self.gamemode] 
 #gamemode cannot be random here since if is random the gamemap window cannot be opened
                      newSurface=pygame.Surface((300,numberofmaps*100))
                      newSurface.fill(allGameData.azure)
                      # newSurface.set_colorkey(allGameData.black)
                      for mapcount in range(numberofmaps):
                         maplabel=allGameData.superlargeFont.render("Map %d"%(mapcount+1),1,allGameData.red)
                         newSurface.blit(maplabel,(100,40+mapcount*100))
                      screen.blit(newSurface,allGameData.gamewindowposition)
               else:
                    ready="Cancel" if self.isReady else "Ready"
                    readylabel=allGameData.superlargeFont.render(ready,1,allGameData.black)
                    screen.blit(readylabel,(695,635))
               colorindex=allGameData.colors.index(self.playerteams[self.myid])
               tickx,ticky=648+38*colorindex,486
               screen.blit(allGameData.tickimage,(tickx,ticky))

            except:
              pass

            if self.checkUserInfoWindow and self.otheruserinfolist[0]!=None:
              try:
               #because the server might have not sent the info yet
               xpos=130+(self.otherplayerroomid%4)*150
               ypos=120+(self.otherplayerroomid//4)*420

               newSurface=pygame.Surface((230,210))
#self.otheruserinfolist=[userid,username,win,lose,tie,experience,level,winningpercentage]
               newSurface.fill(allGameData.azure)
               usernamelabel=allGameData.largeFont.render("Username: %s"%self.otheruserinfolist[1],
                1,allGameData.black)
               worldidlabel=allGameData.largeFont.render("World id: %s"%self.otheruserinfolist[0],
                1,allGameData.black)
               levelname=allGameData.levelnames[self.otheruserinfolist[6]]
               levelImg=allGameData.levelImgs[self.otheruserinfolist[6]]
               levellabel=allGameData.largeFont.render("Level: %s"%levelname,
                1,allGameData.black)
               explabel=allGameData.largeFont.render("Total Experience: %s"%self.otheruserinfolist[5],
                1,allGameData.black)
               wtllabel=allGameData.largeFont.render("Wins:%s  Ties:%s  Loses:%s"%(
                self.otheruserinfolist[2],self.otheruserinfolist[4],self.otheruserinfolist[3]),
                1,allGameData.black)
               winningpercentagelabel=allGameData.largeFont.render("Winning Percentage: %s"%self.otheruserinfolist[7]+"%",
                1,allGameData.black)                       


               ydist=30
               newSurface.blit(usernamelabel,(0,0))
               newSurface.blit(worldidlabel,(0,ydist))
               newSurface.blit(levellabel,(0,ydist*2))
               newSurface.blit(levelImg,(190,ydist*2))
               newSurface.blit(explabel,(0,ydist*3))
               newSurface.blit(wtllabel,(0,ydist*4))
               newSurface.blit(winningpercentagelabel,(0,ydist*5))

               #only the room owner can kick out the other players who are not ready
               if (self.myid==self.ownerID and 
                self.otherplayerroomid!=self.myid and not
                (self.isReadyList[self.otherplayerroomid])):
                  kicklabel=allGameData.largeFont.render("Kick this player out",
                1,allGameData.red)
                  kickrect=30,ydist*6,170,30
                  pygame.draw.rect(newSurface,allGameData.brown,kickrect)
                  newSurface.blit(kicklabel,(30,ydist*6))

               screen.blit(newSurface,(xpos,ypos))
              except: 
                 pass
            if self.opensShop:
                
                horizontallines,verticallines=allGameData.shophorizontallines,allGameData.shopverticallines
                newSurface=pygame.Surface((100*horizontallines,100*verticallines+allGameData.ymargin))
                newSurface.fill(allGameData.azure)
                shoplabel=allGameData.supersuperlargeFont.render("Shop",1,allGameData.red)
                newSurface.blit(shoplabel,(65,0))
                for row in range(verticallines):
                   for col in range(horizontallines):
                      xpos,ypos=100*col,100*row
                      newSurface.blit(allGameData.shopItemImgs[row*horizontallines+col],(xpos,ypos+allGameData.ymargin))
                screen.blit(newSurface,(allGameData.shopx,allGameData.shopy))
   
            if self.rankingWindow:
               try:
                  boardimg=allGameData.rankingboardImg
                  startx,starty,xwid,yhei=150,220,137,35
                  allinfo=self.worldRankingInfo.split("_")
                  for i in range(len(allinfo)):
                     userinfo=allinfo[i]
                     userinfolist=userinfo.split("*")
                     for j in range(len(userinfolist)):
                         detailedinfo=userinfolist[j]
                         optionalwid=0
                         if j==2:
                           optionalwid=-45
                           levelimg=allGameData.levelImgs[int(detailedinfo)]
                           boardimg.blit(levelimg,(startx+j*xwid+optionalwid,starty+i*yhei))
                           label=allGameData.slightlargeFont.render(
                            allGameData.levelnames[int(detailedinfo)],1,allGameData.white)
                           boardimg.blit(label,(startx+j*xwid-10,starty+i*yhei))
                         else:
                           if j==0: #the username
                             detailedinfo="%s: %s"%(i+1,detailedinfo)
                             optionalwid=-15
                           elif j==1:
                             optionalwid=50
                           elif j==3:
                             optionalwid=30
                             detailedinfo+="%"
                           label=allGameData.slightlargeFont.render(detailedinfo,1,allGameData.white)
                           boardimg.blit(label,(startx+j*xwid+optionalwid,starty+i*yhei))

                     
                  screen.blit(boardimg,(100,100))
               except:
                  pass
               
            screen.blit(allGameData.cursorimage,(self.cursorx,self.cursory))


    def keepalive(self):


       try:
          sent=self.server.send(bytes("checkAlive\n", "UTF-8")) 
          if sent==0:
             raise RuntimeError("socket connection broken")
       except:
          self.lostconnection=True
          try:
            self.server.shutdown(2)
          except:
            pass
             # print("failed to shut down server")
          self.maininit()
    def roomtimerFired(self):
      #if the owner does not start the game after the users are ready, the user
      #is kicked out
        if self.canstart:
           self.canstartcount+=1
        if self.canstartcount>=allGameData.maxcanstartcount:
           self.server.send(bytes("kickoutplayer_%d\n"%(self.myid),
                       "UTF-8"))

    def timerFired(self,dt):
        self.owntimecount+=1
        if self.mode!="main" and not self.isreplaying:
            if self.owntimecount%50==0:
               self.keepalive() #always check if connected to the server
        if self.mode=="game":
          self.gametimerFired()
        elif self.mode=="room":
           self.roomtimerFired()
        elif self.mode=="main":
          self.mainTimerFired()
        elif self.mode=="account":
          self.accountTimerFired()

    def mouseMotion(self,x,y):
      if self.mode!="game":
            self.cursorx=x
            self.cursory=y


    def changeStuff(self,mymsg):
      # if (self.serverMsg.qsize() > 0):
      #     mymsg = self.serverMsg.get(False)
          # print(mymsg)
          if mymsg.startswith("serverShutDown"):
             self.lostconnection=True
             try:
                self.server.shutdown(2)
             except:
                 pass
             self.maininit()
          if self.mode=="game":
              self.changeGameStuff(mymsg)
          elif self.mode=="room":
              self.changeRoomStuff(mymsg)
          elif self.mode=="account":
              self.changeAccountStuff(mymsg)
          elif self.mode=="main":
              if mymsg.startswith("youSuccessfullyConnected"): 
                self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.accountinit()
              else:
                self.lostconnection=True
                try:
                  self.server.shutdown(2)
                except:
                   pass
                  # print("failed to shutdown server")


    def changeRoomStuff(self,msg):
        
             if msg.startswith("assignID"): 
                   msg=msg.split("_")
                   self.myid=int(msg[1])
                   self.replaystring+="%s\n"%self.myid
                   self.playercharacters[self.myid]=msg[2]
                   self.playerteams[self.myid]=msg[3]
                   isOwner=True if msg[4]=="True" else False
                   self.gamemode=msg[5]
                   self.usernameinplay[self.myid]=msg[7]
                   self.userlevelsinplay[self.myid]=int(msg[8])
                   try:
                      self.mapindex=int(msg[6])
                   except:
                      self.mapindex=msg[6]  #if the mapindex is random
                   if isOwner: self.ownerID=self.myid
                   lockedpositions=msg[9]
                   if lockedpositions!='':
                     for pos in lockedpositions.split("*"):
                        self.lockedpositionlist.append(int(pos))
             elif msg.startswith("youarekickedout"):
                  self.lostconnection=True
                  self.server.shutdown(2)
                  self.maininit()
             elif msg.startswith("worldRankingInfo"):
                  self.worldRankingInfo=msg[17:]  #17 is length of "worldRankingInfo_"+1
             elif msg.startswith("roompositionstatuschange"):
                 msg=msg.split("_")
                 posindex=int(msg[1])
                 islocked=True if msg[2]=="True" else False
                 if islocked:
                    self.lockedpositionlist.append(posindex)
                 else:
                    self.lockedpositionlist.remove(posindex)

             elif msg.startswith("getshopitem"):
                  msg=msg.split("_")
                  playerid=int(msg[1])
                  self.useritemlist[playerid]=int(msg[2])
             elif msg.startswith("newUser"):
                   msg=msg.split("_")
                   playerid=int(msg[1])
                   self.playercharacters[playerid]=msg[2]
                   self.playerteams[playerid]=msg[3]
                   isOwner=True if msg[4]=="True" else False
                   self.isReadyList[playerid]=True if msg[5]=="True" else False
                   if isOwner: self.ownerID=playerid
                   self.usernameinplay[playerid]=msg[6]
                   self.userlevelsinplay[playerid]=int(msg[7])
                   if msg[8]!="None":
                       self.useritemlist[playerid]=int(msg[8])
             elif msg.startswith("requestedUserInfo"):
                   msg=msg.split("_")                  
                   userid,username,win,lose,tie,experience,level=(int(msg[1]),
                    msg[2],int(msg[3]),int(msg[4]),int(msg[5]),int(msg[6]),
                    int(msg[7]))
                   try:
                      winningpercentage=int(win/(win+lose+tie)*100)
                   except:
                      winningpercentage=0
                   self.otheruserinfolist=[userid,username,win,lose,tie,
                   experience,level,winningpercentage]
             elif msg.startswith("playerQuitRoom"):
                  msg=msg.split("_")
                  playerid=int(msg[1])
                  self.playercharacters[playerid]=None
                  self.useritemlist[playerid]=None
                  self.playerteams[playerid]=None
                  self.isReadyList[playerid]=False
                  self.usernameinplay[playerid]=None
                  self.userlevelsinplay[playerid]=None
             elif msg.startswith("ownerChange"):
                  msg=msg.split("_")
                  self.ownerID=int(msg[1])
                  self.isReadyList[self.ownerID]=False #owner need not be ready
                  if self.ownerID==self.myid:
                     self.isReady=False

             elif msg.startswith("changeMap"):
                   msg=msg.split("_")
                   self.mapindex=int(msg[1])
             elif msg.startswith("changeColor"):
                   msg=msg.split("_")
                   playerid=int(msg[1])
                   self.playerteams[playerid]=msg[2]
             elif msg.startswith("changeCharacter"):
                   msg=msg.split("_")
                   playerid=int(msg[1])
                   self.playercharacters[playerid]=msg[2]
             elif msg.startswith("changeReady"):
                   msg=msg.split("_")
                   playerid=int(msg[1])
                   self.isReadyList[playerid]=not self.isReadyList[playerid]
                   if playerid==self.myid:
                     self.isReady=not self.isReady
             elif msg.startswith("gameCanStart"):
                  self.canstart=True
                  self.canstartcount=0
             elif msg.startswith("gameCannotStart"):
                  self.canstart=False
                  self.canstartcount=0
             elif msg.startswith("changeGameMode"):
                  msg=msg.split("_")
                  newgamemode=msg[1]
                  self.gamemode=newgamemode
             elif msg.startswith("pinning speed"):
                   self.server.send(bytes("pinning speed\n", "UTF-8"))
             elif msg.startswith("gamestarts"):
                     self.server.send(bytes("pinning speed\n", "UTF-8"))

                     self.replaystring+="%s\n"%msg
                     playerteamstr,playerchrstr,playernamestr="","",""
                     for pteam in self.playerteams:
                        playerteamstr+="%s_"%pteam
                     for pchar in self.playercharacters:
                        playerchrstr+="%s_"%pchar
                     for pname in self.usernameinplay:
                         playernamestr+="%s_"%pname
                     self.replaystring+="%s\n%s\n%s\n"%(playerteamstr[:-1],
                      playerchrstr[:-1],playernamestr[:-1])
                     msg=msg.split("_")
                     mapindex=int(msg[1])
                     gamemode=msg[2]
                     self.mydata.initmaps(gamemode)
                     self.mydata.initGameImages(self.playerteams,self.playercharacters)
                     actualmap=allGameData.maps[mapindex]
                     numplayers=int(msg[3])
                     teamstr=msg[4]
                     teams=teamstr.split("*")
                     teamlist=[]
                     for team in teams:
                        teamlist.append(team)
                     self.gameinit(actualmap,gamemode,numplayers,teamlist)


             elif msg.startswith("newPlayer"):
                        self.replaystring+="%s\n"%msg
                        msg=msg.split("_")           
                        (pr,pc,pn,pid,pt)=(int(msg[1]),int(msg[2]),msg[3],
                        int(msg[4]),msg[5])
                        try:
                          item=int(msg[6])
                        except:
                          item=None
                        newPlayer=Player(pr,pc,pn,pid,pt,item)
                        self.playerGroup.add(newPlayer)

             elif msg.startswith("gameactuallystarts"):
                self.mode="game"

   

        # self.serverMsg.task_done()
    def sendOptionalClientQuitMsg(self):
      try:
        self.server.send(bytes("iquit\n", "UTF-8"))
        self.server.shutdown(2)
      except:
         pass

    def changeGameStuff(self,mymsg):
               if not self.isreplaying:
                  self.replaystring+="%d_%s\n"%(self.replaytimecount,mymsg)
                
                # if self.gamestarts:
              #this happens most often, so put it first
               if mymsg.startswith("playerMoved"): 
                    mymsg=mymsg.split("_")
                    singleid=int(mymsg[1])
                    singleplayer=self.findPlayerWithID(singleid)
                    singleplayer.x,singleplayer.y=int(mymsg[2]),int(mymsg[3])
                    singleplayer.direction=int(mymsg[4])
                    singleplayer.walkingcount+=2
                    
               elif mymsg.startswith("timecount"):
                    mymsg=mymsg.split("_")
                    self.timecount=int(mymsg[1])
               elif mymsg.startswith("speak"):
                    mymsg=mymsg.split("_")
                    for chat in self.speaklist:
                       chat[1]-=5
                    self.speaklist.append([mymsg[1],allGameData.chatMaxY])
               elif mymsg.startswith("blockPushed"):
                    mymsg=mymsg.split("_")
                    origrow,origcol=int(mymsg[1]),int(mymsg[2])
                    drow,dcol=int(mymsg[3]),int(mymsg[4])
                    pygame.mixer.Sound.play(allGameData.pushblockSound)
                    for block in self.blockGroup:
                       if (block.row,block.col)==(origrow,origcol):
                          block.ispushed(drow,dcol)
                          break
               elif  mymsg.startswith("playerQuitGame"):
                
                  mymsg=mymsg.split("_")
                  playerid=int(mymsg[1])
                  if not self.isreplaying:
                    self.playercharacters[playerid]=None
                    self.useritemlist[playerid]=None
                    self.playerteams[playerid]=None
                    self.isReadyList[playerid]=False
                    self.usernameinplay[playerid]=None
                    self.userlevelsinplay[playerid]=None
                  for player in self.playerGroup:
                     if player.playerno==playerid:
                       self.playerGroup.remove(player)
                       break

               elif mymsg.startswith("ownerChange"):
                  if not self.isreplaying:
                    mymsg=mymsg.split("_")
                    self.ownerID=int(mymsg[1])
                    self.isReadyList[self.ownerID]=False #owner need not be ready

               elif mymsg.startswith("playerRevive"):
                    mymsg=mymsg.split("_")
                    singleid=int(mymsg[1])
                    singleplayer=self.findPlayerWithID(singleid)
                    singleplayer.isDead=False
                    singleplayer.deadCount=0
                    singleplayer.invincible=True
                    #only affects screen display, collision detection is in server
                    singleplayer.invincibleCount=0 
                    singleplayer.x,singleplayer.y=int(mymsg[2]),int(mymsg[3])
                    singleplayer.direction,singleplayer.walkingcount=0,0
                    self.playerGroup.update()
               elif mymsg.startswith("playerJelly"):
                    mymsg=mymsg.split("_")
                    jellyid=int(mymsg[1])
                    jellyplayer=self.findPlayerWithID(jellyid)
                    jellyplayer.isJelly=True
                    self.playerGroup.update()
               elif mymsg.startswith("isSaved"):
                    mymsg=mymsg.split("_")
                    jellyid=int(mymsg[1])
                    jellyplayer=self.findPlayerWithID(jellyid)
                    jellyplayer.isJelly=False
                    jellyplayer.y-=allGameData.Gridh//2
                    self.playerGroup.update()
                    pygame.mixer.Sound.play(allGameData.thankyouSound)
               elif mymsg.startswith("killCount"):
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    player=self.findPlayerWithID(playerid)
                    player.killcount+=1
                    if self.gamemode=="Kungfu":
                         player.killstreak+=1
                         if player.killstreak>=2:
                            player.streaklabel=True
                         if player.killstreak==2:
                            pygame.mixer.Sound.play(allGameData.doublekillSound)
                         elif player.killstreak==3:
                            pygame.mixer.Sound.play(allGameData.triplekillSound)
                         elif player.killstreak==4:
                            pygame.mixer.Sound.play(allGameData.dominatingSound)
                         elif player.killstreak==5:
                            pygame.mixer.Sound.play(allGameData.rampageSound)
                                
               elif mymsg.startswith("saveCount"):
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    player=self.findPlayerWithID(playerid)
                    player.savecount+=1
               elif mymsg.startswith("isKilled"):
                    pygame.mixer.Sound.play(allGameData.killSound)
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    player=self.findPlayerWithID(playerid)
                    player.isJelly=False
                    player.isDead=True
                    player.deadtimes+=1
                    player.jellyCount=0
                    player.usefulitemdict=dict() #clear all useful items
                    player.itemkeydict=dict()
                    player.itemKey=1
                    self.playerGroup.update()
                    if self.gamemode=="Kungfu":
                         player.killstreak=0
               

               elif mymsg.startswith("yShift"):
                    mymsg=mymsg.split("_")
                    jellyid=int(mymsg[1])
                    jellyplayer=self.findPlayerWithID(jellyid)
                    jellyplayer.y+=allGameData.Gridh//2
               elif mymsg.startswith("bubblePut"):
                    mymsg=mymsg.split("_")
                    givenid=int(mymsg[5])
                    if givenid==self.myid:
                        pygame.mixer.Sound.play(allGameData.bubbleSound)
                    ishidden=True if mymsg[6]=="True" else False
                    isnotshown=True if mymsg[7]=="True" else False
                    newbubble=Bubble(int(mymsg[1]),int(mymsg[2]),int(mymsg[3]),int(mymsg[4]),int(mymsg[5]),ishidden,isnotshown)
                    self.bubbleGroup.add(newbubble)
               elif mymsg.startswith("tileExplode"):
                    mymsg=mymsg.split("_")
                    mymsg=mymsg[1:]
                    for tileExpInfo in mymsg:
                        tileExpInfo=tileExpInfo.split("*")
                        tilerow,tilecol,tiledir=int(tileExpInfo[0]),int(tileExpInfo[1]),int(tileExpInfo[2])
                        for tile in self.tileGroup:
                           if (tile.row,tile.col)==(tilerow,tilecol):
                               tile.updateTile(tiledir)
               elif mymsg.startswith("tileRecover"):
                    mymsg=mymsg.split("_")
                    mymsg=mymsg[1:]
                    for tileRecoInfo in mymsg:
                        tileRecoInfo=tileRecoInfo.split("*")
                        tilerow,tilecol=int(tileRecoInfo[0]),int(tileRecoInfo[1])
                        for tile in self.tileGroup:
                           if (tile.row,tile.col)==(tilerow,tilecol):
                               tile.updateTile(0)
               elif mymsg.startswith("bubbleRemove"):
                    pygame.mixer.Sound.play(allGameData.explodeSound)
                    mymsg=mymsg.split("_")
                    mymsg=mymsg[1:]
                    for bubbleRemovInfo in mymsg:
                        bubbleRemovInfo=bubbleRemovInfo.split("*")
                        bubblerow,bubblecol,bubbleplayer=int(bubbleRemovInfo[0]),int(bubbleRemovInfo[1]),int(bubbleRemovInfo[2])
                        for bubble in self.bubbleGroup:
                           if (bubble.row,bubble.col,bubble.playerno)==(bubblerow,bubblecol,bubbleplayer):
                               self.bubbleGroup.remove(bubble)
               elif mymsg.startswith("newItem"):
                    mymsg=mymsg.split("_")
                    itemrow,itemcol,itemname=int(mymsg[1]),int(mymsg[2]),mymsg[3]
                    newItem=Item(itemrow,itemcol,itemname)
                    self.itemGroup.add(newItem)
                    #for darts,each client controls its own image positions,
                    #until dart is removed
                    #but the bubble effect is only in the server
                    if "dart" in itemname and len(itemname)>5:
                        newItem.origrow,newItem.origcol=itemrow,itemcol
                        self.dartGroup.add(newItem)
                        itemdirname=itemname[:-4]
                        newItem.dartdir=allGameData.directionList.index(itemdirname)
                        newItem.dartno=int(mymsg[4])
               elif mymsg.startswith("dartRemoved"):
                    mymsg=mymsg.split("_")
                    killeddart=int(mymsg[1])
                    for dart in self.dartGroup:
                       if dart.dartno==killeddart:
                          self.dartGroup.remove(dart)
                          self.itemGroup.remove(dart)
                          break

               elif mymsg.startswith("playerDropItem"):
                    mymsg=mymsg.split("_")
                    popItem=mymsg[1]
                    myself=self.findPlayerWithID(self.myid)
                    if popItem=="power": myself.powerItem-=1
                    elif popItem=="bubble": myself.bubbleItem-=1
                    elif popItem=="speed": myself.speedItem-=1
               elif mymsg.startswith("playerGetItem"):
                    mymsg=mymsg.split("_")
                    newItem=mymsg[1]
                    pygame.mixer.Sound.play(allGameData.itemSound)
                    myself=self.findPlayerWithID(self.myid)
                    if newItem=="power": myself.powerItem+=1
                    elif newItem=="bubble": myself.bubbleItem+=1
                    elif newItem=="speed": myself.speedItem+=1
                    elif newItem in allGameData.UsefulItems: #b/c we have already done the hero operations
                         myself.usefulitemdict[newItem]=myself.usefulitemdict.get(newItem,0)+1
                         if myself.usefulitemdict[newItem]<=1:
                           myself.itemkeydict[myself.itemKey]=newItem
                           myself.itemKey+=1
                           
                    #the one time items do not need to be known by clients. Only the server needs to know
               elif mymsg.startswith("blockExploded"):
                    mymsg=mymsg.split("_")
                    blockrow,blockcol=int(mymsg[1]),int(mymsg[2])
                    for block in self.blockGroup:
                      if (block.row,block.col)==(blockrow,blockcol):
                         self.blockGroup.remove(block)
                         break
               elif mymsg.startswith("itemRemoved"):
                    mymsg=mymsg.split("_")
                    itemrow,itemcol,itemname=int(mymsg[1]),int(mymsg[2]),mymsg[3]
                    for item in self.itemGroup:
                      if (item.row,item.col,item.chosenname)==(itemrow,itemcol,itemname):
                         self.itemGroup.remove(item)
                         break 
               elif mymsg.startswith("gameends"):
                      self.gameends=True


               elif mymsg.startswith("playerLevelUp"):
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    self.userlevelsinplay[playerid]=int(mymsg[2])
                    self.userhasleveledup[playerid]=True
               elif mymsg.startswith("playerGetExperience"):
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    player=self.findPlayerWithID(playerid)
                    player.experience=int(mymsg[2])
               elif mymsg.startswith("isWin"):
                    mymsg=mymsg.split("_")
                    playerid=int(mymsg[1])
                    player=self.findPlayerWithID(playerid)
                    if mymsg[2]=="True":  player.isWin=True
                    elif mymsg[2]=="False":  player.isWin=False
               elif mymsg.startswith("usedItem"):
                    mymsg=mymsg.split("_")
                    itemname,itemkey=mymsg[1],int(mymsg[2])
                    myself=self.findPlayerWithID(self.myid)
                    if myself.usefulitemdict[itemname]>0:
                        myself.usefulitemdict[itemname]-=1
                    if myself.usefulitemdict[itemname]==0:
                       myself.itemKey-=1
                       newitemkeydict=dict()
                       for newitemkey in myself.itemkeydict:
                          if newitemkey<itemkey:
                             newitemkeydict[newitemkey]=myself.itemkeydict[newitemkey]
                             #don't change items corresponding to smaller keys
                          elif newitemkey>=itemkey and newitemkey<len(myself.itemkeydict):
                            newitemkeydict[newitemkey]=myself.itemkeydict[newitemkey+1]
                       myself.itemkeydict=newitemkeydict
               elif mymsg.startswith("backToRoom"):
                   if not self.isreplaying:
                      self.writeFile(self.replayfilename,self.replaystring) 
                   #write the recorded details to file
                  
                   self.roominit()
               elif self.gamemode=="Kungfu":
                    if mymsg.startswith("transformcharacter"):
                        mymsg=mymsg.split("_")
                        playerid=int(mymsg[1])
                        player=self.findPlayerWithID(playerid)
                        if player.newName=="devil" and playerid==self.myid:
                           temp=copy.copy(self.multiKeySet)
                           self.multiKeySet[0],self.multiKeySet[1],self.multiKeySet[2],self.multiKeySet[3]=temp[2],temp[3],temp[0],temp[1]
                        player.transformcharacter(mymsg[2])
                        if player.newName=="gentleman":
                            if not ("dart" in player.usefulitemdict) or player.usefulitemdict["dart"]==0:
                              player.itemkeydict[player.itemKey]="dart"
                              player.itemKey+=1
                            player.usefulitemdict["dart"]=player.usefulitemdict.get("dart",0)+4
                        elif player.newName=="devil" and playerid==self.myid:
                             temp=[None]*4
                             temp[0],temp[1],temp[2],temp[3]=self.multiKeySet[2],self.multiKeySet[3],self.multiKeySet[0],self.multiKeySet[1]
                             self.multiKeySet=temp                           
                    elif mymsg.startswith("transformback"):
                        mymsg=mymsg.split("_")
                        playerid=int(mymsg[1])
                        player=self.findPlayerWithID(playerid)
                        if player.newName=="devil" and playerid==self.myid:
                           temp=copy.copy(self.multiKeySet)
                           self.multiKeySet[0],self.multiKeySet[1],self.multiKeySet[2],self.multiKeySet[3]=temp[2],temp[3],temp[0],temp[1]
                        player.transformback()
                        
                    elif mymsg.startswith("kickBubble"):
                        mymsg=mymsg.split("_")
                        origrow,origcol=int(mymsg[1]),int(mymsg[2])
                        targetrow,targetcol=int(mymsg[3]),int(mymsg[4])
                        pygame.mixer.Sound.play(allGameData.kickbubbleSound)
                        for bubble in self.bubbleGroup:
                            if (bubble.row,bubble.col)==(origrow,origcol):
                                bubble.row,bubble.col=targetrow,targetcol
                                bubble.iskicked()
                                break
                    elif mymsg.startswith("becomeInvisible"):
                        mymsg=mymsg.split("_")
                        playerid=int(mymsg[1])
                        player=self.findPlayerWithID(playerid)
                        player.becomeInvisible()
                    elif mymsg.startswith("becomeVisible"):
                        mymsg=mymsg.split("_")
                        playerid=int(mymsg[1])
                        player=self.findPlayerWithID(playerid)
                        player.becomeVisible()
               elif self.gamemode=="captureTheFlag":
                       if mymsg.startswith("dropBun"):
                                mymsg=mymsg.split("_")
                                playerid=int(mymsg[1])
                                player=self.findPlayerWithID(playerid)
                                player.hasBun=False
                                prow,pcol=player.getPlayerGrid()
                                self.itemGroup.add(Item(prow,pcol,"bun"))
                                allGameData.GridList[prow][pcol]=1

                       elif mymsg.startswith("bunChange"):
                            mymsg=mymsg.split("_")
                            bunid=int(mymsg[1])
                            bunplayer=self.findPlayerWithID(bunid)
                            bunplayer.hasBun=not bunplayer.hasBun
                       elif mymsg.startswith("hbChange"):
                            mymsg=mymsg.split("_")
                            hbteam,dx=mymsg[1],int(mymsg[2])
                            for homebase in self.homebaseGroup:
                               if homebase.team==hbteam:
                                    homebase.numbuns+=dx
               elif self.gamemode=="Hero":
                     if mymsg.startswith("drophero"):
                                mymsg=mymsg.split("_")
                                playerid=int(mymsg[1])
                                player=self.findPlayerWithID(playerid)
                                player.hashero=False
                                prow,pcol=player.getPlayerGrid()
                                self.itemGroup.add(Item(prow,pcol,"hero"))
                                allGameData.GridList[prow][pcol]=1
                     elif mymsg.startswith("buildTower"):
                          mymsg=mymsg.split("_")
                          playerid=int(mymsg[1])
                          player=self.findPlayerWithID(playerid)
                          player.hashero=False
                          for herotower in self.homebaseGroup:
                             if herotower.team==mymsg[2]:
                                herotower.numheros+=1
                     elif mymsg.startswith("towerDestroyed"):
                          mymsg=mymsg.split("_")
                          destroyedteam=mymsg[1]
                          for herotower in self.homebaseGroup:
                             if herotower.team==destroyedteam:
                                herotower.numheros-=1
                                pygame.mixer.Sound.play(allGameData.explodeSound)
                                break
                     elif mymsg.startswith("getHero"):
                            mymsg=mymsg.split("_")
                            playerid=int(mymsg[1])
                            heroPlayer=self.findPlayerWithID(playerid)
                            heroPlayer.hashero=True

                                

               elif self.gamemode=="treasurehunt":
                   if mymsg.startswith("playerGetGem"):
                      mymsg=mymsg.split("_")
                      playerid=int(mymsg[1])
                      player=self.findPlayerWithID(playerid)
                      if mymsg[2]=="red": 
                          player.redgem+=1
                      elif mymsg[2]=="yellow":
                          player.yellowgem+=1
                      elif mymsg[2]=="green":
                          player.greengem+=1
                      player.update()
                      if player.gemscore>self.highestscore:
                        self.highestscoreplayers=[player.playerno]
                        self.highestscore=player.gemscore
                      elif player.gemscore==self.highestscore:
                        self.highestscoreplayers.append(player.playerno)
                   elif mymsg.startswith("playerDropGem"):
                        mymsg=mymsg.split("_")
                        playerid=int(mymsg[1])   
                        player=self.findPlayerWithID(playerid)
                        player.redgem=0
                        player.yellowgem=0
                        player.greengem=0   
                        player.update()
                        self.highestscore,self.highestscoreplayers=self.updateScores()      


               # elif mymsg.startswith("GameStarts!"):
               #        self.gamestarts=True

               # elif mymsg.startswith("newPlayer"):
               #          mymsg=mymsg.split("_")           
               #          (pr,pc,pn,pid,pt)=(int(mymsg[1]),int(mymsg[2]),mymsg[3],
               #          int(mymsg[4]),mymsg[5])
               #          newPlayer=Player(pr,pc,pn,pid,pt)
               #          self.playerGroup.add(newPlayer)
               # elif mymsg.startswith("assignID"):
               #          mymsg=mymsg.split("_")
               #          mr,mc=int(mymsg[1]),int(mymsg[2])
               #          self.myname,self.myid,self.myteam=mymsg[3],int(mymsg[4]),mymsg[5]
               #          #this self.myid is crucial
               #          player = Player(mr,mc,self.myname,self.myid,self.myteam)
               #          self.playerGroup.add(player)



    def writeFile(self,path, contents):
       with open(path, "wt") as f:
           f.write(contents)           
              
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
        
    def gameredrawAll(self, screen):

        #all the playernos are +1 when displayed to the user, because the 
        #original playernos are 0-7 but we want to see 1-8

        one_surface=pygame.Surface((980,735))

        #Fill color to surface
        one_surface.blit(allGameData.gamewindowimage,(0,0)) #white

        #Blitting surface in to window
        screen.blit(one_surface,(0,0))


        if self.gamemode=="Kungfu":
           screen.blit(allGameData.backgroundImg,(0,0))

        for player in self.playerGroup:
              if player.playerno==self.myid:
                index=0
                for basicitem in [player.bubbleItem,player.powerItem,player.speedItem]:

                    label = allGameData.smallFont.render(str(basicitem), 1, (0,0,0))
                    screen.blit(label, (62+index*65, 697))
                    index+=1
        try:
          for player in self.playerGroup:
                if player.playerno==self.myid:
                  index=0
                  tempdict=player.itemkeydict.copy()  #thread safe
                  for key in tempdict:
                      usefulitem=tempdict[key]
                      if player.usefulitemdict[usefulitem]>0:
                        self.itemimage = allGameData.itemImgDict[usefulitem]
                        self.itemimage=pygame.transform.scale( self.itemimage.convert_alpha(),(50,50))
                        screen.blit(self.itemimage,(248+index*62,655))
                        # render text
                        label = allGameData.smallFont.render(str(player.usefulitemdict[usefulitem]), 1, (0,0,0))
                        screen.blit(label, (289+index*62, 694))
                        index+=1
                  break
        except:
            pass
            
        #this group is used only to draw (in 2.5 D)
        #visible image is Surface
        allgroup = pygame.sprite.LayeredUpdates()
        for tile in self.tileGroup:
          allgroup.add(tile) #tile has default layer 0 (lowest layer)

#the other layers are based on row. We draw from top to bottom
        for block in self.blockGroup:
          allgroup.add(block)
          allgroup.change_layer(block,block.row*10)

        
        for item in self.itemGroup:
          if item in self.itemGroup:#thread safe
            allgroup.add(item)
            allgroup.change_layer(item,item.row*10)
          
               ## print("item position: x:%d  y:%d  width:%d  height:%d"% (item.x,item.y,item.width,item.height))
        
        for bubble in self.bubbleGroup:
             allgroup.add(bubble)
             allgroup.change_layer(bubble,bubble.row*10)
        playerSameRowDict=dict()
        for player in self.playerGroup:
          if player.image!=None: #in case player is dead or in an empty block
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
                    player.bunshouldnotshow=True

        
           
              # print("player position: x:%d  y:%d  width:%d  height:%d"% (player.x,player.y,player.width,player.height))
        allgroup.draw(screen)

        if self.isSpeaking:
            myself=self.findPlayerWithID(self.myid)
            speaklabel=allGameData.largeFont.render(self.speakString, 1, myself.color)
            screen.blit(speaklabel,(allGameData.chatX,600))


        for chat in self.speaklist:
            playerid=int(chat[0][7])-1
            speakingplayer=self.findPlayerWithID(playerid)
            chatlabel=allGameData.largeFont.render(chat[0], 1, speakingplayer.color)
            screen.blit(chatlabel,(allGameData.chatX,chat[1]))

        lefttime=(allGameData.maxPlayingTime-self.timecount)//80
        if lefttime>=0:
          minute=lefttime//60
          second=lefttime-60*minute
          if second<10: second="0%d"%second
          mylabel = allGameData.superlargeFont.render("%d:%s"%(minute,second), 1, allGameData.yellow)
        else:
           mylabel = allGameData.superlargeFont.render("0:00", 1, allGameData.yellow)
        screen.blit(mylabel, (820,60))

        for player in self.playerGroup:
              if player.playerno==self.myid and not player.isDead:
                 screen.blit(allGameData.arrowimage,(player.x-17,player.y-105))
              if player.invincible and player.image!=None:
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
                      screen.blit(allGameData.heroitemImg,(player.x-27,player.y-80))

        if self.gamemode=="captureTheFlag":
          for homebase in self.homebaseGroup:
                   for bunindex in range(homebase.numbuns):
                     screen.blit(allGameData.smallbunitemImg,(homebase.x-23+12*bunindex,homebase.y-122))

        elif self.gamemode=="Hero":
          for herotower in self.homebaseGroup:
                   for heroindex in range(herotower.numheros):
                     screen.blit(allGameData.statueImg,(herotower.x-25,herotower.y-90-heroindex*20))

        # playerstr="Player %d"%(self.myid+1)
        playerstr=self.usernameinplay[self.myid]
        myself=self.findPlayerWithID(self.myid)
        playerlabel=allGameData.superlargeFont.render(playerstr,1,myself.color)
        screen.blit(playerlabel,(0,0))

        for player in self.playerGroup:
            xpos=890
            ypos=130+60*player.playerno
            playerstr=self.usernameinplay[player.playerno]
            playerlabel=allGameData.largeFont.render(playerstr,1,allGameData.yellow)
            screen.blit(playerlabel,(800,ypos+20))
            userlevel=self.userlevelsinplay[player.playerno]
            levelImg=allGameData.levelImgs[userlevel]
            screen.blit(levelImg,(780,ypos+20))
            if (player.isDead and not self.gameends) or player.isWin==False:
                cryindex=(self.owntimecount//4)%2
                playerimage=allGameData.malecryImgs[cryindex]
            else:
                playerimage=allGameData.gameImgDict[player.playerno]
            screen.blit(playerimage,(xpos,ypos))
            
            if self.gamemode=="treasurehunt":
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
        

  
        if self.gameends:
          screen.blit(allGameData.resultsimage,(100,100))
          rowindex=0
          displaytitle=["P.No","Kill","Save","Die","W\\L","Exp"]
          for index in range(len(displaytitle)): 
                self.displayLabels(screen,displaytitle[index],index*100,-50,allGameData.yellow)
          for player in self.playerGroup:
             if player.isWin==None:
                isWin="Tie"
             elif player.isWin==True:
                isWin="Win"
             elif player.isWin==False:
                isWin="Lost"
             displaylist=[player.playerno+1,player.killcount,player.savecount,player.deadtimes,isWin,player.experience]

             for index in range(len(displaylist)): 
                self.displayLabels(screen,str(displaylist[index]),index*100,rowindex*30,player.color)
             rowindex+=1  
        if self.isreplaying:
            replaylabel=allGameData.superlargeFont.render("Replaying...",1,allGameData.red)
            screen.blit(replaylabel,(300,0))



    def displayLabels(self,screen,str1,x,y,color):
        mylabel = allGameData.superlargeFont.render(str1, 1, color)
        screen.blit(mylabel,(200+x,215+y))
    
    def randomChance(self,a,b):
            b=random.randint(1,b)
            if b<=a: return True  

    def mysort(self,player):
          return player.y

    def findPlayerWithID(self,playerid):
       for player in self.playerGroup:
          if player.playerno==playerid:
              return player


    def keyReleased(self, keyCode, modifier):
        if self.mode=="game" and not self.gameends and not self.isreplaying:
                 msg=""
                 myself=self.findPlayerWithID(self.myid)
                 if self.isSpeaking:
                    if keyCode==pygame.K_BACKSPACE:
                       self.speakString=self.speakString[:-1]
                    elif keyCode==pygame.K_RETURN:
                       self.server.send(bytes("speak_%d_%s\n"%(self.myid,self.speakString), "UTF-8"))
                       self.speakString=""
                       self.isSpeaking=False
                    elif keyCode==pygame.K_ESCAPE:
                        self.speakString=""
                        self.isSpeaking=False
                    elif keyCode<=127:
                        self.speakString+=(chr(keyCode))
                        
                 elif not self.isSpeaking and keyCode==pygame.K_RETURN:
                    self.isSpeaking=True

                 elif (not myself.isDead) :
              
                 
                     if keyCode==pygame.K_1 and myself.itemKey>1:
                         msg+="key1"
                     elif keyCode==pygame.K_2 and myself.itemKey>2:
                         msg+="key2"
                     elif keyCode==pygame.K_3 and myself.itemKey>3:
                         msg+="key3"
                     elif keyCode==pygame.K_4 and myself.itemKey>4:
                         msg+="key4"
                     elif keyCode==pygame.K_5 and myself.itemKey>5:
                         msg+="key5"
                     elif keyCode==pygame.K_6 and myself.itemKey>6:
                         msg+="key6"
                     elif self.gamemode=="Kungfu" and keyCode==pygame.K_t:
                         myself=self.findPlayerWithID(self.myid)
                         if myself.newName=="pudding":
                             msg+="becomeInvisible"
                         elif myself.newName=="transparentpudding":
                             msg+="becomeVisible"
                     if keyCode==pygame.K_r:
                         msg+="endgame"

                     msg+="\n"
                     self.server.send(bytes(msg, "UTF-8"))


    def gametimerFired(self):
          
          self.replaytimecount+=1 #used to record time
          # print("current time:%d"%self.replaytimecount)
          if self.isreplaying:
            if self.replaytimecount==self.nextreplaytime:
                 self.processreplayloop()


          if not self.gameends:

            if not self.isSpeaking:
                msg=""
                myself=self.findPlayerWithID(self.myid)
                if self.isKeyPressed(pygame.K_SPACE):
                    msg += "space " 
                    # print("sending: ", msg, end="")
                    
                if myself.direction in [0,3]:
        #if the player is moving up or down originally, 
                 #the left and right keys can influence his direction
                    if self.isKeyPressed(self.multiKeySet[1]):
                        msg += "right " 
                        # print("sending: ", msg, end="")
                        
                    elif self.isKeyPressed(self.multiKeySet[0]):
                        msg += "left " 
                        # print("sending: ", msg, end="")
                        
                    elif self.isKeyPressed(self.multiKeySet[2]):
                        msg += "up " 
                        # print("sending: ", msg, end="")
                        
                    elif self.isKeyPressed(self.multiKeySet[3]):
                        msg += "down " 
                        # print("sending: ", msg, end="")
                    msg+="\n"
                    if not self.isreplaying:
                      self.server.send(bytes(msg, "UTF-8"))

                else:#if the player is moving left or right originally, 
                 #the up and down keys can influence his direction
                    if self.isKeyPressed(self.multiKeySet[2]):
                        msg += "up " 
                        # print("sending: ", msg, end="")
                        
                    elif self.isKeyPressed(self.multiKeySet[3]):
                        msg += "down " 
                        # print("sending: ", msg, end="")

                    elif self.isKeyPressed(self.multiKeySet[1]):
                        msg += "right " 
                        # print("sending: ", msg, end="")
                        
                    elif self.isKeyPressed(self.multiKeySet[0]):
                        msg += "left " 
                        # print("sending: ", msg, end="")
                        
                    msg+="\n"
                    if not self.isreplaying:
                      self.server.send(bytes(msg, "UTF-8"))
             

            for bubble in self.bubbleGroup:
                bubble.bubbleChangeForm()
                bubble.timetillexp-=2
            for player in self.playerGroup:
              if player.isJelly:  player.jellyCount+=2
              if player.isDead: player.deadCount+=2
            self.playerGroup.update()

            for dart in self.dartGroup:
                dart.dartMove(int(allGameData.dartSpeed*1.5))
            
            for chat in self.speaklist:
                chat[1]-=1
                if chat[1]<allGameData.chatMinY:
                   self.speaklist.remove(chat)


        

def main():
    game1 = GamePlayer()
    game1.run()


if __name__ == '__main__':
    main()
