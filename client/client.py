# UDP Client
# Spring 2018
# Christopher Kelly
# Christopher Corbett
# https://pymotw.com/3/socket/multicast.html
import socket
import struct
import sys
import threading

class ThreadedClient(threading.Thread):
		# THIS PART IS FULLY FUNCTIONING UDP SEND FUNCTIONS, TAILORED TO CONTACT
		# SERVER IP DIRECTLY
		# address = "127.0.0.1"
		port = 12000
		
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		client_socket.settimeout(4.0)
		addr = (address, port)

	def sendMessage(self, username, socket, addr):
		message = ""
		while(True):
			if(message):
				message = (username + ">>" + input(username + ">>")).encode()
				socket.sendto(message, addr) # send to server
		return False
		#if(message):
			#print("\033[A                             \033[A")    # ansi escape arrow up then overwrite the line

	def recvMessage(self, sock):
		

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
		while(True):
			data, address = sock.recvfrom(1024) # receive from multicast groupto', address)
			if(data):
				print(data.decode())
				data = ""
		return False


	def listen(self):
		address = input("Enter IP/hostname (empty for localhost):\n")
		if not address:
			address = "127.0.0.1" # default

		username = input("Enter Nickname: ")


		
		#print(socket.gethostbyname_ex(socket.gethostname()))
		try:
			threading.Thread(target = self.sendMessage, args = username, ).start()
			#sendMessage(username, client_socket, addr)
			threading.Thread(target = self.recvMessage).start()
			#data, address = recvMessage(sock)
			#print(data.decode())
		except Exception as e:
			print("Server Disconnect: " + str(e))

def main():
	ThreadedClient().listen()

if __name__ == '__main__':
	main()