#!/usr/bin/env/ python3
mport unittest
from findSameLineByRam import *

class Main(unittest.TestCase):

  def test_hashrange(self):
    for i in range(100):
      num = hash(str(i))
      self.assertIn(num, range(65536))

  def test_struct(self):
    content, index = get_data_param('你好:1:00')
    self.assertEqual(content, '你好')
    self.assertEqual(index, '1:00')

if __name__ == '__main__':
    unittest.main()