import sys,os,random,shutil,random,multiprocessing
from time import time

textList = ['测','测','啊','不','从','到','鹅','非','个','好','再','跑','里','前','了','开','噢','题','吃','新','写','上','走','字','空','还']

fileA = 'a'
fileB = 'b'

# 随机创建文件内容
def createFile(filename):
  tList = []
  for i in range(1024 * 10):
    # 一行=1kb
    line = ''
    for i in range(512):
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
  createFile(fileB)

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