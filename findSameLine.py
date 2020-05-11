import sys,os,random,shutil
from hashlib import md5
from time import time

fileA = 'a'
fileB = 'b'
fileSum = 'sum.txt'
hashPath = 'hashtable'
tempFile = 'temp'

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

# 散列函数
def hash(line):
  return md5(line.encode("utf-8")).hexdigest()[0:2]

# 散列内容到文件
def hash2File(lable, index, content):
  filename = hash(content)
  with open('%s/%s'%(hashPath, filename), 'a+') as f:
    f.write('%s:%s:%s'%(index, lable, content))
  f.close()

# 随机创建文件内容
def createFile(filename):
  with open(filename, 'a+') as f:
    for i in range(1000):
      line = md5(str(int(random.random() * 10000)).encode("utf-8")).hexdigest()
      # line = int(random.random() * 100000)
      f.write('%s\n'%(line))
  f.close()


def delFiles(path):
  for i in os.listdir(path) :
    data = path + "/" + i
    if os.path.isfile(path) == True:
      os.remove(data)
    else:
      delFiles(data)


def fileSize(filePath):
  fsize = os.path.getsize(filePath)
  fsize = fsize/float(1024 * 1024)
  return round(fsize, 2)

def write(filename, data):
  with open(filename, 'a+') as f:
    f.write(data)
  f.close()

def writeTemp(data):
  with open(tempFile, 'a+') as f:
    f.write(data)
  f.close()

def saveResult(line):
  with open(fileSum, 'a+') as f:
    f.write(line)
  f.close()
  # print('save', line)

def splitFile(filePath):
  size = fileSize(filePath)
  if size >= 1024:
    # 拆分的文件数量
    num = int(size/1024) + 1

    # 打开文本进行拆分
    f = open(filePath)
    index = 1
    line = f.readline()
    while line:
      # 行内容重写到拆分文件中
      write('%s%s'%(filePath, index%num), line)
      line = f.readline()
      index += 1
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
  # 清除temp
  if os.path.exists(tempFile):
    os.remove(tempFile)

  # 打开读取文件内容
  f = open(filename)
  line = f.readline()
  if len(line) < 3:
    return
  # 当前要查找的内容
  cIndex, cLable, current = getDataParam(line)
  if cLable == fileA:
    aList.append(cIndex)
  else:
    bList.append(cIndex)

  while line:
    line = f.readline()
    if line:
      index,lable,content = getDataParam(line)
      # 内容相同
      if content == current:
        if lable == fileA:
          aList.append(index)
        else:
          bList.append(index)
      # 行内容不同，写到新的文件中去，最后覆盖当前文件
      else:
        writeTemp(line)

  # 写入结果
  if len(aList) > 0 and len(bList) > 0:
    saveResult('a:%s b:%s %s\n'%(aList, bList, current.strip('\n')))
  
  # 覆盖当前文件
  if os.path.exists(tempFile):
    shutil.copyfile(tempFile, filename) 
  else:
    return
  # 递归文件
  calcSame(filename)
  

if __name__=='__main__':

  # 初始化数据
  print('初始化数据')
  createFile(fileA)
  createFile(fileB)

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
  createHash(fileB)
  print("散列耗时" + str(time() - start) + "秒")
  
  # 计时
  start = time()
  # 散列文本遍历
  for i in os.listdir(hashPath):
    itemPath = hashPath + "/" + i
    if os.path.isfile(itemPath):
      # 是否需要拆分
      num = splitFile(itemPath)
      print(itemPath, num)
      if num is 0:
        # 不需要拆分,进行文件的遍历统计
        calcSame(itemPath)
      # 打开文本
      else:
        for i in range(num):
          calcSame('%s%s'%(itemPath, i))
  print("查找耗时:" + str(time() - start) + "秒")

  

