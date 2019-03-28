#!/usr/bin/env python3

import cv2
import imutils
import numpy as np

def main():
    # import image and crop to field height
    img = cv2.imread('constants/easytofind.jpeg', -1)
    shape = img.shape
    img = img[55:shape[0], :]

    # crop direction, convert to HSV
    right = img[:, int(shape[1]*0/4):int(shape[1]*1/4)]
    hsv = cv2.cvtColor(right, cv2.COLOR_BGR2HSV)

    # Color ranges for masks
    lower_white = (0, 0, 190)
    upper_white = (180, 90, 255)

    lower_blue = (96, 70, 40)
    upper_blue = (107, 256, 256)

    lower_yellow = (20, 100, 100)
    upper_yellow = (30, 255, 255)

    lower_green = (30, 75, 105)
    upper_green = (86, 256, 256)
    
    shape = right.shape

    black_img = lambda: np.zeros((shape[0], shape[1]), np.uint8)

    # create masks
    turf_mask = cv2.inRange(hsv.copy(), lower_green, upper_green)
    line_mask = cv2.inRange(hsv.copy(), lower_white, upper_white)
    goal_mask = cv2.inRange(hsv.copy(), lower_blue, upper_blue)
    
    # turf contours
    turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 5)

    # goal contours
    goal_contours = imutils.grab_contours(cv2.findContours(goal_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    goal_contours_img = cv2.drawContours(black_img(), goal_contours, -1, (255, 255, 255), 20)

    comb_img = cv2.bitwise_and(turf_contours_img, goal_contours_img)

    '''lines = cv2.HoughLines(comb_img,1,np.pi/180,500)
    for [[rho,theta]] in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(right,(x1,y1),(x2,y2),(0,0,255),2)
        cv2.circle(right, (x0, y0), 10, (255, 255, 255))'''
   
    # find centroid
    M = cv2.moments(comb_img)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(right, (cx, cy), 10, (255, 0, 0))

    # display results
    cv2.imshow('img', right)
    cv2.imshow('turf mask', turf_mask)
    cv2.imshow('line mask', line_mask)
    cv2.imshow('goal mask', goal_mask)
    cv2.imshow('turf contours', turf_contours_img)
    cv2.imshow('comb', comb_img)
    
    cv2.waitKey(0)

if __name__ == '__main__':
    main()