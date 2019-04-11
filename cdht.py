#!python3

from ping import UdpClient, UdpServer




# client config 
my_id = 0


if __name__ == "__main__":
    import sys
    from store import Store

    # this client's id 
    Store()['my_id'] = int(sys.argv[1])
    peer_1 = int(sys.argv[2])
    peer_2 = int(sys.argv[3])

    # worker array 
    workers = []
    
    # This client need to ping these server 
    workers.append(UdpClient(peer_1))
    workers.append(UdpClient(peer_2))
    # start this server 
    workers.append(UdpServer())

    # start all the workers 
    for w in workers:
        w.start()