#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for, render_template

from time import sleep
from math import isnan
import sys
import sqlite3
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.exceptions import PubNubException
from pubnub.pubnub import PubNub, SubscribeListener

pubconf = PNConfiguration()
pubconf.subscribe_key='sub-c-dbf66bda-16b9-11e8-8f67-36fe363f7ef0'
pubconf.publish_key='pub-c-14a6f403-3bab-4945-8656-7cba4ca4bb1f'
secret_key="sec-c-Nzk1ZWE3OTItNjdkOS00ZDVlLThiZjAtODBmMWU2MjI2Y2Ji"
pubconf.ssl = False
pubnub = PubNub(pubconf)


#assign a channel
my_channel = 'pi-weather-station'

db_name = "sensors.db"
table_name="temp_press"
primary_key="ID"

import RPi.GPIO as GPIO  ## Import GPIO library
import time  ## Import 'time' library. Allows us to use 'sleep'
gpio_r_pin = 7
try:
    GPIO.cleanup()
except:
    pass
GPIO.setmode(GPIO.BOARD)  ## Use board pin numbering
GPIO.setup(gpio_r_pin, GPIO.OUT)  ## Setup GPIO Pin to OUT
GPIO.output(gpio_r_pin, 1)  ## Switch off pin

# init flask instance
app = Flask(__name__, static_url_path = "")

def get_data_from_pubnub():
    my_listener = SubscribeListener()
    pubnub.add_listener(my_listener)

    pubnub.subscribe().channels(my_channel).execute()
    my_listener.wait_for_connect()


    result = my_listener.wait_for_message_on('awesomeChannel')
    print(result.message)

    pubnub.unsubscribe().channels('awesomeChannel').execute()
    my_listener.wait_for_disconnect()

    print('unsubscribed')

#error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

# @app.route('/')
# @app.route('/index')
# def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
#     labels = ["2018-03-20_01:51:21", "2018-03-20_01:51:11", "2018-03-20_01:51:01", "2018-03-20_01:50:51", "2018-03-20_01:50:41"]
#     temp_values = [68.5, 68.03,  68.7, 68.558, 68.54]
#     press_values = [1.01625, 1.01627, 1.016209, 1.016247, 1.016233]
#     # return render_template('line_chart.html', values=values, labels=labels)
#     return render_template('two_line_chart.html', temp_values=temp_values, press_values=press_values, labels=labels)
#


# GET request handler
@app.route('/assignment9/api/sensors', methods = ['GET'])
def get_sensors():
    sensors = list()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # sql = "select * from {} order by {} DESC limit 5".format(table_name, primary_key)
    sql = "select * from {} order by {} DESC limit 25".format(table_name, primary_key)
    cursor.execute(sql)
    data=cursor.fetchall()

    print("Data {}".format(data))

    dt = list()
    temp = list()
    press = list()
    for row in data:
        print("Row {}".format(row))
        datetime = row[3]
        t = round(float(row[1]),2)
        p = round(float(row[2]),5)

        dt.append(datetime)
        temp.append(t)
        press.append(p)

        sensor_data = {}
        sensor_data["temperature"] = temp
        sensor_data["pressure"] = press
        sensor_data["date_time"] = dt
        sensors.append(sensor_data)

    cursor.close()
    conn.close()
    # return render_template('line_chart.html', values=values, labels=labels)
    return render_template('two_line_chart.html', temp_values=temp, press_values=press, labels=dt)

# POST request hander
@app.route('/assignment8/api/led/<int:toggle>', methods=['POST'])
def set_led(toggle):
    switch_status = "off"
    if not request.json or not "toggle" in request.json:
        abort(400)
    toggle = request.json['toggle']
    if (toggle > 0):
        # turn on led
        switch_status = "on"
        GPIO.output(gpio_r_pin, False)  ## Switch on pin

    else:
        # turn off led
        switch_status = "off"
        GPIO.output(gpio_r_pin, True)  ## Switch on pin

    return jsonify({'Light': switch_status})


# main
if __name__ == '__main__':
    app.run(debug=True, port=8080)
