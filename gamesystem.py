import util, random

def kill(game,pursuer,target):
  newTarget = str(util.getTarget(game,target))
  util.changeTarget(game,str(pursuer),newTarget)
  util.addKill(game,str(pursuer))
  util.setLive(game,str(target),False)
  util.setTarget(game,str(target),"")
  util.setPursuer(game,str(target),"")
  if newTarget == pursuer:
    end(game)
  return True
  
def checkIn(game,player,loc):
  util.setLoc(game,player,loc)
  pursuer = getPursuer(game,player)
  return getLastLoc(game,pursuer)
  
def score(game,player):
  score = util.getKills(game,player)
  return score

def end(game):
  winners = util.getRankings(game)
  util.removeGame(game)
  return winners
  
def penalize(game,player):
  util.penalize(game,player)
  return True
  
def respawn(game,player):
  util.setLive(game,player,True)
  rankings = util.getRankings(game)
  l = []
  for key in rankings:
    if key != player:
      for n in range(rankings[key]):
        l.append(key)
  random.shuffle(l)
  newTarget = l[0]
  util.setTarget(game,player,newTarget)
  return True
  


