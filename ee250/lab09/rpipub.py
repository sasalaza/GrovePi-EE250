import paho.mqtt.client	as mqtt
import time
import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are able to successfully `import grovepi`
sys.path.append('../../Software/Python/')
import	grovepi
from grovepi import *
from grove_rgb_lcd import *

# Determines which digital port	the	ultrasonic ranger is plugged into (e.g.	a 
# value	of 4 would mean	port D4)
led_port = 3
temphum_port = 2
lcd_port = 7

#pinMode(led_port, "OUTPUT")

mqtt_broker_hostname = "eclipse.usc.edu"
mqtt_broker_port = 11000

led_topic = "anrg-pi15/led"
lcd_topic = "anrg-pi15/lcd"
temp_topic = "anrg-pi15/temp"
hum_topic = "anrg-pi15/hum"

def led_callback(client, userdata, msg):
	global power_stat
	if digitalRead(led_port) == 1:
		digitalWrite(led_port, 0)
	else:
		digitalWrite(led_port, 1)
		

def lcd_callback(client, userdata, msg):
	global mymessage
	mymessage = msg.payload[2:]
	setText(mymessage)
	setRGB(255,255,255)

def	on_connect(client, userdata, flags,	rc):
	print("Connected to server	(i.e., broker) with	result code	"+str(rc))
	client.subscribe(led_topic)
	client.message_callback_add(led_topic, led_callback)
	client.subscribe(lcd_topic)
	client.message_callback_add(lcd_topic, lcd_callback)

def	on_message(client, userdata, msg):
	print("on_message:	" +	msg.topic +	" "	+ str(msg.payload, "utf-8"))

	
if __name__	== '__main__':

	client	= mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(mqtt_broker_hostname, mqtt_broker_port,	keepalive=60)
	# have	paho.mqtt spawn	a background thread	for	us
	client.loop_start()

	while True:
		[temp,hum] = dht(temphum_port,0)
		t=str(temp)
		h=str(hum)
		#print(t+"\t"+h)
		client.publish(temp_topic,t)
		client.publish(hum_topic,h)
		time.sleep(1)
