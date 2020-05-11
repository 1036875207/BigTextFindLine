#### 说明:
前提设定：如何找两个100G文件的相同行？

实现了三种方式

1.mapFile.py 简单遍历AB文件

2.findSameLine.py 实现了AB文件散列 -> 查询过程中删除查询过的行

3.findSameLine2.py 在findSameLine.py基础上，把删除查询过的行优化为，标记并跳过查找过的行


### 运行:

python3 findSameLine.py

python3 findSameLine2.py

python3 mapFile.py
