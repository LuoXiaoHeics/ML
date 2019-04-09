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

Types = ["kNN","Logistic","SVM","DTree"]

switcher = {
    0:trainkNN,
    1:trainLogistic,
    2:trainSVM,
    3:trainNB,
}

para_range = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]

class XiaoHeiLearn():
    def __init__(self,typeOfModel,DataFile):
        self.modelType = typeOfModel
        self.DataFile = DataFile

    def dealWithData(self):
        fp = open(self.DataFile)
        arrayOfLines = fp.readlines()
        fea = arrayOfLines[0]
        del(arrayOfLines)
        self.features = fea.strip().split()
        numberOfLines = len(arrayOfLines)
        numberOfFeatures = len(self.features)
        data = zeros((numberOfLines,numberOfFeatures-1))
        classLabels = []
        index = 0
        for line in arrayOfLines:
            line = line.strip().split()
            data[index,:] = line[0:numberOfFeatures-1] 
            classLabels.append(line[-1])
            index+=1
        self.data = data
        self.labels = labels
    
    def trainModel(self):
        typeId = Types.index(self.modelType)
        switcher.get(typeId)()

    def trainkNN(self):
        X_train,X_test,y_train,y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid = [
            {
                'weights':['uniform'],
                'n_neighbors':[i for i in range(1,20)]
            },
            {
                'weights':['distance'],
                'n_neighbors':[i for i in range(1,20)],
                'p':[i for i in range(1,6)]
            }
        ]
        pipe_lr = Pipeline([('sc', StandardScaler()),
                    ('pca', PCA(n_components=2)),
                    ('clf', KNeighborsClassifier(random_state=1))
                    ])
        grid_search = GridSearchCV(pipe_lr,param_grid,n_jobs=-1,verbose=2)
        grid_search.fit(X_train,y_train)
        return grid_search


    def trainLogistic(self):
        X_train,X_test,y_train,y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid = {'penalty':['l1','l2'],'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        pipe_lr = Pipeline([('sc', StandardScaler()),
                    ('pca', PCA(n_components=2)),
                    ('clf', LogisticRegression(random_state=1))
                    ])
        grid_search= GridSearchCV(pipe_lr, param_grid,cv=5, scoring='accuracy')   
        grid_search.fit(X_train,y_train)
        return grid_search


    def trainSVM(self):
        X_train,X_test,y_train,y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
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
        pipe_lr = Pipeline([('sc', StandardScaler()),
                    ('pca', PCA(n_components=2)),
                    ('clf', SVC()(random_state=1))
                    ])
        grid_search = GridSearchCV(pipe_lr,param_grid,cv=5) #实例化一个GridSearchCV类
        grid_search.fit(X_train,y_train) #训练，找到最优的参数，同时使用最优的参数实例化一个新的SVC estimator。
        return grid_search

    def trainDTree(self):
        X_train,X_test,y_train,y_test = train_test_split(self.data,self.labels,test_size=0.3,random_state=2)
        param_grid=[{'max_depth': [i for i in range(1,20)]}]
        pipe_lr = Pipeline([('sc', StandardScaler()),
                    ('pca', PCA(n_components=2)),
                    ('clf', DecisionTreeClassifier(random_state=0)
                    ])
        grid_search = GridSearchCV(pipe_lr,param_grid,scoring='accuracy',cv=2)
        grid_search.fit(X_train,y_train)
        return grid_search
        