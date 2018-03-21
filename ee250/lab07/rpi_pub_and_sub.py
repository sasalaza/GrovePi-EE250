"""EE 250L Lab 07 Skeleton Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import grovepi

ultrasonic_pin = 3
led_pin = 2

def custom_callback(client, userdata, message):
	print("custom_callback: " + message.topic + " " + "\"" + str(message.payload, "utf-8") + "\"")

	if message.topic == "LED_ON":
		digitalWrite(led_pin, 1)
	else:
		digitalWrite(led_pin, 0)

def on_connect(client, userdata, flags, rc):
	print("Connected to server (i.e., broker) with result code "+str(rc))

	#subscribe to topics of interest here
	client.subscribe("anrg-pi3/led")
	client.message_callback_add("anrg-pi3/led", custom_callback)

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
		time.sleep(1)
