from threading import Thread
import socket
from store import Store
from headers import Message

BASE_PORT = Store()['BASE_PORT']

# enum of info to pass 
INFO_FILE_REQ = 10 
INFO_FILE_RES = 11 
INFO_PEER_LOSS = 20 
INFO_NEW_PEER = 21
# gracefully exit 
INFO_PEER_EXIT = 30 

"""
FILE REQUEST:
Header: FILE_REQ : Requester Id 
Body: Request file
"""


class InfoWorker(Thread):
    def __init__(self, conn:socket, addr ):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
    def run(self):
        """
        This thead to handle it 
        """
        while True:
            data = self.conn.recv(1024)
            msg = Message(data)
            
            print(data)
        # close the connection 
        self.conn.close()

class InfoSer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", BASE_PORT + Store()['my_id'] ))
        self.sock.listen(5)
    def run(self):
        while True:
            # accept the newcomming connection
            con, addr = self.sock.accept()
            # new thead to handle the connection
            InfoWorker(con, addr).start()

class InfoClient(Thread):
    def __init__(self, server_id, info_type):
        Thread.__init__(self)
        self.server_id = server_id
    def run(self):
        pass

if __name__ == "__main__":
    pass