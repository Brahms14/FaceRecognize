import cv2 as cv
import sqlite3
from input_mocker import InputMocker

class Phathien:
    face_cascade = cv.CascadeClassifier('D:\Tailieu\FaceID\Face_Detect\Face_Detect\haarcascade_frontalface_default.xm')

    def insertOrUpdate(Id, Name):
        conn = sqlite3.connect("FaceDb.db")
        cmd = "SELECT * FROM People Where ID=" + str(Id)
        cusor = conn.execute(cmd)
        isRecordExist = 0
        for row in cusor:
            isRecordExist = 1
        if (isRecordExist == 1):
            cmd = "UPDATE People SET Name=' " + str(Name) + " ' WHERE ID=" + str(Id)
            print("Update thanh cong")

        else:
            cmd = "INSERT INTO People(ID,Name) Values(" + str(Id) + ",' " + str(Name) + " ' )"
            print("Them thanh cong")
        conn.execute(cmd)
        conn.commit()
        conn.close()

    id = input("Nhap ma ID: ")
    name = input("Nhap ten: ")
    insertOrUpdate(id,name)

    sampNumber = 0
    cap = cv.VideoCapture(0)
    while True:
        _, img = cap.read()

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # đổi ảnh sang thang màu xám
        faces = face_cascade.detectMultiScale(gray, 1.2, 3)  # chỗ số 3 là số phần tử lân cận, mình giảm xuống để xác định được các gương mặt nhỏ hơn
        for (x, y, w, h) in faces:
            sampNumber = sampNumber + 1
            cv.imwrite("dataSet/User." + str(id) + "." + str(sampNumber) + ".jpg", gray[y:y + h, x:x + w])
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # vẽ hình vuông khi thấy gương mặt, số 2 là độ dày nét vẽ
            cv.waitKey(20)

        cv.imshow('img', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        if (sampNumber > 200):
            break
    cap.release()
