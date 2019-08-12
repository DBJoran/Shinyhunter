import numpy as np
import cv2
import directkeys
import ocr
import time
import math
import win32gui
import json
import sys
import toolkit
import datastore as ds
from mss import mss
from PIL import Image
from collections import Counter

# TODO: Make script exit if the window loses focus
# IMPORTANT, this script will not work if you use other colors then default VisualBoyAdvance colors
# IMPORTANT, the OCR will not work if your screen is blurry
# This script is ran at the following setting: Options > Video > x3

# Load shinyList
with open('shinylist.json') as f:
    shinyList = json.load(f)

# ===================================================================================
# Actual functionality starts here :)

# Find the emulator window, focus the window and set the dimensions in the store
# We need the dimensions for the screenshots
ds.setBbox(toolkit.findWindow())

def loadPokemon():
    # Sleep for loading screen
    time.sleep(4)
    # Press A to continue
    directkeys.keyPress(ds.getControls()['gba-a'])
    
    ds.incrEncounterCount()
    print('Pokemons encountered: ' + str(ds.getEncounterCount()))
    # User will throw Pokeball on battlefield
    time.sleep(4)

def leaveBattle():
    ds.setCanEscape(False)
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    health = ocr.ocr('health', img).split(' ')

    # Sometimes the OCR doesn't recognize the health properly
    # The OCR function returns an array list. For a Pokemon with 127 current hp and a max hp of 227 something like the following should be returned
    # expected output (when it goes right): ['127', '227']
    # expected output (when it goes WRONG): ['127227']
    # If the output is wrong we should expect a array length of 1, if it goes right we should expect a array length of 2
    # If we happen to get a array length of 1 we need to take a new screenshot and try it again until it returns a proper array with a lenght of 2 (like mentioned above).

    while len(health) == 1:
        toolkit.takeScreenshot()
        img = ds.getScreenshot()
        health = ocr.ocr('health', img).split(' ')

    ds.setCurrentHealth(int(health[0]))
    ds.setMaxHealth(int(health[1]))

    if int(ds.getCurrentHealth()) < math.floor(int(ds.getMaxHealth()) / 2):
        print("healing...")        
        healPokemon()
    
    moveToBattleOption(ds.getBattleOption(), 'RUN')

    # Press A to leave
    # Press RUN
    while ds.getCanEscape() == False:
        # Make sure we are our battleOption is RUN, if not move to RUN
        if ds.getBattleOption() == 'RUN':
            directkeys.keyPress(ds.getControls()['gba-a'])
        else:
            moveToBattleOption(ds.getBattleOption(), 'RUN')
            directkeys.keyPress(ds.getControls()['gba-a'])

        time.sleep(6)

        # We just tried to run, we need to take a screenshot to know if we can leave safely
        toolkit.takeScreenshot()
        img = ds.getScreenshot()
        epoch = int(time.time())
        cv2.imwrite('leave-test/' +str(epoch) + '.png', img)
        text = ocr.ocr('chat', img)
        print(text)

        # If we can't leave we will have to text 'Can't escape' 
        if 'escape' not in text:
            ds.setCanEscape(True)

            # Press A to dismiss text
            directkeys.keyPress(ds.getControls()['gba-a'])
            # We will now exit the WHILE loop

        else:
            ds.setCanEscape(False)

        # Press A to dismiss text
        directkeys.keyPress(ds.getControls()['gba-a'])

        # Enemy will do attack
        # TODO: Decrease this timeout, 10 works fine, but I think we could also do with a couple seconds less of timeout
        time.sleep(9)

    # Before we set the inBattle status we need to make sure we are actually not in battle anymore
    # we can do this by checking the far right bottom corner for color
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    height, width = img.shape[:2]
    centerPixel = img[(height - 10)][(width - 10)]
    color = str(centerPixel[2]) + str(centerPixel[1]) + str(centerPixel[0])

    if color != '404848':
        ds.setInBattle(False)
    else:
        ds.setInBattle(True)

    print('done')

def getDirection():
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    centerPixel = img[282][367]
    color = str(centerPixel[2]) + str(centerPixel[1]) + str(centerPixel[0])
    if color == '1044040' or color == '1206464':
        ds.setDirection('N')
    elif color == '16812064':
        ds.setDirection('E')
    elif color == '5656120':
        ds.setDirection('S')
    elif color == '216144112':
        ds.setDirection('W')

