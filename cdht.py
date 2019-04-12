#!python3

from ping import UdpClient, UdpServer
from store import Store
from threading import Timer
from peer import Peer


def debug_print():
    print("DEBUG"+ str(Store()))
    Timer(10, debug_print)


class Controller(object):
    def __init__(self,my_id, peer_ids ):
        # set up the peer object 
        self.peer = Peer(my_id)
        [self.add_suc(t) for t in peer_ids]
        

        # start up this ping server to accept pign 
        self.start_pign_ser()


    def add_suc(self, peer_id):
        """
        start the client
        and record the new successor
        """ 
        UdpClient(peer_id).start()
        self.peer.add_suc(peer_id)
        
    def start_pign_ser(self):
        UdpServer().start()

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

    def pre_leave (self, pre, new_pre):
        """
        Pre seccsor ask to depreacate a precessor
        """
        # leaving of presuccor 
        self.peer.del_pre(pre)
        self.peer.add_pre(new_pre)


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