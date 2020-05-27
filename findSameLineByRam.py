# -*- coding: utf-8 -*-
# 4G内存 硬盘无限
import sys,os,random,shutil,random,multiprocessing
from hashlib import md5
from time import time

# 字符集

TARGET_FILE = 'a'
FILE_SUM = 'ram_sum.txt'

cache_range = 11000
file_cache = {}
cache_memery = 0
# 缓存释放大小 4G
cacheSize = 1024*1024*1

# 缓存结果
result_cache = []
result_memery = 0
result_size = 1024*1024

# 读文件并创建散列
def createHash(filename, hashIndex):
  f = open(filename, encoding='utf-8')
  index = 1
  line = f.readline()
  while line:
    # 行内容散列
    # if (TARGET_FILE == filename and index not in aReadList) or (fileB == filename and index not in bReadList):
    hash2File(filename, index, line, hashIndex)
    line = f.readline()
    index += 1
  f.close()

# 散列函数 结果范围[0, 50]的整数
def hash(line):
  return int(md5(line[0:4].encode("utf-8")).hexdigest()[0:4], 16)

# 散列内容到文件
def hash2File(lable, index, content, hashIndex):
  # 数据暂存
  global cache_memery
  filename = hash(content)
  data = '%s:%s'%(content, index)
  if filename < hashIndex and filename >= hashIndex - cache_range:
    # if lable == TARGET_FILE:
    #   aReadList.append(index)
    # else:
    #   bReadList.append(index)
    if filename not in file_cache.keys():
      file_cache[filename] = []
    file_cache[filename].append(data)
    cache_memery += 1
  # 缓存到了4G就先比较当前文件
  if cache_memery >= cacheSize:
    clear_file_cache()

# 清除文件缓存
def clear_file_cache():
  global cache_memery
  print('释放缓存')
  for value in file_cache.values():
    #print(len(value))
    calcSame(value)
  file_cache.clear()
  cache_memery = 0
  print('成功释放')

def write_result(list):
  with open(FILE_SUM, 'a+', encoding='utf-8') as f:
    f.write('\n'.join(list))
  f.close()

def save_result(line):
  global result_memery
  result_cache.append(line)
  result_memery += 1
  # print(result_memery)
  if result_memery >= result_size:
    # 写结果
    print('写结果')
    write_result(result_cache)
    result_cache.clear()
    result_memery = 0

# 还原数据结构 index:lable:content
def get_data_param(str):
  index = str.find(':')
  lable = str[index + 1:].find(':')
  return str[:index], str[index + 1:]


def calcSame(lineList):
  fIndex = 0
  # 按首排序
  lineList.sort()
  listLength = len(lineList)
  # while fIndex < listLength:
  while fIndex < listLength:
    resultList = []
    firstLine = lineList[fIndex]

    # 当前比较的内容
    current, i = get_data_param(firstLine)

    resultList.append(i)

    fIndex += 1

    secondIndex = fIndex
    for secondLine in lineList[fIndex:]:
      # if secondIndex not in readList:
      if secondLine[0] != current[0]:
        break
      secondData, index = get_data_param(secondLine)
      if secondData == current:
        fIndex = secondIndex + 1
        # readList.append(secondIndex)
        resultList.append(index)
      secondIndex += 1

    # 写入结果
    if len(resultList) > 1:
      save_result('%s result: %s \n'%(current.strip('\n'), ','.join(resultList)))

def singelRun(iRange):
  print(iRange)
  createHash(TARGET_FILE, iRange + cache_range)
  # 释放
  clear_file_cache()

  write_result(result_cache)
  result_cache.clear()
  result_memery = 0

if __name__=='__main__':
 
  # 计时
  start = time()
  proces = []

  print('开始散列')
  # 多线程
  nCpu = multiprocessing.cpu_count()
  chunk = 65536 / nCpu
  # 计算每个线程查找的hash的范围
  cache_range = int(chunk + 5)
  for k in range(nCpu):
    min = int(chunk * k)
    max = int(chunk * (k + 1))
    for i in range(min, max):
      if i%cache_range == 0:
        proces.append(multiprocessing.Process(target=singelRun, args=(i,)))
   
  for proc in proces:
    proc.start()

  for proc in proces:
    proc.join()

  print("查找耗时" + str(time() - start) + "秒")
