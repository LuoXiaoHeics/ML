# 机器学习WebService
- 网页1 : 上传数据,并设置模型种类
- 网页2 : 进行测试,显示已训练好的模型与未训练好的模型

## 使用的库 
- python框架 Django
- 机器学习库 sklearn

## 目标实现功能:
拟模型支持 : kNN, Logistic, SVM, NormalBayes, DecisionTree

1. 上传文件,并保存至服务器
 - 文件格式要求:第1行为特征名与种类名,第2-n行,前m列为特征值,最后一列为种类。数据间以 ','或 '\t' 隔开,（之后可以提供多文件类型支持）
 - 文件上传后,将相关属性存储到数据库中
 - ORM : trainingTask ( OID (训练任务序号), trainingName (训练名称, 也是模型名称), trainingDataFil (数据文件路径), typeOfModel (模型种类), onTraining (是否在训练,-1未开始训练, 0正在训练, 1已经完成训练), uploadTime (上传时间) )

2. 训练模型并进行交叉检验
- 如果线程数<n, 则新建线程用于训练模型,并修改训练任务onTraining为0；否则不新建线程
- 线程训练好一个模型后,修改onTraining为1,执行3; 之后检查数据库是否有未开始训练的任务,若有则继续进行新的训练
- （源数据文件可以删除）
- 应能自动寻找较好表现的模型参数

3. 利用python.pickle保存训练好的模型,并将相关数据保存至数据库
- ORM: trainingModels ( trainingName (模型名称,外键), modelFile  (模型路径), typeOfModel (模型种类), rate (正确率) )

