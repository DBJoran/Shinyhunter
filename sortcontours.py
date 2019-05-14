# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

#Source https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/
def sortContours(contours):
	#TODO: Check out if this 'i' var is needed
	i = 0

	# construct the list of bounding boxes and sort them from left to right
	boundingBoxes = [cv2.boundingRect(c) for c in contours]
	(contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes),
		key=lambda b:b[1][i], reverse=False))
 
	# return the list of sorted contours and bounding boxes
	return (contours, boundingBoxes)