import sys,os,random,shutil
from hashlib import md5
from time import time

TARGET_FILE = 'a'
FILE_SUM = 'sum3.txt'
HASH_PATH = 'hashtable'

read_list = []
file_cache = {}
cache_memery = 0
# 缓存释放大小 
cache_size = 2*1024*1024*100
# 缓存结果
result_cache = []
result_memery = 0
result_size = 1000

# 读文件并创建散列
def create_hash(filename):
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
  clear_file_cache()


# 散列函数
def hash(line):
  return md5(line[0:4].encode("utf-8")).hexdigest()[0:4]


# 散列内容到文件
def hash2File(lable, index, content):
  # 数据暂存
  global cache_memery
  filename = hash(content)
  data = '%s:%s'%(index, content)
  if len(content.strip('\n')):
    if filename not in file_cache.keys():
      file_cache[filename] = []
    file_cache[filename].append(data)
    cache_memery += len(content)
  # 缓存到了10M就写文件
  if cache_memery >= cache_size:
    clear_file_cache()


# 清除文件缓存
def clear_file_cache():
  global cache_memery
  print('释放缓存')
  for key in file_cache.keys():
    if file_cache[key]:
      write_cache(key, file_cache[key])
  # 清空缓存
  file_cache.clear()
  cache_memery += 0

# 写hash缓存数据
def write_cache(filename, list):
  with open('%s/%s'%(HASH_PATH, filename), 'a+') as f:
    for i in range(len(list)):
      f.write(list[i])
  f.close()

# 写结果缓存
def write_result(list):
  with open(FILE_SUM, 'a+') as f:
    for i in range(len(list)):
      f.write(list[i])
  f.close()

# 暂存结果
def save_result(line):
  global result_memery
  result_cache.append(line)
  result_memery += 1
  # print(result_memery)
  if result_memery >= result_size:
    # 写结果
    print('写结果')
    write_result(result_cache)
    result_cache.clear()
    result_memery = 0


# 还原数据结构 index:lable:content
def get_data_param(str):
  index = str.find(':')
  lable = str[index + 1:].find(':')
  return str[:index], str[index + 1:]


def calc_same(filename):
  first = open(filename)
  firstIndex = 1
  while True:
    result_list = []

    read_list.append(firstIndex)
    first_line = first.readline()
    if not first_line:
      break

    # 当前比较的内容
    i, current = get_data_param(first_line)
    result_list.append(i)

    # 打开文件行进行比较
    second = open(filename)
    second_index = 0
    while True:
      secondLine = second.readline()
      second_index += 1
      if not secondLine:
        break
      # 当前行没有比较过
      if second_index not in read_list:
          index, second_data = get_data_param(secondLine)
          if second_data == current:
            read_list.append(second_index)
            result_list.append(index)
    # 写入结果
    if len(result_list) > 1:
      save_result('%s result:%s \n'%(current.strip('\n'), result_list))
    firstIndex += 1


if __name__=='__main__':
  # 计时
  start = time()

  isExists = os.path.exists(HASH_PATH)
  if isExists:
    # 如果不存在则创建目录
    shutil.rmtree(HASH_PATH)
  os.makedirs(HASH_PATH, mode=0o777)
  
  print('开始散列')
  # # 创建散列文本
  create_hash(TARGET_FILE)
  print("散列耗时" + str(time() - start) + "秒")
  
  # 计时
  print('开始查找')
  start = time()
  # 散列文本遍历
  for i in os.listdir(HASH_PATH):
    itemPath = HASH_PATH + "/" + i
    if os.path.isfile(itemPath):
      read_list.clear()
      calc_same(itemPath)

  print('写入剩余结果')
  write_result(result_cache)
  result_cache.clear()
  print("查找耗时:" + str(time() - start) + "秒")