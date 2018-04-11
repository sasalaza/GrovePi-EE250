import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime 

# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
ultrasonic_ranger1_topic = "ultrasonic_ranger1"
ultrasonic_ranger2_topic = "ultrasonic_ranger2"

# Lists holding the ultrasonic ranger sensor distance readings. Change the
# value of MAX_LIST_LENGTH depending on how many distance samples you would
# like to keep at any point in time.
MAX_LIST_LENGTH = 100
SUB_LIST_LENGTH = 10
ranger1_dist = []
ranger2_dist = []
average1 = []
average2 = []
difference1 = []
difference2 = []
temp1 = []
temp2 = []
set1 = []
set2 = []
differencelist = [0, 0]

def ranger1_callback(client, userdata, msg):
	global ranger1_dist
	ranger1_dist.append(int(msg.payload))
	#truncate list to only have the last MAX_LIST_LENGTH values
	ranger1_dist = ranger1_dist[-MAX_LIST_LENGTH:]

def ranger2_callback(client, userdata, msg):
	global ranger2_dist
	ranger2_dist.append(int(msg.payload))
	#truncate list to only have the last MAX_LIST_LENGTH values
	ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(ultrasonic_ranger1_topic)
	client.message_callback_add(ultrasonic_ranger1_topic, ranger1_callback)
	client.subscribe(ultrasonic_ranger2_topic)
	client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))

