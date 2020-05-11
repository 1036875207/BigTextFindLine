import sys,os,random,shutil
from time import time
filA = 'a'
filB = 'b'
fileSum = 'mapSum.txt'

def saveResult(line):
  with open(fileSum, 'a+') as f:
    f.write(line)
  f.close()

def mapSame(current, filename):
  dataList = []
  f = open(filename)
  index = 1
  line = f.readline()
  while line:
      if line == current:
        dataList.append(index)
      # 再遍历自身
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
      # 遍历文件B
      bList = mapSame(line, filB)
      # 再遍历自身
      aList = mapSame(line, filA)
      # 保存结果
      if len(aList) > 0 and len(bList) > 0:
        saveResult('data(%s) a:%s b: %s\n'%(line.strip('\n'), aList, bList))
      line = f.readline()
      index += 1
  f.close()
  print('查找耗时' + str(time() - start) + '秒')