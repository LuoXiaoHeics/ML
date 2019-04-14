from numpy import *
import pandas as pd 
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

para_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

class XiaoHeiLearn():
    def __init__(self,typeOfModel,DataFile,modelName):
        self.modelType = typeOfModel
        self.DataFile = DataFile
        self.modelName = modelName
        self.trainFunction ={
            'kNN':self.trainkNN,
            'Logistic':self.trainLogistic,
            'SVM':self.trainSVM,
            'DTree':self.trainDTree
        }

    def dealWithData(self):
        fp = open(self.DataFile)
        arrayOfLines = fp.readlines()
        fea = arrayOfLines[0]
        del(arrayOfLines[0])
        self.features = fea.strip().split()
        numberOfLines = len(arrayOfLines)
        numberOfFeatures = len(self.features)
        data = zeros((numberOfLines,numberOfFeatures-1))
        classLabels = []
        index = 0
        for line in arrayOfLines:
            line = line.strip().split()
            data[index,:] = line[0:numberOfFeatures-1] 
            classLabels.append(str(line[-1]))
            index+=1
        self.data = data
        self.labels = classLabels
    
    def trainModel(self):
        modelResult = self.trainFunction[self.modelType]()
        #保存结果
        return modelResult
        
    def trainkNN(self):
        X_train,X_test,Y_train,Y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        knn = KNeighborsClassifier()
        k_range = list(range(1,20))
        leaf_range = list(range(1,2))
        weight_options = ['uniform','distance']
        algorithm_options = ['auto','ball_tree','kd_tree','brute']
        param_grid = dict(n_neighbors = k_range,weights = weight_options,algorithm=algorithm_options,leaf_size=leaf_range)
        gridsearch = GridSearchCV(knn,param_grid,scoring='accuracy',cv =5)
        pipe_lr = Pipeline([
            ('scale',StandardScaler()),\
            ('pca',PCA(n_components=0.9)),\
            ('clf',gridsearch)\
        ])
        pipe_lr.fit(X_train,Y_train)
        score = pipe_lr.score(X_test,Y_test)
        return pipe_lr,score


    def trainLogistic(self):
        X_train,X_test,Y_train,Y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid = [
            {'penalty':['l1'],
             'solver':['liblinear'],
             'C':para_range
            },
            {
                'penalty':['l2'],
                'solver':['liblinear','lbfgs','newton-cg','sag'],
                 'C':para_range
            }
        ]
        gridsearch = GridSearchCV(LogisticRegression(solver='liblinear'), param_grid,cv=5, scoring='accuracy')
        pipe_lr = Pipeline([('sc',StandardScaler()),\
            ('pca', PCA(n_components=0.9)),\
            ('clf', gridsearch)\
            ])
        pipe_lr.fit(X_train,Y_train)
        score = pipe_lr.score(X_test,Y_test)
        return pipe_lr,score


    def trainSVM(self):
        X_train,X_test,Y_train,Y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid = [
            {
                "kernel":['rbf'],
                "gamma":para_range,
                "C":para_range
            },
            {
                "kernel":['linear'],
                "C":para_range
            }
        ] 
        gridsearch = GridSearchCV(SVC(),param_grid,cv=5)
        pipe_lr = Pipeline([('sc', StandardScaler()),
            ('pca', PCA(n_components=0.9)),
            ('clf', gridsearch)
            ])
        pipe_lr.fit(X_train,Y_train)
        score = pipe_lr.score(X_test,Y_test)
        return pipe_lr,score

    def trainDTree(self):
        X_train,X_test,Y_train,Y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid=[{'max_depth': [i for i in range(1,20)]}]
        gridsearch = GridSearchCV(DecisionTreeClassifier(),param_grid,scoring='accuracy',cv=5)
        pipe_lr = Pipeline([
            ('sc', StandardScaler()),
            ('pca', PCA(n_components=0.9)),
            ('clf',  gridsearch)
            ])
        pipe_lr.fit(X_train,Y_train)
        score = pipe_lr.score(X_test,Y_test)
        return pipe_lr,score