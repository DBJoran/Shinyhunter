import math
import cv2

"""
This function will crop a screenshot to your preferred area. The preferred area is decided by the mode that you use.

The following modes can be used:
- chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
- health, the box where your POKéMONS health will be displayed
- pokemon, the box where the name of the POKéMON you are battling against is displayed
- itemname, the area inside the bag where the itemname is displayed e.g. POTION, BERRY JUICE, ANTIDOTE
    itemname1 is the first item on display, itemname2 is the second item on display etc.
- bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS

Parameters
----------
mode : string
    mode, either 'chat', 'health', 'pokemon', 'itemname', 'bagname'

img : numpy array
    The screenshot that has just been taken. The screenshot now needs to be processed.

Returns
-------

img: numpy array
    The cropped screenshot. Ready for OCR.
"""
# @mode, either 'health', 'chat', 'pokemon' or 'bagname'
# chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
# health, the box where your POKéMONS health will be displayed
# pokemon, the box where the name of the POKéMON you are battling against is displayed
# bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS
# @img, the full image taken by the screenshot function

def crop(mode, img):
    height, width = img.shape[:2]

    if mode == 'health':
        health = img[math.floor(height / 2 + 70): (height - 170), math.floor(width / 2  + 55): (width - 60)]
        return [health]
    elif mode == 'chat':
        # Crop first and second chat line
        chatLineOne = img[math.floor(height / 2 + 145): (height - 80), 35: (width - 35)]
        chatLineTwo = img[math.floor(height / 2 + 190): (height - 35), 35: (width - 35)]
        return [chatLineOne, chatLineTwo]

    elif mode == 'pokemon':
        pokemonName = img[100: math.floor(height / 2 - 125), 50: math.floor(width / 2 - 105)]
        return [pokemonName]

    elif mode == 'bagname':
        bagName = img[75: math.floor(height / 2) - 150, 30: math.floor(width / 2) - 120]
        return [bagName]

    # Special crop modes here for the itemnames in the bag.
    elif mode == 'itemname1':
        itemname1 = img[86: 120 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname1]

    elif mode == 'itemname2':
        itemname2 = img[134: 168 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname2]

    elif mode == 'itemname3':
        itemname3 = img[181: 215 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname3]

    elif mode == 'itemname4':
        itemname4 = img[230: 260 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname4]

    elif mode == 'itemname5':
        itemname5 = img[280: 310 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname5]

    elif mode == 'itemname6':
        itemname6 = img[328: 358 , math.floor(width / 2 - 75): (width - 135)]
        return [itemname6]

    else:
        raise ValueError('Unsupported crop mode.')

