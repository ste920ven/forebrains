import util

def kill(game,pursuer,target):
  newTarget = getTarget(game,player)
  setTarget(game,pursuer,newTarget)
  isAlive(game,target,FALSE)
  return TRUE
  
def checkIn(game,player,loc):
  setLoc(game,player,loc)
  return getLastLoc(game,player)
  
def score(game,player):
  
def end(game):
  
def penalize(game,player):
  newPenalty = getPenalty(game,player)+1
  setPenatly(game,player,newPenalty)
  return TRUE
  
def respawn(game,player):
