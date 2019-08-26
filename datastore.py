import json
import yaml

def loadShinyList():
    with open('shinylist.json') as f:
        return json.load(f)

def loadConfig():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
        return config['config'], config['controls']

"""
bbox : the bounding box for the screenshots
screenshot : the placeholder of the screenshot
walking : if the player is currently moving or not
walkPosition : how many steps the player has taken in the walkRange
    everytime the user takes one step the walkPosition gets incremented
walkRange : the amount of tiles the user will walk
inBattle : if the user is currently battling or not
encounterCount : how many Pokemons the user has encountered
shinyList : a list containing all the information for shiny checking
canEscape : if the user can escape the battle (against a wild Pokemon) or not
battleOption : which battleOption is selected during battle
direction : the direction the user is headed. e.g: N (North), W (West) etc.
currentHealth : the current health from the Pokemon the user is battling with (not against)
maxHealth :  the max health from the Pokemon the user is battling with (not against)
config : stores all the config information from the config.yaml
controls: stores all the controls information from the config.yaml
"""
class ds:
    bbox = None
    screenshot = None
    walking = False
    walkPosition = 0
    walkRange = 3
    inBattle = False
    encounterCount = 0
    shinyList = loadShinyList()
    canEscape = False
    battleOption = 'FIGHT'
    direction = None
    currentHealth = 0
    maxHealth = 0
    config, controls = loadConfig()

def getConfig():
	return ds.config

def getControls():
    return ds.controls

def getCurrentHealth():
    return ds.currentHealth

def setCurrentHealth(newval):
    ds.currentHealth = newval

def getMaxHealth():
    return ds.maxHealth

def setMaxHealth(newval):
    ds.maxHealth = newval
    
def getDirection():
    return ds.direction

def setDirection(newval):
    ds.direction = newval

def getBattleOption():
    return ds.battleOption

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