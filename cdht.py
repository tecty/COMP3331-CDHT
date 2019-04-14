#!python3

from ping import UdpClient, UdpServer, FileSender
from store import Store
from threading import Timer,Thread
from peer import Peer
from info import InfoClient, InfoSer, INFO_FILE_REQ, INFO_PEER_EXIT, INFO_PEER_EXIT, INFO_PEER_LOSS, INFO_FILE_RES

def debug_print():
    print("DEBUG"+ str(Store()))
    Timer(10, debug_print)

class InputWorker(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        while(True):
            # always want to accept new value
            in_val= input()
            argv = in_val.split()
            if not argv:
                # not response anything
                pass
            elif argv[0] == 'request':
                try:
                    file_id = int(argv[1])
                except Exception as e:
                    print("Invalid input:" + str(argv))
                    continue
                if ( file_id < 0  or file_id > 10000):
                    print("File Id out of bound")
                    continue
                # let controller to handle file request 
                Store()['controller'].request_file(int(argv[1]))
            else: 
                print("Not Support: " + str(argv))

class Controller(object):
    def __init__(self,my_id, peer_ids, no_ping = False):
        # store my_id 
        self.my_id = my_id
        # set up the peer object 
        self.peer = Peer(my_id)
        if not no_ping: 
            # when we debug it, we don't want ping to border us
            [self.add_suc(t) for t in peer_ids]

        # start up this ping server to accept pign 
        self.ping_ser = UdpServer()
        self.ping_ser.start()
        # start to accept the user input
        InputWorker().start()

    def add_suc(self, peer_id):
        """
        start the client
        and record the new successor
        """ 
        UdpClient(peer_id).start()
        self.peer.add_suc(peer_id)
        

    def departure(self):
        """
        This client will leave, send message by TCP
        """
        pass

    def suc_leave (self, sec):
        # leaving of succsor 
        self.peer.del_suc(sec)
        # get the current alive succsor
        """
        Send a request for new successor via TCP
        """

    def add_pre(self, pre_id):
        """
        Call by Pingserver to record the presessor        
        """
        self.peer.add_pre(pre_id)

    def pre_leave (self, pre, new_pre):
        """
        Pre seccsor ask to depreacate a precessor
        """
        # leaving of presuccor 
        self.peer.del_pre(pre)
        self.peer.add_pre(new_pre)

    def handle_file_request (self, requester_id:int, file_id:int):
        if self.peer.has_file(file_id):
            # prompt
            print("File "+str(file_id)+" is here.")

            # send to the recevier to open the port 
            InfoClient(requester_id, INFO_FILE_RES, file_id).start()

            # startup the file tr 
            FileSender(requester_id, str(file_id)+".pdf").start()
        else: 
            # print File not here promet
            print("File "+str(file_id)+" is not stored here.")
            print("File request message has been forwarded to my successor.")

    def handle_file_waiting(self,from_id:int, file_id:int):
        print("Received a response message from peer "+str(from_id)+
            ", which has the file "+str(file_id)+".")
        self.ping_ser.wait_file(file_id)

    def request_file(self, file_id:int):
        if self.peer.has_file(file_id):
            print(
                "This peer have file " + str(file_id) + 
                " no need for request."
            )
            return
        # send to the recevier to open the port 
        InfoClient(self.peer.get_suc(0), INFO_FILE_RES, file_id).start()
        
        
if __name__ == "__main__":
    import sys


    """
    Set up the arguements 
    """
    Store()['my_id'] = int(sys.argv[1])
    Store()['MSS'] = float(sys.argv[4])
    Store()['LOSS_RATE'] = float(sys.argv[5])


    """
    Start up the controller 
    """
    Store()['controller'] =\
        Controller(Store()['my_id'],[
            int(sys.argv[2]),
            int(sys.argv[3])
        ])

    # start up the debug mode 
    debug_print()