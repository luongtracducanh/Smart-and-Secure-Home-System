import MySQLdb
import cv2
import paho.mqtt.client as mqtt
import serial
from discord_webhook import DiscordWebhook
from google.cloud import storage

storage_client = storage.Client.from_service_account_json("api-key.json")

# create a Bucket object
bucket = storage_client.get_bucket("security-image")
filename = "%s/%s" % ('', "unknown/Unknown.jpg")
blob = bucket.blob(filename)
filename2 = "%s/%s" % ('', "known/Known.jpg")
blob2 = bucket.blob(filename2)

webhook_url = 'ENTER_YOUR_API_KEY'


def send_discord_msg(msg):
    webhook = DiscordWebhook(url=webhook_url, content=msg)
    response = webhook.execute()


# establish serial connection between Arduino and RPi using the 9600 port
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # configure the port if needed


def gate_pub_on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connect success")
    else:
        print("Connect failed")


# initialize varibles for mqtt communication
broker = "10.1.4.87"
gate_pub = mqtt.Client()
gate_pub.on_connect = gate_pub_on_connect
gate_pub.connect(broker, 1883, 60)

# training images and libraries from face detection
face_cascasde = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')


# get profile by id from database
def getProfile(id):
    conn = MySQLdb.connect("localhost", "root", "ducanh2003", "IOT") or die("Could not connect to the database.")
    query = "SELECT * FROM people WHERE ID = " + str(id)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    profile = None

    for row in result:
        profile = row
    cursor.close()
    return profile


cap = cv2.VideoCapture(0)
fontface = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascasde.detectMultiScale(gray)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        id, confidence = recognizer.predict(roi_gray)

        if confidence < 40:
            profile = getProfile(id)
            if profile is not None:
                cv2.putText(frame, "" + str(profile[1]), (x + 30, y + h + 30), fontface, 1, (0, 255, 0), 2)
                # save the image of the known person
                cv2.imwrite("known/Known.jpg", frame)
                with open('unknown/Unknown.jpg', 'rb') as f:
                    blob.upload_from_file(f)
                print("Upload unknown complete")
                # send signal to Arduino to open the door
                ser.write(b"1")
        else:
            cv2.putText(frame, "Unknown", (x + 30, y + h + 30), fontface, 1, (0, 0, 255), 2)
            # save the image of the unknown person
            cv2.imwrite('unknown/Unknown.jpg', frame)
            with open('known/Known.jpg', 'rb') as f:
                blob2.upload_from_file(f)
            print("Upload known complete")
            # send signal to Arduino to alert system
            ser.write(b"0")

    value = ser.readline().decode('utf-8').rstrip()
    if (value):
        if (int(value) == 1):
            print("authenticated")
            # insert data to database
            gate_pub.publish("gate_security", payload="1", qos=0, retain=False)
        elif (int(value) == 0):
            payload = {"content": "/unknown"}
            send_discord_msg("Someone is trying to break in!")
            gate_pub.publish("gate_security", payload="0", qos=0, retain=False)
            print("unathenticated")  # insert data to database

    if len(faces) == 0:
        ser.write(b"2")

    cv2.imshow('image', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