if __name__ == '__main__':
	# Connect to broker and start loop
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(broker_hostname, broker_port, 60)
	client.loop_start()
	hdr = {
	    'Content-Type': 'application/json',
	    'Authoerization': None
	}
	payload = {
	    'time': str(datetime.now()),
	    'event': "None"
	}

	string1 = ""
	string2 = ""
	time.sleep(4)

	set1 = ranger1_dist[-10:]
	set2 = ranger2_dist[-10:]
	sum1 = 0
	sum2 = 0
	for i in range(0,len(set1)):
		if set1[i] >= 125:
			set1[i]=125
		if set2[i] >= 125:
			set2[i]=125
		sum1 = sum1 + set1[i]
		sum2 = sum2 + set2[i]
	threshold1 = sum1/SUB_LIST_LENGTH
	threshold2 = sum2/SUB_LIST_LENGTH
	print("Threshold1: " + str(threshold1))
	print("Threshold2: " + str(threshold2))
	
	while True:
		""" You have two lists, ranger1_dist and ranger2_dist, which hold a window
		of the past MAX_LIST_LENGTH samples published by ultrasonic ranger 1
		and 2, respectively. The signals are published roughly at intervals of
		200ms, or 5 samples/second (5 Hz). The values published are the
		distances in centimeters to the closest object. Expect values between
		0 and 512. However, these rangers do not detect people well beyond
		~125cm. """

		# TODO: detect movement and/or position

		#print("ranger1: " + str(ranger1_dist[-1:]) + ", ranger2: " +
		#    str(ranger2_dist[-1:]))
		tempstring = ""
		sum1 = 0
		sum2 = 0
		temp1 = ranger1_dist[-10:]
		temp2 = ranger2_dist[-10:]

		#print(temp1)
		
		#print(temp2)

		for i in range(0,len(temp1)):
			if temp1[i] >= 125:
				temp1[i]=125
			if temp2[i] >= 125:
				temp2[i]=125
			sum1 = sum1 + temp1[i]
			sum2 = sum2 + temp2[i]
		sum1 = sum1/SUB_LIST_LENGTH
		sum2 = sum2/SUB_LIST_LENGTH

		#print(str(sum1)+","+str(sum2))
			
		average1.append(sum1)
		average2.append(sum2)
		difference1.append(int(threshold1-sum1))
		difference2.append(int(threshold2-sum2))
		sum1 = 0
		sum2 = 0
		average1 = average1[-SUB_LIST_LENGTH:]
		average2 = average2[-SUB_LIST_LENGTH:]
		difference1 = difference1[-SUB_LIST_LENGTH:]
		difference2 = difference2[-SUB_LIST_LENGTH:]
		#print(difference1)
		#print(difference2)
	
		for i in range(0,len(difference1)-1):
			if difference1[i] > 20 and difference1[i]>sum1:
				sum1 = difference1[i]
			if difference2[i] > 20 and difference2[i]>sum2:
				sum2 = difference2[i]
		if difference1[-1] <= 20 and sum1 > 20:
			if string1 == "":
				string1 = "sensor1"
			elif string2 == "" and string1 != "sensor1":
				if string2 == "":
					string2 = "sensor1"
		if difference2[-1] <= 20 and sum2 > 20:
			if string1 == "":
				string1 = "sensor2"
			elif string2 == "" and string1 != "sensor2":
				if string2 == "":
					string2 = "sensor2"
				
		if string1 != "" and string2 !="":
			if string1 == "sensor1":
				tempstring = "Moving Left"
			elif string1 == "sensor2":
				tempstring = "Moving Right"
			string1 = ""
			string2 = ""
			difference1[:] = []
			difference2[:] = []
		print(tempstring)
		
		"""
		sum1 = (average1[len(average1)-1]-average1[0])/(SUB_LIST_LENGTH-1)
		sum2 = (average2[len(average2)-1]-average2[0])/(SUB_LIST_LENGTH-1)

		difference1.append(sum1)
		difference2.append(sum2)
		sum1 = 0
		sum2 = 0
		if len(difference1) >= MAX_LIST_LENGTH:
			for i in range(0,len(difference1)):
				sum1 = sum1 + difference1[i]
				sum2 = sum2 + difference2[i]
			sum1 = sum1/len(difference1)
			sum2 = sum2/len(difference2)
			if abs(sum1)>=abs(sum2)-1 or abs(sum1)<=abs(sum2)+1:
				tempstring = "Still"
			elif sum1 < sum2:
				tempstring = "Moving Right"
			elif sum2 > sum1:
				tempstring = "Moving Left"
			difference1[:] = []
			difference2[:] = []
		"""
		#print(average1)
		#print(average2)
		"""
		if tempstring != "":
			payload['event'] = tempstring
			response = requests.post("http://0.0.0.0:5000/post-event", headers = hdr, data = json.dumps(payload))
			print(response.json())
		"""	
		"""
		#sum1 = average1[len(average1)-1]-average1[0]
		#sum2 = average2[len(average2)-1]-average2[0]
		#print(str(sum1)+","+str(sum2))

		for i in range(0, len(average1)-1):
			difference1.append(int(average1[len(average1)-1-i]-average1[len(average1)-1-i-1]))
			difference2.append(int(average2[len(average2)-1-i]-average2[len(average2)-1-i-1]))		
		difference1 = difference1[-SUB_LIST_LENGTH:]
		difference2 = difference2[-SUB_LIST_LENGTH:]
		
		for i in range(0, len(difference1)):
			sum1 = sum1 + difference1[i]
			sum2 = sum2 + difference2[i]

		sum1 = sum1/SUB_LIST_LENGTH
		sum2 = sum2/SUB_LIST_LENGTH

		print(str(sum1)+","+str(sum2))	

		
		for i in range(0,len(average1)-1):
			difference1.append(int(average1[i]-average1[i+1]))
			sum1 = sum1 + difference1[i]
			difference2.append(int(average2[i]-average2[i+1]))
			sum2 = sum2 + difference2[i]
		difference1 = difference1[-SUB_LIST_LENGTH:]
		difference2 = difference2[-SUB_LIST_LENGTH:]	
	
		#print(difference1)
		#print(difference2)	
		#print(str(sum1-sum2))
		
		differencelist.append(sum1-sum2)
		differencelist = differencelist[-2:]
		second_diff = differencelist[1]-differencelist[0]
		if abs(second_diff)<40:
			print("still")
		else:
			if second_diff>=50:
				print("moving right")
			elif second_diff<=-50:
				print("moving left")
		"""
		time.sleep(0.2)
