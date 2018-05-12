import socket
import struct
import threading

class UDPClient(threading.Thread):
    def __init__(self, serverhost = '0.0.0.0', serverport = 12000, mcastgroup = '224.1.1.1', mcastport = 5007):
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
        messageThread = threading.Thread(target = self.message, args = (clientSocket,))
        messageThread.start()
        self.threads.append(messageThread)
        listenudpThread = threading.Thread(target = self.listenudp, args = (clientSocket,))
        listenudpThread.start()
        self.threads.append(listenudpThread)

    def listenmulticast(self):
        multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        multicastSocket.bind((self.mcastgroup, self.mcastport))
        mreq = struct.pack("4sl", socket.inet_aton(self.mcastgroup), socket.INADDR_ANY)

        multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            message = multicastSocket.recv(2048)
            print(message.decode())

    def listenudp(self, sock):
        clientSocket = sock
        while True:
            message, address = clientSocket.recvfrom(2048)
            print(message)

    def message(self, sock):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            message = input('').encode()
            clientSocket.sendto(message, (self.serverhost, self.serverport))

if __name__ == '__main__':
    chatClient = UDPClient()
    chatClient.start()