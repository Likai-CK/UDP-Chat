import socket
import struct
import sys
import threading
import tkinter

class UDPClient(threading.Thread):
    def __init__(self, serverhost = '192.168.80.102', serverport = 12000, mcastgroup = '224.1.1.1', mcastport = 5007, bufsize = 2048):
        self.serverhost = serverhost
        self.serverport = serverport
        self.mcastgroup = mcastgroup
        self.mcastport = mcastport
        self.bufsize = bufsize
        self.running = True
        self.sockets = []
        self.threads = []
        self.top = tkinter.Tk()
        self.messagelist = []
        self.inputmessage = []

    def start(self):
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clientSocket.settimeout(0.2)

        self.top.title("Chatter")
        messages_frame = tkinter.Frame(self.top)
        self.inputmessage = tkinter.StringVar()
        #self.inputmessage.set("Message server")
        scrollbar = tkinter.Scrollbar(messages_frame)
        self.messagelist = tkinter.Listbox(messages_frame, height = 30, width = 100, yscrollcommand = scrollbar.set)
        scrollbar.pack(side = tkinter.RIGHT, fill = tkinter.Y)
        self.messagelist.pack(side = tkinter.LEFT, fill = tkinter.BOTH)
        self.messagelist.pack()
        messages_frame.pack()

        self.entry_field = tkinter.Entry(self.top, textvariable = self.inputmessage)
        self.entry_field.insert(0, 'Enter message')
        self.entry_field.bind('<FocusIn>', self.on_entry_click)
        self.entry_field.bind('<FocusOut>', self.on_focusout)
        self.entry_field.config(fg = 'grey')
        self.entry_field.bind("<Return>", lambda event, sock = clientSocket:
                                    self.sendmessage(sock))
        self.entry_field.pack()
        send_button = tkinter.Button(self.top, text = "Send", command = lambda sock = clientSocket:
                                                                        self.sendmessage(sock))
        send_button.pack()

        self.top.protocol("WM_DELETE_WINDOW", self.quit)

        listenmulticastThread = threading.Thread(target = self.listenmulticast)
        listenmulticastThread.start()
        self.threads.append(listenmulticastThread)

        self.sockets.append(clientSocket)
        listenudpThread = threading.Thread(target = self.listenudp, args = (clientSocket,))
        listenudpThread.start()
        self.threads.append(listenudpThread)
        message = '/hello'
        clientSocket.sendto(message.encode(), (self.serverhost, self.serverport))

        tkinter.mainloop()

    def listenmulticast(self):
        multicastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        multicastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        multicastSocket.settimeout(0.2)
        multicastSocket.bind((self.mcastgroup, self.mcastport))
        mreq = struct.pack('4sl', socket.inet_aton(self.mcastgroup), socket.INADDR_ANY)
        multicastSocket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while self.running:
            try:
                message = multicastSocket.recv(self.bufsize)
                self.messagelist.insert(tkinter.END, message)
            except socket.timeout:
                continue

    def listenudp(self, sock):
        clientSocket = sock
        while self.running:
            try:
                message, address = clientSocket.recvfrom(self.bufsize)
                msglist = message.decode().split("\n")
                for msg in msglist:
                    self.messagelist.insert(tkinter.END, msg)
            except socket.timeout:
                continue

    def sendmessage(self, sock, event = None):
        clientSocket = sock
        message = self.inputmessage.get()
        self.inputmessage.set('')
        if(message == '/quit'):
            self.quit()
        clientSocket.sendto(message.encode(), (self.serverhost, self.serverport))

    def on_entry_click(self, event):
        if self.entry_field.get() == 'Enter message':
            self.entry_field.delete(0, "end") # delete all the text in the entry
            self.entry_field.insert(0, '') #Insert blank for user input
            self.entry_field.config(fg = 'black')

    def on_focusout(self, event):
        if self.entry_field.get() == '':
            self.entry_field.insert(0, 'Enter message')
            self.entry_field.config(fg = 'grey')

    def quit(self):
        self.running = False
        for socket in self.sockets:
            socket.close()
        for thread in self.threads:
            thread.join()
        self.top.quit()
        sys.exit(0)

if __name__ == '__main__':
    chatClient = UDPClient()
    chatClient.start()
