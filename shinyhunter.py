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

# TODO: You can only start the script walk script with your character facing north
# Use openCV to solve this. Check which direction the character is facing and adjust the walk script for that direction
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
    directkeys.keyPress(0x10)
    
    ds.incrEncounterCount()
    print('Pokemons encountered: ' + str(ds.getEncounterCount()))
    # User will throw Pokeball on battlefield
    time.sleep(4)

def leaveBattle():
    ds.setCanEscape(False)
    
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    currentHealth, maxHealth = ocr.ocr('health', img).split(' ')
    ds.setCurrentHealth(int(currentHealth))
    ds.setMaxHealth(int(maxHealth))

    if int(ds.getCurrentHealth()) < math.floor(int(ds.getMaxHealth()) / 2):
        usePotion()
    
    moveToBattleOption(ds.getBattleOption(), 'RUN')

    # Press A to leave
    # Press RUN
    while ds.getCanEscape() == False:
        # Make sure we are our battleOption is RUN, if not move to RUN
        if ds.getBattleOption() == 'RUN':
            directkeys.keyPress(0x10)
        else:
            moveToBattleOption(ds.getBattleOption(), 'RUN')
            directkeys.keyPress(0x10)

        time.sleep(1.5)

        # We just tried to run, we need to take a screenshot to know if we have can leave safely
        toolkit.takeScreenshot()
        img = ds.getScreenshot()
        text = ocr.ocr('chat', img)
        # If we can't leave we will have to text 'Can't escape' 
        if 'escape' not in text:
            ds.setCanEscape(True)
            # Press A to dismiss text
            directkeys.keyPress(0x10)
            break
        else:
            ds.setCanEscape(False)
            # Press A to dismiss text
            directkeys.keyPress(0x10)
        # Enemy will do attack
        time.sleep(5)
    time.sleep(3)

    ds.setInBattle(False)

def getHeading():
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    centerPixel = img[282][367]
    color = str(centerPixel[2]) + str(centerPixel[1]) + str(centerPixel[0])
    if color == '1044040':
        ds.setHeading('N')
    elif color == '16812064':
        ds.setHeading('E')
    elif color == '5656120':
        ds.setHeading('S')
    elif color == '216144112':
        ds.setHeading('W')

def moveToBattleOption(currentPosition, newPosition):
    # FIGHT > BAG
    if currentPosition == 'FIGHT' and newPosition == 'BAG':
        # Move right
        directkeys.keyPress(0x20)
        ds.setBattleOption('BAG')
    # FIGHT > RUN
    if currentPosition == 'FIGHT' and newPosition == 'RUN':
        # Move down
        directkeys.keyPress(0x1F)
        # Move right
        directkeys.keyPress(0x20)
        ds.setBattleOption('RUN')
    # FIGHT > POKEMON
    if currentPosition == 'FIGHT' and newPosition == 'POKEMON':
        # Move down
        directkeys.keyPress(0x1F)
        ds.setBattleOption('POKEMON')

    # POKEMON > BAG
    if currentPosition == 'POKEMON' and newPosition == 'BAG':
        # Move right
        directkeys.keyPress(0x20)
        # Move up
        directkeys.keyPress(0x11)
        ds.setBattleOption('BAG')
    # POKEMON > RUN
    if currentPosition == 'POKEMON' and newPosition == 'RUN':
        # Move right
        directkeys.keyPress(0x20)
        ds.setBattleOption('RUN')
    # POKEMON > FIGHT
    if currentPosition == 'POKEMON' and newPosition == 'FIGHT':
        # Move up
        directkeys.keyPress(0x11)
        ds.setBattleOption('FIGHT')

    # RUN > BAG
    if currentPosition == 'RUN' and newPosition == 'BAG':
        # Move up
        directkeys.keyPress(0x11)
        ds.setBattleOption('BAG')
    # RUN > POKEMON
    if currentPosition == 'RUN' and newPosition == 'POKEMON':
        # Move left
        directkeys.keyPress(0x1E)
        ds.setBattleOption('POKEMON')
    # RUN > FIGHT
    if currentPosition == 'RUN' and newPosition == 'FIGHT':
        # Move left
        directkeys.keyPress(0x1E)
        # Move up 
        directkeys.keyPress(0x11)
        ds.setBattleOption('FIGHT')

    # BAG > RUN
    if currentPosition == 'BAG' and newPosition == 'RUN':
        # Move down
        directkeys.keyPress(0x1F)
        ds.setBattleOption('RUN')
    # BAG > POKEMON
    if currentPosition == 'BAG' and newPosition == 'POKEMON':
        # Move down
        directkeys.keyPress(0x1F)
        # Move left
        directkeys.keyPress(0x1E)
        ds.setBattleOption('POKEMON')
    # BAG > FIGHT
    if currentPosition == 'BAG' and newPosition == 'FIGHT':
        # Move left
        directkeys.keyPress(0x1E)
        ds.setBattleOption('FIGHT')
    
# TODO: support for left and right, now there is only support for up and down
def walk():

    getHeading()

    ds.setWalking(True)

    # Sleep for 0.2 seconds every step
    # Decreasing the sleep time even more will make the steps innacurate
    time.sleep(.25)

    if ds.getWalkPosition() >= (ds.getWalkRange() * 2 + 2):
        ds.setWalkPosition(0)

    if ds.getWalkPosition() > ds.getWalkRange():
        directkeys.keyPress(0x11)
        ds.incrWalkPosition()
        
    if ds.getWalkPosition() <= ds.getWalkRange():
        directkeys.keyPress(0x1F)
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

def usePotion():
    #TODO: Make sure we have a potion in our bag, if not exit the script

    moveToBattleOption(ds.getBattleOption(), 'BAG')
    # Press A (Q)
    directkeys.keyPress(0x10)
   
    # We are now in the bag
    time.sleep(1)
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    bagName = ocr.ocr('bagname', img)

    # Check if we are on the right page, we need to be on the ITEMS page
    if bagName == 'ITEMS':
        # Press arrow up
        directkeys.keyPress(0x11)
    elif bagName == 'KEY ITEMS':
        # Press A to move to left in the bag
        directkeys.keyPress(0x1E)
        # Press arrow up
        directkeys.keyPress(0x11)
    elif bagName == 'POKé BALLS':
        # Press A to move to left in the bag
        directkeys.keyPress(0x1E)
        # Press A to move to left in the bag
        directkeys.keyPress(0x1E)
        # Press arrow up
        directkeys.keyPress(0x11)

    # Press A to select
    directkeys.keyPress(0x10)
    time.sleep(1)

    # Press A to use
    directkeys.keyPress(0x10)
    time.sleep(1)

    # Press A to use on Pokemon
    directkeys.keyPress(0x10)   
    time.sleep(5)

    # Press A again to dismiss chat message
    directkeys.keyPress(0x10)

    # Time sleep couple of seconds for the enemy to do a attack
    time.sleep(10)
    # moveToBattleOption(ds.getBattleOption(), 'FIGHT')

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