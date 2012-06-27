#!/usr/bin/python

# -*- coding: utf-8 -*-

import unittest
import sys
import datetime

sys.path.append('lib')

import crontimesequence


class TestScalarValue(unittest.TestCase):
	""" test ScalarValue class """
	
	def test_minute_hour_day_month(self):
		""" check if minute, hour, day and month -check of ScalarValue rule class is correct """
		
		test_values = {"minute": 16, "hour": 23, "day": 9, "month": 3}
		
		for test_key, test_val in test_values.iteritems():
			test_rule_obj = crontimesequence.ScalarValue(test_val, test_key)
			
			for minute in range(0, 60):
				for hour in range(0, 24):
					for day in range(1, 29):
						for month in range(1, 13):
							test_subj = datetime.datetime(2012, month, day, hour, minute, 39)
							
							ret = test_rule_obj.is_accept(test_subj)
							
							if ( (("minute" == test_key) and (16 == minute))
									or (("hour" == test_key) and (23 == hour))
									or (("day" == test_key) and (9 == day))
									or (("month" == test_key) and (3 == month)) ):
								self.assertTrue(ret)
							else:
								self.assertFalse(ret)
	# ### def test_minute_hour_day_month
	
	def test_weekday(self):
		""" check if weekday check of ScalarValue rule class is correct """
		
		test_rule_set = [crontimesequence.ScalarValue(wdv, "weekday") for wdv in range(0, 8)]
		
		for minute in range(0, 60):
			for hour in range(0, 24):
				for day in range(1, 30):
					for month in range(1, 13):
						test_subj = datetime.datetime(2012, month, day, hour, minute, 39)
						
						for wdv in range(0, 8):
							ret = test_rule_set[wdv].is_accept(test_subj)
							
							w = test_subj.isoweekday()
							if (w == wdv) or ( ((0 == w) or (7 == w)) and ((0 == wdv) or (7 == wdv)) ):
								self.assertTrue(ret)
							else:
								self.assertFalse(ret)
	# ### def test_weekday
# ### class TestScalarValue


if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowrap
