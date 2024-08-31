import pytesseract
import os
import cv2 as cv
import numpy as np

cwd = os.getcwd()
file = "\\siak.png"
img = cv.imread("" + cwd + file)

cv.namedWindow('Threshold Window',cv.WINDOW_AUTOSIZE)
cv.createTrackbar('Low','Threshold Window',0,255, lambda x: None)
cv.createTrackbar('High','Threshold Window',0,255, lambda x: None)

#optimal for kemjar = 229

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)


while (True):
    low = cv.getTrackbarPos('Low','Threshold Window')
    high = cv.getTrackbarPos('High','Threshold Window')
    retval, thresholded_image = cv.threshold(img_gray, low, high, cv.THRESH_BINARY)
    img_final = thresholded_image
    cv.imshow('Image',img_final)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        print(pytesseract.image_to_string(img_final))
        break
