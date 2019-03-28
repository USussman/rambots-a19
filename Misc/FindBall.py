import cv2
import numpy as np
import imutils

# img = cv2.imread('/Users/Benjy/WorkSpace/Robotics 2019/OrangeBallTurf1.png', cv2.IMREAD_UNCHANGED)
#img = cv2.imread('/Users/Benjy/WorkSpace/Robotics 2019/OrangeBallTurfOccluded3.png', cv2.IMREAD_UNCHANGED)
img = cv2.imread('constants/easytofind.jpeg', -1)
img = cv2.medianBlur(img, 5)
# cv2.imshow('img', img)
# cv2.waitKey(100000)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_orange = (2, 128, 128)
upper_orange = (15, 255, 255)

lower_green = (40, 20, 20)
upper_green = (66, 256, 256)

ball_mask = cv2.inRange(hsv, lower_orange, upper_orange)
turf_mask = cv2.inRange(hsv, lower_green, upper_green)

# cv2.imshow('img', img)
# cv2.imshow('mask', turf_mask)
# cv2.imshow('res', res)
# cv2.waitKey(100000)

# bgr_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
# bw_res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

h, w, *_ = img.shape

ball_contours = imutils.grab_contours(cv2.findContours(ball_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))

black_img = lambda: np.zeros((h, w), np.uint8)

ball_contours_img = cv2.drawContours(black_img(), ball_contours, -1, (255, 255, 255), 2)
turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 2)

# Get the shared edges of ball and turf
comb_contours_img = cv2.bitwise_and(ball_contours_img, turf_contours_img)

# cv2.imshow('ball_contours_img', ball_contours_img)
# cv2.imshow('turf_contours_img', turf_contours_img)
# cv2.imshow('comb_contours_img', comb_contours_img)
# cv2.waitKey(100000)


# Find all white pixels in combined mask
points = []
for y in range(h):
    for x in range(w):
        if comb_contours_img[y,x] == 255:
            points.append((x,y))

(x1, y1), (x2, y2), (x3, y3) = points[0], points[len(points)//2], points[-1]

cv2.circle(img, (int(x1), int(y1)), 5, (255, 0, 0), 2)
cv2.circle(img, (int(x2), int(y2)), 5, (255, 0, 0), 2)
cv2.circle(img, (int(x3), int(y3)), 5, (255, 0, 0), 2)

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

cv2.circle(img, (int(cx), int(cy)), int(r), (0, 255, 0), 2)
cv2.circle(img, (int(cx), int(cy)), 1, (255, 0, 255), 2)

cv2.imshow('img', img)
cv2.waitKey(100000)