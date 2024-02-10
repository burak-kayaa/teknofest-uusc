import cv2 
import numpy as np

img = cv2.imread("polygons.png")
font= cv2.FONT_HERSHEY_COMPLEX


img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret , th = cv2.threshold(img_gray,240,255,cv2.THRESH_BINARY)

contours,grabe = cv2.findContours(th,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    epsilon = 0.01*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    cv2.drawContours(img,[approx],0,(0),2)
    print(approx)
    print(len(approx))
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if(len(approx) == 3):
        cv2.putText(img,"UCGEN",(x,y),font,3,(0,0,0))

cv2.imshow("Original Picture",img)



cv2.waitKey(0)
cv2.destroyAllWindows()