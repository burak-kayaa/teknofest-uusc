import cv2
import numpy as np 
import time 
import serial

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
cap = cv2.VideoCapture(0)
canvas = np.zeros((512,512,3),np.uint8)+255
def nothing(x):
    pass


cv2.namedWindow("trackbar_menu")
cv2.createTrackbar("Min_th","trackbar_menu",0,255,nothing)
cv2.createTrackbar("Max_th","trackbar_menu",0,255,nothing)
cv2.setTrackbarPos("Min_th","trackbar_menu",244)
cv2.setTrackbarPos("Max_th","trackbar_menu",255)

while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    frame = cv2.flip(frame,1)
    if(ret == False):
        break

    min_th = cv2.getTrackbarPos("Min_th","trackbar_menu")
    max_th = cv2.getTrackbarPos("Max_th","trackbar_menu")

    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,th = cv2.threshold(frame_gray,min_th,max_th,cv2.THRESH_BINARY)


    M = cv2.moments(th)
    if(M["m00"] != 0):
        X = int(M["m10"]/M["m00"])
        Y = int(M["m01"]/M["m00"])
        cv2.circle(frame,(X,Y),5,(0,0,255),-1)

        print("X ---> "+str(X))
        print("Y ---> "+str(Y))
        if(X<190):
            num = '4' 
        if(X>190 & X<410):
            num = '1'
        if(X>410):
            num = '3'
    else:
        num = '5' 

    arduino.write(bytes(num, 'utf-8'))
        
    #sol 190 - orta 190-410  - sag 


   
    cv2.imshow("original",frame)
    cv2.imshow("th",th)
    if(cv2.waitKey(30) & 0xFF == ord("q")):
        break

cap.release()
cv2.destroyAllWindows()