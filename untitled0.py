#OpenCv kütüphanesini programımıza dahil ediyoruz.
import cv2
sayac=0
 
#görüntü alacağımız kamerayı tanımlıyoruz.
kamera=cv2.VideoCapture(0)
 
#Eğer kameranız IP kamera ise (veya cep telefonu) video adresini tanımlıyoruz.
#Aşağıdaki link benim ağım için geçerlidir.
#Siz telefonun kendi ağınızda alacağı adresi yazmalısınız.
#Bu satırı aktif ederseniz üstteki "kamera=cv2.VideoCapture(0)" satırını yorum haline getirebilirsiniz.
#kamera=cv2.VideoCapture("192.168.0.13:8080/video")
 
#Kameradan gelecek görüntünün çözünürlüğü değeri 640x480 olarak ayarlanıyor.
kamera.set(3,640)
kamera.set(4,480)
 
#Kamera açıldıysa aşağıdaki blok sürekli çalışacak.
while kamera.isOpened():
 
    #kamera'dan 1 kare okunuyor.
    ret,kare=kamera.read()
 
    #eğer kamera'dan veri doğru bir şekilde okunduysa
    if ret== True:
 
        #Burada kareyi 180 derece döndürdüm çünkü benim kameram ters duruyor.
        kare=cv2.flip(kare,0)
 
        #Kameradan alınan görüntü "resim" isimli pencerede gösteriliyor.
        cv2.imshow("resim",kare)
 
        #1milisaniye boyunca Klavyeden bir tuşa basılması bekleniyor
        basilanTus=cv2.waitKey(1) & 0xFF
 
        #Eğer basılan tuş 's' ise görüntü jpg formatında ismi numaralandırılarak kaydediliyor.
        if basilanTus==ord('s'):
            cv2.imwrite("resim"+str(sayac)+".jpg",kare)
            sayac+=1
 
        #Eğer basılan tuş x ise programdan çıkılıyor.
        if basilanTus==ord('x'):
            break
 
#Pencereleri kapat.
cv2.destroyAllWindows();
 
#Programı durdur.
exit()