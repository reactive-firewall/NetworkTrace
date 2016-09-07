# -*- coding: utf-8 -*-

import unittest


class BasicTestSuite(unittest.TestCase):
	"""Basic test cases."""

	def test_absolute_truth_and_meaning(self):
		"""Insanitty Test."""
		assert True

	def test_syntax(self):
		"""Test case importing code."""
		theResult = False
		try:
			from .context import code
			from code import record_pcap
			from code import analyze_pcap
			theResult = True
		except Exception:
			theResult = False
		assert theResult

if __name__ == '__main__':
	unittest.main()