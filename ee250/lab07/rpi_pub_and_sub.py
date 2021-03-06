"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""
import sys
sys.path.append('../../Software/Python/')

import paho.mqtt.client as mqtt
import time
import grovepi

from grovepi import *
from grove_rgb_lcd import *

ultrasonic_pin = 3
led_pin = 2
button = 8

pinMode(led_pin, "OUTPUT")
pinMode(button, "INPUT")

def custom_callback(client, userdata, message):
	print("custom_callback: " + message.topic + " " + "\"" + str(message.payload, "utf-8") + "\"")
	print(str(message.payload, "utf-8"))
	if str(message.payload) == "b\'LED_ON\'":
		print("on")
		digitalWrite(led_pin, 1)
	elif str(message.payload) == "b\'LED_OFF\'":
		print("off")
		digitalWrite(led_pin, 0)

def custom_callback2(client, userdata, message):
	print("custom_callback: " + message.topic + " " + "\"" + str(message.payload, "utf-8") + "\"")
	print(str(message.payload, "utf-8"))
	if str(message.payload) == "b\'w\'":
		print("on")
		setText("w")
		setRGB(255, 0, 0)
	elif str(message.payload) == "b\'a\'":
		print("off")
		setText("a")
		setRGB(0, 255, 0)
	elif str(message.payload) == "b\'s\'":
		print("off")
		setText("s")
		setRGB(0, 0, 255)
	elif str(message.payload) == "b\'d\'":
		print("off")
		setText("d")
		setRGB(255, 255, 255)

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))

	#subscribe to topics of interest here
	client.subscribe("anrg-pi3/led")
	client.message_callback_add("anrg-pi3/led", custom_callback)
	
	client.subscribe("anrg-pi3/lcd")
	client.message_callback_add("anrg-pi3/lcd", custom_callback2)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
	print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

if __name__ == '__main__':
	#this section is covered in publisher_and_subscriber_example.py
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()

	while True:
		try:
			message = str(grovepi.ultrasonicRead(ultrasonic_pin))
		except TypeError:
			message = "TypeError"
		except IOError:
			message = "IOError"
		client.publish("anrg-pi3/ultrasonicRanger", message)
		buttonState = digitalRead(button)
		if buttonState == 1:
			client.publish("anrg-pi3/button", "Button pressed!")
		time.sleep(1)
