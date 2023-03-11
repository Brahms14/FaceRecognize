# coding=utf-8
import cv2
import sqlite3



face_cascade = cv2.CascadeClassifier('D:\Tailieu\FaceID\Face_Detect\Face_Detect\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recongnizer\\trainningData.yml")
fontface = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontscale=1
fontColor=(0,0,255)

def getProfile(id):
    conn=sqlite3.connect("FaceDb.db")
    cmd = "SELECT * FROM People Where ID=" + str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile
while True:
    rect, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # đổi ảnh sang thang màu xám
    faces = face_cascade.detectMultiScale(gray, 1.2, 3)  # chỗ số 3 là số phần tử lân cận, mình giảm xuống để xác định được các gương mặt nhỏ hơn
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # vẽ hình vuông khi thấy gương mặt, số 2 là độ dày nét vẽ
        id,conf = rec.predict(gray[y:y + h, x:x + w])
        profile=getProfile(id)
        if(profile!=None):
            cv2.putText(img, str(profile[1]), (x, y + h), fontface,fontscale,fontColor)

    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
