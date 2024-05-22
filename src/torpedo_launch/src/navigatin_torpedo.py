import cv2
import move
import time 
import sensor
import colors
import utils
import pylint

yon = True #True --> sol / False --> sağ
ilk_yon = True

# pusula_veri = sensor.pusula()
duz_yon = 180
kamera_gorus_mesafesi_yan=100
kamera_gorus_mesafesi_on=200
hedef_bulundu = False
cap = cv2.VideoCapture(0)
color_name = "blue"
real_distance = 15
vertical_tolerance = 30
horizontal_tolerance = 10
distance_tolerance = 40


x_mesafe = list()
y_mesafe = list()
aracin_hizi = 1

x_sure_bas = 0
x_sure_son = 0  

y_sure_bas = 0
y_sure_son = 0  
# dolum_sayisi = dosya 


toplam_x_mesafe = 0
toplam_y_mesafe = 0


gorev_algoritmasi = True
dolum_algoritmasi = False

gudum_algoritmasi = False
navigasyon_algoritmasi = True

gorulmedi = False
dolum_yapildi = True
hedefe_git = False

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
                print("!!FIRE!!")
                dolum_algoritmasi=True
                gorev_algoritmasi=False
                return 1


def dondur(yon,belirlenen_derece,aciklama = "VERİLEN YÖNDE VERİLEN AÇI KADAR DÖNDÜRÜR"): 
    if(yon == True):
        hedef_derece  = pusula_veri - belirlenen_derece

        if(hedef_derece<0): 
            hedef_derece =+360

        while(not((hedef_derece-5)< pusula_veri < (hedef_derece+5))):
            pusula_veri = sensor.pusula()
            move.turn_left()

    elif(yon != False):           
        hedef_derece  = pusula_veri + belirlenen_derece

        if(hedef_derece>360):
            hedef_derece =-360       
        while(not((hedef_derece-5)< pusula_veri < (hedef_derece+5))):
            pusula_veri = sensor.pusula()
            move.turn_right()


def belirli_sure_git(sure,aciklama = "VERİLEN SÜREDE İLERİ GİDER"):
    onceki_zaman = time.time()
    simdiki_zaman = time.time()
    while(simdiki_zaman-onceki_zaman<sure): #ZAMANA KÜÇÜK OLUCAK
        simdiki_zaman = time.time()
        move.go()
    return 0

# # ARACIN HAVUZA GÖRE KENDİ DÜZLEMESİ -> 1
# if(pusula_veri>duz_yon):
#     while pusula_veri>=duz_yon:
#         pusula_veri = sensor.pusula()
#         move.turn_left()   

# elif(pusula_veri<duz_yon):
#     while pusula_veri<=duz_yon:
#         pusula_veri = sensor.pusula()
#         move.turn_right()


# # ARACIN DUVARA HİZALAMASI -> 2
# dondur(yon,90)

# # ARACIN KAMERAYA BAĞLI DUVARDAN UZAKLAŞMASI -> 3
# if(hedefe_git == False):
#     if(yon == True):
#         while(sensor.sol_mesafe()<kamera_gorus_mesafesi_yan):
#             move.go_right()
#     elif(yon == False):
#         while(sensor.sag_mesafe()<kamera_gorus_mesafesi_yan):
#             move.go_left()

