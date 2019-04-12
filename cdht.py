#!python3

from ping import UdpClient, UdpServer
from store import Store
from threading import Timer


def debug_print():
    print("DEBUG"+ str(Store()))
    Timer(10, debug_print)


class Controller(object):
    def __init__(self,my_id, peer):
        # get the peer list by order 
        peer =  [t for t in peer if t > my_id] +
            [t+256 for t in peer if t < my_id]




if __name__ == "__main__":
    import sys


    """
    Set up the arguements 
    """
    Store()['my_id'] = int(sys.argv[1])
    peer_1 = int(sys.argv[2])
    peer_2 = int(sys.argv[3])
    Store()['MSS'] = float(sys.argv[4])
    Store()['LOSS_RATE'] = float(sys.argv[5])
    # worker array 
    workers = []

    debug_print()

    
    """
    Set up the environment for each thread 
    """
    # This client need to ping these server 
    workers.append(UdpClient(peer_1))
    workers.append(UdpClient(peer_2))
    # start this server 
    workers.append(UdpServer())

    """
    Run it!
    """
    for w in workers:
        w.start()