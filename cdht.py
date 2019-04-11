#!python3

from ping import UdpClient, UdpServer




# client config 
my_id = 0


if __name__ == "__main__":
    import sys
    from store import Store


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