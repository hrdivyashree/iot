from time import sleep
from math import isnan
from bmp280 import BMP280
import sys

from datetime import datetime
import sqlite3
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.exceptions import PubNubException

pubconf = PNConfiguration()
pubconf.subscribe_key='sub-c-dbf66bda-16b9-11e8-8f67-36fe363f7ef0'
pubconf.publish_key='pub-c-14a6f403-3bab-4945-8656-7cba4ca4bb1f'
pubconf.ssl = False
secret_key="sec-c-Nzk1ZWE3OTItNjdkOS00ZDVlLThiZjAtODBmMWU2MjI2Y2Ji"
pubnub = PubNub(pubconf)

#assign a channel
my_channel = 'pi-weather-station'

db_name = "sensors.db"
table_name="temp_press"

ID=1
conn = sqlite3.connect(db_name)

#callback section
def publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        # Message successfully published to specified channel.
        print("Message Sent")
    else:
        # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
        print("Error Sending!")

def publish_callback(message, channel):
    print(message)

def publish_pubnub(sensor_data):
    try:
        envelope = pubnub.publish().channel(my_channel).message(sensor_data).sync()
        print("publish timetoken: %d" % envelope.result.timetoken)
    except PubNubException as e:
        print("ERROR: Channel {} - {}".format(my_channel, e.message))


def write2db(temp, press, current_dt):
    global ID
    cursor = conn.cursor()
    ID+=1
    create_table_comm = \
        "CREATE TABLE IF NOT EXISTS {} (ID INTEGER, TEMPERATURE REAL, " \
        "PRESSURE REAL, DT TEXT)".\
            format(table_name)

    cursor.execute(create_table_comm)

    insert_row_comm = \
        "INSERT INTO {0} (ID, TEMPERATURE, PRESSURE, DT) VALUES ({1}, {2}, {3}, \"{4}\")". \
            format(table_name, ID, float(temp), round(float(press),5), current_dt)

    cursor.execute(insert_row_comm)
    conn.commit()
    cursor.close()


def close_db():
    conn.close()

bmp280 = BMP280()

while True:
    try:

        temp = bmp280.read_temperature()
        press = bmp280.read_pressure()
        dt = date = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        print("Temperature = {} F Pressure = {} bar".format(temp, press))

        # check if we have nans
        # if so, then raise a type error exception
        if isnan(temp) is True:
            print("Temperature is NAN")
            temp = "NAN"

        if isnan(press) is True:
            print("Pressure is NAN")
            press = "NAN"

        t = str(temp)
        p = str(press)

        write2db(t,p,dt)

        sensor_data = {}
        sensor_data["temperature"] = t
        sensor_data["pressure"] = p
        sensor_data["date_time"] = dt

        publish_pubnub(sensor_data)

        # wait some time before next iteration
        sleep(10)

    except (IOError, TypeError) as e:
        # and since we got a type error
        # close_db()
        print(str(e))
        continue

    except KeyboardInterrupt as e:
        # since we're exiting the program
        close_db()
        print(str(e))
        sys.exit()