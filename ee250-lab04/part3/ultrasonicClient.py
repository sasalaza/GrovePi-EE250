import socket
import grovepi
import sys
sys.path.append('../../Software/Python')

def Main():
	# Change the host and port as needed. For ports, use a number in the 9000
	# range.
	ultrasonic_ranger = 3
	host = '192.168.1.169'
	port = 1024

	server_addr = '192.168.1.206'

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))

	# UDP is connectionless, so a client does not formally connect to a server
	# before sending a message.
	dst_port = input("destination port-> ")
	message = ''

	while message != 'q':

		try:
			message = str(grovepi.ultrasonicRead(ultrasonic_ranger))
		except TypeError:
			message = "Error"
		except IOError:
			message = "Error"

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
