# 机器学习WebService
## 使用的库 
- python框架 Django
- 机器学习库 sklearn

## 目标实现功能:
拟支持模型 : kNN, Logistic, SVM, DecisionTree

1. 上传文件,并保存至服务器
 - 文件格式要求:第1行为特征名与种类名,第2-n行,前m列为特征值,最后一列为种类。数据间以 ' '或 '\t' 隔开,（之后可以提供多文件类型支持）
 - 文件上传后,将相关属性存储到数据库中
 - ORM : trainingTask ( OID (训练任务序号), trainingName (训练名称, 也是模型名称), trainingDataFile (数据文件路径), typeOfModel (模型种类), onTraining (是否在训练,-1未开始训练, 0正在训练, 1已经完成训练), uploadTime (上传时间) )

2. 数据处理
- 对字符串数据
- 对缺失数据
- （对数据的归一化位于下面pipeline中）

3. 训练模型保存模型文件
- Pipeline: 管道机制，过程包括归一化和PCA
- GridsearchCV: 用于寻找表现良好的参数组合，评价标准为交叉验证的正确率
- 再次访问任务页面时,检查"正在训练"任务是否在模型文件夹中存在对应的模型文件, 若存在则更新数据库，将其修改为训练完成（暂时以这种方式来处理）

4. 测试模型
- 测试主要是在页面提交数据，之后返回测试结果
- 测试结果可以下载到本地

## 页面:
- 网页1 : 上传数据, 并设置模型种类
![上传页面](https://github.com/LuoXiaoHeics/MLWebService/blob/master/server_MLs/images/upload.JPG)
- 网页2 : 任务页面, 显示未开始训练的，正在训练的，以及训练完成的模型
![任务页面](https://github.com/LuoXiaoHeics/MLWebService/blob/master/server_MLs/images/tasks.JPG)
- 网页3 : 测试页面, 用已训练好的模型进行分类
![测试页面](https://github.com/LuoXiaoHeics/MLWebService/blob/master/server_MLs/images/test.JPG)
- 网页4 ： 测试结果页面
![测试结果页面](https://github.com/LuoXiaoHeics/MLWebService/blob/master/server_MLs/images/result.JPG)
