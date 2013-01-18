import urllib
import json
import sys
import time
import base64
import random
from pymongo import Connection

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.FinalProjUsers
games = db.FinalProjGames

def createUser(user,password):
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp, "game" : 0, "wins" : 0, "loses" : 0,"friends" : []}
    users.insert(newuser)

def createGame(creator,password,name):
    if password != "":
        tmp = base64.b64encode(password)
    else:
        tmp = False
    newgame = {"creator" : creator, "pass" : tmp, "name" : name, "players" : {creator : {"loc":[0,0], "pursuer" : "", "target" : "", "kills" = 0, "live" : False}}}
    games.insert(newgame)

def addPlayer(game,user):
    tmp = games.find_one({"name":game})["players"]
    tmp[user] = {"loc":[0,0], "pursuer" : "", "target" : "", "kills" = 0, "live" : False, "penalty" : 0}
    games.update({"name" : game},{"$set" : {"players" : tmp}})

def checkuserpass(user,password):
    encpass = base64.b64encode(password)
    tmp = users.find_one({"user" : user})
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def checkgamepass(game,password):
    encpass = base64.b64encode(password)
    tmp = games.find_one({"name":game})
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def startGame(game):
    tmp = games.find_one({"name":game})
    k = tmp.keys()
    targets = tmp.keys()
    random.shuffle(targets)
    current = 0
    for person in k:
        tmp[person]["live"] = True
        tmp[person]["target"] = targets[current]
        current = current + 1
    games.update({"name":game},{"$set":game})
    return True
       
def getTarget(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["target"]

def getPursuer(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["target"]

def isAlive(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["live"]

def getKills(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["kills"]

def getLastLoc(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["loc"]
    
def getPenalty(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["penalty"]
    
def setLoc(game,player,loc):
    games.update({"name":game},{"$set":{"loc":loc}})
    return True
    
def setTarget(game,pursuer,target):


def setPenatly(game,player,penalty):

    
def setAlive(game,player,status):


def getRankings(game):
    rankings = []
    return rankings

    
def addFriend(player,friend):
    tmp = users.find_one({"user":player})
    tmp["friends"].append(friend)
    users.update({"user":player},{"$set":{"friends":tmp}})
    return True

def getAllLocs(game):
    locations = []
    tmp = games.find_one({"name":game})
    k = tmp.keys()
    for person in k:
        

#encode password for check

    
