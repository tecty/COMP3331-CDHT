#!python3 
from store import Store
import time
"""
This is a helper class for logging 
"""

# Evnet type 
EVENT_SEND = 1
EVENT_RECV = 2 
EVENT_DROP = 3
EVENT_RETR = 4


class EventLog(object):
    def __init__(self, fp):
        """
        only need to pass the hanlde for log file 
        """
        self.log_fp = fp 
        self.reset_state()

    def reset_state(self):
        self.event   =0
        self.seq_val =0
        self.buf_len =0 
        self.ack = 0


    def log(self):
        log_s = ""

        """
        Log the event type 
        """
        if self.event== EVENT_SEND:
            log_s += "snd"
        elif self.event== EVENT_RECV:
            log_s += "rcv"
        elif self.event== EVENT_DROP:
            log_s += "drop"
        elif self.event== EVENT_RETR:
            log_s += "RTX"
        log_s +="\t"
        
        """
        Log time 
        """
        log_s += str(time.time() - Store()["START_TIME"]) + "\t"

        """
        Log all the numbers 
        """
        log_s += str(self.seq_num) +"\t" 
        log_s += str(self.buf_len) +"\t" 
        log_s += str(self.ack) +"\t" 
        
        """
        Log to file 
        """
        self.log_fp.write(log_s+ "\n")

        self.reset_state()

    def finish(self):
        self.log_fp.close()

if __name__ == "__main__":
    # open a log file as EventLog type
    e = EventLog(open('responding_log.txt', 'w+'))
    
    e.event = EVENT_SEND
    e.seq_num = 0
    e.buf_len = 500 
    e.ack = 0
    e.log()

    e.event = EVENT_DROP
    e.seq_num = 0
    e.buf_len = 500 
    e.ack = 0
    e.log()

    e.event = EVENT_RETR 
    e.seq_num = 0
    e.buf_len = 500 
    e.ack = 0
    e.log()

    e.event = EVENT_RECV 
    e.seq_num = 0
    e.buf_len = 500 
    e.ack = 500
    e.log()
