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
        [self.peer.add_suc(t) for t in peer_ids]
        
        # star the ping client 
        for i in range(2):
            self.start_ping_client(i)

        # start up this ping server to accept pign 
        self.start_pign_ser()


    def start_ping_client(self, index):
        # wrap and start the client 
        UdpClient(self.peer.get_suc(index)).start()
        
    def start_pign_ser(self):
        UdpServer().start()


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