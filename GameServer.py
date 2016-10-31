       
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
import socket
from _thread import *
from queue import Queue
from Herotower import Herotower
import copy
import select
import re
import os
import pexpect
import time


class GameServer(PygameGame):


    def __init__(self):
            super().__init__()
            self.mydata=allGameData()
            self.firstRun=True
            self.serverhasshutdown=False # if the server has shut down
            self.outsideclients=dict()   #is a dict of all the clients wanting to create accounts or log in
            self.outsideclientid=0  #id of outsideclients
            self.usernamesinplay=[None]*8  #list of the users in the game, indexed by playerid
            self.userlevelsinplay=[None]*8
            self.filename="userinfo.txt"
            self.databaseinfo=["userid","username","password","win","lose","tie","experience","level"]
            self.roominit()
            self.initSocket()


    def roominit(self):
        self.mydata.roominit()
        self.mode="room"
        self.gameCanStart=False

        self.gameends=False #double make sure
        pygame.mouse.set_visible(False)
        

        self.roomtimecount=0


    #call game-specific initialization


        self.isReadyList=[False]*8

        self.userspincount=[0]*8
        self.userpinstarttime=[None]*8
        self.userpinendtime=[None]*8
        self.numberofpinchecks=allGameData.numberofpinchecks

        if self.firstRun:
            self.playernolist=[0,1,2,3,4,5,6,7]  #possible player numbers
        #each player is assigned a number when entering the room. This number
        #is used to identify the player in the room and in the game
            self.playerteams=[None]*8 #the teams of players
            self.playercharacters=[None]*8
            self.useritemlist=[None]*8
            self.firstRun=False
            self.gamemode="Random"
            self.currID = None
            self.ownerID=None 
            self.lockedpositionlist=[]
            self.mapindex="random"



    def timerFired(self,dt):
        if self.mode=="game":
          self.gametimerFired()
        elif self.mode=="room":
          self.roomtimerFired()
        elif self.mode=="main":
          pass
    def roomtimerFired(self):
        self.roomtimecount+=1

        if self.roomtimecount%50==0:
            self.keepalive()


    def keepalive(self):
        temp=copy.copy(self.clientele)
        for cID in temp:
               try:
                  sent=temp[cID].send(bytes("checkAlive\n", "UTF-8")) 
                  if sent==0:
                     raise RuntimeError("socket connection broken")
               except:
                  self.sendPlayerQuitRoomInfo(cID)

        temp1=copy.copy(self.outsideclients)
        for cID in temp1:
               outsideclient=temp1[cID]
               try:
                  sent=outsideclient.send(bytes("checkAlive\n", "UTF-8")) 
                  if sent==0:
                     raise RuntimeError("socket connection broken")
               except:
                  del self.outsideclients[cID]


    def checkCanStart(self):
         everyoneisready=True
         for index in range(8):
           if self.playerteams[index]!=None: 
             if self.isReadyList[index]==False and index!=self.ownerID:
                 everyoneisready=False
                 # (index)print
                 break
         if everyoneisready:
             teamdict=dict()
             # print("A")
             for team in self.playerteams:
               if team!=None:
                if not (team in teamdict):
                  teamdict[team]=1
                else:
                  teamdict[team]+=1
             # print(teamdict)
             if 2<=len(teamdict)<=allGameData.gamemodemaxteams[self.gamemode]:
               if self.gamemode in ["captureTheFlag","Hero","Random"]:
                  # print(self.gamemode)
                  if len(teamdict)==2:
                    teamcount=None
                    for team in teamdict:
                       if teamcount==None:
                          teamcount=teamdict[team]
                       else:
                         if teamdict[team]==teamcount:  #the number of players in the two teams are equal
                            return True
                            

               else:
                  return True

                 


    def sendGameCanStartInfo(self):
        temp=copy.copy(self.clientele)
        for cID in temp:
             if cID==self.ownerID:
               try:
                  temp[cID].send(bytes("gameCanStart\n", "UTF-8")) 
               except:
                  self.sendPlayerQuitRoomInfo(cID)

    def sendGameCannotStartInfo(self):
        temp=copy.copy(self.clientele)
        for cID in temp:
             if cID==self.ownerID:
               try:
                  temp[cID].send(bytes("gameCannotStart\n", "UTF-8")) 
               except:
                  self.sendPlayerQuitRoomInfo(cID)

       
    def sendPlayerQuitRoomInfo(self,pid):
      if pid in self.clientele: #thread safe
         del self.clientele[pid]
         # print(self.playernolist)
         self.playernolist.append(pid)
         self.playercharacters[pid]=None
         self.usernamesinplay[pid]=None
         self.useritemlist[pid]=None
         self.userlevelsinplay[pid]=None
         self.playerteams[pid]=None
         self.isReadyList[pid]=False
         if len(self.clientele)>0:

            if pid==self.ownerID:
               self.ownerID=random.choice(list(self.clientele.keys())) 
               self.isReadyList[self.ownerID]=False
               #choose a random user from the remaining users to be the new owner of the room
               temp=copy.copy(self.clientele)
               for cID in temp:
                   temp[cID].send(bytes("ownerChange_%d\n"%(self.ownerID), "UTF-8")) 
            temp=copy.copy(self.clientele)
            for cID in temp:
                 temp[cID].send(bytes("playerQuitRoom_%d\n"%pid, "UTF-8")) 
         else:
           self.firstRun=True

    def sendOptionalClientQuitMsg(self):
        temp=copy.copy(self.clientele)
        self.serverhasshutdown=True
        for cID in temp:
               try:
                  sent=temp[cID].send(bytes("serverShutDown\n", "UTF-8")) 
                  if sent==0:
                     raise RuntimeError("socket connection broken")
               except:
                  self.sendPlayerQuitRoomInfo(cID)

        temp1=copy.copy(self.outsideclients)
        for cID in temp1:
               outsideclient=temp1[cID]
               try:
                  sent=outsideclient.send(bytes("serverShutDown\n", "UTF-8")) 
                  if sent==0:
                     raise RuntimeError("socket connection broken")
               except:
                  del self.outsideclients[cID]

    def sendPlayerQuitGameInfo(self,pid):
      if pid in self.clientele: #thread safe
         del self.clientele[pid]
         # print(self.playernolist)
         self.playernolist.append(pid)
         self.playercharacters[pid]=None
         self.usernamesinplay[pid]=None
         self.useritemlist[pid]=None
         self.userlevelsinplay[pid]=None
         self.playerteams[pid]=None
         self.isReadyList[pid]=False

         for player in self.playerGroup:
           if player.playerno==pid:
             self.allteamsdict[player.team]=self.allteamsdict[player.team]-1
             self.playerGroup.remove(player)
             if self.allteamsdict[player.team]<=0:
                del self.allteamsdict[player.team]
             break

         if len(self.clientele)>0:

            if pid==self.ownerID:
               self.ownerID=random.choice(list(self.clientele.keys())) 
               self.isReadyList[self.ownerID]=False
               #choose a random user from the remaining users to be the new owner of the room
               temp=copy.copy(self.clientele)
               for cID in temp:
                #the future owner of the room changes even while in game
                   temp[cID].send(bytes("ownerChange_%d\n"%(self.ownerID), "UTF-8")) 
            temp=copy.copy(self.clientele)
            for cID in temp:
                 temp[cID].send(bytes("playerQuitGame_%d\n"%pid, "UTF-8")) 
         else:
           self.firstRun=True
           self.roominit()

         if len(self.allteamsdict)==1: #all the players in the remaining team wins
            self.gameends=True
            for player in self.playerGroup: 
               player.isWin=True
            self.sendGameEndInfo()


    # def mousePressed(self,x,y):
    #      pass
    # def mouseMotion(self,x,y):
    #    pass
  #GridList:
    #can get in : 0: empty tile
    #             1:item
    
    #: can't get in:
    #             2: blocks
    #             3: bubble
    #             4: homebase 
    def connectToServer(self,port):
        try:    
           
           self.server.bind((self.HOST,port))
           return True
        except:
          # print("failed connection: port "+str(port))
          return False

  #change self.HOST to '' here if your andrew id and password are not working
    def initSocket(self):
        BACKLOG = 100

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.HOST = socket.gethostbyname(socket.gethostname())


        self.writeFile("myip.txt",self.HOST)


        try:
            mypassword  = self.readFile("mypassword.txt")
            myandrewid  = self.readFile("myandrewid.txt")
            mycommand = "scp myip.txt  %s@unix.andrew.cmu.edu:www/"%myandrewid
            #make sure in the above command that username and hostname are according to your server
            child = pexpect.spawn(mycommand)
            successindex= child.expect(["%s@unix.andrew.cmu.edu's password:"%myandrewid, pexpect.EOF])
            # print(successindex)
            if successindex==0: # send password                
                   child.sendline(mypassword)
                   child.expect(pexpect.EOF)

        except: 
          pass
           # print("failed")
        
        # subprocess.call(["scp","Desktop/tp/myip.txt","shengx@unix.andrew.cmu.edu:www/"])

        # print("succeeded")

        for port in range(6110,6121):
          if self.connectToServer(port):
               # print("Successfully Connected! Port: "+str(port))
               self.server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
               self.server.listen(BACKLOG)
               # print("looking for connection")
               break
       
       

        self.clientele = {}


        self.serverChannel = Queue(100)
        start_new_thread(self.serverThread,())
        start_new_thread(self.waitThread,())

 
    
    def waitThread(self):
       #only accept clients when a game is not going on 
        while self.mode!="game" and not self.serverhasshutdown: 
          client, address = self.server.accept()
          if not self.serverhasshutdown:
              client.send(bytes("youSuccessfullyConnected\n", "UTF-8"))
              self.outsideclients[self.outsideclientid]=client         
              start_new_thread(self.handleclient, (client,self.outsideclientid))
              self.outsideclientid+=1
              # print("# outside clients: %d   newoutsideclientid: %d"%(len(self.outsideclients),self.outsideclientid))
        
        # print("wait thread exitted")

