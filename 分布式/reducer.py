import sys,os,random,shutil
from hashlib import md5
from time import time

fileA = 'book1.txt'
fileB = 'book2.txt'
fileSum = sys.argv[2]
readList = []
# 由参数获得
hashPath = sys.argv[1]

# 缓存结果
resultCache = []
resultMemery = 0
resultSize = 200

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


  

