"""EE 250L Lab 04 Starter Code
Team:
Michael Cross
Repo:
git@github.com:usc-ee250-spring2020/lab04-crossm.git


Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
import _thread #https://raspberrypi.stackexchange.com/questions/22444/importerror-no-module-named-thread/22464

PORT = 4

#global voltageVal
voltageVal = 0

def dim(client):

    print("Dim function activated")
    global voltageVal
    #https://www.geeksforgeeks.org/global-local-variables-python/
    while True:
        print("Running")
        if voltageVal != 0:
            voltageVal -= 1
            print("Light Value: {}".format(voltageVal))
            client.publish("dimUpdate", voltageVal)
        time.sleep(1)
            
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("buttonpress")
#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    
    global voltageVal
    if(msg.topic == 'buttonpress'):
        voltageVal = int(str(msg.payload, "utf-8"))
        print("Light Value: {}".format(voltageVal))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    
    voltageVal = 0
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    _thread.start_new_thread(dim, (client)) #https://www.tutorialspoint.com/python3/python_multithreading.htm
    
    while True:
        
        time.sleep(1)
            

