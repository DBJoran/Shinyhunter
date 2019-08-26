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

# This script is ran at the following settings: 
# Options > Video > x3
# Options > Video > Render Method > Direct 3D
# Options > Gameboy > Real Colors

# Load shinyList
with open('shinylist.json') as f:
    shinyList = json.load(f)
    
"""
===================================================================================
Actual functionality starts here :)
"""

# Find the emulator window, focus the window and set the dimensions in the store
# We need the dimensions for the screenshots
ds.setBbox(toolkit.findWindow())

"""
This function interacts with the loading screen
It waits 4 seconds, after those four seconds it will press the A button to skip the first dialogue

The encounter count will be incremented, after this we will wait another four seconds before we do anything, 
during these four seconds the player will throw his Pokeball on the battlefield
"""
def loadPokemon():
    # Sleep for loading screen
    time.sleep(4)
    # Press A to continue
    directkeys.keyPress(ds.getControls()['gba-a'])
    
    ds.incrEncounterCount()
    print('Pokemons encountered: ' + str(ds.getEncounterCount()))
    # User will throw Pokeball on battlefield
    time.sleep(4)

#TODO: documentation
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

"""
Obtains the direction the user is pointing, by checking the color of a single pixel to see in which direction the user is pointing
The pixel will have a different color for each direction the user is pointing at.

"""
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

"""
When the user is in battle we have four options:
- FIGHT 
- BAG
- POKEMON
- RUN

This function will move the cursor to the correct battle option.
Everytime we move to a new battle option we set the battleOption variable with the current selected battle option
Because we save the current selected battle option everytime we know where the cursor is without having to check it with computer vision

Parameters
----------
currentPosition : string
    The currently selected battle option e.g. 'BAG'

newPosition : string
    The battle option that has to be selected e.g. 'FIGHT'

"""
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

"""
Here we obtain all the information required for the checking of a shiny.
First we take a screenshot and obtain the name of the Pokemon we are battling against.

With this name we obtain the required information from the Shinylist stored in the datastore (ds)

Returns
-------

x : int
    The X coordinates of the pixel we have to check. Each Pokemon has a specific pixel on which we decide if the Pokemon is shiny or not
    e.g. 250

y : int
    The Y coordinates of the pixel we have to check. Each Pokemon has a specific pixel on which we decide if the Pokemon is shiny or not
    e.g. 120

shinyColor : int
    The color the pixel has to be if we have encountered a shiny Pokemon. The color is a RGB value concatted as a int.
    e.g. [168, 152, 88] turns into 16815288
"""
def getPokemonInfo():
    toolkit.takeScreenshot()
    img = ds.getScreenshot()
    pokemonName = ocr.ocr('pokemon',img).lower()
    x = ds.getShinyListX(pokemonName)
    y = ds.getShinyListY(pokemonName)
    shinyColor = ds.getShinyListColor(pokemonName)

    return x, y, shinyColor

"""
Obtains the X coordinate, Y coordinate and the color the pixel has to be.

With the information we have obtained we check at the X and Y coordinate to 
see if the pixel color matches the obtained shinyColor.

If we have a match (a shiny) the script will be executed and the user can catch the Pokemon himself.
"""
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

"""
Will heal your Pokemon. 
We select the bag and go into the bag, after we are in the bag we need to navigate to the right page inside the bag
The bag has several different pages inside it:
- ITEMS
- KEY ITEMS
- POKEMONS
We need to be at the ITEMS page, if we are on any different page we will navigate to the right page.

After we have arrived at the ITEMS page we need to check if our preffered heal item is actually available in our bag
this will be done with the checkItems() function. To see how checkItems() works check out the documentation of that function.

checkItems() now puts the cursor at the right heal item, now we select the item, use the item and use the item on our Pokemon
the game will now display a chat message saying we have healed our Pokemon, we will now dismiss this message.

The final step is to sleep for 10 seconds and let the enemy do his attack.
"""
def healPokemon():
    moveToBattleOption(ds.getBattleOption(), 'BAG')
    # Press A (Q)
    directkeys.keyPress(ds.getControls()['gba-a'])
   
    # We are now in the bag, make sure we have a potion
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
# TODO: Return False if the item has not been found, ALSO UPDATE DOCUMENTATION

""" 
Checks if the passed item is in the bag.
We will need to go to the top of our bag, we actually don't know how many items the users has thus we don't know how many items we need to move up in the bag.
Because we don't know how many items we need to go up in the bag we take the predefined 'bag-items' from the config.yaml. 
The default value is 50, the script will try to move 50 times up to the top off the bag. If you have less items in your bag you can change this value in the config.yaml and the script will be slightly faster.

Scrolling in the bag works on a special way, the first three items will not be in the center of the screen thus we cannot do the same procedure for these items. We will screenshot the item and OCR it
and move on to the next item until we have done the first three. After we have done the first three items we will proceed with the next items.
The next items follow the same procedure, screenshot, crop, ocr and check if the ocr results match the item we will be looking for.
The last three items in the bag will follow the same procedure as the first three items in the bag, the only difference is that the last three items will have a different 
crop mode then the first three items.

If we have found the correct healing item we will return True
Parameters 
----------

item : String
    the item that has to be checked if its in the bag. e.g: Potion, Berry Juice.
    the item has to be a item that can heal a Pokemon.

Returns
-------

Boolean
    True, if we have found the item
"""
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