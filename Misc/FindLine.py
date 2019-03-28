#!/usr/bin/env python3

import cv2
import imutils
import numpy as np
from statistics import median

def main():
    # import image and crop to field height
    img = cv2.imread('constants/easytofind.jpeg', -1)
    shape = img.shape
    img = img[55:shape[0], :]

    # crop direction, convert to HSV
    right = img[:, int(shape[1]*1/4):int(shape[1]*2/4)]
    hsv = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)

    # Color ranges for masks
    lower_white = (0, 0, 190)
    upper_white = (180, 90, 255)

    lower_green = (20, 20, 20)
    upper_green = (86, 256, 256)
    
    shape = right.shape

    black_img = lambda: np.zeros((shape[0], shape[1]), np.uint8)

    # create masks
    turf_mask = cv2.inRange(hsv.copy(), lower_green, upper_green)
    line_mask = cv2.inRange(hsv.copy(), lower_white, upper_white)
    
    # get contours
    turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 5)

    comb_contours_img = cv2.bitwise_and(turf_contours_img, line_mask)

    green_white = cv2.bitwise_and(line_mask, turf_mask)

    # find centroid
    M = cv2.moments(green_white)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(right, (cx, cy), 10, (255, 0, 0))

    # display results
    cv2.imshow('img', right)
    
    cv2.waitKey(0)

if __name__ == '__main__':
    main()