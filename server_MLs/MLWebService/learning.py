import threading
import time
from .models import *

class learnThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self) 

    def run(self):
        print ("start...%s" %self.fileName)
        for i in range(20):
            time.sleep(1)
            print (i)
        print ("end.... %s"%self.fileName)

#set-executionpolicy remotesigned
