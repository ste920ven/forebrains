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
    newgame = {"creator" : creator, "pass" : tmp, "name" : name, creator : {"loc":[0,0], "pursuer" : "", "target" : "", "kills" : 0, "live" : False, "penalty" : 0, "bonus" : False}}
    games.insert(newgame)
    return True

def addPlayer(game,user):
    tmp = games.find_one({"name":game})
    tmp[user] = {"loc":[0,0], "pursuer" : "", "target" : "", "kills" : 0, "live" : False, "penalty" : 0, "bonus" : False}
    games.update({"name" : game},tmp)

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
    exceptions = ["creator","pass","name","_id"]
    for person in players:
        if person in exceptions:
            players.remove(person)
            if current == len(players):
                current = -1
                tmp[person]["target"] = players[current+1]
                tmp[players[current+1]]["pursuer"] = person
                current = current + 1
                games.update({"name":game},tmp)
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
    
def getPenaltyTime(game,player):
    tmp = games.find_one({"name":game})
    return tmp[player]["penalty"]
    
def setLoc(game,player,loc):
    games.update({"name":game},{"$set":{player:{"loc":loc}}})
    return True
    
def setTarget(game,pursuer,target):
    games.update({"name":game},{"$set":{pursuer:{"target":target}}})
    games.update({"name":game},{"$set":{target:{"pursuer":pursuer}}})
    return True

def penalize(game,player):
    now = time.time()
    games.update({"name":game},{"$set":{"penalty":now}})
    pser = games.find_one({"name":game})[player]["pursuer"]
    games.update({"name":game},{"$set":{pser:{"bonus":True}}})
    return True

def setLive(game,player,status):
    games.update({"name":game},{"$set":{player:{"live":status}}})

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
    invalids = ["creator","pass","name"]
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
        exceptions = ["creator","pass","name","_id"]
        for person in players:
            if person in exceptions:
                players.remove(person)   
    return players

def getCreator(game):
    tmp = games.find_one({"name":game})
    return tmp["creator"]

    
