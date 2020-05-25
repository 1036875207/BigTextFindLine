#### 说明:
前提设定：如何找两个100G文件的相同行？

实现了三种方式

1.createFile.py 创建文件

2.mapFile.py 简单遍历AB文件

3.findSameLine.py 实现了AB文件散列 -> 查询过程中删除查询过的行

4.findSameLine2.py 在findSameLine.py基础上，把删除查询过的行优化为，标记并跳过查找过的行

5.findSameLine3.py 在findSameLine2.py基础上，散列写入和结果写入存为缓存，每次写入多行数据

4.findSameLine3.py 在findSameLine3.py基础上，把散列结果放在内存中排序查找


### 运行:

python3 createFile.py

python3 findSameLine.py

python3 findSameLine2.py

python3 findSameLine3.py

python3 findSameLine4.py

python3 mapFile.py


### 运行结果：（只展示效果最好的方案六 findSameLine4.py）

#### 结果一

AB文件 9.39G 耗时350s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/WechatIMG2.jpeg)

#### 结果二

AB文件 20.4G 耗时 560s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/WechatIMG1.png)

#### 结果三

AB文件 39.4G 和 38.4G 耗时 1148s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/WechatIMG3.png)