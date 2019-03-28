#!/usr/bin/env python3

import cv2
import imutils
import numpy as np
import timeit

def main():
    img = cv2.imread('constants/easytofind.jpeg', -1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_blue = (96, 70, 40)
    upper_blue = (107, 256, 256)

    lower_green = (20, 20, 20)
    upper_green = (86, 256, 256)

    goal_mask = cv2.inRange(hsv.copy(), lower_blue, upper_blue)
    turf_mask = cv2.inRange(hsv.copy(), lower_green, upper_green)

    goal_contours = imutils.grab_contours(cv2.findContours(goal_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))

    h, w, *_ = img.shape

    black_img = lambda: np.zeros((h, w), np.uint8)

    goal_contours_img = cv2.drawContours(black_img(), goal_contours, -1, (255, 255, 255), 20)
    turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 20)

    # Get the shared edges of goal and turf
    comb_contours_img = cv2.bitwise_and(goal_contours_img, turf_mask)
    comb_contours = imutils.grab_contours(cv2.findContours(comb_contours_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    img = cv2.cvtColor(comb_contours_img, cv2.COLOR_BAYER_BG2BGR)

    cnt = cv2.findContours(comb_contours_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(cnt)
    rows,cols = img.shape[:2]
    print(cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01))
    [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
    lefty = int((-x*vy/vx) + y)
    righty = int(((cols-x)*vy/vx)+y)
    cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)


    cv2.imshow('img', img)
    #cv2.imshow('goal_contours_img', goal_contours_img)
    # cv2.imshow('turf_contours_img', turf_contours_img)
    #cv2.imshow('turf_mask', turf_mask)
    #cv2.imshow('goal_mask', goal_mask)
    cv2.waitKey(10000000)
if __name__ == '__main__':
    main()