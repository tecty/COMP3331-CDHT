import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 50005
MESSAGE = "Hello, World!"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE,'utf-8'), (UDP_IP, UDP_PORT))