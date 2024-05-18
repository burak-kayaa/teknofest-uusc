import cv2
import move
import time 
import sensor
import colors
import utils

yon = True #True --> sol / False --> sağ
pusula_veri = sensor.pusula()
duz_yon = 180
kamera_gorus_mesafesi_yan=100
kamera_gorus_mesafesi_on=200
tur_sayisi = 0
hedef_bulundu = False
cap = cv2.VideoCapture(0)
color_name = "blue"
real_distance = 15
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


def dondurme(yon,derece):
    if(yon == True):
        hedef  = pusula_veri - derece
        while(pusula_veri > hedef):
            pusula_veri = sensor.pusula()
            move.turn_left()
    elif(yon != False):
        hedef  = pusula_veri + derece
        while(pusula_veri < hedef):
            pusula_veri = sensor.pusula()
            move.turn_right()

def belirli_sure_git(sure):
    onceki_zaman = time.time()
    simdiki_zaman = time.time()
    while(simdiki_zaman-onceki_zaman>sure):
        move.go()

# ARACIN HAVUZA GÖRE KENDİ DÜZLEMESİ
if(pusula_veri>duz_yon):
    while pusula_veri>=duz_yon:
        pusula_veri = sensor.pusula()
        move.turn_left()   

elif(pusula_veri<duz_yon):
    while pusula_veri<=duz_yon:
        pusula_veri = sensor.pusula()
        move.turn_right()


# ARACIN DUVARA HİZALAMASI
dondurme(yon,90)
yon = not(yon)

# ARACIN KAMERAYA BAĞLI DUVARDAN UZAKLAŞMASI 
if(yon == True):
    while(sensor.sol_mesafe()<kamera_gorus_mesafesi_yan):
        move.go_right()
elif(yon != False):
    while(sensor.sag_mesafe()<kamera_gorus_mesafesi_yan):
        move.go_left()


while tur_sayisi == 4:
    # ÖN DUVARA KADAR İLERLEME
    while(sensor.on_mesafe()>kamera_gorus_mesafesi_on):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask,mask2 = colors.create_mask(color_name,hsvImage)
        contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if(area>30000):
                    hedef_bulundu = True
                    break
        move.go()

    # HEDEF TESPİT EDİLDİ İSE GÜDÜME GEÇ 
    if(hedef_bulundu==True):
        break

    # KISA DUVARI YANINA AL
    dondurme(yon,90)

    # BELİRLİ SÜRE İLERLEME
    belirli_sure_git(5)

    # KISA DUVARI ARKANA AL
    dondurme(yon,90)
    yon = not(yon)
    tur_sayisi+=1


# GÜDÜM ALGORİTMASI 

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
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if(area>30000):
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                x_c, y_c = x + (w / 2), y + (h / 2)
                cv2.circle(frame, (int(x_c), int(y_c)), 5, (255, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                distance = utils.get_distance(w, real_distance)
                print(distance)
                vertical_error = utils.get_error_range(h, real_distance)
                move_vehicle(x, w, x_c, y_c, distance, vertical_error)
    else:
        # SÜRE NE KADARDIR YOK 
        pass
        
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

