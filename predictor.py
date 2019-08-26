import cv2
import math
import pandas as pd
import numpy as np
import os

# load our finalClassifier and finalScaler
from sklearn.externals import joblib

finalClassifier = joblib.load('./finalClassifier.joblib')
finalScaler = joblib.load('./finalScaler.joblib')

# Get all white pixels
def getPixels(img, side):
    height, width = img.shape[:2]
    if side is 'all':
        img = img
    elif side is 'top':
        img = img[0: int(math.floor(height / 2)), 0: width]

    elif side is 'bottom':
        img = img[int(math.floor(height / 2)): height, 0: width]

    elif side is 'right':
        img = img[0: height, int(math.floor(width / 2)): width]

    elif side is 'left':
        img = img[0: height, 0: int(math.floor(width / 2))]
    
    flatImg = img.flatten()
    
    count = list(filter(lambda x: x == 255, flatImg))

    return len(count)

def getCorners(img):
    corners = cv2.goodFeaturesToTrack(img, 2000, 0.02, 0)

    if corners is None:
        return 0
    else:
        corners = np.int0(corners)
        return len(corners)

def getHeight(img):
    height, width = img.shape[:2]
    return height

def getWidth(img):
    height, width = img.shape[:2]
    return width

# Returns csv with all features
def getFeatures(img):
    dataList = []

    # data = [getPixels(thresh), getTopPixels(thresh), getBottomPixels(thresh), getRightPixels(thresh), getLeftPixels(thresh), getCorners(thresh)]
    data = [getPixels(img, 'all'), getPixels(img, 'top'), getPixels(img, 'bottom'), getPixels(img, 'right'), getPixels(img, 'left'), getHeight(img), getWidth(img), getCorners(img)]
    dataList.append(data)
    
    return dataList

# function to get features from the selected image 
# and based on our scaler and classifier do a prediction what the character in the image is
def predictSelectedImage(img):
    if img is None:
        print('No img given')
        return
    
    # get the features of the selected image
    dfFeatures = pd.DataFrame(getFeatures(img)) 
    
    # transform the features use our scaler
    X = finalScaler.transform(dfFeatures)

    # use our classifier to predict the data
    prediction = finalClassifier.predict(X)

    # print('Prediction: ', prediction)
    # print('Answer: ', label)
    return prediction[0]
