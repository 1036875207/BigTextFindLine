#!/usr/bin/env/ python3
import sys,os,random,shutil
from time import time

TARGET_FILE = 'a'
FILE_SUM = 'mapSum.txt'

def saveResult(line):
  with open(FILE_SUM, 'a+') as f:
    f.write(line)
  f.close()

def map_same(current, filename, instruct):
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
  f = open(TARGET_FILE)
  index = 1
  line = f.readline()
  while line:
      # 遍历
      result_list = map_same(line, TARGET_FILE, index)
      # 保存结果
      if len(result_list) > 0:
        result_list.append(index)
        saveResult('data(%s) a:%s\n'%(line.strip('\n'), result_list))
      line = f.readline()
      index += 1
  f.close()
  print('查找耗时' + str(time() - start) + '秒')