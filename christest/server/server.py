import queue
import socket
import time
import threading

SVR_ADDR = '0.0.0.0'
SVR_PORT = 12000

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

class UDPServer(threading.Thread):
    def __init__(self, serverhost = '0.0.0.0', serverport = 12000, mcastgroup = '224.1.1.1', mcastport = 5007):
        self.serverhost = serverhost
        self.serverport = serverport
        self.mcastgroup = mcastgroup
        self.mcastport = mcastport
        self.messagebuffer = queue.Queue()
        self.threads = []
        self.aliases = {}

    def start(self):
        listenThread = threading.Thread(target = self.listen)
        listenThread.start()
        print('Listen thread started')
        self.threads.append(listenThread)
        multicastThread = threading.Thread(target = self.multicasthandling)
        multicastThread.start()
        print('Multicast handling thread started')
        self.threads.append(multicastThread)

    def listen(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverSocket.bind((self.serverhost, self.serverport))
        print('Server ready to receive messages at address {address}'.format(address = serverSocket.getsockname()))
        while True:
            message, address = serverSocket.recvfrom(255)
            self.messagebuffer.put((address, message))

    def multicasthandling(self):
        multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        while True:
            if self.messagebuffer.empty():
                continue
            item = self.messagebuffer.get()
            address = item[0]
            message = item[1].decode()
            if address not in self.aliases:
                self.aliases[address] = address[0]
            if message[0] == '/':
                commands = message.split(' ')
                commands[0].lower()
                if commands[0] == '/alias':
                    alias = " ".join(commands[1:])
                    prevalias = self.aliases[address]
                    self.aliases[address] = alias
                    modifiedmessage = '{prevalias} aliased to {alias}'.format(prevalias = prevalias, alias = self.aliases[address]).encode()
                elif commands[0] == '/hello':
                    modifiedmessage = 'Welcome, {alias}.  You can find commands /help'.format(alias = self.aliases[address]).encode()
                elif commands[0] == '/help':
                    modifiedmessage = ('/alias [alias] : Changes your display name from ip address\n/hello          : Displays the welcome message\n/help           : Displays available commands').encode()
                else:
                    modifiedmessage = 'Unrecognized command {commands[0]}'.format(commands = commands).encode()
                multicastSocket.sendto(modifiedmessage, address)
            else:
                modifiedmessage = '<{alias}> : {message}'.format(alias = self.aliases[address], message = message).encode()
                multicastSocket.sendto(modifiedmessage, (self.mcastgroup, self.mcastport))

if __name__ == '__main__':
    chatServer = UDPServer()
    chatServer.start()
