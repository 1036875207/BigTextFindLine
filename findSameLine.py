#!/usr/bin/env/ python3
import sys,os,random,shutil
from hashlib import md5
from time import time

TARGET_FILE = 'a'
FILE_SUM = 'sum.txt'
HASH_PATH = 'hashtable'
TEMP_FILE = 'temp'

# 读文件并创建散列
def create_hash(filename):
  f = open(filename)
  index = 1
  line = f.readline()
  while line:
      # 行内容散列
      hash2File(index, line)
      line = f.readline()
      index += 1
  f.close()


# 散列函数
def hash(line):
  return md5(line.encode("utf-8")).hexdigest()[0:2]


# 散列内容到文件
def hash2File(index, content):
  filename = hash(content)
  with open('%s/%s'%(HASH_PATH, filename), 'a+') as f:
    f.write('%s:%s'%(index, content))
  f.close()


# 删除文件夹和文件
def delFiles(path):
  for i in os.listdir(path) :
    data = path + "/" + i
    if os.path.isfile(path) == True:
      os.remove(data)
    else:
      delFiles(data)


# 临时文件，存储
def write_temp(data):
  with open(TEMP_FILE, 'a+') as f:
    f.write(data)
  f.close()


# 保存结果
def save_result(line):
  with open(FILE_SUM, 'a+') as f:
    f.write(line)
  f.close()


# 还原数据结构 index:content
def get_data_param(str):
  index = str.find(':')
  lable = str[index + 1:].find(':')
  return str[:index], str[index + 1:]


def calcSame(filename):
  # 删除临时文件
  if os.path.exists(TEMP_FILE):
    os.remove(TEMP_FILE)

  result_list = []

  # 打开读取文件内容
  f = open(filename)
  line = f.readline()
  if not line.strip('\n'):
    return
  # 当前要查找的内容
  c_index, current = get_data_param(line)
  result_list.append(c_index)

  while line:
    line = f.readline()
    if line:
      index, content = get_data_param(line)
      # 内容相同
      if content == current:
        result_list.append(index)
      # 行内容不同，写到新的文件中去，最后覆盖当前文件
      else:
        write_temp(line)

  # 写入结果
  if len(result_list) > 1:
    save_result('%s result: %s\n'%(current.strip('\n'), result_list))
  
  # 覆盖当前文件
  if os.path.exists(TEMP_FILE):
    shutil.copyfile(TEMP_FILE, filename) 
  else:
    return
  # 递归文件
  calcSame(filename)
  

if __name__=='__main__':
  # 计时
  start = time()

  isExists = os.path.exists(HASH_PATH)
  if isExists:
    # 如果不存在则创建目录
    shutil.rmtree(HASH_PATH)
  os.makedirs(HASH_PATH, mode=0o777)
  
  print('开始散列')
  # 创建散列文本
  create_hash(TARGET_FILE)
  print("散列耗时" + str(time() - start) + "秒")
  
  # 计时
  start = time()
  # 散列文本遍历
  for i in os.listdir(HASH_PATH):
    item_path = HASH_PATH + "/" + i
    if os.path.isfile(item_path):
      calcSame(item_path)

  print("查找耗时:" + str(time() - start) + "秒")

  

