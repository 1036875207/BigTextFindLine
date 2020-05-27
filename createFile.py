import sys,os,random,shutil,random,multiprocessing
from time import time

textList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

fileA = 'a'

# 随机创建文件内容
def createFile(filename):
  tList = []
  for i in range(1024):
    # 一行=1kb
    line = ''
    for i in range(10):
      line += random.choice(textList)
    tList.append(line)
  print('init success')
  with open(filename, 'a+', encoding='utf-8') as f:
    # 1024 * 1024 * 100 为100G
    f.write('\n'.join(tList))
  f.close()
  tList.clear()

def singleCreate():
  createFile(fileA)

if __name__=='__main__':

  proces = []
  # 初始化数据
  print('初始化数据')
  start = time()
  nCpu = multiprocessing.cpu_count()
  for i in range(nCpu):
    proces.append(multiprocessing.Process(target=singleCreate, args=()))
  for proc in proces:
    proc.start()

  for proc in proces:
    proc.join()
  print("文件创建" + str(time() - start) + "秒")