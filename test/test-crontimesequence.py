#!/usr/bin/python

# -*- coding: utf-8 -*-

import unittest
import sys
import datetime

sys.path.append('lib')

import crontimesequence


class TestScalarValue(unittest.TestCase):
	""" test ScalarValue class """
	
	def test_minute_hour_day_month_2012(self):
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
	
	def test_weekday_2012(self):
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


class TestLastDayOfMonthValue(unittest.TestCase):
	""" test LastDayOfMonthValue class """
	
	def test_1999_2022_5927sec_step(self):
		""" exams every 5927sec step to check if LastDayOfMonthValue work correctly """
		
		test_rule_obj = crontimesequence.LastDayOfMonthValue()
		
		test_subj = datetime.datetime(1999, 1, 1, 0, 0, 0)
		test_boundary = datetime.datetime(2022, 1, 1, 0, 0, 0)
		delta_1_day = datetime.timedelta(days=1)
		eval_step = datetime.timedelta(seconds=5927)
		
		while test_boundary > test_subj:
			tomorrow = test_subj + delta_1_day
			ret = test_rule_obj.is_accept(test_subj)
			
			is_last_month = False
			if ((12 == test_subj.month) and (1 == tomorrow.month)) or (((1 + test_subj.month) == tomorrow.month) and (tomorrow.month <= 12)):
				is_last_month = True
			
			if is_last_month:
				self.assertTrue(ret)
			else:
				self.assertFalse(ret)
			
			test_subj = test_subj + eval_step
	# ### def test_1999_2022_30sec_step
# ### class TestLastDayOfMonthValue


class TestNearestWorkDayValue(unittest.TestCase):
	""" test NearestWorkDayValue class """
	
	def test_nearest_workday_2012_sampled(self):
		""" exam with selected 2012 dates """
		
		eval_step = datetime.timedelta(seconds=5927)
		delta_7_day = datetime.timedelta(days=7)
		
		egde_sample = [(1, 1, 2,), (5, 16, 16), (7, 15, 16,), (7, 19, 19), (7, 28, 27), (9, 1, 3,), (9, 30, 28,), (12, 1, 3,), (12, 31, 31,),]
		
		for e in egde_sample:
			month, day_subject, day_positive, = e
			rule_obj = crontimesequence.NearestWorkDayValue(day_subject)
			
			eval_subj_date = datetime.datetime(2012, month, day_subject, 1, 30, 0)
			eval_rolling = eval_subj_date - delta_7_day
			eval_end_date = eval_subj_date + delta_7_day
			
			while eval_rolling < eval_end_date:
				ret = rule_obj.is_accept(eval_rolling)
				
				msg = "%r => %r" % (e, eval_rolling,)
				if day_positive == eval_rolling.day:
					self.assertTrue(ret, msg)
				else:
					self.assertFalse(ret, msg)
				
				eval_rolling = eval_rolling + eval_step
	# ### def test_nearest_workday_2012_sampled
# ### class TestNearestWorkDayValue



if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowrap
