# UDP Server 
# Spring 2018
# Christopher Kelly
# Christopher Corbett
import socket

port = 12000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp socket
server_socket.bind(('', port)) # listen on port 

while True:
	message, address = server_socket.recvfrom(1024)
	server_socket.sendto(message, address)
	