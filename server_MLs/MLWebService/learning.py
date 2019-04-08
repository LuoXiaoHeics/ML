import threading
import time
class learnThread(threading.Thread):
    def __init__(self,fileName,typeOfModel):
        threading.Thread.__init__(self) 
        self.fileName = fileName
        self.typeOfModel = typeOfModel

    def run(self):
        print ("start...%s" %self.fileName)
        for i in range(20):
            time.sleep(1)
            print (i)
        print ("end.... %s"%self.fileName)

#set-executionpolicy remotesigned