def moveToBattleOption(currentPosition, newPosition):
    # FIGHT > BAG
    if currentPosition == 'FIGHT' and newPosition == 'BAG':
        # Move right
        directkeys.keyPress(ds.getControls()['right'])
        ds.setBattleOption('BAG')
    # FIGHT > RUN
    if currentPosition == 'FIGHT' and newPosition == 'RUN':
        # Move down
        directkeys.keyPress(ds.getControls()['down'])
        # Move right
        directkeys.keyPress(ds.getControls()['right'])
        ds.setBattleOption('RUN')
    # FIGHT > POKEMON
    if currentPosition == 'FIGHT' and newPosition == 'POKEMON':
        # Move down
        directkeys.keyPress(ds.getControls()['down'])
        ds.setBattleOption('POKEMON')

    # POKEMON > BAG
    if currentPosition == 'POKEMON' and newPosition == 'BAG':
        # Move right
        directkeys.keyPress(ds.getControls()['right'])
        # Move up
        directkeys.keyPress(ds.getControls()['up'])
        ds.setBattleOption('BAG')
    # POKEMON > RUN
    if currentPosition == 'POKEMON' and newPosition == 'RUN':
        # Move right
        directkeys.keyPress(ds.getControls()['right'])
        ds.setBattleOption('RUN')
    # POKEMON > FIGHT
    if currentPosition == 'POKEMON' and newPosition == 'FIGHT':
        # Move up
        directkeys.keyPress(ds.getControls()['up'])
        ds.setBattleOption('FIGHT')

    # RUN > BAG
    if currentPosition == 'RUN' and newPosition == 'BAG':
        # Move up
        directkeys.keyPress(ds.getControls()['up'])
        ds.setBattleOption('BAG')
    # RUN > POKEMON
    if currentPosition == 'RUN' and newPosition == 'POKEMON':
        # Move left
        directkeys.keyPress(ds.getControls()['left'])
        ds.setBattleOption('POKEMON')
    # RUN > FIGHT
    if currentPosition == 'RUN' and newPosition == 'FIGHT':
        # Move left
        directkeys.keyPress(ds.getControls()['left'])
        # Move up 
        directkeys.keyPress(ds.getControls()['up'])
        ds.setBattleOption('FIGHT')

    # BAG > RUN
    if currentPosition == 'BAG' and newPosition == 'RUN':
        # Move down
        directkeys.keyPress(ds.getControls()['down'])
        ds.setBattleOption('RUN')
    # BAG > POKEMON
    if currentPosition == 'BAG' and newPosition == 'POKEMON':
        # Move down
        directkeys.keyPress(ds.getControls()['down'])
        # Move left
        directkeys.keyPress(ds.getControls()['left'])
        ds.setBattleOption('POKEMON')
    # BAG > FIGHT
    if currentPosition == 'BAG' and newPosition == 'FIGHT':
        # Move left
        directkeys.keyPress(ds.getControls()['left'])
        ds.setBattleOption('FIGHT')
    
# TODO: support for left and right, now there is only support for up and down
def walk():
    ds.setWalking(True)

    # Sleep for 0.25 seconds every step
    # Decreasing the sleep time even more will make the steps innacurate
    time.sleep(.25)

    if ds.getWalkPosition() >= (ds.getWalkRange() * 2 + 2):
        ds.setWalkPosition(0)

    if ds.getWalkPosition() > ds.getWalkRange():
        directkeys.keyPress(ds.getControls()['up'])
        ds.incrWalkPosition()
        
    if ds.getWalkPosition() <= ds.getWalkRange():
        directkeys.keyPress(ds.getControls()['down'])
        ds.incrWalkPosition()

    ds.setWalking(False)

def checkShiny():
    x, y, shinyColor = getPokemonInfo()
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    # OpenCV does YX and not XY
    colorPixel = img[y][x]
    color = str(colorPixel[2]) + str(colorPixel[1]) + str(colorPixel[0])
    if color == str(shinyColor):
        print('shiny!')
        # Terminate the script here
        sys.exit()
    else: 
        print('no shiny')

def getPokemonInfo():
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    pokemonName = ocr.ocr('pokemon',img).lower()
    x = ds.getShinyListX(pokemonName)
    y = ds.getShinyListY(pokemonName)
    shinyColor = ds.getShinyListColor(pokemonName)

    return x, y, shinyColor