# yon = not(yon)
    
    
while True:
    # gorev_algoritmasi -> navigasyon_algoritmasi + gudum_algoritmasi
    # dolum_algoritmasi -> dolum_yapildi + hedefe_git 

    while gorev_algoritmasi:

        # NAVİGASYON ALGORİTMASI 
        while navigasyon_algoritmasi:

            x_sure_bas = time.time() #X DE GİTTİĞİ YOLU BULABİLMEK İÇİN SÜREYİ BAŞLATIYORUZ

            while(1):#BURAYA ON MESAFE BELİRLENEN MESAFEDEN UZAK OLDUĞU SÜRECE ÇALIŞTIR (on_mesafe_sensor()>belirlenen_uzaklik)
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask,mask2 = colors.create_mask(color_name,hsvImage)
                contours, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.putText(frame,"NAVIGASYON",(350,37),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,255),3)
                utils.draw_center(frame)
                if contours:
                    for cnt in contours:
                        utils.draw_contours(frame,cnt)
                        area = cv2.contourArea(cnt)

                        if(area>30000): #30000 DEĞERİ GÖRÜLEN CİSMİN ALANINA BAĞLI / WHİLE İLE SAĞLAMLAŞTIRMAYA DİKKAT
                            hedef_bulundu = True
                            break

                    if(hedef_bulundu):
                        break

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    gorev_algoritmasi = False
                    break
                move.go()
            x_sure_son = time.time()


            # HEDEF TESPİT EDİLDİ İSE GÜDÜME GEÇ -> 5
            if(hedef_bulundu==True):
                if(yon==True):
                    mesafe = (x_sure_son-x_sure_bas)*aracin_hizi*1
                else:
                    mesafe = (x_sure_son-x_sure_bas)*aracin_hizi*-1
                x_mesafe.append(mesafe)
                hedef_bulundu=False 
                gudum_algoritmasi=True
                navigasyon_algoritmasi = False
                for i in x_mesafe:
                    toplam_x_mesafe = toplam_x_mesafe + i
                break
            
            # X DEKİ MESAFEYİ ALIYOR
            if(yon==True):
                mesafe = (x_sure_son-x_sure_bas)*aracin_hizi*1
            else:
                mesafe = (x_sure_son-x_sure_bas)*aracin_hizi*-1
            x_mesafe.append(mesafe)


            # # KISA DUVARI YANINA AL -> 6
            # dondur(yon,90)
    
            # # BELİRLİ SÜRE İLERLEME -> 7
            # belirli_sure_git(5)
    
    
            # # KISA DUVARI ARKANA AL -> 8
            # dondur(yon,90)
            # yon = not(yon)
          
        
    
        # GÜDÜM ALGORİTMASI 
        while gudum_algoritmasi:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask,mask2 = colors.create_mask(color_name,hsvImage)
            contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            utils.draw_center(frame)
            cv2.putText(frame,"GUDUM",(460,37),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,255,255),3)



            
            if contours2:
                for cnt2 in contours2:
                    utils.draw_contours(frame,cnt2)
                    area2 = cv2.contourArea(cnt2)
                    if(area2>10000):   
                        gorulmedi=False
                        onceki_zaman = time.time()
                        simdiki_zaman = time.time()                 
                        largest_contour = max(contours2, key=cv2.contourArea)
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
                        x_c, y_c = x + (w / 2), y + (h / 2)
                        cv2.circle(frame, (int(x_c), int(y_c)), 5, (255, 255, 0), 2)
                        distance = utils.get_distance(w, real_distance)
                        vertical_error = utils.get_error_range(h, real_distance)
                        if(move_vehicle(x, w, x_c, y_c, distance, vertical_error)):
                            dolum_sayisi =+ 1
                            if(dolum_sayisi>5):
                                exit()
                            else:
                                gudum_algoritmasi=False
                                gorev_algoritmasi=False
                                dolum_algoritmasi=True
                    else:
                        gorulmedi = True
            if(not(contours2) or gorulmedi):
                # SÜRE NE KADARDIR YOK 
                simdiki_zaman = time.time()
                print("GECEN ZAMAN --------->"+str(simdiki_zaman-onceki_zaman))
                if(simdiki_zaman-onceki_zaman>=4):
                    gorulmedi=False
                    navigasyon_algoritmasi = True
                    gudum_algoritmasi = False
                    break
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                gorev_algoritmasi = False
                break


    while dolum_algoritmasi:
        while dolum_yapildi:
            y_sure_bas = time.time()
            yon = not(yon) #yonü düzelttik
            # ARAÇ YAN DUVARA GELECEK
            if(yon == True):
                while (sensor.sol_mesafe()>30):
                    move.go_right() 
            elif(yon == False):
                while (sensor.sag_mesafe()>30):
                    move.go_left()
    
            # DOSYAYA YAZILACAKLAR
            y_sure_son = time.time()
            toplam_y_mesafe = ((y_sure_son-y_sure_bas)*aracin_hizi)
            if(toplam_x_mesafe>0):
                yon = ilk_yon
                # dosyaya yaz
            elif(toplam_x_mesafe<0):
                yon = not(ilk_yon)
                #dosyaya yaz
            dolum_yapildi       = False
            gorev_algoritmasi   = False
            dolum_algoritmasi   = True
            hedefe_git          = True
            dolum_sayisi =+ 1
        # ******************************
            while True:
                move.go_up()
        while hedefe_git:
            baslangic_sure = time.time()
            bitis_sure = time.time()
            while((bitis_sure-baslangic_sure)<((toplam_y_mesafe)/aracin_hizi)):
                bitis_sure = time.time()
                if(yon == True):
                    move.go_left()
                elif(yon == False):
                    move.go_right()
            baslangic_sure = time.time()
            bitis_sure = time.time()
            while((bitis_sure-baslangic_sure)<((toplam_x_mesafe)/aracin_hizi)):
                bitis_sure = time.time()
                move.go()
            dolum_algoritmasi = False
            gudum_algoritmasi = True
            gorev_algoritmasi = True        
            break
                
        
        
        
cap.release()
cv2.destroyAllWindows()
    
    