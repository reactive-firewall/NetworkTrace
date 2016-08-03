# -*- coding: utf-8 -*-

from .context import code
from code import core
from code import helpers

import unittest


class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""

	def test_absolute_truth_and_meaning(self):
		assert True

	def test_IP_to_IPv4(self):
		"""Test IP binary string to IPv4 Dot notation"""
		self.assertEqual(helpers.IP_to_IPv4('00000000000000000000000000000000'), '0.0.0.0')

	def test_IPv4_to_IP(self):
		"""Test IPv4 Dot notation to IP binary string"""
		self.assertEqual(helpers.IPv4_to_IP('0.0.0.0'), '00000000000000000000000000000000')


if __name__ == '__main__':
	unittest.main()