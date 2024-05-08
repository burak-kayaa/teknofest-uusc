import cv2
import numpy as np


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
    epsilon = 0.02 * cv2.arcLength(
        cnt, True
    )  # epsilon degeri buluyoruz sabit denklem
    approx = cv2.approxPolyDP(cnt, epsilon, True)  # kose buluyoruz
    if (
        cv2.contourArea(cnt) > 600
    ):  # buldugu ufak nesneleri almasin diye contour alaniyla beraber filtreliyoruz
        x, y, w, h = cv2.boundingRect(cnt)
        x_center = int(x + (w / 2))  # X merkezini buluyoruz
        y_center = int(y + (h / 2))  # Y merkezini buluyoruz

        # cv2.circle(frame,(x_center,y_center),3,(0,0,255),-1) # merkezine bir nokta koyuyoruz
        # cv2.line(frame,(int(width/2),int(height/2)),(x_center,y_center),(0,0,0),2)  #goruntunun merkezinden nesnenin merkezine cizgi ciziyoruz

        print(
            len(approx)
        )  # len(approx) sayesinde kose sayisi aliyoruz ve ona gore sekli algiliyoruz
        if len(approx) == 3:
            cv2.putText(
                frame,
                "Ucgen",
                (x_center, y_center),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (0),
                2,
            )
        if len(approx) == 4:
            cv2.putText(
                frame,
                "Dortgen",
                (x_center, y_center),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (0),
                2,
            )
        if len(approx) > 7:
            cv2.putText(
                frame,
                "Cember",
                (x_center, y_center),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (0),
                2,
            )
