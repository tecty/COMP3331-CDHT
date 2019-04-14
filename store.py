import time
class Store(dict):
    """
    Signleton dictionary 

    """
    
    # basic settings here 
    __instance = {
        'BASE_PORT' : 50000,
        'PING_SLEEP': 15,
        'LOSS_RATE' : 0,
        'MSS' : 500,
        # Programme start time stamp
        'START_TIME': time.time()
    }

    def __new__(cls):

        return cls.__instance