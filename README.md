#### 说明:
前提设定：如何找两个100G文件的相同行？

实现了三种方式

1.mapFile.py 简单遍历AB文件

2.findSameLine.py 实现了AB文件散列 -> 查询过程中删除查询过的行

3.findSameLine2.py 在findSameLine.py基础上，把删除查询过的行优化为，标记并跳过查找过的行

3.findSameLine3.py 在findSameLine2.py基础上，散列写入和结果写入存为缓存，每次写入多行数据


### 运行:

python3 findSameLine.py

python3 findSameLine2.py

python3 findSameLine3.py

python3 mapFile.py


### 运行结果：

#### 结果一

AB文件 3000行

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/2020-05-17.jpg)

#### 结果二

A文件(235k 40000行) B文件(236k 40000行)数据

散列耗时0.6404030323028564秒

查找耗时:63.16252303123474秒

#### 结果三

网上下载西游记(**1.9M 3921行**) 和 红楼梦(**2.6M 6000行**)做对比

散列耗时0.402972936630249秒

查找耗时:1.9904489517211914秒

#### 结果四

网上下载小说book1.txt(**18.7M 234744行**) 网上下载小说book2.txt(**9.4M 133460行**)

散列耗时2.7268898487091064秒

~~查找耗时:过长未知~~

**重新散列为4096个文件**

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/20205.jpg)

散列耗时6.548444747924805秒

查找耗时:82.83577013015747