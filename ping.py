#!python3
import socket
import threading
from time import sleep
from store import Store

BASE_PORT = Store()['BASE_PORT']
PING_SLEEP= Store()['PING_SLEEP']
LOSS_RATE = Store()['LOSS_RATE']

class UdpClient(threading.Thread):
    def __init__(self, server_id):
        threading.Thread.__init__(self)
        # create a udp socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # store the server id need to connect 
        self.server_id = server_id

    def run(self):
        while True:
            # ping the server 
            sleep(PING_SLEEP)
            self.sock.sendto(
                Store()['my_id'].to_bytes(8,byteorder='big'), 
                ("127.0.0.1", BASE_PORT+self.server_id)
            )

            #  I should have a response from server 
            data, addr = self.sock.recvfrom(2048)
            print(
                "A ping response message was received from Peer " + 
                str(addr[1]-BASE_PORT) + "."
            )

        
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
            client_id = int.from_bytes(data, 'big')
            
            print(
                "A ping request message was received from Peer " + 
                str(client_id) + "."
            )
            # send back to ping client 
            self.sock.sendto(Store()['my_id'].to_bytes(8, byteorder='big'), addr)
