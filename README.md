#### 说明:
前提设定：大文件如何找相同行？

实现优化了五种方式

1.mapFileByAll.py 读入所有内容，遍历文件

2.mapFile.py 按行读入内容，遍历

3.findSameLine.py 实现了AB文件散列 -> 查询过程中删除查询过的行

4.findSameLine2.py 在findSameLine.py基础上，把删除查询过的行优化为，标记并跳过查找过的行

5.findSameLine3.py 在findSameLine2.py基础上，散列写入和结果写入存为缓存，每次写入多行数据

6.findSameLineByRam.py 在findSameLine3.py基础上，把散列结果放在内存中，排序并查找，多线程并发执行


### 运行:

python3 createFile.py #创建文件

python3 findSameLine.py

python3 findSameLine2.py

python3 findSameLine3.py

python3 findSameLineByRam.py 效果最好

python3 mapFile.py

python3 mapFileByAll.py 


### 运行结果：（只展示效果最好的方案六 findSameLine4.py）

单机运行 12G空余内存 6核6线程

耗时 = 文件加载 + hash + 数据存储 + 排序查找

#### 结果一

文件 10.2G 耗时69.5s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/11590551079_.pic_hd.jpg)

<!-- #### 结果二

AB文件 20.4G 耗时 560s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/WechatIMG1.png) -->

#### 结果二

文件 60G 耗时 436s

![image](https://github.com/1036875207/BigTextFindLine/blob/master/images/11590551551_.pic_hd.jpg)
