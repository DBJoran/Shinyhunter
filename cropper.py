import math
import cv2

# @mode, either 'health', 'chat', 'pokemon' or 'bagname'
# chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
# health, the box where your POKéMONS health will be displayed
# pokemon, the box where the name of the POKéMON you are battling against is displayed
# bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS
# @img, the full image taken by the screenshot function
def crop(mode, img):
    height, width = img.shape[:2]
    croppedImg = []

    if mode == 'health':
        lineHealth = img[math.floor(height / 2 + 70): (height - 170), math.floor(width / 2  + 55): (width - 60)]
        croppedImg.append(lineHealth)
        return croppedImg
    elif mode == 'chat':
        # Crop first and second chat line
        lineOne = img[math.floor(height / 2 + 145): (height - 80), 35: (width - 35)]
        lineTwo = img[math.floor(height / 2 + 190): (height - 35), 35: (width - 35)]
        croppedImg.extend([lineOne, lineTwo])
        return croppedImg
    elif mode == 'pokemon':
        lineName = img[100: math.floor(height / 2 - 125), 50: math.floor(width / 2 - 105)]
        croppedImg.append(lineName)
        return croppedImg
    elif mode == 'bagname':
        bagName = img[75: math.floor(height / 2) - 150, 30: math.floor(width / 2) - 120]
        croppedImg.append(bagName)
        return croppedImg
    else:
        raise ValueError('Unsupported crop mode.')

