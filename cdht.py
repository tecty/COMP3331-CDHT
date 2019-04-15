#!python3
import os
from ping import UdpClient, UdpServer, FileSender
from store import Store
from threading import Timer,Thread, Lock
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
            elif argv[0] == 'quit':
                # gracefully depart 
                Store()['controller'].departure()
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
            self.workers = [self.add_suc(t) for t in peer_ids]
            # start the info server (TCP server)
            # to receive the information
            InfoSer().start()


        # start up this ping server to accept pign 
        self.ping_ser = UdpServer()
        self.ping_ser.start()
        # start to accept the user input
        InputWorker().start()

        # exit approve count 
        self.exit_approve = 0
        self.exit_approve_lock = Lock()

    def add_suc(self, peer_id):
        """
        start the client
        and record the new successor
        """ 
        self.peer.add_suc(peer_id)
        worker = UdpClient(peer_id)
        worker.start()
        return worker

    def get_suc(self,  index):
        # just pass the implementation to reduce 
        # coupling 
        return self.peer.get_suc(index)
        

    def prompt_sus(self):
        # prompt the new relationship 
        print("My first successor is now peer "+str(self.peer.get_suc(0))+".")
        print("My second successor is now peer "+str(self.peer.get_suc(1))+".")



    def departure(self):
        """
        This client will leave, kill all ping client send message by TCP
        """
        # stop pinging
        [w.stop() for w in self.workers]

        # Inform the preseccor to exit 
        InfoClient(
            self.peer.get_pre(0), INFO_PEER_EXIT, self.peer.get_suc(1)
        ).start()
        InfoClient(
            self.peer.get_pre(1), INFO_PEER_EXIT, self.peer.get_suc(0)
        ).start()

    def handle_allow_exit(self):
        # other peer tell me I can exit
        self.exit_approve_lock.acquire()
        self.exit_approve += 1
        if self.exit_approve == 2:
            # exit the main thread 
            os._exit(0)
        self.exit_approve_lock.release()


    def handle_peer_departure(self, depart_id:int, new_next:int):
        # prompt the depart 
        print("Peer "+str(depart_id)+" will depart from the network.")
        # print("Debug: new sus: "+ str(new_next))
        
        # remove the old successor 
        self.peer.del_suc(depart_id)
        # stop the ping to depart server
        [w.stop() for w in self.workers if w.server_id == depart_id]
        # update the worker list
        self.workers = [w for w in self.workers if w.server_id != depart_id]
        
        # add a worker for new successor 
        self.handle_new_sus(new_next)
        
    def suc_leave (self, depart_id:int):
        # leaving of succsor 
        self.workers = [w for w in self.workers if w.server_id != depart_id]
        self.peer.del_suc(depart_id)
        # get the current alive succsor
        """
        Send a request for new successor via TCP
        """
        # print("Debug: I get help from " + str(self.peer.get_suc(0)))
        InfoClient(self.peer.get_suc(0), INFO_PEER_LOSS, depart_id).start()
        

    def handle_new_sus(self, new_next:int):
        # print("Debug: I will get a new suc: " + str(new_next))
        self.workers.append(self.add_suc(new_next))
        self.prompt_sus()

    def add_pre(self, pre_id):
        """
        Call by Pingserver to record the presessor        
        """
        self.peer.add_pre(pre_id)

    def pre_leave (self, pre, new_pre):
        """
        Pre seccsor ask to depreacate a precessor
        This will not use
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
            InfoClient(
                self.peer.get_suc(0), INFO_FILE_REQ, file_id, requester_id
            ).start()

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
        print(
            "File request message for "+str(file_id)+
            " has been sent to my successor."
        )
        # send to the recevier to open the port 
        InfoClient(
            self.peer.get_suc(0), INFO_FILE_REQ, file_id, self.my_id
        ).start()
        
        
if __name__ == "__main__":
    import sys


    """
    Set up the arguements 
    """
    Store()['my_id'] = int(sys.argv[1])
    Store()['MSS'] = int(sys.argv[4])
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