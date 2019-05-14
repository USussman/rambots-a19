import cv2
import numpy as np
import multiprocessing as mp
import imutils
from .distance import distance, distance2


# TODO : test with new height dewarping for reimplementing accurate center distance

class Camera:
    """
    A class for interfacing with camera for 360 view.

    Attributes
    ----------
    direction : mp.Value float
        direction of ball in radians
    distance : mp.Value float
        distance to ball in (insert units)
    b_location : mp.Array int 2
        ball location absolute coordinate (experimental)
    location : mp.Array int 2
        robot location absolute coordinates (experimental)
    process : mp.Process
        multiprocessing Process object for object position evaluation loop
    """

    def __init__(self):
        """
        Initializes class attributes.

        Creates shared memory variables to allow for access to specific
        information inside and outside of the image evaluation process loop.
        Initializes camera object and loads maps.
        Creates and starts image evaluation process loop.
        """

        # Create shared memory variables
        # ball info
        self._radius = mp.Value('d')
        self._center = mp.Array('i', 2)
        self.direction = mp.Value('d')
        self.distance = mp.Value('d')
        self.b_location = mp.Array('i', 2)

        # other markers
        self._goal = mp.Array('i', 2)
        self._circles = mp.Array('i', 2)
        self.location = mp.Array('i', 2)
        self.goal_behind = mp.Value('i', 0)

        # camera object
        self._cam = cv2.VideoCapture()

        # Load maps for dewarping
        maps = np.load('maps.npz')
        self._xmap = maps['xmap']
        self._ymap = maps['ymap']
        
        # Create and start process
        self.process = mp.Process(target=self._handler)
        self.process.start()

    def _handler(self):
        """
        Loop to look for objects in image to find ball and position.
        """

        # Evaluate and store ball info
        while True:
            raw = self._cam.read()[1]
            dewarped = cv2.remap(raw, self._xmap, self._ymap, cv2.INTER_LINEAR)
            #self._location(dewarped)
            self._ball(dewarped)

    def _location(self, frame):
        """
        Find absolute position of robot on the field.

        Gets y coordinate from polar with goals. (centroid of border with turf)
        Get x coordinate from polar with reference circles on sides of field.
        (centroid of color mask)

        :param frame: frame from camera
        :return: saves location to shared memory
        """

        # convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Color ranges for masks
        lower_white = (0, 0, 190)
        upper_white = (180, 90, 255)

        lower_blue = (96, 70, 40)
        upper_blue = (107, 256, 256)

        lower_yellow = (20, 100, 100)
        upper_yellow = (30, 255, 255)

        lower_green = (30, 75, 105)
        upper_green = (86, 256, 256)

        lower_magenta = (145, 153, 204)
        upper_magenta = (155, 255, 255)

        black_img = lambda: np.zeros((img.shape[0], img.shape[1]), np.uint8)

        # create masks
        turf_mask = cv2.inRange(hsv.copy(), lower_green, upper_green)
        line_mask = cv2.inRange(hsv.copy(), lower_white, upper_white)
        goal_mask = cv2.inRange(hsv.copy(), lower_blue, upper_blue)
        circle_mask = cv2.inRange(hsv.copy(), lower_magenta, upper_magenta)

        # turf contours
        turf_contours = imutils.grab_contours(cv2.findContours(turf_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
        turf_contours_img = cv2.drawContours(black_img(), turf_contours, -1, (255, 255, 255), 5)

        # goal contours
        goal_contours = imutils.grab_contours(cv2.findContours(goal_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
        goal_contours_img = cv2.drawContours(black_img(), goal_contours, -1, (255, 255, 255), 20)

        # circle contours
        circle_contours = imutils.grab_contours(cv2.findContours(circle_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE))
        circle_contours_img = cv2.drawContours(black_img(), circle_contours[0], -1, (255, 255, 255), 5)

        comb_img = cv2.bitwise_and(turf_contours_img, goal_contours_img)

        # find centroid of goal
        M = cv2.moments(comb_img)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        rho = distance(cy)
        theta = (cx / img.shape[1]) * (2 * np.pi)

        y = rho * np.sin(theta)

        self._goal[:] = cx, cy

        # find centroid of circles
        M = cv2.moments(circle_contours_img)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        self._circles[:] = cx, cy

        rho = distance2(cy)
        theta = (cx / img.shape[1]) * (2 * np.pi)

        x = rho * np.cos(theta)

        self.location[:] = x, y

    def _ball(self, frame, mode=False):
        """
        Variable method for finding ball

        :param frame: frame array from camera
        :param mode: True=_three_point_method False=_centroid
        """

        if mode:
            self._three_point_method(frame)
        else:
            self._centroid(frame)

    def _centroid(self, frame):
        """
        Finds ball location and stores to shared memory.

        Gets location of ball from centroid of visible color.

        :param frame: dewarped numpy array image to find ball in
        :return: stores ball location to shared memory
        """

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

        M = cv2.moments(ball_mask)

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # Calculate direction of ball
        theta = (cx/w) * (2 * np.pi)
        rho = distance(cy)

        x, y = rho * np.cos(theta), rho * np.sin(theta)

        # save results
        self._radius.value = r
        self.direction.value = theta
        self._center[:] = [cx, cy]

        self.b_location[0] = self.location[0] - x
        self.b_location[1] = self.location[1] - y

    def _three_point_method(self, frame):
        """
        Get location of ball on field.

        Finds 3 points on ball then calculates intersection of perpendicular
        bisectors of chords between them.

        :return: stores to shared memory
        """

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
        rho = distance(cy)

        x, y = rho * np.cos(theta), rho * np.sin(theta)

        # save results
        self._radius.value = r
        self.direction.value = theta
        self.distance.value = rho
        self._center[:] = [cx, cy]

        self.b_location[0] = self.location[0] - x
        self.b_location[1] = self.location[1] - y
