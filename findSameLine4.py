# 方案六
import sys,os,random,shutil,random,multiprocessing
from hashlib import md5
from time import time

# 字符集

fileA = 'a'
fileB = 'b'
fileSum = 'sum4.txt'
hashPath = 'hashtable'
tempFile = 'temp'

aReadList = []
bReadList = []

readList = []

cacheRange = 800
fileCache = {}
cacheMemery = 0
# 缓存释放大小 4G
cacheSize = 1024*1024*4

# 缓存结果
resultCache = []
resultMemery = 0
resultSize = 1024*10

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
  #return int((int(md5(line.encode("utf-8")).hexdigest()[0:2], 16) + 0.5) / 5.1)
  return int(md5(line.encode("utf-8")).hexdigest()[0:3], 16)

# 散列内容到文件
def hash2File(lable, index, content, hashIndex):
  # 数据暂存
  global cacheMemery
  filename = hash(content)
  data = '%s:%s:%s'%(content, index, lable)
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
    # print(len(value))
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
  print(resultMemery)
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
  return str[:index], str[index + 1:][:lable], str[index + 1:][lable+ 1:]

def calcSame(lineList):
  aList = []
  bList = []

  fIndex = 0
  # 按首排序
  lineList.sort()
  # readList.clear()
  for firstLine in lineList:
    # clear
    aList.clear()
    bList.clear()

    # 当前比较的内容
    current, i, l = getDataParam(firstLine)

    fIndex += 1
    # readList.append(fIndex)

    if l == fileA:
      aList.append(i)
    else:
      bList.append(i)

    secondIndex = 1
    for secondLine in lineList[fIndex:]:
      # if secondIndex not in readList:
      if secondLine[0] != current[0]:
        break
      secondData, index, lable = getDataParam(secondLine)
      if secondData == current:
        # readList.append(secondIndex)
        if lable == fileA:
          aList.append(index)
        else:
          bList.append(index)
      secondIndex += 1
    # 写入结果
    if len(aList) > 1 or len(bList) > 1 or (len(bList) > 0 and len(aList) > 0):
      saveResult('%s:%s:%s \n'%(current.strip('\n'), ','.join(aList), ','.join(bList)))

def singelRun(iRange):
  print(iRange)
  createHash(fileA, iRange + cacheRange)
  createHash(fileB, iRange + cacheRange)
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
    chunk = 4097 / nCpu
    min = int(chunk * k)
    max = int(chunk * (k + 1))
    for i in range(min, max):
      if i%cacheRange == 0:
        proces.append(multiprocessing.Process(target=singelRun, args=(i,)))
   
  for proc in proces:
    proc.start()

  for proc in proces:
    proc.join()

  print("查找耗时" + str(time() - start) + "秒")
