import os

import MySQLdb
import cv2


def insertOrUpdate(id, name):
    conn = MySQLdb.connect("localhost", "root", "ducanh2003", "IOT") or die("Could not connect to the database.")
    print(conn)
    query = "INSERT INTO people (ID, Name) VALUES(" + str(id) + ",'" + str(name) + "')"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()


# load tv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

# insert to db
id = input('Enter your ID: ')
name = input('Enter your name: ')
insertOrUpdate(id, name)
sampleNum = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if not os.path.exists('dataset'):
            os.makedirs('dataset')

        sampleNum += 1
        cv2.imwrite('dataset/User.' + str(id) + '.' + str(sampleNum) + '.jpg', gray[y:y + h, x:x + w])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if sampleNum >= 100:
        break

cap.release()
cv2.destroyAllWindows()
