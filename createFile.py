#!/usr/bin/env/ python3
import sys,os,random,shutil,random,multiprocessing
from time import time

TEXT_LIST = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

TARGET_FILE = 'a'

# 随机创建文件内容
def create_file(filename):
  line_list = []
  for i in range(100):
    # 一行=1kb
    line = ''
    for i in range(1024):
      line += random.choice(TEXT_LIST)
    line_list.append(line)
  print('init success')
  with open(filename, 'a+', encoding='utf-8') as f:
    # 1024 * 1024 * 100 为100G
    f.write('\n'.join(line_list))
  f.close()
  line_list.clear()


def single_create():
  create_file(TARGET_FILE)


# 多线程并发创建文件
if __name__=='__main__':
  proces = []
  # 初始化数据
  print('初始化数据')
  start = time()
  nCpu = multiprocessing.cpu_count()
  for i in range(nCpu):
    proces.append(multiprocessing.Process(target=single_create, args=()))
  for proc in proces:
    proc.start()

  for proc in proces:
    proc.join()
  print("文件创建" + str(time() - start) + "秒")