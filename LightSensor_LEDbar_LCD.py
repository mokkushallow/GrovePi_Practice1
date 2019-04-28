# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 13:52:24 2019

"""
#---------------
# Import
#---------------
import time,sys
import grovepi

# Setup SMBus (From grove_rgb_lcd.py)
if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)
#---------------
# Define
#---------------        
LEVEL1  = 1
LEVEL2  = 2
LEVEL3  = 3
LEVEL4  = 4
LEVEL5  = 5
LEVEL6  = 6
LEVEL7  = 7
LEVEL8  = 8
LEVEL9  = 9
LEVEL10 = 10
LIGHT_LEVEL1  = 0
LIGHT_LEVEL2  = 100
LIGHT_LEVEL3  = 200
LIGHT_LEVEL4  = 300
LIGHT_LEVEL5  = 400
LIGHT_LEVEL6  = 500
LIGHT_LEVEL7  = 600
LIGHT_LEVEL8  = 700
LIGHT_LEVEL9  = 800
LIGHT_LEVEL10 = 900

#---------------
# Function
#---------------
# set backlight to (R,G,B) (values from 0..255 for each) (From grove_rgb_lcd.py)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use) (From grove_rgb_lcd.py)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)
    
# set display text \n for second line(or auto wrap) (From grove_rgb_lcd.py)
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

#Update the display without erasing the display (From grove_rgb_lcd.py)
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

#---------------
# Main
#---------------

# Connect the Grove Light Sensor to analog port A0
light_sensor = 0

# Connect the Grove LED Bar to digital port D5
ledbar = 5

# RGB LCD display device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# Config Grove Light Sensor & LED bar
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(ledbar,"OUTPUT")

# Initialize LED bar
grovepi.ledBar_init(ledbar, 0)
time.sleep(.5)

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        #resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        
        print("sensor_value = %d " %(sensor_value))
        
        if sensor_value > LIGHT_LEVEL10:
            LED_Level = LEVEL10
            grovepi.ledBar_setBits(ledbar,  0b1111111111)
        elif sensor_value > LIGHT_LEVEL9:
            LED_Level = LEVEL9
            grovepi.ledBar_setBits(ledbar,  0b0111111111)
        elif sensor_value > LIGHT_LEVEL8:
            LED_Level = LEVEL8
            grovepi.ledBar_setBits(ledbar,  0b0011111111)
        elif sensor_value > LIGHT_LEVEL7:
            LED_Level = LEVEL7
            grovepi.ledBar_setBits(ledbar,  0b0001111111)
        elif sensor_value > LIGHT_LEVEL6:
            LED_Level = LEVEL6
            grovepi.ledBar_setBits(ledbar,  0b0000111111)
        elif sensor_value > LIGHT_LEVEL5:
            LED_Level = LEVEL5
            grovepi.ledBar_setBits(ledbar,  0b0000011111)
        elif sensor_value > LIGHT_LEVEL4:
            LED_Level = LEVEL4
            grovepi.ledBar_setBits(ledbar,  0b0000001111)
        elif sensor_value > LIGHT_LEVEL3:
            LED_Level = LEVEL3
            grovepi.ledBar_setBits(ledbar,  0b0000000111)
        elif sensor_value > LIGHT_LEVEL2:
            LED_Level = LEVEL2
            grovepi.ledBar_setBits(ledbar,  0b0000000011)
        elif sensor_value > LIGHT_LEVEL1:
            LED_Level = LEVEL1
            grovepi.ledBar_setBits(ledbar,  0b0000000001)
        else:
            print ("LED Level Error")
        
        # Make text
        #display_text = "sensor = {} \n".sensor_value + "LED Level = {}".LED_Level
        display_text = "sensor = {} \n".format(str(sensor_value)) + "LED Level = {}".format(str(LED_Level))
        setText_norefresh(display_text)
        setRGB(0,100,0)
        print("LED_Level = %d " %(LED_Level))

        time.sleep(.5)

    except IOError:
        print ("Error")
