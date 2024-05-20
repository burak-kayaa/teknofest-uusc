import cv2
import move
import time 
import sensor


yon = True #True --> sol / False --> sağ
pusula_veri = sensor.pusula()
duz_yon = 180
kamera_gorus_mesafesi_yan=100
kamera_gorus_mesafesi_on=200
tur_sayisi = 0

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
    while(simdiki_zaman-onceki_zaman<sure):
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


while tur_sayisi < 4:

    # ÖN DUVARA KADAR İLERLEME
    while(sensor.on_mesafe()>kamera_gorus_mesafesi_on):
        move.go()

    # KISA DUVARI YANINA AL
    dondurme(yon,90)

    # BELİRLİ SÜRE İLERLEME
    belirli_sure_git(5)

    # KISA DUVARI ARKANA AL
    dondurme(yon,90)
    yon = not(yon)
    tur_sayisi+=1
