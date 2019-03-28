#!/usr/bin/env python3
"""What does this do?"""

import numpy as np
import cv2
import imutils
import time


# Set library globals

# define the lower and upper boundaries of the
# color of the ball in HSV color space
colorLower = (20, 100, 100)
colorUpper = (30, 255, 255)

# output values for dewarp calibration
vals = list()

# maps
xmap = None
ymap = None

# create map for dewarp
def build_map(Wd,Hd,R1,R2,Cx,Cy):
    """Creates map for dewarp"""
    map_x = np.zeros((int(Hd),int(Wd)),np.float32)
    map_y = np.zeros((int(Hd),int(Wd)),np.float32)
    for y in range(0,int(Hd-1)):
        for x in range(0,int(Wd-1)):
            r = (y/Hd)*(R2-R1)+R1
            theta = (x/Wd)*2.0*np.pi
            xS = Cx+r*np.sin(theta)
            yS = Cy+r*np.cos(theta)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))
        
    return map_x, map_y

# function to capture clicks coordinates
def get_pts(event, x, y, flags, param):
    global vals
    if event == cv2.EVENT_LBUTTONDOWN:
        vals.append((x,y))

# get camera mount info manually input
def getUnwarpDims():
    """So this is what a doc string does."""

    # Set up window
    #global vals
    cv2.namedWindow('disp', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('disp', 800, 600)
    cv2.setMouseCallback('disp', get_pts)
    
    # Load video
    vc = cv2.VideoCapture(0)
    
    # Allow camera to warm up
    time.sleep(1)

    # Show the user a frame let them left click the center
    # of the "donut" and the right inner and outer edge
    # in that order. Press any key to exit the display
    img = vc.read()[1]
    cv2.imshow('disp', img)
    cv2.waitKey(0)
    vc.release()
    cv2.destroyWindow('disp')

    # 0 = xc yc
    # 1 = r1
    # 2 = r2
    # center of the "donut"    
    Cx = vals[0][0]
    Cy = vals[0][1]
    # Inner donut radius
    R1x = vals[1][0]
    R1y = vals[1][1]
    R1 = np.hypot(R1x-Cx, R1y-Cy)
    # outer donut radius
    R2x = vals[2][0]
    R2y = vals[2][1]
    R2 = np.hypot(R2x-Cx, R2y-Cy)
    # our input and output image sizes
    Wd = 2.0*R2*np.pi
    Hd = R2-R1
    Hs, Ws = img.shape[:2]
    
    # build map
    global xmap, ymap
    xmap,ymap = buildMap(Wd,Hd,R1,R2,Cx,Cy)
    return xmap, ymap

# dewarp the image
# calibrate camera if necessary
# FOR TESTING PURPOSES ONLY
# TO BE CHANGED TO READING MAP
# FROM A PRE-WRITTEN CSV FILE
def unwarp(img):
    global xmap, ymap
    if xmap is None or ymap is None:
        xmap, ymap = getUnwarpDims()
    output = cv2.remap(img,xmap,ymap,cv2.INTER_LINEAR)
    return output

# returns center coordinates, radius, direction of ball
# using naive centroid of orange blob
def getCenter(camera, dewarp=1):
    # get frame
    frame = camera.read()[1]
    
    # check if dewarp is set
    if dewarp:
        frame = unwarp(frame)
    
    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    #scale = round(600/frame.shape[1])
    #cv2.resize(frame, 0, frame, scale, scale)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the ball color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnt)

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            return [((int(x), int(y)), int(radius)), center, int(x/frame.shape[1]*360)]
    return "No contour found"

# wrapper on getCenter() for testing
def ballInfo(dewarp=0, camera=None):
    if camera is None:
        camera = cv2.VideoCapture(0)
    while True:
        print(getCenter(camera,dewarp))
        time.sleep(1)

def getGoal(camera, dewarp=1):
    # get frame
    frame = camera.read()[1]
    
    # check if dewarp is set
    if dewarp:
        frame = unwarp(frame)
    
    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    #scale = round(600/frame.shape[1])
    #cv2.resize(frame, 0, frame, scale, scale)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the ball color, then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, colorLower, colorUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnt = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnt)

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        if w > 10:
            return [x, y, w, h, int((x+w/2)/frame.shape[1]*360)]
    return [0,0,0,0,0]

# Find center of ball and radius by intersection
# with the field
# Returns dict with radius and center coordinates
def getCenter1(frame):

    # blur image to get rid of noise
    img = cv2.medianBlur(frame, 5)

    # convert to HSV colorspace for easier masking
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set color Bounds
    lower_orange = (2, 128, 128)
    upper_orange = (15, 255, 255)

    lower_green = (40, 20, 20)
    upper_green = (66, 256, 256)

    # Create Masks
    ball_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    turf_mask = cv2.inRange(hsv, lower_green, upper_green)

    # find contours
    ball_contours = imutils.grab_contours(cv2.findContours(ball_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
    turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))

    # Create blank frame and draw contours onto it
    h, w, *_ = img.shape

    black_img = lambda: np.zeros((h, w), np.uint8)

    ball_contours_img = cv2.drawContours(black_img(), ball_contours, -1, (255, 255, 255), 2)
    turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 2)

    # Get the shared edges of ball and turf
    comb_contours_img = cv2.bitwise_and(ball_contours_img, turf_contours_img)

    # Find all white pixels in combined mask
    points = []
    for y in range(h):
        for x in range(w):
            if comb_contours_img[y,x] == 255:
                points.append((x,y))
    
    # Get 3 points on the circle
    (x1, y1), (x2, y2), (x3, y3) = points[0], points[len(points)//2], points[-1]

    # Draw a cirlce around the points
    #cv2.circle(img, (int(x1), int(y1)), 5, (255, 0, 0), 2)
    #cv2.circle(img, (int(x2), int(y2)), 5, (255, 0, 0), 2)
    #cv2.circle(img, (int(x3), int(y3)), 5, (255, 0, 0), 2)

    # Calculate slopes of perpendicular bisectors
    m1 = -(x2 - x1) / (y2 - y1)
    m2 = -(x3 - x2) / (y3 - y2)

    # Calculate midpoints of both chords, to find
    # the y-intercepts of the perp bisectors
    xp1 = (x2 + x1) / 2
    yp1 = (y2 + y1) / 2
    xp2 = (x2 + x3) / 2
    yp2 = (y2 + y3) / 2

    # cv2.circle(img, (int(xp1), int(yp1)), 5, (0, 0, 255), 2)
    # cv2.circle(img, (int(xp2), int(yp2)), 5, (0, 0, 255), 2)

    # Calculate y-intercepts of perp bisectors
    b1 = yp1 - m1*xp1
    b2 = yp2 - m2*xp2

    # Center
    cx = (b2 - b1) / (m1 - m2)
    cy = m1*cx + b1

    # Radius
    r = np.hypot(cx-x1, cy-y1)

    # Draw center and radius
    #cv2.circle(img, (int(cx), int(cy)), int(r), (0, 255, 0), 2)
    #cv2.circle(img, (int(cx), int(cy)), 1, (255, 0, 255), 2)

    # Show image with markup
    #cv2.imshow('img', img)
    #cv2.waitKey(100000)

    # Calculate direction of ball
    direction = (cx/w) * (2 * np.pi)

    # Return results
    return r, (cx,cy), direction