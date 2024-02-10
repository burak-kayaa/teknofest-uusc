import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow("Trackbar")
cv2.createTrackbar("Lower-Hue"         ,"Trackbar",0,180,nothing)
cv2.createTrackbar("Lower-Saturation"  ,"Trackbar",0,255,nothing)
cv2.createTrackbar("Lower-Value"       ,"Trackbar",0,255,nothing)
cv2.createTrackbar("Upper-Hue"         ,"Trackbar",0,180,nothing)
cv2.createTrackbar("Upper-Saturation"  ,"Trackbar",0,255,nothing)
cv2.createTrackbar("Upper-Value"       ,"Trackbar",0,255,nothing)
font = cv2.FONT_HERSHEY_COMPLEX


while True:
    ret , frame = cap.read()
    frame = cv2.flip(frame,1)
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("Lower-Hue"        ,"Trackbar")
    ls = cv2.getTrackbarPos("Lower-Saturation" ,"Trackbar")
    lv = cv2.getTrackbarPos("Lower-Value"      ,"Trackbar")
    uh = cv2.getTrackbarPos("Upper-Hue"        ,"Trackbar")
    us = cv2.getTrackbarPos("Upper-Saturation" ,"Trackbar")
    uv = cv2.getTrackbarPos("Upper-Value"      ,"Trackbar")

    lower_hsv = np.array([lh,ls,lv])
    upper_hsv = np.array([uh,us,uv])

    mask = cv2.inRange(frame_hsv,lower_hsv,upper_hsv)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel)

    countours,grabe = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in countours:
        area  = cv2.contourArea(cnt)
        epsilon = 0.02*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        
        x = approx.ravel()[0]
        y = approx.ravel()[1]

        if area > 400:
            cv2.drawContours(frame,[approx],0,(0,0,0),2)
            
            if len(approx)==3:
                cv2.putText(frame,"Triangle",(x,y),font,2,(0,0,255))
                
            elif len(approx)==4:
                cv2.putText(frame,"Rectangle",(x,y),font,2,(0,0,255))
                
            elif len(approx)>6:
                cv2.putText(frame,"Circle",(x,y),font,2,(0,0,255))
    M = cv2.moments(mask)
    if(M["m00"] != 0):
        X = int(M["m10"]/M["m00"])
        Y = int(M["m01"]/M["m00"])
        cv2.circle(frame,(X,Y),5,(0,0,255),-1)
        print("X ---> "+str(X))
        print("Y ---> "+str(Y))
        
    cv2.imshow("frame",frame)
    cv2.imshow("mask",mask)

    if cv2.waitKey(3) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
