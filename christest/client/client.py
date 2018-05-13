import socket
import struct
import threading

class UDPClient(threading.Thread):
    def __init__(self, serverhost = '192.168.80.102', serverport = 12000, mcastgroup = '224.1.1.1', mcastport = 5007):
        self.serverhost = serverhost
        self.serverport = serverport
        self.mcastgroup = mcastgroup
        self.mcastport = mcastport
        self.sockets = []
        self.threads = []

    def start(self):
        listenmulticastThread = threading.Thread(target = self.listenmulticast)
        listenmulticastThread.start()
        self.threads.append(listenmulticastThread)
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockets.append(clientSocket)
        listenudpThread = threading.Thread(target = self.listenudp, args = (clientSocket,))
        listenudpThread.start()
        self.threads.append(listenudpThread)
        messageThread = threading.Thread(target = self.message, args = (clientSocket,))
        messageThread.start()
        self.threads.append(messageThread)

    def listenmulticast(self):
        multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        multicastSocket.bind((self.mcastgroup, self.mcastport))
        mreq = struct.pack("4sl", socket.inet_aton(self.mcastgroup), socket.INADDR_ANY)
        multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            message = multicastSocket.recv(255)
            print(message.decode())

    def listenudp(self, sock):
        clientSocket = sock
        while True:
<<<<<<< HEAD
            message, address = clientSocket.recvfrom(255)
            print(message)
=======
            message, address = clientSocket.recvfrom(2048)
            print(message.decode())
>>>>>>> 8243d075b3ec1adb4cb5f0345a0eca6cdf998998

    def message(self, sock):
        clientSocket = sock
        message = '/hello'.encode()
        clientSocket.sendto(message, (self.serverhost, self.serverport))
        while True:
            message = input('').encode()
            clientSocket.sendto(message, (self.serverhost, self.serverport))

if __name__ == '__main__':
    chatClient = UDPClient()
    chatClient.start()
