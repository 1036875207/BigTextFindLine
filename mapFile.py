import sys,os,random,shutil
from time import time
filA = 'm'
fileSum = 'mapSum.txt'

def saveResult(line):
  with open(fileSum, 'a+') as f:
    f.write(line)
  f.close()

def mapSame(current, filename, instruct):
  dataList = []
  f = open(filename)
  index = 1
  line = f.readline()
  while line:
    if line == current and index > instruct:
      dataList.append(index)
    line = f.readline()
    index += 1
  f.close()
  return dataList

if __name__=='__main__':
  start = time()
  f = open(filA)
  index = 1
  line = f.readline()
  while line:
      # 再遍历自身
      aList = mapSame(line, filA, index)
      # 保存结果
      if len(aList) > 0:
        saveResult('data(%s) a:%s\n'%(line.strip('\n'), aList))
      line = f.readline()
      index += 1
  f.close()
  print('查找耗时' + str(time() - start) + '秒')