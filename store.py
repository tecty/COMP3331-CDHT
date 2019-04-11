

class Store(dict):
    """
    Signleton dictionary 

    """
    
    # basic settings here 
    __instance = {
        'BASE_PORT' : 50000,
        'PING_SLEEP': 2  

    }

    def __new__(cls):

        return cls.__instance