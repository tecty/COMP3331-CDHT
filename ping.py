#!python3
import socket
import threading
import random
from time import sleep
from store import Store
from headers import Message
from event import * 

BASE_PORT = Store()['BASE_PORT']
PING_SLEEP= Store()['PING_SLEEP']
LOSS_RATE = Store()['LOSS_RATE']


# Const for request type 
PING = 1
RECV_PING= 2
FILE = 3 
FILE_ACK = 4

# Evnet type 
EVENT_SEND = 1
EVENT_RECV = 2 
EVENT_DROP = 3
EVENT_RETR = 4


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
            msg = Message()
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
        self.ping(0.99)            

class UdpServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # create a socket 
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        # bind to a port 
        self.sock.bind(("127.0.0.1", BASE_PORT + Store()['my_id']) ) 
        self.file = None

    def answer_ping(self, msg, addr):
        client_id = msg.header[1] 
        
        print(
            "A ping request message was received from Peer " + 
            str(client_id) + "."
        )

        # register this server is alive 
        Store()['controller'].add_pre(client_id)

        
        # send back to ping client 
        msg= Message()
        msg.setHeader(RECV_PING, Store()['my_id'])
        
        self.sock.sendto(msg.segment, addr)

    def wait_file(self, file_name:int ):
        # tell the server to prepare a file income
        self.file = open(
            str(file_name) +"_"+ str(Store()['my_id'])+".pdf",
            'wb+'
        )

        # a log file to write 
        self.event_log = EventLog(open('requesting_log.txt' , 'w+'))

        print("We now start receiving the file ………")

        self.ack = 0 

    def answer_file(self, msg:Message, addr):
        self.file.write(msg.body)
        # record the expected ack 
        self.ack += msg.getBodySize()

        # Log it 
        self.event_log.event = EVENT_RECV
        self.event_log.seq_num = msg.header[1]
        self.event_log.ack = self.ack
        self.event_log.buf_len = msg.getBodySize()
        self.event_log.log()

        if msg.getBodySize() != Store()['MSS']:
            # this file transfer is finished 
            self.event_log.finish()
            self.file.close()
            print("The file is received.")

        # construct the new message
        msg = Message()
        msg.setHeader(FILE_ACK, self.ack)
        


        # DEBUG：
        # print("ACK: " + str(msg.header))
        # exit()
        # send back an ack for sender to send next 
        self.sock.sendto(msg.segment, addr)

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(2048)
            # loss the package as setted 
            # critical value for idenitfy loss
            critical_val = random.random()

            # deconstruct the message
            msg = Message(data)
            
            # we lost this package 
            if  critical_val <= Store()['LOSS_RATE']:
                # log the packet drop if it's file request 
                if msg.header[0] == FILE:
                    self.event_log.event =  EVENT_DROP
                    self.event_log.ack = -1 
                    self.event_log.seq_num = msg.header[1]
                    self.event_log.buf_len = msg.getBodySize()
                    self.event_log.log()
                continue
            
            
            # dispatch by header type 
            if msg.header[0] == PING:
                self.answer_ping(msg, addr)
            elif msg.header[0] == FILE:
                self.answer_file(msg, addr)



class FileSender(threading.Thread):
    """
    Sender send to UDP server 
    """
    def __init__(self, peer_id, file_name='cdht.py'):
        threading.Thread.__init__(self)
        self.port_num = peer_id + BASE_PORT
        self.file_name = file_name

        # set up the sender as udp 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

        # file
        self.file = open(file_name, 'rb')
        # log handle 
        self.event_log = EventLog(open('responding_log.txt' , 'w+'))

        # ack byte 
        self.ack = 0


    def send_buf(self, buf, is_retr:bool = False):
        """
        Logic for send the buffer 
        """

        # buffer to message 
        msg = Message()
        # set up the message 
        msg.setHeader(FILE, self.ack)
        # print("SEND: " + str(msg.header))
        msg.body = buf

        # send the datagrame
        self.sock.sendto(
            msg.segment, 
            ("127.0.0.1", self.port_num)
        )

        # log this send 
        if is_retr :
            self.event_log.event = EVENT_RETR
        else:
            self.event_log.event = EVENT_SEND
        self.event_log.ack = self.ack 
        self.event_log.buf_len = len(buf)
        self.event_log.seq_num = self.ack
        self.event_log.log()

        try:
            #  I should have a response from server 
            data, addr = self.sock.recvfrom(2048)
            msg = Message(data)

            if msg.header[1] == self.ack + len(buf):
                # log this receive 
                self.event_log.event = EVENT_RECV
                self.event_log.ack = msg.header[1]
                self.event_log.buf_len = 0
                self.event_log.seq_num = self.ack
                self.event_log.log()

            else:
                # re-send it 
                self.send_buf(buf, True)
        except socket.timeout as e:
            # send this buffer again
            self.send_buf(buf, True)

    def run(self):
        # wait for the peer to setup it's waiting file 
        buf = self.file.read(Store()['MSS'])
        print("We now start sending the file ………")
        time.sleep(1)
        while  buf:
     
            # try to send the buffer to server
            self.send_buf(buf)

            # expect ack increment 
            self.ack += len(buf)

            # get new buffer
            buf = self.file.read(Store()['MSS'])

        print("The file is sent.")

if __name__ == "__main__":
    """
    Self sending test 
    """
    # we can handling the loss
    Store()['LOSS_RATE'] = 0.1

    Store()['my_id'] = 2

    ser = UdpServer()
    ser.wait_file(2012)
    ser.start()


    # send file 2012 to 2 server 
    FileSender(2, "2012.pdf").start()