#starts with handling clients that wish to join the room (logging in,creating accounts, etc.)
#then change userid as user goes in the room, also handles in game stuff
    def handleclient(self,client,cID):
              client.setblocking(0)
              msg = ""
              goon=True
              isinroom=False
              userid=cID

              while goon:
                    rlist,wlist,xlist=select.select([client],[],[])
                    if len(rlist)>0:
                      try:
                          msg += client.recv(512).decode("UTF-8")                
                          command = msg.split("\n")
                          while (len(command) > 1):
                            readyMsg = command[0]
                            msg = "".join(command[1:])

                            if isinroom:
                              self.serverChannel.put("%d_%s"%(userid,readyMsg)) 

                            elif (not isinroom) and (userid in self.outsideclients): 

                                self.serverChannel.put("%d_%s"%(userid,readyMsg)) 

                  #change to room mode, will only enter this statement once 
                            elif (not isinroom): 
                                isinroom=True
                                temp=copy.copy(self.clientele)
                                for otherid in temp:
                                  if temp[otherid]==client:
                                     userid=otherid
                                     self.serverChannel.put("%d_%s"%(userid,readyMsg)) 
                                     break 
                                # print("old id: %d  new id: %d"%(cID,userid))
                           

                            command=command[1:]
                      except:
                        goon=False

              # print("client exitted %d %s"%(userid,isinroom))


    def newRoomPlayer(self,client,username,userlevel):
       # if len(self.playernolist)>0 and self.mode=="room":
          self.currID = random.choice(self.playernolist)
          self.playernolist.remove(self.currID)
          isOwner=False
          defaultcharacter=random.choice(allGameData.characters)
          defaultteam=random.choice(allGameData.colors)
          if len(self.clientele)==0:
             isOwner=True
             self.ownerID=self.currID  
          #the first entering player initially becomes the owner of the room
          # print("New player: "+str(self.currID))
          self.playercharacters[self.currID]=defaultcharacter
          self.playerteams[self.currID]=defaultteam
          self.usernamesinplay[self.currID]=username
          self.userlevelsinplay[self.currID]=userlevel
          lockedposstr=""
          # print(self.lockedpositionlist)
          for lockedposition in self.lockedpositionlist:
             lockedposstr+="%d*"%lockedposition
          lockedposstr=lockedposstr[:-1]
          client.send(bytes("assignID_%d_%s_%s_%s_%s_%s_%s_%d_%s\n"%(self.currID,
            defaultcharacter,defaultteam,isOwner,self.gamemode,self.mapindex,
            username,userlevel,lockedposstr), "UTF-8"))
          temp=copy.copy(self.clientele)
          for cID in temp:
              try:
                 temp[cID].send(bytes("newUser_%d_%s_%s_%s_%s_%s_%d_%s\n"%(
                self.currID,defaultcharacter,defaultteam,isOwner,
                self.isReadyList[self.currID],username,userlevel,
                self.useritemlist[self.currID]), "UTF-8"))
              except:
                  self.sendPlayerQuitRoomInfo(cID)
              #send existing player info to new player
              clientIsOwner=True if cID==self.ownerID else False
              client.send(bytes("newUser_%d_%s_%s_%s_%s_%s_%d_%s\n"%(cID,
                self.playercharacters[cID],self.playerteams[cID],clientIsOwner,
                self.isReadyList[cID],self.usernamesinplay[cID],
                self.userlevelsinplay[cID],self.useritemlist[cID]), "UTF-8"))

          self.clientele[self.currID] = client
          # print("connection received")
          # start_new_thread(self.handleClient, (client,self.currID))

        # print("Wait Thread Exitted!!!")




    def findPlayerWithID(self,playerid):
       for player in self.playerGroup:
          if player.playerno==playerid:
              return player




    def serverThread(self):
          while True:
            
              msg = self.serverChannel.get(True, None)
              # print("msg recv: ", msg)
              temp=msg.split("_")
              removelen=len(temp[0])+1
              senderID = int(temp[0])
              mymsg=msg[removelen:]
              # print(msg)
              if (mymsg):
                  

                  # print(msg)
                  if self.mode=="room":
                     self.roomserverThread(senderID,mymsg)
                  elif self.mode=="game":
                     self.gameserverThread(senderID,mymsg)


                  self.serverChannel.task_done()
    
    def readFile(self,path):
       with open(path, "rt") as f:
           return f.read()

    
    def writeFile(self,path, contents):
       with open(path, "wt") as f:
           f.write(contents)