def healPokemon():
    moveToBattleOption(ds.getBattleOption(), 'BAG')
    # Press A (Q)
    directkeys.keyPress(ds.getControls()['gba-a'])
   
    # We are now in the bag
    # Make sure we have a potion
    time.sleep(1)
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    bagName = ocr.ocr('bagname', img)
    print(bagName)

    # Check if we are on the right page, we need to be on the ITEMS page
    if bagName == 'ITEMS':
        # Press arrow up
        directkeys.keyPress(ds.getControls()['up'])
    elif bagName == 'KEY ITEMS':
        # Press A to move to left in the bag
        directkeys.keyPress(ds.getControls()['left'])
        # Press arrow up
        directkeys.keyPress(ds.getControls()['up'])
    elif bagName == 'POKé BALLS':
        # Press A to move to left in the bag
        directkeys.keyPress(ds.getControls()['left'])
        # Press A to move to left in the bag
        directkeys.keyPress(ds.getControls()['left'])
        # Press arrow up
        directkeys.keyPress(ds.getControls()['up'])

    checkItems(ds.getConfig()['heal-item'])
    
    # Press A to select
    directkeys.keyPress(ds.getControls()['gba-a'])
    time.sleep(1)

    # Press A to use
    directkeys.keyPress(ds.getControls()['gba-a'])
    time.sleep(1)

    # Press A to use on Pokemon
    directkeys.keyPress(ds.getControls()['gba-a'])   
    time.sleep(5)

    # Press A again to dismiss chat message
    directkeys.keyPress(ds.getControls()['gba-a'])

    # Time sleep couple of seconds for the enemy to do a attack
    time.sleep(10)

# @item, the item that has to be checked if its in the bag
# TODO: Check if this still works with only 3 items in the bag
def checkItems(item):
    print('Searching for ' + item)
    itemFound = False
    previousItem = ''

    # Go all the way to thes top of the bag
    print(type(ds.getConfig()['bag-items']))
    for i in range(0, ds.getConfig()['bag-items']):
        time.sleep(0.25)
        directkeys.keyPress(ds.getControls()['up'])



    print('first three')
    for i in range(0, 3):
        time.sleep(0.25)
        toolkit.takeScreenshot()
        img = ds.getScreenshot()
        itemName = ocr.ocr('itemname' + str(i + 1), img)

        if itemName.lower() == item.lower():
            itemFound = True
            break

        print(previousItem.lower())
        print(itemName.lower())
        if previousItem.lower() != itemName.lower():
            print('down')
            directkeys.keyPress(ds.getControls()['down'])
        
        previousItem = itemName

    print('middle')
    while itemFound == False:
        time.sleep(0.25)
        print('---------------')
        toolkit.takeScreenshot()
        img = ds.getScreenshot()
        itemName = ocr.ocr('itemname4', img)

        if itemName.lower() == item.lower():
            itemFound = True
            # print('item found!')
            return True

        print(previousItem.lower())
        print(itemName.lower())
        if previousItem.lower() != itemName.lower():
            print('down')
            directkeys.keyPress(ds.getControls()['down'])

        # Check if we have reached the bottom if we have CANCEL as last 'item' in the list
        lastItem = ocr.ocr('itemname6', img)
        if lastItem.lower() == 'cancel':
            break

        previousItem = itemName
        

    directkeys.keyPress(ds.getControls()['down'])
    print('down last item')
    time.sleep(0.25)
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    itemName = ocr.ocr('itemname5', img)
    if itemName.lower() == item.lower():
        itemFound = True
        print('itemfound')
        return True
        
    # if itemFound == False:
        # raise RuntimeError('The item: "' + item + '" was not found in the bag!')
        
# If the user is not pointing north, make the user point north before starting
getDirection()
if ds.getDirection() != 'N':
    directkeys.keyPress(ds.getControls()['up'])
controls = ds.getControls()

while ds.getInBattle() == False:
    toolkit.takeScreenshot()

    if ds.getWalking() == False and ds.getInBattle() == False:
        walk()

    if ds.getInBattle() == True:
        # Set to FIGHT cause FIGHT is default and we just started a new battle
        ds.setBattleOption('FIGHT')
        loadPokemon()
        checkShiny()
        leaveBattle()