import cv2
import numpy as np

def create_mask(color_name,hsv): #'create_mask' fonksiyonu 2 adet parametre aliyor ve 1 tane cikti veriyor
    """
    1.parametre     ---> String olarak renk ismi aliyor.Örnek olarak-> "blue"
    2.parametre     ---> Aldigimiz görüntünün hsv halini yolluyoruz. Örneğin frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) deki frame_hsv yi istiyor
    Cikti           ---> Fonksiyonun ciktisi parametre olarak gonderdigimiz renge gore oluşturduğu maskeyi geri gonderiyor
    Ornek Kullanim  ---> mask = create_mask("red",frame_hsv)
    """
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



cap = cv2.VideoCapture(0) #Webcam kamerasini algiliyoruz

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1) #frame i y eksenine gore donduruyoruz  

    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #frame i hsv formatina donduruyoruz
    mask = create_mask("blue",frame_hsv) #fonksiyona rengi ve hsv formatindeki goruntuyu yollayip maske cikartiyoruz

    contours , empty = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #contour olusturuyoruz 
    #"cv2.CHAIN_APPROX_SIMPLE" yerine "cv2.CHAIN_APPROX_NONE" kullanabiliriz fakat simple kullanmamiz daha fazla bellek alani sagliyor

    if(len(contours) != 0):#contour bulmus mu diye kontrol ediyoruz
        for cnt in contours:
            area  = cv2.contourArea(cnt)                #contourlarin alanini buluyoruz
            epsilon = 0.02*cv2.arcLength(cnt,True)      #epsilon degeri buluyoruz sabit denklem
            approx = cv2.approxPolyDP(cnt,epsilon,True) #kose buluyoruz
            if(cv2.contourArea(cnt)>600):               #buldugu ufak nesneleri almasin diye contour alaniyla beraber filtreliyoruz
                x,y,w,h = cv2.boundingRect(cnt)   
                x_center = int(x+(w/2))                 #X merkezini buluyoruz
                y_center = int(y+(h/2))                 #Y merkezini buluyoruz
                cv2.circle(frame,(x_center,y_center),3,(0,0,255),-1) # merkezine bir nokta koyuyoruz

                print(len(approx))                      #len(approx) sayesinde kose sayisi aliyoruz ve ona gore sekli algiliyoruz
                if(len(approx)==3):                     
                    cv2.putText(frame,"Ucgen",(x_center,y_center),cv2.FONT_HERSHEY_COMPLEX,2,(0),2)             
                if(len(approx)==4):               
                    cv2.putText(frame,"Dortgen",(x_center,y_center),cv2.FONT_HERSHEY_COMPLEX,2,(0),2)                
                if(len(approx)>7):                      
                    cv2.putText(frame,"Cember",(x_center,y_center),cv2.FONT_HERSHEY_COMPLEX,2,(0),2)    
                cv2.drawContours(frame,contours,-1,(0,0,255),2) #cismin disini contourluyoruz 

    cv2.imshow("Mask",mask)
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()    
