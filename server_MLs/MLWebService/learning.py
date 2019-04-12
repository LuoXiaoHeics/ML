import threading
import time
from .ML import *

class learnThread(threading.Thread):
    def __init__(self,modelName,DataFile,TypeOfModel):
        threading.Thread.__init__(self) 
        self.modelName = modelName 
        self.DataFile = DataFile 
        self.TypeOfModel = TypeOfModel

    def run(self):
        Learns = XiaoHeiLearn(self.typeOfModel,self.DataFile,self.modelName)
        Learns.dealWithData()
        model = Learns.trainModel()
        #记录文件
        print ("start...%s" %self.fileName)
        for i in range(20):
            time.sleep(1)
            print (i)
        print ("end.... %s"%self.fileName)

#set-executionpolicy remotesigned
