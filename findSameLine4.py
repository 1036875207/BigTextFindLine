# -*- coding: utf-8 -*-
# 4G内存 硬盘无限
import sys,os,random,shutil,random,multiprocessing
from hashlib import md5
from time import time

# 字符集
textList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

fileA = 'f'
fileSum = 'sum.txt'
tempFile = 'temp'

aReadList = []
bReadList = []

cacheRange = 11000
fileCache = {}
cacheMemery = 0
# 缓存释放大小 4G
cacheSize = 1024*1024*1

# 缓存结果
resultCache = []
resultMemery = 0
resultSize = 1024*1024

# 读文件并创建散列
def createHash(filename, hashIndex):
  f = open(filename, encoding='utf-8')
  index = 1
  line = f.readline()
  while line:
    # 行内容散列
    # if (fileA == filename and index not in aReadList) or (fileB == filename and index not in bReadList):
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
  global cacheMemery
  filename = hash(content)
  data = '%s:%s'%(content, index)
  if filename < hashIndex and filename >= hashIndex - cacheRange:
    # if lable == fileA:
    #   aReadList.append(index)
    # else:
    #   bReadList.append(index)
    if filename not in fileCache.keys():
      fileCache[filename] = []
    fileCache[filename].append(data)
    cacheMemery += 1
  # 缓存到了4G就先比较当前文件
  if cacheMemery >= cacheSize:
    clearFileCache()

# 清除文件缓存
def clearFileCache():
  global cacheMemery
  print('释放缓存')
  for value in fileCache.values():
    #print(len(value))
    calcSame(value)
  fileCache.clear()
  cacheMemery = 0
  print('成功释放')

def writeResult(list):
  with open(fileSum, 'a+', encoding='utf-8') as f:
    f.write('\n'.join(list))
  f.close()

def saveResult(line):
  global resultMemery
  resultCache.append(line)
  resultMemery += 1
  # print(resultMemery)
  if resultMemery >= resultSize:
    # 写结果
    print('写结果')
    writeResult(resultCache)
    resultCache.clear()
    resultMemery = 0

# 还原数据结构 index:lable:content
def getDataParam(str):
  index = str.find(':')
  lable = str[index + 1:].find(':')
  # return str[:index], str[index + 1:][:lable], str[index + 1:][lable+ 1:]
  return str[:index], str[index + 1:][:lable]

def calcSame(lineList):
  resultList = []

  fIndex = 0
  # 按首排序
  lineList.sort()
  listLength = len(lineList)
  # while fIndex < listLength:
  while fIndex < listLength:
    
    firstLine = lineList[fIndex]

    # clear
    resultList.clear()

    # 当前比较的内容
    current, i = getDataParam(firstLine)

    resultList.append(i)

    fIndex += 1

    secondIndex = fIndex
    for secondLine in lineList[fIndex:]:
      # if secondIndex not in readList:
      if secondLine[0] != current[0]:
        break
      secondData, index = getDataParam(secondLine)
      if secondData == current:
        fIndex = secondIndex + 1
        # readList.append(secondIndex)
        resultList.append(index)
      secondIndex += 1

    # 写入结果
    if len(resultList) >= 2 :
      saveResult('%s result:%s \n'%(current.strip('\n'), ','.join(resultList)))

def singelRun(iRange):
  print(iRange)
  createHash(fileA, iRange + cacheRange)
  # 释放
  clearFileCache()

  writeResult(resultCache)
  resultCache.clear()
  resultMemery = 0

if __name__=='__main__':
 
  # 计时
  start = time()
  proces = []

  print('开始散列')
  # 创建散列文本
  nCpu = multiprocessing.cpu_count()
  for k in range(nCpu):
    chunk = 65536 / nCpu
    min = int(chunk * k)
    max = int(chunk * (k + 1))
    for i in range(min, max):
      if i%cacheRange == 0:
        proces.append(multiprocessing.Process(target=singelRun, args=(i,)))
    #   break
    # break
   
  for proc in proces:
    proc.start()

  for proc in proces:
    proc.join()

  print("查找耗时" + str(time() - start) + "秒")
