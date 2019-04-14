import threading
import time
from .ML import *
from sklearn.externals import joblib

class learnThread(threading.Thread):
    def __init__(self,modelName,DataFile,TypeOfModel):
        threading.Thread.__init__(self) 
        self.modelName = modelName 
        self.DataFile = DataFile 
        self.TypeOfModel = TypeOfModel

    def run(self):
        print("开始训练%s" %self.modelName)
        Learns = XiaoHeiLearn(self.TypeOfModel,self.DataFile,self.modelName)
        Learns.dealWithData()
        model,score = Learns.trainModel()
        #记录文件
        PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        modelPath = os.path.join(PROJECT_ROOT,'MLWebService\CompleteModels',self.modelName+'.model')
        joblib.dump(model,modelPath)
        print("训练完成%s"%self.modelName)

#set-executionpolicy remotesigned
