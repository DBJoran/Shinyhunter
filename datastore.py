import json

def loadShinyList():
    shinyList = []
    with open('shinylist.json') as f:
        shinyList = json.load(f)
    return shinyList
    
class ds:
    exitFlag = 0
    bbox = 0
    screenshot = None
    walking = False
    walkPosition = 0
    walkRange = 3
    inBattle = False
    encounterCount = 0
    shinyList = loadShinyList()
    canEscape = False
    battleOption = 3

def getBattleOption():
    return ds.battleOption

# BAG = 0
# RUN = 1
# POKEMON = 2
# FIGHT = 3
def setBattleOption(newval):
    ds.battleOption = newval

def getCanEscape():
    return ds.canEscape

def setCanEscape(newval):
    ds.canEscape = newval

def getShinyList():
    return ds.shinyList

def getShinyListX(pokemonName):
    return ds.shinyList[pokemonName]['x']

def getShinyListY(pokemonName):
    return ds.shinyList[pokemonName]['y']

def getShinyListColor(pokemonName):
    return ds.shinyList[pokemonName]['shinyColor']

def setShinyList(newval):
    ds.shinyList = newval

def getScreenshot():
    return ds.screenshot

def setScreenshot(newval):
    ds.screenshot = newval

def getEncounterCount():
    return ds.encounterCount

def incrEncounterCount():
    ds.encounterCount = ds.encounterCount + 1

def getWalkPosition():
    return ds.walkPosition

def setWalkPosition(newval):
    ds.walkPosition = newval

def incrWalkPosition():
    ds.walkPosition = ds.walkPosition + 1
    
def getWalkRange():
    return ds.walkRange

def setWalkRange(newval):
    ds.walkRange = newval

def getInBattle():
    return ds.inBattle

def setInBattle(newval):
    ds.inBattle = newval

def getWalking():
    return ds.walking

def setWalking(newval):
    ds.walking = newval

def getBbox():
    return ds.bbox
    
def setBbox(newval):
    ds.bbox = newval

def getExitFlag():
    return ds.exitFlag

def setExitFlag(newval):
    ds.exitFlag = newval