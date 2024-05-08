import cv2
import numpy as np 
from hsv_range_finder import get_limits
from PIL import Image

def nothing(x):
    pass

blue=[255,37,0]
brown = [19,69,139]
red = [0,0,255]
white = [255,255,255]
orange = [0,255,255]
cap = cv2.VideoCapture(0)
#cv2.namedWindow("trackbar")
#cv2.createTrackbar("B","trackbar",0,255,nothing)
#cv2.createTrackbar("G","trackbar",0,255,nothing)
#cv2.createTrackbar("R","trackbar",0,255,nothing)

while True:
    ret , frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #b = cv2.getTrackbarPos("B","trackbar")
    #g = cv2.getTrackbarPos("G","trackbar")
    #r = cv2.getTrackbarPos("R","trackbar")
    #blue=[b,g,r]

    lowerLimit , upperLimit = get_limits(color=red)
    mask = cv2.inRange(frame_hsv,lowerLimit,upperLimit)
    contours , empty = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area  = cv2.contourArea(cnt)
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        X = approx.ravel()[0]
        Y = approx.ravel()[1]

        if area > 400:
            if(len(approx)>9):
                mask_ = Image.fromarray(mask)
                bbox = mask_.getbbox()
                if bbox is not None:
                    x1, y1, x2, y2 = bbox
                    frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)
                    # x = int((x2+x1)/2)
                    # y = int((y2+y1)/2)
                    # cv2.circle(frame,(x,y),int(x/2),(0,0,255),3)
        



    cv2.imshow("Original Video",frame)
    cv2.imshow("Mask",mask)


    if(cv2.waitKey(1) & 0xFF == ord("q")):
        break

cap.release()
cv2.destroyAllWindows()