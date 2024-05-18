import cv2
import numpy as np

w_center = 640
h_center = 480
center_x1 = 310
center_x2 = 330
center_y1 = 230
center_y2 = 250

def is_in_center(x, y):
    if x < center_x2 and x > center_x1:
        if y < center_y2 and y > center_y1:
            return True
    # if (x < 640 and )
    return False

def create_mask(color_name, hsv):  #'create_mask' fonksiyonu 2 adet parametre aliyor ve 1 tane cikti veriyor
    if color_name == "blue":
        lowwer_color = np.array([94, 80, 2])
        upper_color = np.array([126, 255, 255])
    elif color_name == "red":
        lowwer_color = np.array([0, 120, 70])
        upper_color = np.array([10, 255, 255])
    elif color_name == "dark_red":
        lowwer_color = np.array([170, 120, 70])
        upper_color = np.array([180, 255, 255])
    elif color_name == "green":
        lowwer_color = np.array([45, 50, 50])
        upper_color = np.array([75, 255, 255])
    elif color_name == "yellow":
        lowwer_color = np.array([20, 100, 100])
        upper_color = np.array([40, 255, 255])
    elif color_name == "white":
        lowwer_color = np.array([0, 0, 200])
        upper_color = np.array([180, 20, 255])
    mask = cv2.inRange(hsv, lowwer_color, upper_color)
    return mask

def empty(x):
    pass

def detect_shape(cnt,frame):
    area = cv2.contourArea(cnt)  # contourlarin alanini buluyoruz
    epsilon = 0.02 * cv2.arcLength(cnt, True)  # epsilon degeri buluyoruz sabit denklem
    approx = cv2.approxPolyDP(cnt, epsilon, True)  # kose buluyoruz
    if (cv2.contourArea(cnt) > 600):  # buldugu ufak nesneleri almasin diye contour alaniyla beraber filtreliyoruz
        x, y, w, h = cv2.boundingRect(cnt)
        x_center = int(x + (w / 2))  # X merkezini buluyoruz
        y_center = int(y + (h / 2))  # Y merkezini buluyoruz
        cv2.circle(frame,(x_center,y_center),3,(0,0,255),-1) # merkezine bir nokta koyuyoruz
        # cv2.line(frame,(int(width/2),int(height/2)),(x_center,y_center),(0,0,0),2)  #goruntunun merkezinden nesnenin merkezine cizgi ciziyoruz
        cv2.rectangle(frame, (center_x1, center_y1), (center_x2, center_y2), (255, 0, 0), 2)
        print(len(approx))  # len(approx) sayesinde kose sayisi aliyoruz ve ona gore sekli algiliyoruz
        if (cv2.contourArea(cnt) > 1200): 
            if len(approx) > 7:
                if (is_in_center(x_center, y_center)):
                    cv2.putText( frame, "Ates", (x_center, y_center), cv2.FONT_HERSHEY_COMPLEX, 2, (0), 2)
                else:
                    cv2.putText( frame, "Hedef", (x_center, y_center), cv2.FONT_HERSHEY_COMPLEX, 2, (0), 2)
