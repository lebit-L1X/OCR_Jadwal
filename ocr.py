import pytesseract
import os
import cv2 as cv
import numpy as np

def nothing(x):
    pass

cwd = os.getcwd()
file = "\\siak.png"
img = cv.imread(""+cwd+file)

img_hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)

lower_window = 'HSV Mask Lower'
cv.namedWindow(lower_window, cv.WINDOW_AUTOSIZE)
cv.createTrackbar('H',lower_window,0,179,nothing)
cv.createTrackbar('S',lower_window,0,255,nothing)
cv.createTrackbar('V',lower_window,0,255,nothing)

upper_window = 'HSV Mask Upper'
cv.namedWindow(upper_window, cv.WINDOW_AUTOSIZE)
cv.createTrackbar('H',upper_window,0,179,nothing)
cv.createTrackbar('S',upper_window,0,255,nothing)
cv.createTrackbar('V',upper_window,0,255,nothing)

# cv.imshow('Jadwal',img_hsv)

while (True):

    h_u = cv.getTrackbarPos('H',upper_window)
    s_u = cv.getTrackbarPos('S',upper_window)
    v_u = cv.getTrackbarPos('V',upper_window)

    h_l = cv.getTrackbarPos('H',lower_window)
    s_l = cv.getTrackbarPos('S',lower_window)
    v_l = cv.getTrackbarPos('V',lower_window)

    blue_mask_lower = np.array([h_u,s_u,v_u])
    blue_mask_upper = np.array([h_l,s_l,v_l])
    blue_mask = cv.inRange(img_hsv,blue_mask_lower,blue_mask_upper)
    filtered_image = cv.bitwise_and(img_hsv,img_hsv,mask=blue_mask)
    
    cv.imshow('Mask',blue_mask)
    cv.imshow('Output',filtered_image)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q'):
        print(pytesseract.image_to_string(blue_mask))
        break
    
    