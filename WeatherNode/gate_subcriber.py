from datetime import datetime

import MySQLdb
import paho.mqtt.client as mqtt


def gate_sub_on_conect(client, userdata, flags, rc):
    print(f"Connect with result code {rc}")
    client.subscribe("gate_security")


def gate_sub_on_message(client, userdata, msg):
    global dbConn
    cursor = dbConn.cursor()
    query = "INSERT INTO gate_security (Time,isAuthorized) values (%s, %s)"
    print(msg.payload.decode('utf-8'))
    if msg.payload.decode('utf-8') == "1":
        data = (datetime.now(), "True")
        cursor.execute(query, data)
        dbConn.commit()
        print("Authorized access")
    else:
        data = (datetime.now(), "False")
        cursor.execute(query, data)
        dbConn.commit()
        print("Unauthorized access")
    cursor.close()


broker = "10.1.4.87"
dbConn = MySQLdb.connect("localhost", "huy", "1", "final") or die("Could not connect to database")
gate_sub = mqtt.Client()
gate_sub.on_connect = gate_sub_on_conect
gate_sub.on_message = gate_sub_on_message
gate_sub.connect(broker, 1883, 60)

# window_sub.loop_forever()
gate_sub.loop_forever()
