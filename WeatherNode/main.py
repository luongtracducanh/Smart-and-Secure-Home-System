# to access MySQL db in terminal: mysql -u root -h localhost IOT -p

import http.client as httplib
import time
import urllib

import MySQLdb
import serial
from discord_webhook import DiscordWebhook

thingspeak_key = "ENTER_YOUR_API_KEY"
webhook_url = 'ENTER_YOUR_API_KEY'


def send_discord_msg(msg):
    webhook = DiscordWebhook(url=webhook_url, content=msg)
    response = webhook.execute()
    
    
def upload_thingspeak(temperature, humidity, gas):
    params = urllib.parse.urlencode({'field1': temperature, 'field2': humidity, 'field3': gas, 'key': thingspeak_key})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()


# establish serial connection between Arduino and RPi using the 9600 port
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # configure the port if needed

# connect to MySQL database
dbConn = MySQLdb.connect("localhost", "huy", "1", "final") or die("Could not connect to the database")
print(dbConn)

# loop the program, exit using Ctrl + C
while True:
    # get input from Arduino's sensor
    data = ser.readline().decode('utf-8').rstrip()

    # an exception in case the temperature change and return an empty string
    try:
        if (data):
            temp = data.split(',')
            if (len(temp) < 3):
                print("Missing input values")
            else:
                temperature = float(temp[0])
                humidity = float(temp[1])
                gas = float(temp[2])
                data = (temperature, humidity, gas)  # tuple to for the sql INSERT statement

                # upload_thingspeak(temperature, humidity, gas)
                cursor = dbConn.cursor()

                # insert the data into our table
                cursor.execute("INSERT INTO weather (Temperature, Humidity, Gas) values (%s, %s, %s)" % (data))
                dbConn.commit()

                # print the details of the table in real time
                cursor.execute("SELECT * FROM weather ORDER BY ID DESC limit 1")
                result = cursor.fetchall()
                for row in result:
                    print(row)

                # check if current values exceeded the alert level or not
                cursor.execute("SELECT * FROM default_alert ORDER BY ID DESC limit 1")
                newAlertValues = cursor.fetchall()[0]
                print(newAlertValues)

                message = "{},{},{}".format(newAlertValues[1], newAlertValues[2], newAlertValues[3])
                print(message)
                ser.write(message.encode())
                cursor.close()

                send_discord_msg("Alert is on")

                # delay for 5 second to collect data
                time.sleep(1)

    # when encounter an empty string, the conversion from string to float will return an error
    # we need to exclude this from our program
    except ValueError:
        print(f'Error inserting "{data}" to database.')
