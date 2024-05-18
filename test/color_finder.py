import cv2
import numpy as np 
import colors

cap = cv2.VideoCapture(0)
color_name = "blue"
while True:
    ret , frame= cap.read()
    frame  = cv2.flip(frame , 1)
    if (ret == 0):
        print("Görüntüye Erişilemedi")
        break

    width   =   int(cap.get(3)) #genislik
    height  =   int(cap.get(4)) #yukseklik
    

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask,mask_filtred = colors.create_mask(color_name,hsv)

    contours,empty = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame,contours,-1,(0,0,0),3)


    cv2.imshow("mask",mask)
    cv2.imshow("mask_filtred",mask_filtred)
    cv2.imshow("webcam",frame)
    if(cv2.waitKey(10) == ord('q')):
        break

cv2.destroyAllWindows()
cap.release()
    
