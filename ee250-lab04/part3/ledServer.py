# LED Server
#
# This program runs on the Raspberry Pi and accepts requests to turn on and off
# the LED via TCP packets.

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')

import grovepi

# use TCP

import socket

import time
from grovepi import *

def Main():

	# Connect the Grove LED to digital port D4
	led = 2

	pinMode(led,"OUTPUT")
	time.sleep(1)

	#print ("This example will blink a Grove LED connected to the GrovePi+ on the port labeled D4.\nIf you're having trouble seeing the LED blink, be sure to check the LED connection and the port number.\nYou may also try reversing the direction of the LED on the sensor.")
	#print (" ")
	#print ("Connect the LED to the port labele D4!" )

	host = '192.168.1.169'
	port = 5000

	s = socket.socket()
	s.bind((host,port))

	s.listen(1)
	c, addr = s.accept()
	print("Connection from: " + str(addr))
	while True:
		data = c.recv(1024).decode('utf-8')
		if not data:
			break
		print("From connected user: " + data)
		if data == 'LED_ON':
			try:
				#Blink the LED
				digitalWrite(led,1)		# Send HIGH to switch on LED
				print ("LED ON!")
				time.sleep(1)

				digitalWrite(led,0)		# Send LOW to switch off LED
				print ("LED OFF!")
				time.sleep(1)

			except KeyboardInterrupt:	# Turn LED off before stopping
				digitalWrite(led,0)
				break
			except IOError:				# Print "Error" if communication error encountered
				print ("Error")
		data = data.upper()
		print("Sending: " + data)
		c.send(data.encode('utf-8'))
	c.close()

if __name__ == '__main__':
	Main()
