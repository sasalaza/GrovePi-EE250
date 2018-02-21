# Ultrasonic Sensor Client
#
# This code runs on the Raspberry Pi. It should sit in a loop which reads from
# the Grove Ultrasonic Ranger and sends the reading to the Ultrasonic Sensor
# Server running on your VM via UDP packets.

import sys
# By appending the folder of all the GrovePi libraries to the system path here,
# we are able to successfully `import grovepi`
sys.path.append('../../Software/Python/')

import grovepi

import socket

def Main():

	# Connect the Grove Ultrasonic Ranger to digital port D4
	# SIG,NC,VCC,GND
	ultrasonic_ranger = 4

	while True:
		try:
			# Read distance value from Ultrasonic
			print(grovepi.ultrasonicRead(ultrasonic_ranger))

		except TypeError:
			print ("Error")
		except IOError:
			print ("Error")

    # Change the host and port as needed. For ports, use a number in the 9000
    # range.
    host = '127.0.0.1'
    port = 1023

    server_addr = '127.0.0.1'

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))

    # UDP is connectionless, so a client does not formally connect to a server
    # before sending a message.
    dst_port = input("destination port-> ")
    message = input("message-> ")
    while message != 'q':
        #tuples are immutable so we need to overwrite the last tuple
        server = (server_addr, int(dst_port))

        # for UDP, sendto() and recvfrom() are used instead
        s.sendto(message.encode('utf-8'), server)
        data, addr = s.recvfrom(1024)
        data = data.decode('utf-8')
        print("Received from server: " + data)
        dst_port = input("destination port-> ")
        message = input("message-> ")
    s.close()

if __name__ == '__main__':
    Main()