#update a piece of an user's info (that is in int), the piece to update is given 
#by identifier string and how much to update is given by update amount
    def updateUserStuff(self,playerusername,identifierstring,updateamount):
        contents=self.readFile(self.filename)
        usernameindex=self.databaseinfo.index("username")
        indextoupdate=self.databaseinfo.index(identifierstring)
        # useridindex=self.databaseinfo.index("userid")
        newlevel=None
        origlevel=None
        contenttowrite=""

        for usercontent in contents.splitlines():
          
              userlist=usercontent.split("_")
              #we have found the right player
              if playerusername==userlist[usernameindex]:
                 originalAmount=int(userlist[indextoupdate])
                 originalAmount+=updateamount

                 if identifierstring=="experience":
                    levelindex=self.databaseinfo.index("level")
                    origlevel=int(userlist[levelindex])
                    newlevel=self.checkUserLevel(originalAmount,origlevel)
                    if newlevel!=None:                                     
                           previousdelimiter=[m.start() for m in re.finditer(r"_",usercontent)][levelindex-1]
                           nextdelimiter=[m.start() for m in re.finditer(r"_",usercontent)][levelindex]
                           temp=usercontent[:previousdelimiter+1]+str(newlevel)+usercontent[nextdelimiter:]
                           usercontent=temp
                           
                 
                 previousdelimiter=[m.start() for m in re.finditer(r"_",usercontent)][indextoupdate-1]
                 nextdelimiter=[m.start() for m in re.finditer(r"_",usercontent)][indextoupdate]

                 temp=usercontent[:previousdelimiter+1]+str(originalAmount)+usercontent[nextdelimiter:]

                 usercontent=temp

              
              contenttowrite+=usercontent+"\n" #add the content to the new string

        self.writeFile(self.filename,contenttowrite)

        if newlevel!=origlevel:
          return newlevel


 #need only start checking from the user's original level to see if he has leveled up
    def checkUserLevel(self,originalAmount,origlevel):
        possibleLevels=allGameData.levelexperiences[origlevel:]
        maxlevel=len(allGameData.levelexperiences)-1
        for level in range(len(possibleLevels)):
           actuallevel=level+origlevel
           if actuallevel<maxlevel:  #not on the max level
              nextlevelexp=allGameData.levelexperiences[actuallevel+1]
              if originalAmount<nextlevelexp: #check the top bound first for efficiency
                 thislevelexp=allGameData.levelexperiences[actuallevel]
                 if thislevelexp<=originalAmount:
                    return actuallevel

    def ranksort(self,userinfostring):
       experienceindex=self.databaseinfo.index("experience")
       userlist=userinfostring.split("_")
       return -int(userlist[experienceindex]) #use negative because we sort from 
       #high to low


    def sendWorldRankingInfo(self,senderID):
        contents=self.readFile(self.filename)
        usernameindex=self.databaseinfo.index("username")
        experienceindex=self.databaseinfo.index("experience")
        winindex=self.databaseinfo.index("win")
        tieindex=self.databaseinfo.index("tie")
        loseindex=self.databaseinfo.index("lose")
        levelindex=self.databaseinfo.index("level")


        contenttosend=""
        sorteduserlist=sorted(contents.splitlines(),key=self.ranksort) 

        for i in range(allGameData.numplayersonranking):
           userinfostring=sorteduserlist[i]
           userinfolist=userinfostring.split("_")
           win,lose,tie=(int(userinfolist[winindex]),int(userinfolist[loseindex]),
            int(userinfolist[tieindex]))
           # print(win,lose,tie)
           try:
              winratio=int(win/(win+lose+tie)*100)
           except:
              winratio=0 #if 0 games are played
           userlevel,username,userexp=(userinfolist[levelindex],
            userinfolist[usernameindex],userinfolist[experienceindex])
           contenttosend+="%s*%s*%s*%d_"%(username,userexp,userlevel,winratio)
        contenttosend=contenttosend[:-1]
        # print(contenttosend)
        self.clientele[senderID].send(bytes("worldRankingInfo_%s\n"%(contenttosend), "UTF-8"))

    def findUserLevel(self,playerusername):   
        contents=self.readFile(self.filename)
        usernameindex=self.databaseinfo.index("username")
        levelindex=self.databaseinfo.index("level")

        for usercontent in contents.splitlines():
          
              userlist=usercontent.split("_")
              #we have found the right player
              if playerusername==userlist[usernameindex]:
                    playerlevel=int(userlist[levelindex])
                    return playerlevel      

    def returnUserAllInfo(self,usernametocheck):     
        contents=self.readFile(self.filename)
        (idindex,nameindex,winindex,loseindex,tieindex,
          experienceindex,levelindex)=(self.databaseinfo.index("userid"),
          self.databaseinfo.index("username"),
          self.databaseinfo.index("win"),self.databaseinfo.index("lose"),
          self.databaseinfo.index("tie"),self.databaseinfo.index("experience"),
          self.databaseinfo.index("level"))

        for usercontent in contents.splitlines():
          
              userlist=usercontent.split("_")
              #we have found the right player
              if usernametocheck==userlist[nameindex]:
                 return (userlist[idindex],userlist[nameindex],
                  userlist[winindex],userlist[loseindex],
                  userlist[tieindex],userlist[experienceindex],userlist[levelindex])

