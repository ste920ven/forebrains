import urllib
import json
import sys
import time
import base64
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
    newgame = {"creator" : creator, "pass" : tmp, "name" : name, "players" : {creator : {"lat": 0, "long": 0, "pursuer" : "", "target" : "", "kills" = 0, "live" : False}}}
    games.insert(newgame)

def addPlayer(user,game):
    tmp = games.find_one({"name":game})["players"]
    tmp[user] = {"lat": 0, "long": 0, "pursuer" : "", "target" : "", "kills" = 0, "live" : False}
    games.update({"name" : game},{"$set" : {"players" : tmp}})

def checkuserpass(user,password):
    tmp = users.find_one({"user" : user})
    if password == tmp["pass"]:
        return True
    else:
        return False

def checkgamepass(game,password):
    tmp = games.find_one({"name":game)}
    if password == tmp["pass"]

#encode password for check

    
