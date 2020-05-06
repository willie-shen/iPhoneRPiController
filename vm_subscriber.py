"""EE 250L Lab 04 Starter Code
Team:
Michael Cross
Repo:
git@github.com:usc-ee250-spring2020/lab04-crossm.git


Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
import _thread
from pynput import keyboard #https://raspberrypi.stackexchange.com/questions/22444/importerror-no-module-named-thread/22464

PORT = 4

#global voltageVal
brightness = 0

onStart = 0
turnedOn = 0
totalOn = 0

def off():
    global onStart, turnedOn, totalOn
    timeElapsed = time.time() - onStart

    totalOn += timeElapsed

    averageTime = totalOn / turnedOn

    elapsedHour = int(timeElapsed / 3600)
    elapsedMin = (int(timeElapsed) - (elapsedHour*3600))/60
    elapsedSeconds = int(timeElapsed) - (elapsedHour*3600) - (elapsedMin*60)

    averageHour = int(averageTime / 3600)
    averageMin = (int(averageTime) - averageHour*3600)/60
    averageSeconds = int(averageTime) - (averageHour * 3600) - (averageMin * 60)

    print("Light was on for {0} hours {1} minutes {2} seconds".format(elapsedHour, elapsedMin, elapsedSeconds))
    print("Average time on is {0} hours {1} minutes {2} seconds".format(averageHour, averageMin, averageSeconds))




def start():
    global onStart, turnedOn
    onStart = time.time()
    turnedOn += 1

def on_press(key):
    try:
        k = key.char # single-char keys
    except:
        k = key.name # other keys
    global brightness
    if k == 'w':

        if brightness >= 0 and brightness < 100:

            if brightness == 0:
                start()

            brightness += 1
    #send "w" character to other console
    #https://www.w3resource.com/python/built-in-function/int.php
            voltageVal = int((brightness/100.0) * 1023)
            print("Light Value: {}".format(voltageVal))

            client.publish("updateBrightness", "{}".format(brightness))

    elif k == 'd':
    
    # send "d" character to other console
        if brightness <= 100 and brightness > 0:
            brightness -= 1
            voltageVal = int((brightness/100.0) * 1023)
            print("Light Value: {}".format(voltageVal))
            client.publish("updateBrightness", "{}".format(brightness))

            if brightness == 0:
                off()

def dim(client):

    print("Dim function activated")
    global brightness
    #https://www.geeksforgeeks.org/global-local-variables-python/
    while True:
        #print("Running")
        if brightness != 0:
            brightness -= 1
            voltageVal = int((brightness/100.0) * 1023)
            print("Light Value: {}".format(voltageVal))
            client.publish("dimUpdate", "{}".format(brightness))

            if brightness == 0:
                off()
        time.sleep(1)
            
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("buttonpress")
    client.subscribe("dimUpdate")
    client.subscribe("updateBrightness")
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    
    print(str(msg.payload, "utf-8"))
    global brightness
    if(msg.topic == 'buttonpress'):

        if brightness == 0:
            start()
        brightness = int(str(msg.payload, "utf-8"))

        if brightness == 0:
            off()
        voltageVal = int((brightness/100.0) * 1023)
        print("Light Value: {}".format(voltageVal))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    
    brightness = 0
    lis = keyboard.Listener(on_press=on_press)
    lis.start()
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="54.197.16.207", port=1883, keepalive=60)
    client.loop_start()

    _thread.start_new_thread(dim, (client,)) #https://www.tutorialspoint.com/python3/python_multithreading.htm
    
    while True:
        
        time.sleep(1)
            

