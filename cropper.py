import math
import cv2

# @mode, either 'health', 'chat', 'pokemon' or 'bagname'
# chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
# health, the box where your POKéMONS health will be displayed
# pokemon, the box where the name of the POKéMON you are battling against is displayed
# bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS
# @img, the full image taken by the screenshot function

# TODO: Can I return the images without having to append to an array?
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

    # Special crop modes here for the itemnames in the bag.
    elif mode == 'itemname1':
        itemname1 = img[86: 120 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname1)
        return croppedImg

    elif mode == 'itemname2':
        itemname2 = img[134: 168 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname2)
        return croppedImg

    elif mode == 'itemname3':
        itemname3 = img[181: 215 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname3)
        return croppedImg

    elif mode == 'itemname4':
        itemname4 = img[230: 260 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname4)
        return croppedImg

    elif mode == 'itemname5':
        itemname5 = img[280: 310 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname5)
        return croppedImg

    elif mode == 'itemname6':
        itemname6 = img[328: 358 , math.floor(width / 2 - 75): (width - 135)]
        croppedImg.append(itemname6)
        return croppedImg

    # Crops all the possible positions of our item selection arrow
    #   POTION
    #   ANTIDOTE
    # > BURN HEAL
    #   PARALYZ HEAL
    # In return we get 6 images cropped images, only 1 image contains the arrow.
    elif mode == 'itemarrow':
        arrow = img[85: 360 , math.floor(width / 2 - 95): 299]
        arrow0 = img[85: 117 , math.floor(width / 2 - 95): 299]
        arrow1 = img[132: 164 , math.floor(width / 2 - 95): 299]
        arrow2 = img[181: 213 , math.floor(width / 2 - 95): 299]
        arrow3 = img[228: 260 , math.floor(width / 2 - 95): 299]
        arrow4 = img[277: 309 , math.floor(width / 2 - 95): 299]
        arrow5 = img[324: 356 , math.floor(width / 2 - 95): 299]
        croppedImg.extend([arrow0, arrow1, arrow2, arrow3, arrow4, arrow5])
        return croppedImg

    else:
        raise ValueError('Unsupported crop mode.')

