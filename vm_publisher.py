"""EE 250L Lab 04 Starter Code
Team:
Michael Cross
Repo:
git@github.com:usc-ee250-spring2020/lab04-crossm.git

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
global val;
val = 1.0;

def update_val(x):
	global val;
	val = x;

def val_plus(x):
    if(x < 1.0):
        return x + 0.1;
    return x;

def val_minus(x):
    if(x > 0.1):
        return x - 0.1;
    return x;

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    
    #subscribe to topics of interest here
    

#Default message callback. Please use custom callbacks.
#NOT USED HERE
def on_message(client, userdata, msg):
    if(msg.topic == "buttonpress"):
        client.publish("VM: " + str(msg.payload, "utf-8") + " Fat button press")

def on_press(key):
    try: 
        k = key.char # single-char keys
    except: 
        k = key.name # other keys
    
    if k == 'w':
        val2 = val_plus(val);
        round(val2, 1);
        update_val(val2);
        #send "w" character to other console
        client.publish("buttonpress", "Light Value: " + "%0.1f" % val2)

    elif k == 'a':
        
        # send "a" character to other console
        client.publish("buttonpress", "a")
        #send "LED_ON"
    elif k == 's':
        val2 = val_minus(val);
        round(val2, 1);
        update_val(val2);
        # send "s" character to other console
        client.publish("buttonpress", "Light Value: " + "%0.1f" % val2)
    elif k == 'd':
        
        # send "d" character to other console
        client.publish("buttonpress", "d")

if __name__ == '__main__':
    #setup the keyboard event listener
    lis = keyboard.Listener(on_press=on_press)
    lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        on_press(lis)
        
        time.sleep(1)
            

