import predictor
import cv2
import math
import sortcontours
import cropper

# IMPORTANT: Q does not work properly, this is caused by the fact that the Q is very close to the following character
# e.g. QR will be seen as one 'character', we can't do predictions on this 'character'

"""
Like the function name suggests, this is the most crucial component of the OCR part in this application.

Here we will crop the image to the correct area (the area where the text is where we need to apply OCR on)
After we have cropped the image to the correct area we will try to find all the contours in the image with OpenCV
Then we do a prediction with our model, the prediction from our model is not 100% the expected result thus we 
sometimes need to tweak it a little.

e.g. the font used in Leaf Green / Fire Red uses the same character for '0' and 'O'. So if we get a 'O' prediction when we use the 'health' mode
it must be a '0', health will never be displayed with letters. Same goes for the 'pokemon' mode, a Pokemon will never have a '0' in his name.
Parameters
----------

mode : string
    mode, either 'chat', 'health', 'pokemon', 'itemname', 'bagname'
    chat, the box where you will see 'Got away safely!' etc. This is the box you see when in battle. 
    health, the box where your POKéMONS health will be displayed
    pokemon, the box where the name of the POKéMON you are battling against is displayed
    itemname, the area inside the bag where the itemname is displayed e.g. POTION, BERRY JUICE, ANTIDOTE
    bagname, the box where the name of the bag is displayed. e.g. ITEMS, KEY ITEMS or POKé BALLS

img : numpy array
    The screenshot that has just been taken. The screenshot now needs to be processed.

Returns
-------

text : string
    The final prediction in text.
"""
def ocr(mode, img):
    processQueue = cropper.crop(mode, img)
    text = ''

    for i in range(0, len(processQueue)):
        img = processQueue[i]
        height, width = img.shape[:2]
        imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = thresholdImage(mode, imgray)
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
            # e.g: if we get a prediction like 'poN' we need to remove the 'po' part so we get the actual prediction: 'N'
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

            if type(rect2) == tuple:
                if spaceRequired(x1,w1,x2) == True:
                    text = text + ' '

    return text

"""
Check if we need a space between two different characters, 
if the distance between the two characters is larger then 10 we need a space. 

the distance is calculated by getting the X position (the beginning) from the second character
and calculating the furthest X position (the ending) of the first character. 
When we have those two numbers we can divide them and tell if we need a space or not

Parameters
----------
x1 : int
    The X position from the first character
w1 : int
    The width from the first character
x2 : int
    The X position from the second character

Returns
-------
Boolean
    True if we need a space, False if we don't need a space.
"""
def spaceRequired(x1, w1, x2):
    distance = x2 - (x1 + w1)
    if distance > 10:
        return True
    else: 
        return False

"""
Some characters have more then one bounding box. e.g: '!' has the tall line at the top and the dot at the bottom.
We need to combine those two bounding boxes so we can get one big bounding box on which we can predict.

Parameters
----------
boundingBoxes : list
    A list containing all the bounding boxes that have been found by OpenCV

Returns
-------
boundingBoxes : tuple
    A list containing all the cleaned bounding boxes, ready for prediction
"""
def cleanBoundingBoxes(boundingBoxes):
    # Fixes 'e' to 'é'
    # Fixes '!' and '?'
    # Fixes 'i' and 'j'
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

        # Check if we have a 'é' or a '!'
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
    print(type(boundingBoxes))
    return boundingBoxes

"""
Thresholds the image for the detection of the bounding boxes, depending on the mode (determined by the background color of the text)
it will do a different kind of threshold, so the characters are easily recognizable as bounding boxes.

Parameters
----------

mode : string
    The mode of the OCR e.g: 'chat', 'health', 'pokemon', 'itemname' or 'bagname',
    each of these mode is explained in further detail explained at the OCR function above

img : numpy array
    The image where we will apply the treshold to.
"""
# @mode, the mode of the OCR
# @img, the cropped grayscale image
def thresholdImage(mode, img):

    print(type(img))
    if mode == 'chat':
        pixel = img[6][12]
        if pixel > 127:
            return cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)            
        else:
            return cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    elif mode == 'health' or mode == 'pokemon' or 'itemname' in mode:
        return cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    elif mode == 'bagname':
        return cv2.threshold(img,203,255,cv2.THRESH_BINARY)