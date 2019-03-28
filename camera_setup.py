import cv2
import numpy as np
import time

vals = list()

# create map for dewarp
def build_map(Wd,Hd,R1,R2,Cx,Cy):
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
def create_dewarp_map(img=cv2.VideoCapture(0).read()[1]):
    # Set up window
    global vals
    cv2.namedWindow('disp', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('disp', 800, 600)
    cv2.setMouseCallback('disp', get_pts)
    
    # Load video
    #vc = cv2.VideoCapture(0)
    
    # Allow camera to warm up
    time.sleep(1)

    # Show the user a frame let them left click the center
    # of the "donut" and the right inner and outer edge
    # in that order. Press any key to exit the display
    #img = vc.read()[1]
    cv2.imshow('disp', img)
    cv2.waitKey(0)
    #vc.release()
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
    xmap,ymap = build_map(Wd,Hd,R1,R2,Cx,Cy)
    #return xmap, ymap

    # save map to file
    np.savez("maps.npz", xmap=xmap, ymap=ymap)

if __name__ == '__main__':
    create_dewarp_map()