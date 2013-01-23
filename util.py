import urllib
import json
import sys
import time
import base64
import random
import gamesystem
import math
from pymongo import Connection

Conn = Connection('ds041367.mongolab.com',41367)
db = Conn['stuycs_sideprojects']
res = db.authenticate('stuycs','stuycs')
users = db.FinalProjUsers
games = db.FinalProjGames

def createUser(user,password):
    if users.find_one({"user" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"user" : user, "pass" : tmp, "game" : 0, "wins" : 0, "loses" : 0,"friends" : []}
    users.insert(newuser)
    return True

def createGame(creator,password,name):
    if games.find_one({"name":name}) != None:
        return False
    if password != "":
        tmp = base64.b64encode(password)
    else:
        tmp = False
    newgame = {"creator" : creator, "pass" : tmp, "name" : name, "started" : False, creator : {"loc":[0,0], "pursuer" : "", "target" : "", "kills" : 0, "live" : False, "penalty" : 0, "bonus" : False}}
    games.insert(newgame)
    return True

def addPlayer(game,user):
    tmp = games.find_one({"name":game})
    k = tmp.keys()
    if user in k:
        return False
    tmp[user] = {"loc":[0,0], "pursuer" : "", "target" : "", "kills" : 0, "live" : False, "penalty" : 0, "bonus" : False}
    games.update({"name" : game},tmp)
    return True

def checkUserPass(user,password):
    encpass = base64.b64encode(password)
    tmp = users.find_one({"user" : user})
    if tmp == None:
        return 0
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def checkGamePass(game,password):
    encpass = base64.b64encode(password)
    tmp = games.find_one({"name":game})
    if tmp == None:
        return 0
    if tmp["pass"] == False:
        return True
    if encpass == tmp["pass"]:
        return True
    else:
        return False

def startGame(game):
    tmp = games.find_one({"name":game})
    players = tmp.keys()
    random.shuffle(players)
    current = 0
    exceptions = ["creator","pass","name","_id","started"]
    toremove = []
    for exception in exceptions:
        players.remove(exception)
    for person in players:
        tmp[person]["live"] = True
        if current == len(players) - 1:
            current = -1
        currentplus = current + 1
        tmp[players[currentplus]]["pursuer"] = person
        tmp[person]["target"] = players[currentplus]
        current = current + 1
    tmp["started"] = True
    games.update({"name":game},tmp)
    return True

def gameStarted(game):
    tmp = games.find_one({"name":game})
    return tmp["started"]
       
def getTarget(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["target"]

def getLoc(game, player):
    tmp = games.find_one({"name":game})
    return tmp[player]["loc"]

def getPursuer(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["pursuer"]

def isAlive(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["live"]

def addKill(game,player):
    tmp = games.find_one({"name":game})[player]
    tmp["kills"] = tmp["kills"] + 1
    games.update({"name":game},{"$set":{player:tmp}})
    return True

def getKills(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["kills"]

def getLastLoc(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["loc"]
    
def getPenaltyTime(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["penalty"]
    
def setLoc(game,player,loc):
    tmp = games.find_one({"name":game})[player]
    tmp["loc"] = loc
    games.update({"name":game},{"$set":{player:tmp}})
    return True

def setTarget(game,player,newTarget):
    tmp = games.find_one({"name":game})[player]
    tmp["target"] = str(newTarget)
    games.update({"name":game},{"$set":{player:tmp}})
    return True

def setPursuer(game,player,newPursuer):
    tmp = games.find_one({"name":game})[player]
    tmp["pursuer"] = newPursuer
    games.update({"name":game},{"$set":{player:tmp}})
    return True
    
def changeTarget(game,pursuer,target):
    tmpone = games.find_one({"name":game})[pursuer]
    tmptwo = games.find_one({"name":game})[target]
    tmpone["target"] = target
    tmptwo["pursuer"] = pursuer
    games.update({"name":game},{"$set":{pursuer:tmpone}})
    games.update({"name":game},{"$set":{target:tmptwo}})
    return True

def penalize(game,player):
    now = time.time()
    tmp = games.find_one({"name":game})[player]
    tmp["penalty"] = now
    games.update({"name":game},{"$set":{player:tmp}})
    return True

def setLive(game,player,status):
    tmp = games.find_one({"name":game})[player]
    tmp["live"] = status
    games.update({"name":game},{"$set":{player:tmp}})

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
    invalids = ["creator","pass","name","_id","started"]
    for person in k:
        if person not in invalids:
            locations.append(tmp[person]["loc"])
    return locations

def getGames():
   tmp = games.find()
   keys = []
   for game in tmp:
       keys.append(str(game["name"]))
   return keys

def getPlayers(game):
    tmp = games.find_one({"name":game})
    players = tmp.keys()
    for player in players:
        current = 0
        exceptions = ["creator","pass","name","_id","started"]
        for person in players:
            if person in exceptions:
                players.remove(person)   
    return players

def getCreator(game):
    tmp = games.find_one({"name":game})
    return tmp["creator"]

def getGameInfos(user):
    l = []
    for game in getGames():
        creator = str(getCreator(game))
        numplayers = len(getPlayers(game))
        tmp = games.find_one({"name":game})
        started = gameStarted(game)
        players = getPlayers(game)
        ingame = False
        for player in players:
            if str(player) == user:
                ingame = True
        if tmp["pass"]==False:
            view = "Public"
        else:
            view = "Private"
        l.append([game,creator,view,numplayers,started,ingame])
    return l

def tryKill(game,player):
    targetLoc = getLoc(game,getTarget(game,player))
    playerLoc = getLoc(game,player)
    lat = playerLoc[0]
    targetLat = targetLoc[0]
    lng = playerLoc[1]
    targetLng = targetLoc[1]
    R = 6371
    dLat = math.radians(lat - targetLat)
    dLon = math.radians(lng - targetLng)
    dLat1 = math.radians(targetLat)
    dLat2 = math.radians(lat)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(dLat1) * math.cos(dLat1) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    if distance < 0.05: 
        gamesystem.kill(game,player,getTarget(game,player))
    else:
        gamesystem.penalize(game,player)
    return True
