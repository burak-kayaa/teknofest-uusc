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
    vertical_angle = 40
    view_angle = vertical_angle * h / 480
    radyan_angle = math.radians(view_angle / 2)
    tan = math.tan(radyan_angle)
    ver_error = 5 * h / real_distance
    return (240 + ver_error)

def draw_center(frame):
    cv2.circle(frame, (320, 240), 10, (0, 0, 255), 2)


