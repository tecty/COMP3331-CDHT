#!python3
import socket
import threading
import random
from time import sleep
from store import Store
from headers import Message


BASE_PORT = Store()['BASE_PORT']
PING_SLEEP= Store()['PING_SLEEP']
LOSS_RATE = Store()['LOSS_RATE']


# Const for request type 
PING = 1
RECV_PING= 2
FILE = 3 
FILE_ACK = 4


class UdpClient(threading.Thread):
    def __init__(self, server_id):
        threading.Thread.__init__(self)
        # create a udp socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # set the timeout to prevent forever waiting 
        self.sock.settimeout(1)


        # store the server id need to connect 
        self.server_id = server_id

    def ping(self, prob):
        """
        record the probability the client is down 
        """
        if prob == 1 : 
            sleep(PING_SLEEP)
        if prob <= 0.001: 
            """
            we have very great confident that this client is lost
            """
            print("Peer "+str(self.server_id)+" is no longer alive.")

            # tell the controller this successor is leaved
            Store()['controller'].suc_leave(self.server_id)

        else:
            # construct the message 
            msg = Message(Store()['MSS'])
            msg.setHeader(PING, Store()['my_id'])

            # server may dead 
            # ping the server 
            self.sock.sendto(
                msg.segment, 
                ("127.0.0.1", BASE_PORT+self.server_id)
            )
            try:
                #  I should have a response from server 
                data, addr = self.sock.recvfrom(2048)
                print(
                    "A ping response message was received from Peer " + 
                    str(addr[1]-BASE_PORT) + "."
                )
            except socket.timeout as e:
                self.ping(Store()['LOSS_RATE']* prob)
            else: 
                # this client is definately alive 
                self.ping(1)
                
    def run(self):
        self.ping(1)            

        
class UdpServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # create a socket 
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # bind to a port 
        self.sock.bind(("127.0.0.1", BASE_PORT + Store()['my_id']) ) 

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(2048)
            # loss the package as setted 
            if random.random() <= Store()['LOSS_RATE']:
                # we lost this package 
                # print('package loss')
                continue
            
            
            # deconstruct the message
            msg = Message(Store()['MSS'])
            msg.segment =data
            client_id = msg.header[1] 
            
            print(
                "A ping request message was received from Peer " + 
                str(client_id) + "."
            )
            # send back to ping client 

            msg= Message(Store()['MSS'])
            msg.setHeader(RECV_PING, Store()['my_id'])
            
            self.sock.sendto(msg.segment, addr)


class FileSender(threading.Thread):
    """
    Sender send to UDP server 
    """
    def __init__(self, peer_id, file_name='cdht.py'):
        threading.Thread.__init__(self)
        self.port_num = peer_id + 50000
        self.file_name = file_name

        # set up the sender as udp 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

        # file
        self.file = open(file_name, 'rb')

        # ack byte 
        self.ack = 0


    def send_buf(self, buf):
        """
        Logic for send the buffer 
        """

        # buffer to message 
        msg = Message(Store()['MSS'])
        # set up the message 
        msg.setHeader(FILE, self.ack)
        msg.body = buf

        # send the datagrame
        self.sock.sendto(
            msg.segment, 
            ("127.0.0.1", self.port_num)
        )
        try:
            #  I should have a response from server 
            data, addr = self.sock.recvfrom(2048)
            msg = Message(data)
            if msg.header[1] == self.ack:
                print(
                    "the client Recieved the buffer"
                )
            else:
                # re-send it 
                self.send_buf(buf)
        except socket.timeout as e:
            # send this buffer again
            self.send_buf(buf)

    def run(self):
        buf = self.file.read(Store()['MSS'])
            
        while  buf:
            # expect ack increment 
            self.ack += Store()['MSS']

            # try to send the buffer to server
            self.send_buf(buf)

            # get new buffer
            buf = self.file.read(Store()['MSS'])

if __name__ == "__main__":
    # send file 2012 to 
    FileSender(2).start()