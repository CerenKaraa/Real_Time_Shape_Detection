#Realtime Shape Detection
import cv2
import numpy as np

def nothing(x):
    pass

cap=cv2.VideoCapture(0)
"""trackbar oluşturucam"""
cv2.namedWindow("Settings")

cv2.createTrackbar("Lower-Hue","Settings",0,180,nothing)
"""Kızak oluşturdum"""
cv2.createTrackbar("Lower-Saturation","Settings",0,255,nothing)
cv2.createTrackbar("Lower-Value","Settings",0,255,nothing)
cv2.createTrackbar("Upper-Hue","Settings",0,180,nothing)
cv2.createTrackbar("Upper-Saturation","Settings",0,255,nothing)
cv2.createTrackbar("Upper-Value","Settings",0,255,nothing)

font=cv2.FONT_HERSHEY_SIMPLEX

while 1:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lh=cv2.getTrackbarPos("Lower-Hue","Settings")
    """hangi kızaktan değer alacam,kızak hangi
    pencerede"""
    ls=cv2.getTrackbarPos("Lower-Saturation","Settings")
    lv=cv2.getTrackbarPos("Lower-Value","Settings")
    uh=cv2.getTrackbarPos("Upper-Hue","Settings")
    us=cv2.getTrackbarPos("Upper-Saturation","Settings")
    uv=cv2.getTrackbarPos("Upper-Value","Settings")
    
    lower_color=np.array([lh,ls,lv])
    upper_color=np.array([uh,us,uv])
    
    mask=cv2.inRange(hsv,lower_color,upper_color)
    kernel=np.ones((5,5),np.uint8)
    """beyazlar üzerinde oluşan siyah
    noktaları yok edecek"""
    mask=cv2.erode(mask,kernel)
    """contourları aricam"""
    contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area=cv2.contourArea(cnt)
        """bu for döngüsünü oluşturuyorum çünkü
        tespit ettiğim şeklin merkez noktalarına
        ihtiyacım var.Bunları kullanarak çizimler
        yapıcam"""
        """areanın 400den büyük olmamasına
        göre işlem yapıcam.400bilimsel bir
        değerdir.400den küçük olan şeylerin
        alanını bulmana gerek yok."""
        epsilon=0.02*cv2.arcLength(cnt,True)
        approx=cv2.approxPolyDP(cnt,epsilon,True)
        """bu işlemler sayesinde daha çok yaklaştım
        ve dönen değerleri burada saklıyorum"""
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        
        if area>400:
            cv2.drawContours(frame,[approx],0,(0,0,0),5)
            """çizeceğim yer,çizim değerleri"""
            if len(approx)==3:
                cv2.putText(frame,"Triangle",(x,y),font,1,(0,0,0))
            if len(approx)==4:
                cv2.putText(frame,"Rectangle",(x,y),font,1,0)
            if len(approx)>6:
                cv2.putText(frame,"Circle",(x,y),font,1,0)  
        
    
    cv2.imshow("mask",mask)
    cv2.imshow("frame",frame)
    
    if cv2.waitKey(3) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    