from threading import Thread
import socket
from store import Store
from headers import Message, int_to_bytes,bytes_to_int

BASE_PORT = Store()['BASE_PORT']

# enum of info to pass 
INFO_FILE_REQ = 10 
INFO_FILE_RES = 11 
INFO_PEER_LOSS = 20 
INFO_NEW_PEER = 21
# gracefully exit 
INFO_PEER_EXIT = 30 
INFO_EXIT_ACK = 31

"""
header: INFO_TYPE: Requester_id 
Body: value

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
        data = self.conn.recv(1024)
        # print(data)
        msg = Message(data)

        # handle by header 
        if msg.header[0] ==INFO_FILE_REQ:
            # print("File Request: " + str(msg.header[1]) )
            Store()['controller'].handle_file_request(
                msg.header[1],
                bytes_to_int(msg.body)
            )
            # callback, no response 
        if msg.header[0] ==INFO_FILE_RES:
            # I can start listening to the file 
            Store()['controller'].handle_file_waiting(
                msg.header[1],
                bytes_to_int(msg.body)
            )

        elif msg.header[0] ==INFO_PEER_LOSS:
            print("Peer Loss "  + str(msg.header[1]))
            # response needed
        elif msg.header[0] ==INFO_PEER_EXIT:
            # gracefully ext a peer
            print("Peer is gracefully exit " + str(msg.header[1]))
            # call back the main to update post
            Store()['controller'].handle_peer_departure(
                msg.header[1], bytes_to_int(msg.body)
            )


            # return the ack 
            reply = Message()
            reply.setHeader(INFO_EXIT_ACK, 0)
            self.conn.send(reply.segment)

        # print(bytes_to_int(msg.body))

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
    def __init__(self, server_id, info_type,
        info_val, requester_id = None):
        Thread.__init__(self)
        # store the passed in values
        self.server_id = server_id
        self.info_type = info_type
        self.info_val = info_val
        if requester_id:
            self.requester_id = requester_id
        else:
            self.requester_id = Store()['my_id']

        # setup the socket 
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.connect(("127.0.0.1", BASE_PORT+self.server_id))
        msg = Message()
        msg.setHeader(self.info_type, self.requester_id)
        msg.body = int_to_bytes(self.info_val)
        # send the message 
        self.sock.send(msg.segment)
        # some cases we need to wait response and do callback 
        if self.info_type in [INFO_PEER_LOSS, INFO_PEER_EXIT]:
            msg = Message(self.sock.recv(1024))
            if msg.header[0] == INFO_EXIT_ACK:
                # this peer is reconised the loss
                # callback the controller 
                Store()["controller"].handle_allow_exit()
            elif msg.header[0] == INFO_NEW_PEER:
                # register new peer
                pass

        # close the connection
        self.sock.close()