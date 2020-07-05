import unittest

class TestTest(unittest.TestCase):

	def test_test(self):
		self.assert_(True)

	def test_test2(self):
		a = 1
		b = 1
		self.assertEqual(a,b)