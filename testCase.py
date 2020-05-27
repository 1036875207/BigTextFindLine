import unittest
from findSameLine import *
class TestStringMethods(unittest.TestCase):

  def test_file(self):
    size = fileSize('./mapFile.py')
    self.assertEqual(size, 100)

if __name__ == '__main__':
    unittest.main()