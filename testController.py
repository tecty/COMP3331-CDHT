#!python3
from cdht import Controller 
from info import *
from store import Store

"""
this is only running in main mode 
test the connection of info server and conntroller functionality
"""

if __name__ == "__main__":
    Store()['my_id'] = 3
    
    """
    Start up the controller 
    """
    controller = Controller(Store()['my_id'],[
            5,
            10
        ], True
    )

    # add some pre 
    controller.add_pre(219)

    # globalise the controller
    Store()['controller'] =controller
    

    """
    File sending test 
    """
    InfoSer().start()
    InfoClient(3, INFO_FILE_REQ, 2012, 3).start()

