import cv2
import imutils
import numpy as np
#from Classes.distance import distance

def ball(frame):

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

    # Calculate slopes of perpendicular bisectors
    m1 = -(x2 - x1) / (y2 - y1)
    m2 = -(x3 - x2) / (y3 - y2)

    # Calculate midpoints of both chords, to find
    # the y-intercepts of the perp bisectors
    xp1 = (x2 + x1) / 2
    yp1 = (y2 + y1) / 2
    xp2 = (x2 + x3) / 2
    yp2 = (y2 + y3) / 2

    # Calculate y-intercepts of perp bisectors
    b1 = yp1 - m1*xp1
    b2 = yp2 - m2*xp2

    # Center
    cx = (b2 - b1) / (m1 - m2)
    cy = m1*cx + b1

    # Radius
    r = np.hypot(cx-x1, cy-y1)

    # Calculate direction of ball
    theta = (cx/w) * (2 * np.pi)
    #rho = distance(cy)

    #x, y = rho * np.cos(theta), rho * np.sin(theta)
    
    cv2.circle(img, (int(cx), int(cy)), 10, (255, 255, 255))
    cv2.imshow('ball', img)
    cv2.waitKey(0)

    # save results
    return r, theta, (cx, cy)

img = cv2.imread('constants/easytofind.jpeg', -1)
print(ball(img))
