# UDP Client
# Spring 2018
# Christopher Kelly
# Christopher Corbett
# https://pymotw.com/3/socket/multicast.html
import socket
import struct
import sys

def main():
	address = input("Enter IP/hostname (empty for localhost):\n")
	if not address:
		address = "127.0.0.1" # default
	
	username = input("Enter Nickname: ")

	
	# THIS PART IS FULLY FUNCTIONING UDP SEND FUNCTIONS, TAILORED TO CONTACT
	# SERVER IP DIRECTLY
	# address = "127.0.0.1"
	port = 12000

	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.settimeout(4.0)
	addr = (address, port)


	# THIS PART IS FULLY FUNCTIONING MULTICAST RECEIPT
	# The client will listen to the multicast group.
	multicast_group = '224.3.29.71'
	server_address = ('', 5007)

	# Create the socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(4.0)
	# Bind to the server address - THIS ISNT NECESSARY ON THE CLIENT!
	sock.bind(server_address)

	# Tell the operating system to add the socket to
	# the multicast group on all interfaces.
	group = socket.inet_aton(multicast_group)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	sock.setsockopt(
		socket.IPPROTO_IP,
		socket.IP_ADD_MEMBERSHIP,
		mreq)

	#print(socket.gethostbyname_ex(socket.gethostname()))

	while True:
		try:
			message = (username + ">>" + input(username + ">>")).encode()
			if(message):
				print("\033[A                             \033[A")    # ansi escape arrow up then overwrite the line
				client_socket.sendto(message, addr) # send to server
				message = ""
			data, address = sock.recvfrom(1024) # receive from multicast groupto', address)
			#sock.sendto(b'ack', address)
			print(data.decode())
		except Exception as e:
			print("Server Disconnect: " + str(e))
	


if __name__ == '__main__':
	main()