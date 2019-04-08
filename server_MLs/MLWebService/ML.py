from numpy import *
import sklearn as sk
import pandas as pd 

class XiaoHeiLearn():
    def __init__(self,typeOfModel,DataFile):
        self.modelType = typeOfModel
        self.DataFile = DataFile

    def dealWithData(self):
        fp = open(self.DataFile)
        arrayOfLines = fp.readlines()
        features = arrayOfLines[0]
        del(arrayOfLines)
        numberOfLines = len(arrayOfLines)
        self.data = zeros(numberOfLines,)
        for line in fp.readlines():
