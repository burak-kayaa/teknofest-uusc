import numpy as np
import cv2
kernel = np.ones((5,5), np.uint8)
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
        lowwer_color = np.array([4, 134, 26])
        upper_color = np.array([26, 255, 255])
    elif color_name == "white":
        lowwer_color = np.array([0, 0, 200])
        upper_color = np.array([180, 20, 255])
    mask = cv2.inRange(hsv, lowwer_color, upper_color)
    mask2 = cv2.dilate(mask, kernel, iterations=1)
    mask2 = cv2.erode(mask2, kernel, iterations=1)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)
    mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernel)


    return mask,mask2


