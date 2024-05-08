import cv2
import numpy as np
from utils import *

# cv2.namedWindow("Trackbar")
# cv2.createTrackbar("Threshold1", "Trackbar", 108, 255, empty)
# cv2.createTrackbar("Threshold2", "Trackbar", 255, 255, empty)
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if(ret == 0):
        break
    frame = cv2.flip(frame, 1)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = create_mask("dark_red", frame_hsv)
    contours, empty = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # "cv2.CHAIN_APPROX_SIMPLE" yerine "cv2.CHAIN_APPROX_NONE" kullanabiliriz fakat simple kullanmamiz daha fazla bellek alani sagliyor
    cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)
    if len(contours) != 0:
        for cnt in contours:
            detect_shape(cnt, frame)
    cv2.imshow("Mask",mask)
    cv2.imshow("Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()