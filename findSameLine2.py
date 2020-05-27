import sys,os,random,shutil
from hashlib import md5
from time import time

TARGET_FILE = 'a'
FILE_SUM = 'sum2.txt'
HASH_PATH = 'hashtable'
read_LIST = []

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


# 散列函数
def hash(line):
  return md5(line.encode("utf-8")).hexdigest()[0:2]

# 散列内容到文件
def hash2File(lable, index, content):
  filename = hash(content)
  with open('%s/%s'%(HASH_PATH, filename), 'a+') as f:
    f.write('%s:%s'%(index, content))
  f.close()

def save_result(line):
  with open(FILE_SUM, 'a+') as f:
    f.write(line)
  f.close()


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
    first_line = first.readline()

    if not first_line:
      break

    # 当前比较的内容
    fIndex, current = get_data_param(first_line)
    result_list.append(fIndex)
    read_list.append(firstIndex)

    # 打开文件行进行比较
    second = open(filename)
    second_index = 1
    while True:
      second_line = second.readline()
      if not second_line:
        break
      # 当前行没有比较过
      if second_index not in read_list:
          index, second_data = get_data_param(second_line)
          if second_data == current:
            read_list.append(index)
            result_list.append(index)
      second_index += 1
    # 写入结果
    if len(result_list) > 1:
      save_result('%s result:%s\n'%(current.strip('\n'), result_list))
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
  # 创建散列文本
  create_hash(TARGET_FILE)
  print("散列耗时" + str(time() - start) + "秒")
  
  # 计时
  start = time()
  # 散列文本遍历
  for i in os.listdir(HASH_PATH):
    item_path = HASH_PATH + "/" + i
    if os.path.isfile(item_path):
      read_list.clear()
      calc_same(item_path)
  print("查找耗时:" + str(time() - start) + "秒")

  

