#!python3
from cdht import Controller 
from info import *
from store import Store

# this is only running in main mode 
# test the connection of info server and conntroller functionality

if __name__ == "__main__":
    Store()['my_id'] = 3

    InfoSer().start()
    InfoClient(3, INFO_FILE_REQ, 2012, 4).start()

