#!python3

class Peer(object):
    def __init__(self, my_id):
        # my id is wont change 
        self.my_id = my_id
        # sus is an array 
        self.successor = set()
        # pre sus is also an array too 
        self.predecessor = set()
    def add_suc(self, peer_id):
        self.successor.add(peer_id)
    def add_pre(self, peer_id):
        self.predecessor.add(peer_id)

    def get_suc(self, index):
        # constructure the correct order
        order = [t for t in self.successor ]
        order.sort() 
        order = [t for t in order if t > self.my_id] + \
        [t + 256 for t in order if t < self.my_id ]

        return order[index] % 256
        
    def get_pre(self, index):
        order = [t for t in self.predecessor ] 
        order.sort()
        order = [t - 256 for t in order if t > self.my_id] + \
        [t  for t in order if t < self.my_id ]

        return order[-index] % 256
        
    """
    leaving of the presuccsor or succssor 
    """
    def del_suc(self, peer_id):
        self.successor.remove(peer_id)

    def del_pre(self, peer_id):
        self.predecessor.remove(peer_id)

    def has_file(self, file_id):
        # who will have the file 
        peer_id = file_id % 256

        if self.get_pre(0) >  self.my_id:
            # pre > my_id 
            # if 0 <= peer_id <= myid or  pre > peer_id  
            # i have file 
            if (peer_id <= self.my_id and peer_id >= 0) or \
                peer_id > self.get_pre(0):
                return True
        else: 
            # normal case 
            if peer_id>self.get_pre(0) and peer_id <= self.my_id:
                return True
        
        # idon't have file 
        return False
        
        

if __name__ == "__main__":
    p = Peer(3)

    p.add_pre(1)
    p.add_pre(10)

    p.add_suc(5)
    p.add_suc(7)

    print(p.get_pre(2)==10)
    print(p.get_pre(1)==1)


    p = Peer(5)
    p.add_pre(3)
    p.add_pre(4)
    p.add_suc(1)
    p.add_suc(10)

    print(p.get_suc(1) == 1)
    print(p.get_suc(0) == 10)

    # identify whether the file is my responsibility
    p = Peer(5)
    p.add_pre(3)
    print(p.has_file(4)== True)
    print(p.has_file(5)== True)
    print(p.has_file(3)== False)
    print(p.has_file(6)== False)
    print(p.has_file(10)== False)
    print(p.has_file(255)== False)

    # special case 
    p = Peer(5)
    p.add_pre(253)
    print(p.has_file(4)== True)
    print(p.has_file(5)== True)
    print(p.has_file(256)== True)
    print(p.has_file(255)== True)
    print(p.has_file(254)== True)
    print(p.has_file(253)== False)

    for i in range(10):
        print(p.has_file(5+ 256*i) == True)