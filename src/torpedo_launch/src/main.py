import cv2
import numpy as np
import colors
import time
import utils
import move
# import serial
# arduino = serial.Serial("/dev/ttyUSB0",timeout = 1)

real_distance = 15
cap = cv2.VideoCapture(0)
color_name = "blue"
vertical_tolerance = 30
horizontal_tolerance = 10
distance_tolerance = 40

def move_vehicle(x, w, x_c, y_c, distance, vertical_error):
    cv2.line(frame,(0, int(vertical_error - 30)), (640,int(vertical_error - 30)), (255,255,0),3)
    cv2.line(frame,(0, int(vertical_error + 30)), (640,int(vertical_error + 30)), (255,255,0),3)
    cv2.line(frame,(0, int(y_c)), (640, int(y_c)), (0, 0, 255), 3)
    if 320 + vertical_tolerance < x_c:
        move.go_left()
    elif x_c < 320 - vertical_tolerance:
        move.go_right()
    else:
        if distance_tolerance < distance:
            move.go()
        else:
            if vertical_error + vertical_tolerance < y_c:
                move.go_up()
            elif y_c < vertical_error - vertical_tolerance:
                move.go_down()
            else:
                # arduino.write(1)
                print("at")
    print(time.localtime().tm_sec)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask,mask2 = colors.create_mask(color_name,hsvImage)
    contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    utils.draw_center(frame)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        x_c, y_c = x + (w / 2), y + (h / 2)
        cv2.circle(frame, (int(x_c), int(y_c)), 5, (255, 255, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        distance = utils.get_distance(w, real_distance)
        vertical_error = utils.get_error_range(h, real_distance)
        move_vehicle(x, w, x_c, y_c, distance, vertical_error)
    else:
        print("cisim yok")
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()








# if 310 < x + w / 2 < 330 and 45 < distance < 50 and vertical_error - 10 < y - (h / 2) < vertical_error + 10:
#     print("ortada")
#     print("******")
