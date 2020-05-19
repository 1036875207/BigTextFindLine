import sys,os,random,shutil
from hashlib import md5
from time import time

fileA = 'book1.txt'
fileB = 'book2.txt'
hashPath = 'hashtable'
fileCache = {}
cacheMemery = 0
# 缓存释放大小 
cacheSize = 2*1024*1024*100

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
  # 4096
  return md5(line.encode("utf-8")).hexdigest()[0:3]

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

def writeCache(filename, list):
  with open('%s/%s'%(hashPath, filename), 'a+') as f:
    for i in range(len(list)):
      f.write(list[i])
  f.close()

if __name__=='__main__':
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

  # 把文件分散
  # 每个分布式处理1000个文件
  index = 0
  filePage = 0
  for i in os.listdir(hashPath):
    itemPath = hashPath + "/" + i
    if os.path.isfile(itemPath):
      if index%1000 == 0:
        filePage += 1
        isE = os.path.exists('reducer'+ str(filePage))
        if isE:
          # 如果不存在则创建目录
          shutil.rmtree('reducer'+ str(filePage))
        os.makedirs('reducer'+ str(filePage), mode=0o777)
      index += 1
      # 移动文件
      shutil.move(itemPath, 'reducer'+ str(filePage) + '/' + i)
  


  

