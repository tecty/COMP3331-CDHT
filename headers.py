#!python3
def int_to_bytes(i:int):
    """
    Convert number to an 8 bytes 
    """
    return i.to_bytes(8, 'big')

def bytes_to_int(b:bytes):
    """
    Convert an 8 bytes arr to int 
    """
    return int.from_bytes(b, 'big')

class Message(object):
    def __init__(self, size):
        self.msg = bytearray()
        self.seg_size = size
        
    def setHeader(self, mes_type, val):
        self.msg[0:16] = int_to_bytes(mes_type) + int_to_bytes(val)

    @property
    def header(self):
        return (bytes_to_int(self.msg[0:8]) ,bytes_to_int(self.msg[8:16])  )

    def getBodySize(self):
        """
        calculat the body size 
        """
        return len(self.msg) - 16 
    
    def getMaxBodySize(self):
        """
        Get how much payload I can load 
        """
        return self.seg_size - 16
    
    @property
    def body(self):
        return self.msg[16:]


    @body.setter
    def body(self, body:bytearray):
        self.msg[16: self.seg_size] = body


    @property
    def segment(self):
        """
        get the messgae we wrapped
        """
        return self.msg

    @segment.setter
    def segment(self, val):
        self.msg = val

  

if __name__ == "__main__":
    i = 9
    print(bytes_to_int(int_to_bytes(i)) == i )

    msg = Message(500)
    msg.setHeader(2, 7)
    msg.body = bytes('helloworld', 'utf-8')
    print(msg.header)
    print(msg.getBodySize())
    print(msg.getMaxBodySize())
    recv = Message(500)
    recv.segment = msg.segment
    print(recv.header)
    print(recv.body)