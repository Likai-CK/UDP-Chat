# UDP Server 
# Spring 2018
# Christopher Kelly
# Christopher Corbett
# https://pymotw.com/3/socket/multicast.html


import socket
import struct
import sys


def main():
	
	# THIS IS A WORKING PORTION THAT WILL HANDLE INCOMING UDP MESSAGES FROM CLIENTS.
	port = 12000
	
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp socket
	server_socket.bind(('', port)) # listen on port 

	# THIS IS A WORKING PORTION THAT WILL HANDLE OUTGOING, MULTICAST MESSAGES TO ALL CLIENTS:
	multicast_group = ('224.3.29.71', 10000)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# Set a timeout so the socket does not block
	# indefinitely when trying to receive data.
	sock.settimeout(0.2)
	
	# Set the time-to-live for messages to 1 so they do not
	# go past the local network segment.
	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	
	output = "Test Output" # this is what the server will output to the clients
	print("Online.")
	while True:
		try:
			message, address = server_socket.recvfrom(1024) # receive from incoming udp messages straight from clients
			# Send data to the multicast group
			print("[" + str(address[0]) + "] " + str(message.decode()))
			#print("Sending a response to {!r}:" + output)
			sock.sendto(message, multicast_group)
		except Exception as e:
			print("unexpected error: " + e)
			
		
		
if __name__ == "__main__":
	main()