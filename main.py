import RPi.GPIO as GPIO
import subprocess
import socket
from heartrate_monitor import HeartRateMonitor
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import GY906
from time import sleep
import time
import numpy as np
import os
import add

file_path = '/media/doungsuda/3337-3239/name.txt'
file_path1 = '/media/doungsuda/3337-3239/HN.txt'
back = 6
next = 5
end = 13
ch = 0
disp = None
image = None
draw = None
with open(file_path, "r") as file:
    data = file.readlines()

with open(file_path1, "r") as file:
    data1 = file.readlines()

network_interface = "wlan0"
output = subprocess.check_output(["iwconfig",network_interface])

state = 1

def welcome(channel):
    global state
    ch = channel
    if ch !=  next and ch != back and ch != end:
       return
    if state == 1 and channel == back:
       print("Hello")
       ch = 0
       pass

    if state == 2 and channel == next:
       print("Please re-measure")
       get_sensor()
       ch = 0
       return

    if state == 2 and channel == back:
       connect_wifi()
       ch = 0
       return

    if state == 3 and channel == back:
       print("Please re-meeasure")
       get_sensor()
       ch = 0
       return


    if state == 3 and channel == next:
       finish()
       ch = 0
       return

    if (state == 1 or state == 2 or state == 3) and channel == end:
       print("Hello")
       oled_init()
       oled_write(draw,0,0,"Hello")
       disp.image(image)
       disp.display()
       state = 1
       ch = 0
       return
    if state == 1 and channel == next:
           if "ESSID:off/any" in str(output):
              print("IS NOT CONNECT")

              oled_init()
              oled_write(draw,0,3,"IS NOT CONNECT")
              disp.image(image)
              disp.display()
              state = 1
           else:
              print("CONNECTED")
              oled_init()
              oled_write(draw,0,3,"CONNECTED")
              disp.image(image)
              disp.display()
              state = 2
           ch = 0
           return


def is_connected(ip, port):
    try:
        socket.create_connection((ip, port))

    except OSError as os:
        print(os)
        pass
    return False

def readSensor():
    bpm = 0
    spo2 = 0
    print('sensor starting...')
    oled_init()
    oled_write(draw,0,2,"Please re-measure")
    oled_write(draw,0,3,'sensor starting...')
    disp.image(image)
    disp.display()
    hrm= HeartRateMonitor()
    hrm.start_sensor()
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print('keyboard interrupt detected, exiting...')

    hrm.stop_sensor()
    bpm = np.mean(hrm.bpm2)
    spo2 = np.mean(hrm.spo2)
    return bpm,spo2


def get_sensor():
       global state
       state = 3
       sleep(1)
       temp = 0.0
       spo2 = 0.0
       bpm = 0.0
       HN = []
       t = []
       r = 1
       sensor = GY906.GY906()
       bpm, spo2 = readSensor()
       hn = data1
       HN = ''.join(map(str, hn))
       while r <= 20:
        temperature = sensor.get_obj_temp()
        print(r, " : ",temperature);
        time.sleep(1)
        if temperature is not None:
            t.append(temperature)
        r += 1
       temp = np.mean(t)
       print(HN, temp, bpm, spo2)
       oled_init()
       oled_write(draw,0,3,"Temp:"+str(temp))
       oled_write(draw,0,4,"BPM:"+str(bpm))
       oled_write(draw,0,5,"SPO2:"+str(spo2))
       oled_write(draw,0,2,'sensor stoped!')
       disp.image(image)
       disp.display()
       add.uploap(int(temp),int(spo2),int(bpm), int(HN))
       return temp

def oled_init():

        RST = 24
        global disp
        global image
        global draw

        disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
        disp.begin()
        disp.clear()
        disp.display()

        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0,0,width,height), outline=0, fill=0)

def oled_write(draw, x, y, msg):
        padding = -2
        top = padding
#       bottom = height-padding
        font = ImageFont.load_default()
        draw.text((x,top + (8*y)), msg,font=font,fill=255)

def finish():
       print("finish")
       oled_init()
       oled_write(draw,0,3,"Finish")
       disp.image(image)
       disp.display()



GPIO.setwarnings(False) # Ignore warning for now

GPIO.setmode(GPIO.BCM) # Use physical pin numbering

GPIO.setup(back, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(next, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(end, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.add_event_detect(back,GPIO.RISING,callback=welcome) # Setup event on pin 10 rising edge
GPIO.add_event_detect(next,GPIO.RISING,callback=welcome)
GPIO.add_event_detect(end,GPIO.RISING,callback=welcome)

#message = input("Press enter to quit\n\n")


oled_init()

with open(file_path, "r") as file:
    data = file.readlines()

oled_write(draw, 0, 0, "Hello")
oled_write(draw, 0, 1,"HN:"+" ".join( data1))
oled_write(draw, 0, 2,"Name:"+" ".join(data))

disp.image(image)
disp.display()

print(data)

message = input("Press enter to quit\n\n")

GPIO.cleanup() # Clean up