#returns False if a username is in the database, else True
    def usernameIsValid(self,newusername):
        contents=self.readFile(self.filename)   
        usernameset=set()
        usernameindex=self.databaseinfo.index("username")
        for usercontent in contents.splitlines():
           
             usercontent=usercontent.split("_")
             usernameset.add(usercontent[usernameindex])

        if newusername in usernameset:
           return False
        else:
           return True
    def loginValid(self,myusername,mypassword):
        if myusername in self.usernamesinplay:
           return False #one user cannot log in twice

        contents=self.readFile(self.filename)       
        usernamelist=[]
        usernameindex=self.databaseinfo.index("username")
        passwordindex=self.databaseinfo.index("password")

        contentlist=contents.splitlines()
        for usercontent in contentlist:
           usercontent=usercontent.split("_")
           usernamelist.append(usercontent[usernameindex])

        if myusername in usernamelist:
           myuserid=usernamelist.index(myusername)
           myinfo=contentlist[myuserid]
           myinfo=myinfo.split("_")
           return myinfo[passwordindex]==mypassword

        else:
           return False # the username does not exist

    def createNewUser(self,username,password):
        originalcontents=self.readFile(self.filename)
        numberofusers=len(originalcontents.splitlines())
        newcontent="%s_%s_%s_0_0_0_0_0_\n"%(numberofusers,username,password)

        contenttowrite=originalcontents+newcontent

        self.writeFile(self.filename,contenttowrite)


    def roomserverThread(self,senderID,msg):
         # print("length of outside clients: "+ str(len(self.outsideclients)))
         if msg.startswith("changeColor"): 
            msg=msg.split("_")
            playerid=int(msg[1])
            self.playerteams[playerid]=msg[2]
            temp=copy.copy(self.clientele) #thread safe
            for cID in temp:
              try:
               temp[cID].send(bytes("changeColor_%d_%s\n"%(playerid,msg[2]), "UTF-8")) 
                 # self.mysend("changeColor_%d_%s\n"%(playerid,msg[2]),self.clientele[cID])
              except:
                 self.sendPlayerQuitRoomInfo(cID)


            if self.checkCanStart():
               self.sendGameCanStartInfo()
            else:
               self.sendGameCannotStartInfo()
         elif msg.startswith("iquit"):
             self.sendPlayerQuitRoomInfo(senderID)
         elif msg.startswith("wantRankingInfo"):
             self.sendWorldRankingInfo(senderID)
         elif msg.startswith("changeRoomPositionStatus"):
             msg=msg.split("_")
             posindex=int(msg[1])
             islocked=None
             if posindex in self.playernolist:
                 self.playernolist.remove(posindex)
                 self.lockedpositionlist.append(posindex)
                 islocked=True
                            
             else:
                 self.playernolist.append(posindex)
                 self.lockedpositionlist.remove(posindex)
                 islocked=False
             temp=copy.copy(self.clientele)
             for cID in temp:
               try:
                 temp[cID].send(bytes("roompositionstatuschange_%d_%s\n"%(posindex,islocked), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
         elif msg.startswith("getshopitem"):
             msg=msg.split("_")
             itemindex=int(msg[1])
             self.useritemlist[senderID]=itemindex
             temp=copy.copy(self.clientele)
             for cID in temp:
               try:
                 temp[cID].send(bytes("getshopitem_%d_%d\n"%(senderID,itemindex), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
         elif msg.startswith("kickoutplayer"):
             msg=msg.split("_")
             kickedoutid=int(msg[1])
             self.clientele[kickedoutid].send(bytes("youarekickedout\n", "UTF-8"))
             self.sendPlayerQuitRoomInfo(kickedoutid)

         elif msg.startswith("wantToSeeUserInfo"):
             msg=msg.split("_")
             usernametocheck=msg[1]
             userid,username,win,lose,tie,experience,level=self.returnUserAllInfo(usernametocheck)
             self.clientele[senderID].send(bytes(
              "requestedUserInfo_%s_%s_%s_%s_%s_%s_%s\n"%(userid,username,
                win,lose,tie,experience,level), "UTF-8"))
         elif msg.startswith("outsidequit"):
             del self.outsideclients[senderID]
         elif msg.startswith("attemptlogin"):
             msg=msg.split("_")
             username,password=msg[1],msg[2]
             if self.loginValid(username,password) and len(self.playernolist)>0: 
             #check if there are empty positions in the room
                self.outsideclients[senderID].send(bytes("successfullyLoggedIn\n", "UTF-8"))  
                userlevel=self.findUserLevel(username)           
                self.newRoomPlayer(self.outsideclients[senderID],username,userlevel)
                del self.outsideclients[senderID]
             else:
              try:
                self.outsideclients[senderID].send(bytes("invalidLogIn\n", "UTF-8"))     
              except:
                 pass
         elif msg.startswith("createaccount"):
             msg=msg.split("_")
             username,password=msg[1],msg[2]
             if self.usernameIsValid(username):
                self.createNewUser(username,password)
                self.outsideclients[senderID].send(bytes("successfullyCreatedAccount\n", "UTF-8"))
             else:
                self.outsideclients[senderID].send(bytes("usernameTaken\n", "UTF-8"))
         elif msg.startswith("changeGameMode"):
             msg=msg.split("_")
             newgamemode=msg[1]
             self.gamemode=newgamemode
             self.mapindex="random" #the map becomes random when a new gamemode is chosen
             temp1=copy.copy(self.clientele)
             for cID in temp1:
               try:

                 temp1[cID].send(bytes("changeGameMode_%s\n"%(self.gamemode), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
             if self.checkCanStart():
               self.sendGameCanStartInfo()
             else:
               self.sendGameCannotStartInfo()
         elif msg.startswith("changeMap"):

             msg=msg.split("_")
             self.mapindex=int(msg[1])
             temp2=copy.copy(self.clientele)
             for cID in temp2:
               try:

                 temp2[cID].send(bytes("changeMap_%d\n"%(self.mapindex), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
         elif msg.startswith("changeCharacter"): 
            msg=msg.split("_")
            playerid=int(msg[1])
            self.playercharacters[playerid]=msg[2]
            temp=copy.copy(self.clientele)
            for cID in temp:

               try:
                 temp[cID].send(bytes("changeCharacter_%d_%s\n"%(playerid,msg[2]), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID) 
            if self.checkCanStart():
               self.sendGameCanStartInfo()
            else:
               self.sendGameCannotStartInfo()
         elif msg.startswith("changeReady"):
             msg=msg.split("_")
             playerid=int(msg[1])
             self.isReadyList[playerid]=not self.isReadyList[playerid]
             temp=copy.copy(self.clientele)
             for cID in temp:
               try:

                 
                 temp[cID].send(bytes("changeReady_%d\n"%(playerid), "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
             if self.checkCanStart():
               self.sendGameCanStartInfo()
             else:
               self.sendGameCannotStartInfo()
         elif msg.startswith("pinning speed"):
           if self.userspincount[senderID]<self.numberofpinchecks:
              try:
                 self.clientele[senderID].send(bytes("pinning speed\n", "UTF-8"))
                 self.userspincount[senderID]+=1
              except:
                 self.sendPlayerQuitRoomInfo(senderID)

           elif self.userspincount[senderID]==self.numberofpinchecks:
               self.userpinendtime[senderID]=self.roomtimecount
               if self.userspincount.count(self.numberofpinchecks)==self.numberOfPlayers:
                  self.userLagTime=dict()
                  for userid in self.clientele:
                     starttime=self.userpinstarttime[userid]
                     endtime=self.userpinendtime[userid]
                     try:
                         if starttime!=None and endtime!=None: #thread safe
                           endtime=self.userpinendtime[userid]
                           self.userLagTime[userid]=endtime-starttime
                     except:
                         pass
                  self.gameactuallystarts()

         elif msg.startswith("gamestarts"):
           if self.checkCanStart(): #double check, thread safe
             if self.gamemode=="Random":
                self.gamemode=random.choice(allGameData.gamemodes)
             self.mydata.initmaps(self.gamemode)
             if self.mapindex=="random":
                 actualmap=random.choice(allGameData.maps)
                 self.mapindex=allGameData.maps.index(actualmap)
             else:
                 actualmap=allGameData.maps[self.mapindex]

             numplayers=0
             self.allteamsdict=dict()
             temp0=copy.copy(self.clientele)
             for cID in temp0:
                   playerteam=self.playerteams[cID]
                   numplayers+=1
                   self.allteamsdict[playerteam]=self.allteamsdict.get(playerteam,0)+1
             self.gameinit(actualmap,self.gamemode,numplayers)

             #create the players for the users
             for cID in self.clientele:
                 prow,pcol=random.choice(self.getEmptyTiles())
                 prow-=1
                 playerteam=self.playerteams[cID]
                 # print("Player id:%d  player team:%s"%(cID,playerteam))
                 # print(self.teamlist)
                 if self.gamemode=="captureTheFlag":
                      for homebase in self.homebaseGroup:
                          # print("Homebase team:%s"%homebase.team)
                          if homebase.team==playerteam:
                              if allGameData.map[homebase.row][homebase.col]==10:
                                 teamindex=0
                              else:
                                 teamindex=1
                              prow,pcol=random.choice(allGameData.revivePositions[self.mapindex][teamindex])

                              prow-=1
                 elif self.gamemode=="Hero":
                      for herotower in self.homebaseGroup:
                          if herotower.team==playerteam:
                             prow,pcol=random.choice(herotower.surroundinglocations)
                             prow-=1
                 item=self.useritemlist[cID] 
                 if type(item)!=int:item=None
                 newPlayer=Player(prow,pcol,self.playercharacters[cID],cID,playerteam,item)
                 self.playerGroup.add(newPlayer)                                  
              
            #send the info of all players to every client and the game start info
             temp1=copy.copy(self.clientele)
             for cID in temp1:
               
                 teamstr=""
                 for team in self.allteamsdict:
                    teamstr+="%s*"%team

                 try: #starts the pinning process between the server and the users
                    temp1[cID].send(bytes("gamestarts_%d_%s_%d_%s\n"%(
                  self.mapindex,self.gamemode,numplayers,teamstr[:-1]), "UTF-8"))
                    self.userpinstarttime[cID]=self.roomtimecount
                 except:
                    self.sendPlayerQuitRoomInfo(cID)
                 temp2=copy.copy(self.clientele)
                 for allIDs in temp2:
                      someplayer=self.findPlayerWithID(allIDs)
                      try:
                        temp1[cID].send(bytes
                          ("newPlayer_%d_%d_%s_%d_%s_%s\n"%
                            (someplayer.row,someplayer.col,someplayer.name,
                              someplayer.playerno,someplayer.team,self.useritemlist[allIDs])
                            , "UTF-8"))
                      except:
                          self.sendPlayerQuitRoomInfo(cID)

    
    def gameactuallystarts(self): 
             minpinningtime=None
             for user in self.userLagTime:
                lagtime=self.userLagTime[user]
                if minpinningtime==None or lagtime<minpinningtime:
                    minpinningtime=lagtime
             for userid in self.clientele:
                 for player in self.playerGroup:
                   if player.playerno==userid:
                     player.lagratio=self.userLagTime[userid]//minpinningtime  
                     if player.lagratio>=1.2:
                       player.lagratio=1.2
             temp=copy.copy(self.clientele)
             for cID in temp:
               try:
                temp[cID].send(bytes("gameactuallystarts\n", "UTF-8"))
               except:
                 self.sendPlayerQuitRoomInfo(cID)
             
             self.mode="game"
                         

    def gameserverThread(self,senderID,msg):   
          if "iquit" in msg:  
            self.sendPlayerQuitGameInfo(senderID)
          
          for player in self.playerGroup:
             # print(player.playerno,senderID)
             if player.playerno==senderID:

                  row,col=player.getPlayerGrid()

                  if "space" in msg: 
                    self.playerPutBubble(player)
                    # start_new_thread(self.handleBubble, (player,))
                  if "key1" in msg:
                      self.useItem(1,row,col,player)
                  elif "key2" in msg:
                      self.useItem(2,row,col,player)
                  elif "key3" in msg:
                      self.useItem(3,row,col,player)
                  elif "key4" in msg:
                      self.useItem(4,row,col,player)
                  elif "key5" in msg:
                      self.useItem(5,row,col,player)
                  elif "key6" in msg:
                      self.useItem(6,row,col,player)
                  elif "becomeInvisible" in msg:
                      player.becomeInvisible()
                      for cID in self.clientele:
                         self.clientele[cID].send(bytes("becomeInvisible_%d\n"%(player.playerno), "UTF-8"))
                  elif "becomeVisible" in msg:
                      player.becomeVisible()
                      for cID in self.clientele:
                         self.clientele[cID].send(bytes("becomeVisible_%d\n"%(player.playerno), "UTF-8"))
                  elif "speak" in msg:
                      mymsg=msg.split("_")
                      playerid=int(mymsg[1])
                      speakmsg=mymsg[2]
                      for cID in self.clientele:
                         self.clientele[cID].send(bytes("speak_Player %d: %s\n"%(playerid+1,speakmsg), "UTF-8"))

                  if "endgame" in msg:
                      self.gameends=True
                      self.sendGameEndInfo()
                  
                  if not player.onBanana:
                      if "left" in msg: 
                         pushresult=player.moveLeft()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"left")
                            elif self.gamemode=="Kungfu":  
                               self.kickBubbles(pushresult)    


                      elif "right" in msg: 
                         pushresult=player.moveRight()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"right")
                            elif self.gamemode=="Kungfu": 
                              self.kickBubbles(pushresult)

                      elif "up" in msg: 
                         pushresult=player.moveUp()
                         if pushresult!=None: 
                            if self.gamemode=="treasurehunt":
                               self.pushBlocks(pushresult,"up")
                            elif self.gamemode=="Kungfu":
                              self.kickBubbles(pushresult) 

                      elif "down" in msg: 
                           pushresult=player.moveDown()
                           if pushresult!=None: 
                              if self.gamemode=="treasurehunt":
                                 self.pushBlocks(pushresult,"down")
                              elif self.gamemode=="Kungfu":
                                 self.kickBubbles(pushresult)
                  
                      self.sendPlayerMovedInfo(player) 
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
               for cID in self.clientele:
                     self.clientele[cID].send(bytes(
                      "kickBubble_%d_%d_%d_%d\n"%(origrow,origcol,targetrow,targetcol), "UTF-8"))
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
                for block in self.blockGroup:
                    if (block.row,block.col)==(brow,bcol):
                       block.ispushed(drow,dcol)
                       for cID in self.clientele:
                           self.clientele[cID].send(bytes(
                            "blockPushed_%d_%d_%d_%d\n"%(brow,bcol,drow,dcol), "UTF-8"))  
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

    def gameinit(self,gamemap,gamemode,numplayers):
        self.gameendcount=0
        self.numberOfPlayers=numplayers
        self.gamemode=gamemode
        self.gameends=False
        self.playerPutItemDict=dict()
        #this dict records the location at which a player put a item, so that 
        #players would not get their own items right
        self.mydata.gameinit(gamemode,gamemap,True)
        self.mydata.initImages()
        self.timecount=0   #used to slow down bubble explosion and other stuff
        self.bubbleExplosionCount=8 #used to extend bubble explosion time
        self.gamemap=gamemap
        self.maxJellyCount=250
        self.bubblePosListOfSets=[]
        self.itemGroup = pygame.sprite.Group()
        self.dartGroup = pygame.sprite.Group()
        self.blockGroup = pygame.sprite.Group()

        
        
        if self.gamemode in ["captureTheFlag","Hero"]:
           self.homebaseGroup = pygame.sprite.Group()
           self.teamlist=[]
           for team in self.allteamsdict:
             self.teamlist.append(team)

        elif self.gamemode=="treasurehunt":
           self.totalpoints=0  #total points possible on the board, used to
           #detect endgame
           self.teamscoredict=dict()
        
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

        self.dartno=0


        # blockitemString="blockItem"
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
                    team=self.teamlist[0] if blocktype==10 else self.teamlist[1]
                    self.homebaseGroup.add(Herotower(brow,bcol,team))
                    allGameData.GridList[brow][bcol]=2               
             elif self.gamemode=="captureTheFlag":
                if 0<blocktype<10:
                    chosenitem=self.chooserandomly(allGameData.itemNames,allGameData.itemfrequency)
                    block=Block(brow,bcol,blocktype,chosenitem)
                    self.blockGroup.add(block)
                    allGameData.GridList[brow][bcol]=2
                elif blocktype>=10:
                    team=self.teamlist[0] if blocktype==10 else self.teamlist[1]
                    self.homebaseGroup.add(Homebase(brow,bcol,team,self.numberOfPlayers//2))
                    allGameData.GridList[brow][bcol]=-1
                    allGameData.GridList[brow-1][bcol-1]=4
                    allGameData.GridList[brow-1][bcol+1]=4
                    allGameData.GridList[brow+1][bcol-1]=4
                    allGameData.GridList[brow+1][bcol+1]=4
                # blockitemString+="_%s"%chosenitem

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


            
    def playerPutBubble(self,player):
            newBubble=player.putBubble()
            if newBubble!=None:

                temp=copy.copy(self.clientele)
                for cID in temp:
                     try:
                        temp[cID].send(bytes("bubblePut_%d_%d_%d_%d_%d_%s_%s\n"%(
                          newBubble.row,newBubble.col,newBubble.type,newBubble.power
                          ,newBubble.playerno,newBubble.bubblehidden,newBubble.bubblenotshown), "UTF-8"))
                     except:
                        self.sendPlayerQuitGameInfo(cID)   
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

         


    def sendDropHeroInfo(self,player):
         for cID in self.clientele:
                   self.clientele[cID].send(bytes("drophero_%d\n"%(player.playerno), "UTF-8"))



#see if two bubbles on the same row has obstacles between
    def noObstacleRow(self,col1,col2,row):
        lowercol=min(col1,col2)
        uppercol=max(col1,col2)
        for col in range(lowercol+1,uppercol):
            if allGameData.GridList[row][col] in [2,5] and not self.isEmptyDirection(row,col,1):
                return False
        return True

#see if two bubbles on the same col has obstacles between
    def noObstableCol(self,row1,row2,col):
        lowerrow=min(row1,row2)
        upperrow=max(row1,row2)
        for row in range(lowerrow+1,upperrow):
            if allGameData.GridList[row][col] in [2,5] and not self.isEmptyDirection(row,col,0):
                return False
        return True

    def sendPlayerMovedInfo(self,player):
        playerInfoString="playerMoved_%d_%d_%d_%d\n"%(player.playerno,
                          player.x,player.y,player.direction)

        temp=copy.copy(self.clientele)
        for cID in temp:
            try:
                temp[cID].send(bytes(playerInfoString, "UTF-8")) 
            except:
              self.sendPlayerQuitGameInfo(cID)

    def sendDartRemoveInfo(self,dart):
         self.itemGroup.remove(dart)
         self.dartGroup.remove(dart)
         for cID in self.clientele:
                self.clientele[cID].send(bytes("dartRemoved_%d\n"%(dart.dartno), "UTF-8")) 
    



    def gametimerFired(self):
      if self.gameends:
            self.gameendcount+=1
            if self.gameendcount>=allGameData.gameendcount:
               self.gameendcount=0
               temp=copy.copy(self.clientele)
               for cID in temp:
                      temp[cID].send(bytes("backToRoom\n", "UTF-8"))
               self.gameends=False
               self.roominit()

      else: #not only timecount, but also keep alive check (we cannot do this too often, else the game lags)
        self.timecount+=1
        if self.timecount%6==0:
            temp=copy.copy(self.clientele)
            for cID in temp:
              try:
                sent=temp[cID].send(bytes("timecount_%d\n"%(self.timecount), "UTF-8")) 
                if sent==0:
                     raise RuntimeError("socket connection broken")
              except:
                  self.sendPlayerQuitGameInfo(cID)
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
                  if player.team in highestteams and len(highestteams)<len(self.allteamsdict):
                      player.isWin=True
                  elif player.team in highestteams and len(highestteams)==len(self.allteamsdict):
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
                  if player.team in highestteams and len(highestteams)<len(self.allteamsdict):
                      player.isWin=True
                  elif player.team in highestteams and len(highestteams)==len(self.allteamsdict):
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
           self.sendGameEndInfo()
        for player in self.playerGroup:
          if player.isJelly:  player.jellyCount+=1
          if player.jellyCount>=self.maxJellyCount:
               self.playerDie(player)
          if player.isDead: 
               player.deadCount+=1
          if player.deadCount>=allGameData.deadCount: 
                self.playerRevive(player) 
        self.playerGroup.update()
        # print(len(self.bubbleGroupgroup))
        if self.timecount%3==0:
           self.bubbleExplosions()
        self.checkKillSave()
        self.checkGetItems()
        try:
                for dart in self.dartGroup:
                  dart.dartMove(allGameData.dartSpeed)
                  drow=dart.row if (dart.dartdir in [0,3]) else dart.row-1
                  dcol=dart.col if (dart.dartdir in [0,3]) else dart.col-1 
                  origrow=dart.origrow if (dart.dartdir in [0,3]) else dart.origrow-1
                  origcol=dart.origcol if (dart.dartdir in [0,3]) else dart.origcol-1 
                  if allGameData.GridList[drow][dcol]==3:
                     self.sendDartRemoveInfo(dart)
                     for bubblegroup in self.bubbleGroupgroup:
                        hasbubble=False 
                      #if the bubblegroup contains the bubble that is hit by the dart
                        for bubble in bubblegroup:
                           if (bubble.row,bubble.col)==(drow,dcol):
                               hasbubble=True
                        if hasbubble:
                           for bubble in bubblegroup:
                               bubble.timetillexp=0
                           break #break after the correct bubblegroup is found
                     # print("asda")
                  elif allGameData.GridList[drow][dcol]>=2 and not( 
                    self.isEmptyDirection(drow,dcol,dart.dartdir)):
                     self.sendDartRemoveInfo(dart)
                  elif ((dart.dartdir in [0,3] and ((drow==0 and origrow!=0) or 
                              (drow==allGameData.Rows-1 and origrow!=allGameData.Rows-1 )))
                  or (dart.dartdir in [1,2] 
                            and ((dcol==0 and origcol!=0) or 
                              (dcol==allGameData.Cols-1 and origcol!=allGameData.Cols-1 )))):

                        self.sendDartRemoveInfo(dart)

                  elif abs(dart.origrow-drow)>8 or abs(dart.origcol-dcol)>8:
                     self.sendDartRemoveInfo(dart)
        except: pass




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
                    
                    self.sendPlayerMovedInfo(player)
                    self.renewPlayerItemDict(player)
                     



                


                 



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
            if (not player.isJelly) or itemname=="fork":
                if itemname=="slow":
                        self.itemGroup.add(Item(row,col,"makeslow",None))
                        allGameData.GridList[row][col]=1
                        self.sendNewItemInfo(row,col,"makeslow")
                        successfullyPut=True
                elif itemname=="banana":
                    self.itemGroup.add(Item(row,col,"bananapeel",None))
                    allGameData.GridList[row][col]=1
                    self.sendNewItemInfo(row,col,"bananapeel")
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
                    newDart.dartno=self.dartno #unique identifer
                    self.dartno+=1
                    self.itemGroup.add(newDart)
                    self.dartGroup.add(newDart)
                    self.sendNewItemInfo(row,col,"%sdart_%d"%(dirname,newDart.dartno))
                    successfullyPut=True
                elif self.gamemode=="Hero" and itemname=="hero":
                    player.hashero=False
                    prow,pcol=player.getPlayerGrid()
                    self.itemGroup.add(Item(prow,pcol,"hero"))
                    allGameData.GridList[prow][pcol]=1
                    self.sendDropHeroInfo(player)
                    successfullyPut=True
                elif self.gamemode=="Hero" and itemname=="bomb":
                    prow,pcol=player.getPlayerGrid()
                    for herotower in self.homebaseGroup:
                       if herotower.team!=player.team:
                          if (prow,pcol)==(herotower.row,herotower.col) and herotower.numheros>0:
                             herotower.numheros-=1
                             successfullyPut=True
                             for cID in self.clientele:
                                self.clientele[cID].send(bytes("towerDestroyed_%s\n"%(herotower.team), "UTF-8"))
                          else:
                            successfullyPut=False
                          break
                if successfullyPut:
                      self.playerPutItemDict[player.playerno]=(row,col)
                      
                      self.clientele[player.playerno].send(bytes("usedItem_%s_%d\n"%(itemname,itemkey), "UTF-8"))
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
                      # print(player.playerno,player.itemkeydict,player.itemKey)

    def playerSaved(self,player):
       player.isJelly=False
       player.y-=allGameData.Gridh//2
       for cID in self.clientele:
               self.clientele[cID].send(bytes("isSaved_%d\n"%(player.playerno), "UTF-8"))

    def checkKillSave(self):
      for player in self.playerGroup:
         if player.isJelly:
            jellypos=player.getPlayerGrid()
            for otherplayer in self.playerGroup:
              if (not otherplayer.isJelly and not otherplayer.isDead and 
                otherplayer.playerno!=player.playerno 
                and GameServer.isIntersecting(player,otherplayer)):

                  if otherplayer.team==player.team:
                       self.playerSaved(player)
                       otherplayer.savecount+=1
                       for cID in self.clientele:
                           self.clientele[cID].send(bytes("saveCount_%d\n"%(otherplayer.playerno), "UTF-8"))
                  else:
                      otherplayer.killcount+=1
                      if self.gamemode=="Kungfu":
                         otherplayer.killstreak+=1
                      for cID in self.clientele:
                           self.clientele[cID].send(bytes("killCount_%d\n"%(otherplayer.playerno), "UTF-8"))
                      self.playerDie(player)

    def playerRevive(self,player):
            player.isDead=False
            player.deadCount=0
            player.invincible=True
            player.invincibleCount=0
            newrow,newcol=random.choice(self.getEmptyTiles())
            if self.gamemode=="captureTheFlag":
                for homebase in self.homebaseGroup:
                   if player.team==homebase.team:
                      newrow,newcol=homebase.row,homebase.col
            elif self.gamemode=="Hero":
              for herotower in self.homebaseGroup:
                if herotower.team==player.team:
                   newrow1,newcol1=random.choice(herotower.surroundinglocations)

            newrow-=1
            player.x, player.y= (newcol*allGameData.Gridw+allGameData.Gridw//2, 
                  newrow*allGameData.Gridh+allGameData.Gridh//2+allGameData.Gridh)
            player.direction=0
            player.walkingcount=0

            for cID in self.clientele:
                     self.clientele[cID].send(bytes("playerRevive_%d_%d_%d\n"%(player.playerno,
                              player.x,player.y), "UTF-8"))

    def playerDie(self,player):
          if self.gamemode=="captureTheFlag" and player.hasBun:
              player.hasBun=False
              prow,pcol=player.getPlayerGrid()
              self.itemGroup.add(Item(prow,pcol,"bun"))
              allGameData.GridList[prow][pcol]=1
              for cID in self.clientele:
                   self.clientele[cID].send(bytes("dropBun_%d\n"%(player.playerno), "UTF-8"))
          elif self.gamemode=="Hero" and player.hashero:
              player.hashero=False
              prow,pcol=player.getPlayerGrid()
              self.itemGroup.add(Item(prow,pcol,"hero"))
              allGameData.GridList[prow][pcol]=1
              self.sendDropHeroInfo(player)
          elif self.gamemode=="Kungfu":
             player.killstreak=0
          player.deadtimes+=1
          player.isJelly=False
          player.jellyCount=0
          player.isSlow=False
          player.bubbleHidden=False
          player.isDead=True

          for cID in self.clientele:
                   self.clientele[cID].send(bytes("isKilled_%d\n"%(player.playerno), "UTF-8"))
          self.playerDropItems(player)


    def playerDropItems(self,player):
        if self.gamemode=="Kungfu":
           shouldnotDrop=True if len(player.usefulitemdict)>0 else False
        player.usefulitemdict=dict() #clear all useful items
        player.itemkeydict=dict()
        player.itemKey=1
        prow,pcol=player.getPlayerGrid()
      
      #in treasure hunt, drop gem first. Then drop items if killed without gems
        if self.gamemode=="treasurehunt" and player.gemscore>0:
             self.teamscoredict[player.team]-=player.gemscore
             for cID in self.clientele:
                  self.clientele[cID].send(bytes("playerDropGem_%d\n"%player.playerno, "UTF-8"))
                        
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
                 self.sendNewItemInfo(newrow,newcol,popItem)

             player.update()
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
                self.clientele[player.playerno].send(bytes("playerDropItem_%s\n"%(popItem), "UTF-8"))

                newrow,newcol=random.choice(self.getEmptyTiles())
                newItem=Item(newrow,newcol,popItem,None)
                self.itemGroup.add(newItem)
                self.sendNewItemInfo(newrow,newcol,popItem)
                allGameData.GridList[newrow][newcol]=1
                player.basicitemlist.remove(popItem)

    def sendNewItemInfo(self,row,col,itemname):
        
          temp=copy.copy(self.clientele)
          for cID in temp:
            try:
                temp[cID].send(bytes("newItem_%d_%d_%s\n"%(row,col,itemname), "UTF-8"))
            except:
              self.sendPlayerQuitGameInfo(cID)
           
        
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
                          allGameData.GridList[item.row][item.col]=0

                          for cID in self.clientele:
                            self.clientele[cID].send(bytes("itemRemoved_%d_%d_%s\n"%(item.row,item.col,item.chosenname), "UTF-8"))
                          self.itemGroup.remove(item)
             if self.gamemode=="captureTheFlag":
                   for homebase in self.homebaseGroup:
                      if homebase.baselocation==(prow,pcol): 
                           if (homebase.team != player.team) and (not player.hasBun):
                                  player.hasBun=True
                                  homebase.numbuns-=1
                                  self.sendHBBunInfo(homebase,-1)
                                  self.sendHaveBunInfo(player)
                           elif (homebase.team == player.team) and player.hasBun:
                                  player.hasBun=False
                                  homebase.numbuns+=1
                                  self.sendHBBunInfo(homebase,1)
                                  self.sendHaveBunInfo(player)
                                  if homebase.numbuns==self.numberOfPlayers:
                                     self.gameends=True #end game when one team gets all the buns
                                     for player in self.playerGroup:
                                       if player.team==homebase.team:
                                          player.isWin=True
                                       else:
                                          player.isWin=False
                                     self.sendGameEndInfo()
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
                              for cID in self.clientele:
                                 self.clientele[cID].send(bytes(
                                  "buildTower_%d_%s\n"%(player.playerno,herotower.team), "UTF-8"))
                              try:
                                self.clientele[player.playerno].send(bytes("usedItem_%s_%d\n"%("hero",itemkey), "UTF-8"))
                              except:
                                self.sendPlayerQuitGameInfo(player.playerno)
                              if herotower.numheros==4:
                                  self.gameends=True
                                  for player in self.playerGroup:
                                       if player.team==herotower.team:
                                          player.isWin=True
                                       else:
                                          player.isWin=False
                                  self.sendGameEndInfo()

#sends game end info to all clients, also 
#calls the updateUserDataAfterGame function 
    def sendGameEndInfo(self):
           
          self.updateUserDataAfterGame()
          for cID in self.clientele:
              for otherID in self.clientele: #send every player the winning info of every player
                    otherplayer=self.findPlayerWithID(otherID)
                    self.clientele[cID].send(bytes("isWin_%d_%s\n"%(
                      otherplayer.playerno,otherplayer.isWin), "UTF-8"))
              self.clientele[cID].send(bytes("gameends\n", "UTF-8"))


    #updates the database for wins, losses, ties, and experience changes
    def updateUserDataAfterGame(self):
        for player in self.playerGroup:
           playerusername=self.usernamesinplay[player.playerno]
           experiencegotten=self.calculateuserexperience(player,playerusername)
           # print("Experience gotten: %s  Player name: %s"%(experiencegotten,playerusername))
           if player.isWin==True:
              winstring="win"
           elif player.isWin==False:
              winstring="lose"
           elif player.isWin==None:
              winstring="tie"
           newlevel=self.updateUserStuff(playerusername,"experience",experiencegotten)
           for cID in self.clientele:
              self.clientele[cID].send(bytes("playerGetExperience_%d_%d\n"%(player.playerno,experiencegotten), "UTF-8"))
            #we send the new level instead of plussing 1 in case the user leveled up more than 1 level
           if newlevel!=None:
              for cID in self.clientele: 
                self.clientele[cID].send(bytes("playerLevelUp_%d_%d\n"%(player.playerno,newlevel), "UTF-8"))
           self.updateUserStuff(playerusername,winstring,1)
    
    def calculateuserexperience(self,player,username):
        experiencegotten=allGameData.basicExp #player gets experience just for completing the game
        experiencegotten+=allGameData.killExp*player.killcount
        experiencegotten+=allGameData.saveExp*player.savecount
        if player.isWin:
            experiencegotten+=allGameData.winExp
        
        return experiencegotten

    



  #number of buns in the homebase changes                              
    def sendHBBunInfo(self,homebase,dx):
       for cID in self.clientele:
              self.clientele[cID].send(bytes("hbChange_%s_%d\n"%(homebase.team,dx), "UTF-8"))


  #the hasbun status of a player changes
    def sendHaveBunInfo(self,player):
        for cID in self.clientele:
              self.clientele[cID].send(bytes("bunChange_%d\n"%(player.playerno), "UTF-8"))

    def sendGetHeroInfo(self,player):
         for cID in self.clientele:
              self.clientele[cID].send(bytes("getHero_%d\n"%(player.playerno), "UTF-8"))

    def getItem(self,player,item):
      if item.chosenname in allGameData.BasicItems:
        isminus=False
        questionname=None
        if item.chosenname=="question":
           questionname=random.choice(["speed","power","bubble"])
           isminus=random.choice([True,False])

        if item.chosenname=="power" and player.power<=player.maxPower:
          if isminus:
             if player.powerItem>0:
                player.powerItem-=1
                player.basicitemlist.remove("power")
          else:
            player.powerItem+=1
            player.basicitemlist.append("power")
          #only append if not over the limit power

        elif item.chosenname=="speed" and player.speed<=player.maxSpeed:
          if isminus:
             if player.speedItem>0:
                player.speedItem-=1
                player.basicitemlist.remove("speed")
          else:
              player.speedItem+=1
              player.basicitemlist.append("speed")

        elif item.chosenname=="bubble":
          if isminus:
             if player.bubbleItem>0:
                player.bubbleItem-=1
                player.basicitemlist.remove("bubble")
          else:
              player.bubbleItem+=1
              player.basicitemlist.append("bubble")
        

      elif item.chosenname in allGameData.UsefulItems:
        player.usefulitemdict[item.chosenname]=player.usefulitemdict.get(item.chosenname,0)+1
        if player.usefulitemdict[item.chosenname]<=1:
          player.itemkeydict[player.itemKey]=item.chosenname
          player.itemKey+=1
        if self.gamemode=="Hero" and item.chosenname=="hero" and not player.hashero:
           player.hashero=True
           self.sendGetHeroInfo(player)
        # print(player.playerno,player.itemkeydict,player.itemKey)

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



      self.clientele[player.playerno].send(bytes("playerGetItem_%s\n"%(item.chosenname), "UTF-8"))
        
      if self.gamemode=="captureTheFlag" and item.chosenname=="bun":
          player.hasBun=True
          self.sendHaveBunInfo(player)

      elif self.gamemode=="Kungfu":
          if item.chosenname in allGameData.transformcharacters:
             player.transformcharacter(item.chosenname)
             if player.newName=="gentleman":
                  if not ("dart" in player.usefulitemdict) or player.usefulitemdict["dart"]==0:
                    player.itemkeydict[player.itemKey]="dart"
                    player.itemKey+=1
                  player.usefulitemdict["dart"]=player.usefulitemdict.get("dart",0)+4
             for cID in self.clientele:
                self.clientele[cID].send(bytes("transformcharacter_%d_%s\n"%(
                  player.playerno,item.chosenname), "UTF-8"))
                


      elif self.gamemode=="treasurehunt":
          if item.chosenname=="redgem":
              player.redgem+=1
              self.sendGetGemInfo(player,"red")
          elif item.chosenname=="yellowgem":
              player.yellowgem+=1
              self.sendGetGemInfo(player,"yellow")
          elif item.chosenname=="greengem":
              player.greengem+=1
              self.sendGetGemInfo(player,"green")


    def sendGetGemInfo(self,player,gem):
        for cID in self.clientele:
            self.clientele[cID].send(bytes("playerGetGem_%d_%s\n"%(player.playerno,gem), "UTF-8"))
        if player.team in self.teamscoredict:
           self.teamscoredict[player.team]+=allGameData.gemScores[gem+"gem"]
        else:
           self.teamscoredict[player.team]=allGameData.gemScores[gem+"gem"]
        if self.teamscoredict[player.team]==self.totalpoints:
              self.gameends=True
              winningteam=player.team
              for allplayers in self.playerGroup:
                 if allplayers.team==winningteam:
                    allplayers.isWin=True
                 else:
                    allplayers.isWin=False
              self.sendGameEndInfo()
            


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
            if isExploding:
                shouldPlaySound=False
                for bubble in bubblegroup: #only check 1 bubble for efficiency 
                    if bubble.hasPlayedSound==False:
                       shouldPlaySound=True
                    break
                if shouldPlaySound: #this occurs exactly once for each exploding bubblegroup
                    tempset=set()
                    for bubble in bubblegroup:
                        bubble.hasPlayedSound=True
                        tempset.add((bubble.row,bubble.col))
                        if self.gamemode=="treasurehunt":
                          allGameData.cannotPushIntoSet.add((bubble.row,bubble.col))
                        if not self.isEmptyBlock(bubble.row,bubble.col):
                            allGameData.GridList[bubble.row][bubble.col]=0
                    self.bubblePosListOfSets.append(tempset)              
                    bubbleRemovString="bubbleRemove_"
                    for bubble in bubblegroup:
                          bubbleRemovString+="%d*%d*%d_"%(bubble.row,bubble.col,bubble.playerno)
                    for cID in self.clientele:
                          self.clientele[cID].send(bytes(bubbleRemovString[:-1]+"\n", "UTF-8"))

                explosioncontinues=False #check if is exploding or recovering
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
                        (downtile,lefttile,righttile,uptile)=((brow+
                          bubble.explodeDistList[0],bcol),
                        (brow,bcol-bubble.explodeDistList[1]),
                        (brow,bcol+bubble.explodeDistList[2]),
                        (brow-bubble.explodeDistList[3],bcol))
                        # print(lefttile,righttile,uptile,downtile)
                        backtracklist=self.collision([downtile,lefttile,righttile,uptile],bubble,bubblegroup)
                        if backtracklist!=None:
                          for backtrackindex in backtracklist:
                             if backtrackindex==0: 
                                 downtile=(brow+bubble.explodeDistList[0]-1,bcol)
                                 
                             elif backtrackindex==1:
                                 lefttile=(brow,bcol-bubble.explodeDistList[1]+1)
                                 
                             elif backtrackindex==2:
                                 righttile=(brow,bcol+bubble.explodeDistList[2]-1)
                                 
                             elif backtrackindex==3:
                                 uptile=(brow-bubble.explodeDistList[3]+1,bcol)
                        tileInfoString="tileExplode_"
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
                                tileInfoString+="%d*%d*%d_"%(tile.row,tile.col,num)

                        for cID in self.clientele:
                                self.clientele[cID].send(bytes(tileInfoString[:-1]+"\n", "UTF-8"))
                        for index in range(4):
                          if bubble.directionList[index]:
                            bubble.explodeDistList[index]+=1
                                
     
                if not explosioncontinues:
                    self.bubbleExplosionCount-=1 #timechecker
                    if self.bubbleExplosionCount<max(bubble.explodeDistList):
                          recoverList=[]
                          for bubble in bubblegroup:
                             recoverList+=self.endExplosion(bubble)
                          tileRecoString="tileRecover_"
                          for tile in self.tileGroup:
                               tpos=(tile.row,tile.col)
                               if tpos in recoverList:
                                   tile.updateTile(0)
                                   tileRecoString+="%d*%d_"%(tile.row,tile.col)
                          if self.gamemode in ["treasurehunt","Hero"]:
                             for bubble in bubblegroup:
                                if (bubble.row,bubble.col) in allGameData.emptyBlocksHaveBubbles:
                                   allGameData.emptyBlocksHaveBubbles.remove((bubble.row,bubble.col))
                          if self.gamemode=="treasurehunt":
                             for bubble in bubblegroup:
                                if (bubble.row,bubble.col) in allGameData.cannotPushIntoSet:
                                   allGameData.cannotPushIntoSet.remove((bubble.row,bubble.col))
                          for cID in self.clientele:
                                self.clientele[cID].send(bytes(tileRecoString[:-1]+"\n", "UTF-8"))
                          self.bubbleGroupgroup.remove(bubblegroup) 
                          for bubble in bubblegroup:
                            for bubblepossets in self.bubblePosListOfSets:
                                 if (bubble.row,bubble.col) in bubblepossets: 
                                    self.bubblePosListOfSets.remove(bubblepossets)
                                    break                                              
                          self.bubbleExplosionCount=6

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
            if ((row,col) in explodedTileList):
              directionindex=explodedTileList.index((row,col))
              if not ( self.isEmptyDirection(row,col,directionindex)):
                  bubble.directionList[directionindex]=False
                  #left,right,up,down
                  if block.canExplode:
               
                    temp=copy.copy(self.clientele)
                    for cID in temp:
                        try:
                          temp[cID].send(bytes("blockExploded_%d_%d\n"%(block.row,block.col), "UTF-8"))
                        except:
                           self.sendPlayerQuitGameInfo(cID)
                    self.blockGroup.remove(block)
                    if block.hiddenItem!="empty":
                        allGameData.GridList[row][col]=1
                        self.itemGroup.add(Item(row,col,block.hiddenItem,bubble))
                        self.sendNewItemInfo(row,col,block.hiddenItem) #client need not know the bubble info

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
                 for cID in self.clientele:
                      self.clientele[cID].send(bytes("transformback_%d\n"%(player.playerno), "UTF-8"))
            else:
                 
                original=player.isJelly
                player.isJelly=True
                player.onBanana=False

                for cID in self.clientele:
                      self.clientele[cID].send(bytes("playerJelly_%d\n"%(player.playerno), "UTF-8"))
                if original!=player.isJelly: 
    #move the player jelly down a bit in the first run to keep position the same

                  for cID in self.clientele:
                          self.clientele[cID].send(bytes("yShift_%d\n"%(player.playerno), "UTF-8"))  
                  player.y+=allGameData.Gridh//2
        
       for item in self.itemGroup:
            itempos=(item.row,item.col)
            if itempos in explodedTileList and (item.fromBubble==None or item.fromBubble not in bubblelist): 
            #bubblelist is the list of bubbles in the same explosion
              if item.chosenname!="bun":
                if self.gamemode=="treasurehunt" and item.chosenname in allGameData.gemItems:
                    self.totalpoints-=allGameData.gemScores[item.chosenname]
                
                temp=copy.copy(self.clientele)
                for cID in temp:
                  try:
                      temp[cID].send(bytes("itemRemoved_%d_%d_%s\n"%(item.row,item.col,item.chosenname), "UTF-8"))
                  except:
                     self.sendPlayerQuitGameInfo(cID)
                self.itemGroup.remove(item)




       if self.gamemode=="captureTheFlag":
           for homebase in self.homebaseGroup:
               hrow,hcol=homebase.row,homebase.col
               rowcolset=set(homebase.cornerlist)#use set for higher efficiency
               for epos in explodedTileList:#use set for higher efficiency
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


        
def main():
    game1 = GameServer()
    game1.run()

if __name__ == '__main__':
    main()

