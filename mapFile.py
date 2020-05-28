#!/usr/bin/env/ python3
import sys,os,random,shutil
from time import time

TARGET_FILE = 'a'
FILE_SUM = 'mapSum.txt'
read_line = []

def save_result(line):
  with open(FILE_SUM, 'a+') as f:
    f.write(line)
  f.close()

def map_same(current, filename, instruct):
  data_list = []
  f = open(filename)
  index = 1
  line = f.readline()
  while line:
    if line == current and index > instruct:
      data_list.append(index)
      read_line.append(index)
    line = f.readline()
    index += 1
  f.close()
  return data_list

if __name__=='__main__':
  start = time()
  f = open(TARGET_FILE)
  index = 1
  line = f.readline()
  while line:
    if index not in read_line:
      # 遍历
      result_list = map_same(line, TARGET_FILE, index)
      # 保存结果
      if len(result_list) > 0:
        result_list.append(index)
        save_result('data(%s) a:%s\n'%(line.strip('\n'), result_list))
    line = f.readline()
    index += 1
  f.close()
  print('查找耗时' + str(time() - start) + '秒')