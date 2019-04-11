

class Store(dict):
    """
    Signleton dictionary 

    """
    
    # basic settings here 
    __instance = {
        'BASE_PORT' : 50000,
        'PING_SLEEP': 2    ,
        'LOSS_RATE' : 0,
        'MSS' : 500,
    }

    def __new__(cls):

        return cls.__instance