import cv2
import math

def get_distance(w, real_distance):
    horizontal_angle = 55
    view_angle = horizontal_angle * w / 640
    radyan_angle = math.radians(view_angle / 2)
    tan = math.tan(radyan_angle)
    distance = (real_distance / 2) / tan
    return (distance)

def get_error_range(h, real_distance):
    pixel_lenght=real_distance/h
    return (240+(5/pixel_lenght))

def draw_center(frame):
    cv2.circle(frame, (320, 240), 10, (0, 0, 255), 2)

def draw_contours(frame , cnt):
    area  = cv2.contourArea(cnt)
    epsilon = 0.02*cv2.arcLength(cnt,True)
    approx = cv2.approxPolyDP(cnt,epsilon,True)
    cv2.drawContours(frame,[approx],0,(252,200,170),2)
    

