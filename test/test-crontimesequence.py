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
	
	def test_repr_method_work(self):
		ruleobj = crontimesequence.ScalarValue(1, "weekday")
		r = repr(ruleobj)
		self.assertEqual(r, '')
	# ### def test_repr_method_work
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

	def test_repr_method_work(self):
		ruleobj = crontimesequence.LastDayOfMonthValue()
		r = repr(ruleobj)
		self.assertEqual(r, '')
	# ### def test_repr_method_work
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

	def test_repr_method_work(self):
		ruleobj = crontimesequence.NearestWorkDayValue(3)
		r = repr(ruleobj)
		self.assertEqual(r, '')
	# ### def test_repr_method_work
# ### class TestNearestWorkDayValue


class TestLastWeekdayOfMonthValue(unittest.TestCase):
	""" test LastWeekdayOfMonthValue class """
	
	def test_last_weekday_2011_2012_2013(self):
		""" check if every weekday value can work correctly """
		
		eval_step = datetime.timedelta(seconds=5927)
		
		for expweekday in range(0, 8):
			rule_obj = crontimesequence.LastWeekdayOfMonthValue(expweekday)
			
			eval_rolling = datetime.datetime(2014, 1, 1, 1, 30, 0)
			eval_end_date = datetime.datetime(2010, 12, 31, 1, 30, 0)
			
			current_month = 1
			last_wd_date_of_current_month = datetime.date(2014, 1, 26)
			
			while eval_rolling > eval_end_date:
				
				if eval_rolling.month != current_month:
					current_month = eval_rolling.month
					last_wd_date_of_current_month = None
				
				rolling_wd = eval_rolling.isoweekday()
				rolling_date = eval_rolling.date()
				
				if (last_wd_date_of_current_month is None) and ( (expweekday == rolling_wd) or ((7 == rolling_wd) and (0 == expweekday)) ):
					last_wd_date_of_current_month = rolling_date
				
				ret = rule_obj.is_accept(eval_rolling)
				
				msg = "expweekday = %d, rolling = %r" % (expweekday, eval_rolling,)
				if rolling_date == last_wd_date_of_current_month:
					self.assertTrue(ret, msg)
				else:
					self.assertFalse(ret, msg)
				
				eval_rolling = eval_rolling - eval_step
	# ### def test_last_weekday_2011_2012_2013

	def test_repr_method_work(self):
		ruleobj = crontimesequence.LastWeekdayOfMonthValue(3)
		r = repr(ruleobj)
		self.assertEqual(r, '')
	# ### def test_repr_method_work
# ### class TestLastWeekdayOfMonthValue


class TestNthWeekdayOfMonthValue(unittest.TestCase):
	""" test NthWeekdayOfMonthValue class """
	
	def test_nth_weekday_2011_2012_2013(self):
		""" exams 1st ~ 4th every week day between 2011 ~ 2013 """
		
		eval_step = datetime.timedelta(seconds=5927)
		
		for expweekday in range(0, 8):
			for nth in range(0, 5):
				rule_obj = crontimesequence.NthWeekdayOfMonthValue(expweekday, nth)
				
				eval_rolling = datetime.datetime(2011, 1, 1, 1, 30, 0)
				eval_end_date = datetime.datetime(2014, 1, 1, 1, 30, 0)
				
				wd_matched_count = 0
				last_wd_matched_date = None
				
				while eval_rolling > eval_end_date:
					if eval_rolling.month != current_month:
						wd_matched_count = 0
						last_wd_matched_date = None
					
					rolling_wd = eval_rolling.isoweekday()
					rolling_date = eval_rolling.date()
					
					if wd_matched_count < nth:
						if (rolling_wd == expweekday) or ((7 == rolling_wd) and (0 == expweekday)):
							if last_wd_matched_date != rolling_date:
								last_wd_matched_date = rolling_date
								wd_matched_count = wd_matched_count + 1
					
					ret = rule_obj.is_accept(eval_rolling)
				
					msg = "expweekday = %d, nth = %d, rolling = %r" % (expweekday, nth, eval_rolling,)
					if rolling_date == last_wd_matched_date:
						self.assertTrue(ret, msg)
					else:
						self.assertFalse(ret, msg)
				
					eval_rolling = eval_rolling + eval_step
	# ### def test_nth_weekday_2011_2012_2013

	def test_repr_method_work(self):
		ruleobj = crontimesequence.NthWeekdayOfMonthValue(3, 2)
		r = repr(ruleobj)
		self.assertEqual(r, '')
	# ### def test_repr_method_work
# ### class TestNthWeekdayOfMonthValue



def is_rule_dateset_compatible(testcase, ruleset, dateset, expret, msg=None):
	""" check if every date in dataset can have expected acceptable test result with given rule object
	
	Argument:
		testcase - testcase
		ruleset - list of rule objects
		dateset - list of dates
		expret - expected return value (T/F) from is_accept() method of rule object
	"""
	
	
	for d in dateset:
		final_ret = False
		for rule in ruleset:
			if rule.is_accept(d):
				final_ret = True
		
		if msg is None:
			fmsg = "%r vs. %r" % (rule, d,)
		else:
			fmsg = "%r (%r vs. %r)" % (msg, rule, d,)
		testcase.assertEqual(expret, final_ret, fmsg)
# ### def is_rule_dateset_compatible


class Test_parse_cronstring_minute(unittest.TestCase):
	""" test the parse_cronstring_minute function """
	
	def test_count_simple_star(self):
		""" check if the generated rule set of "*" have correct rule items """
		
		ruleset = crontimesequence.parse_cronstring_minute("*")
		self.assertEqual(len(ruleset), 60)
		
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(0, 60)], True)
	# ### def test_count_simple_star
	
	def test_count_simple_range(self):
		""" check if the generated rule set of "X-Y" have correct rule items """
		
		ruleset = crontimesequence.parse_cronstring_minute("20-59")
		self.assertEqual(len(ruleset), 40)
		
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(20, 60)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(0, 20)], False)
	# ### def test_count_simple_range
# ### class Test_parse_cronstring_minute


if __name__ == '__main__':
	unittest.main()

# vim: ts=4 sw=4 ai nowrap
