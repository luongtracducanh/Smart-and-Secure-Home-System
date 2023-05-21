import time
from datetime import datetime

import MySQLdb
import paho.mqtt.client as mqtt
from discord_webhook import DiscordWebhook

webhook_url = 'ENTER_YOUR_API_KEY'


def send_discord_msg(msg):
    webhook = DiscordWebhook(url=webhook_url, content=msg)
    response = webhook.execute()


def window_sub_on_connect(client, userdata, flags, rc):
    print(f"Connect with result code {rc}")
    client.subscribe("window_security")


def window_sub_on_message(client, userdata, msg):
    global dbConn, lastMsg, intrusionStartTime, intrusionEndTime, intrusionStartMoment
    print(f"{msg.payload.decode('utf-8')}")
    if lastMsg == "0" and msg.payload.decode('utf-8') == "1":
        intrusionStartTime = time.time()
        intrusionStartMoment = datetime.now()
        send_discord_msg("Window intrusion detected!")
    elif lastMsg == "1" and msg.payload.decode('utf-8') == "0":
        intrusionEndTime = time.time()
        intrusionDuration = int(intrusionEndTime - intrusionStartTime)
        cursor = dbConn.cursor()
        query = "INSERT INTO window_security (Time, Duration) VALUES (%s, %s)"
        value = (intrusionStartMoment, intrusionDuration)
        cursor.execute(query, value)
        dbConn.commit()
    lastMsg = msg.payload.decode('utf-8')


dbConn = MySQLdb.connect("localhost", "huy", "1", "final") or die("Could not connect to database")

lastMsg = "0"
intrusionStartTime = time.time()
intrusionEndTime = time.time()
intrusionStartMoment = datetime.now()

broker = "10.1.4.87"
window_sub = mqtt.Client()
window_sub.on_connect = window_sub_on_connect
window_sub.on_message = window_sub_on_message
window_sub.connect(broker, 1883, 60)
window_sub.loop_forever()
