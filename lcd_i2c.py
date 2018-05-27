#Assignment 7 - Interfcing LCD display using I2C
#For thsi assignment I am using grove sensor kit LCD display board with Rasberry pi
#Below program writes text and
#also changes the back light color of the LCD display, Ref - Dexterindustries Grove sensors opensource
#This program needs smbus python package to be installed using pip

import time,sys
print("Sys Paltform {}".format(sys.platform))
if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    print("GPIO Version {}".format(GPIO.RPI_REVISION))
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

def clear():
    # bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,0x01)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, 0)

# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Main to write data and change the backlight color.
if __name__=="__main__":
    setText("Hello world\nThis is an LCD test")
    setRGB(0,128,64)
    time.sleep(2)
    print("Starting backlight loop")
    for c in range(0,255):
        setText_norefresh("Going to sleep in {}...".format(str(255-c)))
        setRGB(255-c,c,0)
        time.sleep(0.1)
    setRGB(0,255,0)
    setText("Bye bye, this should wrap onto next line")
    time.sleep(10)
    clear()