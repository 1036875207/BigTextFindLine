import sys,os,random,shutil
from hashlib import md5
from time import time

fileA = 'm'
fileSum = 'sum2.txt'
hashPath = 'hashtable'
tempFile = 'temp'
readList = []
fileCache = {}
cacheMemery = 0
# 缓存释放大小 
cacheSize = 2*1024*1024*100

# 缓存结果
resultCache = []
resultMemery = 0
resultSize = 1000

# 读文件并创建散列
def createHash(filename):
  f = open(filename)
  index = 1
  line = f.readline()
  while line:
      # 行内容散列
      hash2File(filename, index, line)
      line = f.readline()
      index += 1
  f.close()
  # 释放
  clearFileCache()

# 散列函数
def hash(line):
  return md5(line[0:4].encode("utf-8")).hexdigest()[0:4]

# 散列内容到文件
def hash2File(lable, index, content):
  # 数据暂存
  global cacheMemery
  filename = hash(content)
  data = '%s:%s:%s'%(index, lable, content)
  if len(content.strip('\n')):
    if filename not in fileCache.keys():
      fileCache[filename] = []
    fileCache[filename].append(data)
    cacheMemery += len(content)
  # 缓存到了10M就写文件
  if cacheMemery >= cacheSize:
    clearFileCache()

# 清除文件缓存
def clearFileCache():
  global cacheMemery
  print('释放缓存')
  # print(fileCache)
  for key in fileCache.keys():
    if fileCache[key]:
      writeCache(key, fileCache[key])
  # 清空缓存
  fileCache.clear()
  cacheMemery += 0

# 随机创建文件内容
def createFile(filename):
  with open(filename, 'a+') as f:
    for i in range(10000):
      line = md5(str(int(random.random() * 10000)).encode("utf-8")).hexdigest()
      # line = int(random.random() * 100000)
      f.write('%s\n'%(line))
  f.close()

def fileSize(filePath):
  fsize = os.path.getsize(filePath)
  fsize = fsize/float(1024 * 1024)
  return round(fsize, 2)

def writeCache(filename, list):
  with open('%s/%s'%(hashPath, filename), 'a+') as f:
    for i in range(len(list)):
      f.write(list[i])
  f.close()

def writeResult(list):
  with open(fileSum, 'a+') as f:
    for i in range(len(list)):
      f.write(list[i])
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

def splitFile(filePath):
  size = fileSize(filePath)
  cache = []
  # 100M为限制
  if size >= 100:
    # 拆分的文件数量
    num = int(size/100) + 1

    # 打开文本进行拆分
    f = open(filePath)
    index = 1
    line = f.readline()
    while line:
      cache.append(line)
      line = f.readline()
      index += 1
      # 行内容重写到拆分文件中, 写1000行
      if int(index/1000)%num == 0:
        with open('%s%s'%(filePath, fileIndex), 'a+') as f:
          for i in range(len(cache)):
            f.write(cache[i])
        f.close()
        cache.clear()
    f.close()
    # 返回拆分的文件数量
    return num
  return 0

# 还原数据结构 index:lable:content
def getDataParam(str):
  index = str.find(':')
  lable = str[index + 1:].find(':')
  return str[:index], str[index + 1:][:lable], str[index + 1:][lable+ 1:]

def calcSame(filename):
  aList = []
  bList = []

  first = open(filename)
  firstIndex = 1
  while True:
    readList.append(firstIndex)
    firstIndex += 1
    firstLine = first.readline()
    if not firstLine:
      break
    # 重置
    aList.clear()
    bList.clear()
    # 当前比较的内容
    i, l, current = getDataParam(firstLine)
    if l == fileA:
      aList.append(i)
    else:
      bList.append(i)
    # 打开文件行进行比较
    second = open(filename)
    secondIndex = 0
    while True:
      secondLine = second.readline()
      secondIndex += 1
      if not secondLine:
        break
      # 当前行没有比较过
      if secondIndex not in readList:
          index, lable, secondData = getDataParam(secondLine)
          if secondData == current:
            readList.append(secondIndex)
            if lable == fileA:
              aList.append(index)
            else:
              bList.append(index)
    # 写入结果
    if len(aList) > 1 or len(bList) > 1 or (len(bList) > 0 and len(aList) > 0):
      saveResult('(%s) a:%s b:%s \n'%(current.strip('\n'), aList, bList))

  

if __name__=='__main__':

  # 初始化数据
  # print('初始化数据')
  # createFile(fileA)
  # createFile(fileB)
  # print('初始化结束')
  # 计时
  start = time()

  isExists = os.path.exists(hashPath)
  if isExists:
    # 如果不存在则创建目录
    shutil.rmtree(hashPath)
  os.makedirs(hashPath, mode=0o777)
  
  print('开始散列')
  # # 创建散列文本
  createHash(fileA)
  # createHash(fileB)
  print("散列耗时" + str(time() - start) + "秒")
  
  # 计时
  print('开始查找')
  start = time()
  # 散列文本遍历
  for i in os.listdir(hashPath):
    itemPath = hashPath + "/" + i
    if os.path.isfile(itemPath):
      # 是否需要拆分
      num = splitFile(itemPath)
      # print(itemPath, num)
      if num is 0:
        # 不需要拆分,进行文件的遍历统计
        readList.clear()
        calcSame(itemPath)
      # 打开文本
      else:
        for i in range(num):
          calcSame('%s%s'%(itemPath, i))
  print('写入剩余结果')
  writeResult(resultCache)
  resultCache.clear()
  print("查找耗时:" + str(time() - start) + "秒")