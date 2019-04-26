#!/usr/bin/python3
import random
import os 

peer_count = random.randint(3,15)
file_num = random.randint(0,9999)
file_location = file_num%256

peer_set = set()
while len(peer_set)  < peer_count:
    peer_set.add(random.randint(0,255))

peer_set = [t for t in peer_set]
peer_set.sort()


file_location = [t for t in peer_set if t > file_location]
if len(file_location) == 0:
    file_location = peer_set[0]
else :
    file_location = file_location[0]

print ("File prepared: " + str(file_num))
print("File location: " + str(file_location) )
print ("Peers ("+str(peer_count)+"): " + str(peer_set))

def get_round_index(index):
    return index % peer_count


cmd_list = [
    "gnome-terminal  -t \"Peer "+ str(peer_set[s]) +
    "\" -- bash -c 'python3  cdht.py "+
        str(peer_set[s])+" "+
        str(peer_set[get_round_index(s+1)])+" "+
        str(peer_set[get_round_index(s+2)])+
        " 300 0.3; exec /bin/bash -i'  "  
    for s in range(len(peer_set))
]

cmd = '&\n'.join(cmd_list)

fd = open('test_start.sh','w+')
fd.write("#!/bin/bash\n")
fd.write(cmd)
fd.close()



fd = open('clean.sh','w+')
fd.write("#!/bin/bash\n")
# simple clean script
# fd.write(cmd+"&& \n")
fd.write("rm "+str(file_num)+"*.pdf test_start.sh clean.sh\n")
fd.close()

os.system('chmod u+x  test_start.sh clean.sh')
os.system('cp send.pdf ' + str(file_num)+".pdf")
print(cmd)