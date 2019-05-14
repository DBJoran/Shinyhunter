import predictor
import cv2
import math
import sortcontours
import cropper

#IMPORTANT: Q does not work properly, this is caused by the fact that the Q is very close to the following character
#e.g. QR will be seen as one 'character', we can't do predictions on this 'character'

# @mode, either 'health', 'chat', 'pokemon' or 'bagname'
# chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
# health, the box where your POKéMONS health will be displayed
# pokemon, the box where the name of the POKéMON you are battling against is displayed
# bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS
# @img, the full image taken by the screenshot function
def ocr(mode, img):
    processQueue = cropper.crop(mode, img)
    text = ''

    for i in range(0, len(processQueue)):
        img = processQueue[i]
        height, width = img.shape[:2]
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = thresholdImage(mode, imgray)
        # ret,thresh = cv2.threshold(imgray,127,255,thresholdType)
        im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours from left to right if we have found any contours
        if len(contours) != 0:
            cnts, boundingBoxes = sortcontours.sortContours(contours)
            # We know we got more letters (contours) coming so we add a space for the letters on the next line
            # Add a space if it's not the first line we are processing
            if text != '':
                text = text + ' '
        else:
            return text

        if mode == 'chat':
            boundingBoxes = cleanBoundingBoxes(boundingBoxes)

        for j in range(0, len(boundingBoxes)):
            floating = False
            rect1 = boundingBoxes[j]
            #TODO: rect2 is only used for x2, for spaceRequired() can we decide spaces differently so we can remove the rect2 var
            rect2 = None
            area = rect1[2] * rect1[3]
            # Filter out the small dots
            # Filter out the arrow down character
            if area < 10 or rect1[2] > 20 : continue
            x1,y1,w1,h1 = rect1

            if j == len(boundingBoxes) - 1:
                rect2 = None
            else:
                rect2 = boundingBoxes[j + 1]
                x2,y2,w2,h2 = rect2               
            # cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(0,255,0),1)
            contour = thresh[y1:y1+h1, x1:x1+w1]
            
            # Check if the contours are above the half of the image
            # The y coordinate starts at the top and ends at the bottom
            # e.g. y top will be 0, y bottom will be 45
            if y1 < math.floor(height / 2):
                floating = True
            else:
                floating = False

            prediction = predictor.predictSelectedImage(contour)

            if prediction == ',' and floating == True:
                prediction = "'"

            # This is used for the special characters used only in the POKéMON names during battle
            # all the characters have 'po' at the beginning to mark that they are the characters from the POKéMON names 
            if 'po' in prediction:
                prediction = prediction[-1]

            # The 0 and O have the exact same features. (Thanks Gamefreak for making such unique fonts...)
            if prediction == '0' and mode == 'pokemon':
                prediction = 'O'

            if prediction == 'O' and mode == 'health':
                prediction = '0'

            # Finding the contours of the / is not as predictable as expected, sometimes it's contours will be found and sometimes not
            # Made the decision to add a empty string to the prediction if we get a /
            # We need this to work properly for the health
            if prediction == '/':
                prediction = ''
            
            text = text + prediction

            # Sometimes we get the following error: 'local variable 'x2' referenced before assignment'
            if type(rect2) != None:
                if spaceRequired(x1,w1,x2) == True:
                    text = text + ' '
    # if text == '':
        # raise ValueError('No text found. Are you sure you are using the correct mode?')
    return text

def spaceRequired(x1, w1, x2):
    difference = x2 - (x1 + w1)
    if difference > 10:
        return True
    else: 
        return False

def cleanBoundingBoxes(boundingBoxes):
    # Fixes 'e' to 'é'
    # Fixes '!' and '?'
    bbList = list(boundingBoxes)
    for k in range(0, len(boundingBoxes)):

        #TODO: Check this statement, If im correct this statement is never reached cause it already exits the loop at (k - 1)
        if k == len(boundingBoxes):
            return boundingBoxes

        rect1 = boundingBoxes[k]
        rect2 = None
        x1,y1,w1,h1 = rect1

        if k == len(boundingBoxes) - 1:
            rect2 = None
            return boundingBoxes
        else:
            rect2 = boundingBoxes[k + 1]

        x2,y2,w2,h2 = rect2
        xDif = x2 - x1
        yDif = y2 - y1

        # Check if we have a 'é, !'
        if xDif == 3 or xDif == 0 and y1 > y2 and h1 < h2:
            newRect = (x1, y2, w1, (y1 + h1) - y2)
            bbList[k] = (newRect)
            del bbList[k + 1]
            boundingBoxes = tuple(bbList)

        # Check if we have a '?'
        if xDif == 6 and yDif == 24:
            newRect = (x1, y1, w1, (y1 + h1) + h2)
            bbList[k] = (newRect)
            del bbList[k + 1]
            boundingBoxes = tuple(bbList)
                
        # Check if we have 'i'
        if xDif == 0 and yDif == -9:
            newRect = (x2, y2, w1, (y1 + h1) - y2)
            bbList[k] = (newRect)
            del bbList[k + 1]
            boundingBoxes = tuple(bbList)

        # Check if we have 'j'
        if xDif == 9 and yDif == -9:
            newRect = (x1, y2, w1, (y1 + h1) - y2)
            bbList[k] = (newRect)
            del bbList[k + 1]
            boundingBoxes = tuple(bbList)
    return boundingBoxes

# @mode, the mode of the OCR
# @img, the cropped grayscale image
def thresholdImage(mode, img):
    if mode == 'chat':
        pixel = img[6][12]
        if pixel > 127:
            return cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)            
        else:
            return cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    elif mode == 'health' or mode == 'pokemon':
        return cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    elif mode == 'bagname':
        return cv2.threshold(img,203,255,cv2.THRESH_BINARY)