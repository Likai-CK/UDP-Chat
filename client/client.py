# UDP Client
# Spring 2018
# Christopher Kelly
# Christopher Corbett

import socket

address = "127.0.0.1"
port = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(30.0)
addr = (address, port)

message = raw_input("msg>>")
client_socket.sendto(message, addr)

try:
		data, server = client_socket.recvfrom(1024)
		print(data)
except socket.timeout:
	print("Server Disconnect: Timed out")
except Exception as e:
	print("Server Disconnect: " + e.value)