import cv2
import numpy as np
import requests


url = "http://192.168.1.236:8080//shot.jpg"


while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content),dtype=np.uint8)
    img = cv2.imdecode(img_arr,cv2.IMREAD_COLOR)
    img = cv2.resize(img , (640,480))
    
    cv2.imshow("kamera",img)
    
    if(cv2.waitKey(30) == 27):
        break

cv2.destroyAllWindows()

"""
import cv2
import numpy as np
import requests

def create_mask(color_name,hsv):
    if(color_name == "blue"):
        lowwer_color    = np.array([94, 80, 2])
        upper_color     = np.array([126, 255, 255])
    elif(color_name == "red"):
        lowwer_color    = np.array([161, 155, 84])
        upper_color     = np.array([179, 255, 255])
    elif(color_name == "green"):
        lowwer_color    = np.array([25, 52, 72])
        upper_color     = np.array([102, 255, 255])
    mask = cv2.inRange(hsv,lowwer_color,upper_color)

    return mask




#cap = cv2.VideoCapture(0)
url = "http://192.168.1.236:8080//shot.jpg"

while True:
    #ret, frame = cap.read()
  
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content),dtype=np.uint8)
    frame = cv2.imdecode(img_arr,cv2.IMREAD_COLOR)
    frame = cv2.flip(frame,1)

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = create_mask("blue",frame_hsv)

    contours , empty = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if(len(contours) != 0):
        for cnt in contours:
            area  = cv2.contourArea(cnt)
            epsilon = 0.02*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            if(cv2.contourArea(cnt)>600):
                print(len(approx))
                if(len(approx)>2):
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.circle(frame,(int(x+(w/2)),int(y+(h/2))),3,(0,0,255),2)
                    cv2.drawContours(frame,contours,-1,(0,0,255),2)

       
   


    cv2.imshow("Mask",mask)
    cv2.imshow("Webcam", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#cap.release()
cv2.destroyAllWindows()    

"""






# Blue color
"""
low_blue = np.array([94, 80, 2])
high_blue = np.array([126, 255, 255])
blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
print(len(blue))
"""

# Red color
"""
low_red = np.array([161, 155, 84])
high_red = np.array([179, 255, 255])
red_mask = cv2.inRange(hsv_frame, low_red, high_red)
red = cv2.bitwise_and(frame, frame, mask=red_mask)
"""


# Green color
"""
low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])
green_mask = cv2.inRange(hsv_frame, low_green, high_green)
green = cv2.bitwise_and(frame, frame, mask=green_mask)
"""

# Every color except white
"""
low = np.array([0, 42, 0])
high = np.array([179, 255, 255])
mask = cv2.inRange(hsv_frame, low, high)
result = cv2.bitwise_and(frame, frame, mask=mask)
"""
