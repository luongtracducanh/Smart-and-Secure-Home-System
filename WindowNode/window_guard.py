import time

import paho.mqtt.client as mqtt
import serial

ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
window_guard_enable = True


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result code {rc}")


broker = "10.1.4.87"
pub = mqtt.Client()
pub.on_connect = on_connect
pub.connect(broker, 1883, 60)

while True:
    data = ser.readline().decode('utf-8').rstrip()
    if data:
        if data == "O":
            pub.publish(topic="window_security", payload=f"1", qos=0, retain=False)
            print("Send window intrusion warn message")

        else:
            pub.publish(topic="window_security", payload=f"0", qos=0, retain=False)
            print("Safe")
    time.sleep(1)
