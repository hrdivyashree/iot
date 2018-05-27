#!/usr/bin/env python

# -*- coding:utf-8 -*-
# pi@raspberrypi: ~ $ mkdir cgi-bin
# pi@raspberrypi: ~ $ cd cgi-bin
# pi@raspberrypi: ~/cgi-bin $ vi gpio.py

# ----------- gpio.py --------------

import cgi
import wiringpi
import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'
from datetime import  datetime

gpio_r_pin=3
gpio_g_pin=13
gpio_b_pin=11

html_template_string = '''<html>
    <head>
        <title>RGB LED - Assignment 5</title>
        <link rel="stylesheet" type="text/css" href="/css/assignment5-hrd.css">
        <script src="/scripts/assignment4-hrd.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    </head>
    <body>
        <h1>Current date - {} Assignment 5 - RGB LED Data with CGI integration</h1>
        <form>
            <input type="button" value="Hello World" onclick="msg()"/>
        </form>
        <table id="mydatatable">
            <tr id="mydataheadrow">
                <td>Red</td>
                <td>Green</td>
                <td>Blue</td>
            </tr>
            <tr id="mydatarow">
                <td id="red" onmouseover="highlight('red')" onmouseout="reset('red')">{}</td>
                <td id="green"  onmouseover="highlight('green')"  onmouseout="reset('green')" >{}</td>
                <td id="blue"  onmouseover="highlight('blue')"  onmouseout="reset('blue')" >{}</td>
            </tr>
        </table>
    </body>
</html>'''

form = cgi.FieldStorage()  # standard cgi script lines to here!

red = form.getfirst("red", 1)  # get the form value associated with form
green = form.getfirst("green", 1)  # similarly for name 'y'
blue = form.getfirst("blue", 1)  # similarly for name 'y'

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(gpio_r_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
GPIO.setup(gpio_g_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
GPIO.setup(gpio_b_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
GPIO.output(gpio_r_pin,int(red))## Switch off pin
GPIO.output(gpio_g_pin,int(green))## Switch off pin
GPIO.output(gpio_b_pin,int(blue))## Switch off pin


datetimestamp=datetime.now()
dt = datetimestamp.strftime("%Y_%m_%d_%H_%M_%S")

html_str=html_template_string.format(dt, GPIO.input(gpio_r_pin), GPIO.input(gpio_g_pin), GPIO.input(gpio_b_pin))
print("Content-type: text/html\n\n")
print(html_str)


