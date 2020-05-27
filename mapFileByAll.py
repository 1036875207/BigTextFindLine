import sys,os,random,shutil
from time import time
TARGET_FILE = 'a'
FILE_SUM = 'mapSum.txt'

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
    line = f.readline()
    index += 1
  f.close()
  return data_list

if __name__=='__main__':
  start = time()
  read_list = []

  f = open(TARGET_FILE, mode="r", encoding="utf-8")
  # 读取所有的文本内容
  content = f.read()
  line_list = content.split('\n')
  # 遍历
  line_length = len(line_list)
  i = 0
  while i < line_length:
    if i not in read_list:
      line = line_list[i]
      same_list = []
      same_list.append(i)
      j = i
      for second_line in line_list[i + 1:]:
        if second_line == line:
          same_list.append(j)
          read_list.append(j)
        j += 1
      if len(same_list) > 1:
        save_result('data(%s) a:%s\n'%(line.strip('\n'), same_list))
    i += 1
  f.close()
  print('查找耗时' + str(time() - start) + '秒')