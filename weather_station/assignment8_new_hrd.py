#!/usr/bin/python3
from flask import Flask, jsonify, abort, request, make_response, url_for

import RPi.GPIO as GPIO
from time import sleep
from math import isnan
import sys
import sqlite3
from bmp280 import BMP280

db_name = "sensors.db"
table_name="temp_press"
primary_key="ID"

# init flask instance
app = Flask(__name__, static_url_path = "")

#error handlers
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad Request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

# GET request handler
@app.route('/assignment8/api/sensors', methods = ['GET'])
def get_sensors():
    sensors = list()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # sql = "select * from {} order by {} DESC limit 5".format(table_name, primary_key)
    sql = "select * from {} order by {} DESC limit 5".format(table_name, primary_key)
    cursor.execute(sql)
    data=cursor.fetchall()
    print("Data {}".format(data))

    for row in data:
        print("Row {}".format(row))
        sensor_data = {}
        sensor_data["temperature"] = "{} F".format(row[1])
        sensor_data["pressure"] = "{} bar".format(row[2])
        sensor_data["date_time"] = row[3]
        sensors.append(sensor_data)

    cursor.close()
    conn.close()

    return make_response(jsonify( { 'sensors': sensors } ),200)

# main
if __name__ == '__main__':
    app.run(debug=True, port=8080)
