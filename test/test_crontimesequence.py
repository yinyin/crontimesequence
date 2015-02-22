#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import datetime
import logging

# {{{ import target module according to Python version
try:
	import crontimesequence #@UnusedImport
except:
	if sys.version_info.major > 2:
		sys.path.append('lib3')
	else:
		sys.path.append('lib2')
	import crontimesequence #@Reimport
# }}} import target module according to Python version



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
		self.assertEqual(r, 'crontimesequence.ScalarValue(1, "weekday")')
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
		self.assertEqual(r, 'crontimesequence.LastDayOfMonthValue()')
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
		self.assertEqual(r, 'crontimesequence.NearestWorkDayValue(3)')
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
		self.assertEqual(r, 'crontimesequence.LastWeekdayOfMonthValue(3)')
	# ### def test_repr_method_work
# ### class TestLastWeekdayOfMonthValue


class TestNthWeekdayOfMonthValue(unittest.TestCase):
	""" test NthWeekdayOfMonthValue class """

	def test_nth_weekday_2011_2012_2013(self):
		""" exams 1st ~ 4th every week day between 2011 ~ 2013 """

		eval_step = datetime.timedelta(seconds=5927)

		for expweekday in range(0, 8):
			for nth in range(1, 6):
				rule_obj = crontimesequence.NthWeekdayOfMonthValue(expweekday, nth)

				eval_rolling = datetime.datetime(2011, 1, 1, 1, 30, 0)
				eval_end_date = datetime.datetime(2014, 1, 1, 1, 30, 0)

				current_month = 1
				wd_matched_count = 0
				last_wd_matched_date = None

				while eval_rolling < eval_end_date:
					if eval_rolling.month != current_month:
						current_month = eval_rolling.month
						wd_matched_count = 0
						last_wd_matched_date = None

					rolling_wd = eval_rolling.isoweekday()
					rolling_date = eval_rolling.date()

					if (rolling_wd == expweekday) or ((7 == rolling_wd) and (0 == expweekday)):
						if last_wd_matched_date != rolling_date:
							last_wd_matched_date = rolling_date
							wd_matched_count = wd_matched_count + 1

					ret = rule_obj.is_accept(eval_rolling)

					msg = "expweekday = %d, nth = %d, rolling = %r" % (expweekday, nth, eval_rolling,)
					if (wd_matched_count == nth) and (rolling_date == last_wd_matched_date):
						self.assertTrue(ret, msg)
					else:
						self.assertFalse(ret, msg)

					eval_rolling = eval_rolling + eval_step
	# ### def test_nth_weekday_2011_2012_2013

	def test_repr_method_work(self):
		ruleobj = crontimesequence.NthWeekdayOfMonthValue(3, 2)
		r = repr(ruleobj)
		self.assertEqual(r, 'crontimesequence.NthWeekdayOfMonthValue(3, 2)')
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
		rulemark = None
		for rule in ruleset:
			if rule.is_accept(d):
				final_ret = True
				if False == expret:
					rulemark = rule
			else:
				if True == expret:
					rulemark = rule

		if msg is None:
			fmsg = "%r vs. %r" % (rulemark, d,)
		else:
			fmsg = "%r (%r vs. %r)" % (msg, rulemark, d,)
		testcase.assertEqual(expret, final_ret, fmsg)
# ### def is_rule_dateset_compatible


class Test_parse_cronstring_minute(unittest.TestCase):
	""" test the parse_cronstring_minute function """

	def _test_star(self, raise_error):
		""" check if the generated rule set of "*" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_minute("*", raise_error=raise_error)
		self.assertEqual(len(ruleset), 60)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(0, 60)], True)
	# --- def _test_star
	def test_star_DEx(self):
		""" check if the generated rule set of "*" have correct rule items  (Disabled Exception Raising) """
		self._test_star(False)
	def test_star_REx(self):
		""" check if the generated rule set of "*" have correct rule items  (Enabled Exception Raising) """
		self._test_star(True)
		# self.assertRaises(ValueError, self._test_star, True)
	# ### def test_star

	def _test_range_1(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_minute("20-59", raise_error=raise_error)
		self.assertEqual(len(ruleset), 40)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(20, 60)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(0, 20)], False)
	# --- def _test_range_1
	def test_range_1_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Disabled Exception Raising) """
		self._test_range_1(False)
	def test_range_1_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Enabled Exception Raising) """
		self._test_range_1(True)
		# self.assertRaises(ValueError, self._test_range_1, True)
	# ### def test_range_1

	def _test_range_2(self, raise_error):
		""" check if the generated rule set of "X-" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_minute("20-", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_2
	def test_range_2_DEx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_2(False)
	def test_range_2_REx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_2, True)
	# ### def test_range_2

	def _test_range_3(self, raise_error):
		""" check if the generated rule set of "-Y" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_minute("-50", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_3
	def test_range_3_DEx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_3(False)
	def test_range_3_REx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_3, True)
	# ### def test_range_3

	def _test_divide_1(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star """

		ruleset = crontimesequence.parse_cronstring_minute("*/17", raise_error=raise_error)
		self.assertEqual(len(ruleset), 4)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 60):
			step = i
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if 0 == (step % 17):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_1
	def test_divide_1_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Disabled Exception Raising) """
		self._test_divide_1(False)
	def test_divide_1_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Enabled Exception Raising) """
		self._test_divide_1(True)
		# self.assertRaises(ValueError, self._test_divide_1, True)
	# ### def test_divide_1

	def _test_divide_2(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range """

		ruleset = crontimesequence.parse_cronstring_minute("20-59/3", raise_error=raise_error)
		self.assertEqual(len(ruleset), 14)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(20, 60):
			step = i - 20
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if 0 == (step % 3):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_2
	def test_divide_2_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Disabled Exception Raising) """
		self._test_divide_2(False)
	def test_divide_2_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Enabled Exception Raising) """
		self._test_divide_2(True)
		# self.assertRaises(ValueError, self._test_divide_2, True)
	# ### def test_divide_2

	def _test_divide_3(self, raise_error):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_minute("1-9/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 9)
	# --- def _test_divide_3
	def test_divide_3_DEx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_3(False)
	def test_divide_3_REx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_3, True)
	# ### def test_divide_3

	def _test_divide_4(self, raise_error):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_minute("1-b/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_4
	def test_divide_4_DEx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_4(False)
	def test_divide_4_REx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_4, True)
	# ### def test_divide_4

	def _test_divide_5(self, raise_error):
		""" check if the generated rule set of "X-/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_minute("1-/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_5
	def test_divide_5_DEx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_5(False)
	def test_divide_5_REx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_5, True)
	# ### def test_divide_5

	def _test_divide_6(self, raise_error):
		""" check if the generated rule set of "/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_minute("/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_6
	def test_divide_6_DEx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_6(False)
	def test_divide_6_REx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_6, True)
	# ### def test_divide_6

	def _test_divide_7(self, raise_error):
		""" check if the generated rule set of "/" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_minute("/", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_7
	def test_divide_7_DEx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_7(False)
	def test_divide_7_REx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_7, True)
	# ### def test_divide_7

	def _test_comma_1(self, raise_error):
		""" check if the generated rule set of "Z,Y,X" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_minute("3,7,11,36,57,59", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 60):
			d = datetime.datetime(2012, 6, 30, 8, i)
			if i in (3, 7, 11, 36, 57, 59,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_1
	def test_comma_1_DEx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Disabled Exception Raising) """
		self._test_comma_1(False)
	def test_comma_1_REx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Enabled Exception Raising) """
		self._test_comma_1(True)
		# self.assertRaises(ValueError, self._test_comma_1, True)
	# ### def test_comma_1

	def _test_comma_2(self, raise_error):
		""" check if the generated rule set of "Z,Y," have correct rule items """

		ruleset = crontimesequence.parse_cronstring_minute(",3,7,11,,36,57,59,", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 60):
			d = datetime.datetime(2012, 6, 30, 8, i)
			if i in (3, 7, 11, 36, 57, 59,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_2
	def test_comma_2_DEx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Disabled Exception Raising) """
		self._test_comma_2(False)
	def test_comma_2_REx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_2, True)
	# ### def test_comma_2

	def _test_comma_3(self, raise_error):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values """

		ruleset = crontimesequence.parse_cronstring_minute( ",".join([str(v) for v in range(-3, 90)]) , raise_error=raise_error)
		self.assertEqual(len(ruleset), 60)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, 8, i) for i in range(0, 60)], True)
	# --- def _test_comma_3
	def test_comma_3_DEx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Disabled Exception Raising) """
		self._test_comma_3(False)
	def test_comma_3_REx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_3, True)
	# ### def test_comma_3

	def _test_hybrid(self, raise_error):
		""" check if the generated rule set with hybrid syntax have correct rule items """

		ruleset = crontimesequence.parse_cronstring_minute("*/10, 5-25/2, 51,52,53,54,55, 55-60/3", raise_error=raise_error)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 60):
			d = datetime.datetime(2012, 6, 30, 8, i)
			if i in (0, 5, 7, 9, 10, 11, 13, 15, 17, 19, 20, 21, 23, 25, 30, 40, 50, 51, 52, 53, 54, 55, 58,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_hybrid
	def test_hybrid_DEx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Disabled Exception Raising) """
		self._test_hybrid(False)
	def test_hybrid_REx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Enabled Exception Raising) """
		self._test_hybrid(True)
		# self.assertRaises(ValueError, self._test_hybrid, True)
	# ### def test_hybrid

	def _test_directfeed_1(self, raise_error):
		""" check if the parser can work correctly with directly feed integer """

		ruleset = crontimesequence.parse_cronstring_minute(6, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 60):
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if 6 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_1
	def test_directfeed_1_DEx(self):
		""" check if the parser can work correctly with directly feed integer  (Disabled Exception Raising) """
		self._test_directfeed_1(False)
	def test_directfeed_1_REx(self):
		""" check if the parser can work correctly with directly feed integer  (Enabled Exception Raising) """
		self._test_directfeed_1(True)
		# self.assertRaises(ValueError, self._test_directfeed_1, True)
	# ### def test_directfeed_1

	def _test_directfeed_2(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value True """

		ruleset = crontimesequence.parse_cronstring_minute(True, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 60):
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if 1 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_2
	def test_directfeed_2_DEx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Disabled Exception Raising) """
		self._test_directfeed_2(False)
	def test_directfeed_2_REx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Enabled Exception Raising) """
		self._test_directfeed_2(True)
		# self.assertRaises(ValueError, self._test_directfeed_2, True)
	# ### def test_directfeed_2

	def _test_directfeed_3(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value False """

		ruleset = crontimesequence.parse_cronstring_minute(False, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 60):
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if 0 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_3
	def test_directfeed_3_DEx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Disabled Exception Raising) """
		self._test_directfeed_3(False)
	def test_directfeed_3_REx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Enabled Exception Raising) """
		self._test_directfeed_3(True)
		# self.assertRaises(ValueError, self._test_directfeed_3, True)
	# ### def test_directfeed_3

	def _test_directfeed_4(self, raise_error):
		""" check if the parser can work correctly with directly feed negative range start """

		ruleset = crontimesequence.parse_cronstring_minute(-100, 29, raise_error=raise_error)
		self.assertEqual(len(ruleset), 30)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 60):
			candidate_val = datetime.datetime(2012, 6, 30, 8, i)
			if (0 <= i) and (29 >= i):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_4
	def test_directfeed_4_DEx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Disabled Exception Raising) """
		self._test_directfeed_4(False)
	def test_directfeed_4_REx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Enabled Exception Raising) """
		self._test_directfeed_4(True)
		# self.assertRaises(ValueError, self._test_directfeed_4, True)
	# ### def test_directfeed_4

	def _test_directfeed_5(self, raise_error):
		""" check if the parser can work correctly with directly feed alphabet as range end """

		ruleset = crontimesequence.parse_cronstring_minute(-3, 'abc', raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_directfeed_5
	def test_directfeed_5_DEx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Disabled Exception Raising) """
		self._test_directfeed_5(False)
	def test_directfeed_5_REx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_directfeed_5, True)
	# ### def test_directfeed_5
# ### class Test_parse_cronstring_minute


class Test_parse_cronstring_hour(unittest.TestCase):
	""" test the parse_cronstring_hour function """

	def _test_star(self, raise_error):
		""" check if the generated rule set of "*" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_hour("*", raise_error=raise_error)
		self.assertEqual(len(ruleset), 24)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, i, 39) for i in range(0, 24)], True)
	# --- def _test_star
	def test_star_DEx(self):
		""" check if the generated rule set of "*" have correct rule items  (Disabled Exception Raising) """
		self._test_star(False)
	def test_star_REx(self):
		""" check if the generated rule set of "*" have correct rule items  (Enabled Exception Raising) """
		self._test_star(True)
		# self.assertRaises(ValueError, self._test_star, True)
	# ### def test_star

	def _test_range_1(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_hour("6-24", raise_error=raise_error)
		self.assertEqual(len(ruleset), 18)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, i, 39) for i in range(6, 24)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, i, 39) for i in range(0, 6)], False)
	# --- def _test_range_1
	def test_range_1_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Disabled Exception Raising) """
		self._test_range_1(False)
	def test_range_1_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Enabled Exception Raising) """
		self._test_range_1(True)
		# self.assertRaises(ValueError, self._test_range_1, True)
	# ### def test_range_1

	def _test_range_2(self, raise_error):
		""" check if the generated rule set of "X-" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_hour("3-", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_2
	def test_range_2_DEx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_2(False)
	def test_range_2_REx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_2, True)
	# ### def test_range_2

	def _test_range_3(self, raise_error):
		""" check if the generated rule set of "-Y" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_hour("-20", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_3
	def test_range_3_DEx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_3(False)
	def test_range_3_REx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_3, True)
	# ### def test_range_3

	def _test_divide_1(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star """

		ruleset = crontimesequence.parse_cronstring_hour("*/5", raise_error=raise_error)
		self.assertEqual(len(ruleset), 5)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 24):
			step = i
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if 0 == (step % 5):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_1
	def test_divide_1_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Disabled Exception Raising) """
		self._test_divide_1(False)
	def test_divide_1_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Enabled Exception Raising) """
		self._test_divide_1(True)
		# self.assertRaises(ValueError, self._test_divide_1, True)
	# ### def test_divide_1

	def _test_divide_2(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range """

		ruleset = crontimesequence.parse_cronstring_hour("3-19/3", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(3, 20):
			step = i - 3
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if 0 == (step % 3):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_2
	def test_divide_2_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Disabled Exception Raising) """
		self._test_divide_2(False)
	def test_divide_2_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Enabled Exception Raising) """
		self._test_divide_2(True)
		# self.assertRaises(ValueError, self._test_divide_2, True)
	# ### def test_divide_2

	def _test_divide_3(self, raise_error):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_hour("1-9/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 9)
	# --- def _test_divide_3
	def test_divide_3_DEx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_3(False)
	def test_divide_3_REx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_3, True)
	# ### def test_divide_3

	def _test_divide_4(self, raise_error):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_hour("1-b/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_4
	def test_divide_4_DEx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_4(False)
	def test_divide_4_REx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_4, True)
	# ### def test_divide_4

	def _test_divide_5(self, raise_error):
		""" check if the generated rule set of "X-/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_hour("1-/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_5
	def test_divide_5_DEx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_5(False)
	def test_divide_5_REx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_5, True)
	# ### def test_divide_5

	def _test_divide_6(self, raise_error):
		""" check if the generated rule set of "/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_hour("/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_6
	def test_divide_6_DEx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_6(False)
	def test_divide_6_REx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_6, True)
	# ### def test_divide_6

	def _test_divide_7(self, raise_error):
		""" check if the generated rule set of "/" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_hour("/", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_7
	def test_divide_7_DEx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_7(False)
	def test_divide_7_REx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_7, True)
	# ### def test_divide_7

	def _test_comma_1(self, raise_error):
		""" check if the generated rule set of "Z,Y,X" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_hour("3,7,11,16,20,23", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 24):
			d = datetime.datetime(2012, 6, 30, i, 39)
			if i in (3, 7, 11, 16, 20, 23,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_1
	def test_comma_1_DEx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Disabled Exception Raising) """
		self._test_comma_1(False)
	def test_comma_1_REx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Enabled Exception Raising) """
		self._test_comma_1(True)
		# self.assertRaises(ValueError, self._test_comma_1, True)
	# ### def test_comma_1

	def _test_comma_2(self, raise_error):
		""" check if the generated rule set of "Z,Y," have correct rule items """

		ruleset = crontimesequence.parse_cronstring_hour(",3,7,11,,16,20,23,", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 24):
			d = datetime.datetime(2012, 6, 30, i, 39)
			if i in (3, 7, 11, 16, 20, 23,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_2
	def test_comma_2_DEx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Disabled Exception Raising) """
		self._test_comma_2(False)
	def test_comma_2_REx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_2, True)
	# ### def test_comma_2

	def _test_comma_3(self, raise_error):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values """

		ruleset = crontimesequence.parse_cronstring_hour( ",".join([str(v) for v in range(-3, 90)]) , raise_error=raise_error)
		self.assertEqual(len(ruleset), 24)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 6, 30, i, 39) for i in range(0, 24)], True)
	# --- def _test_comma_3
	def test_comma_3_DEx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Disabled Exception Raising) """
		self._test_comma_3(False)
	def test_comma_3_REx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_3, True)
	# ### def test_comma_3

	def _test_hybrid(self, raise_error):
		""" check if the generated rule set with hybrid syntax have correct rule items """

		ruleset = crontimesequence.parse_cronstring_hour("*/5, 5-15/2, 10,11,12, 17-23/3", raise_error=raise_error)

		positive_dateset = []
		negative_dateset = []
		for i in range(0, 24):
			d = datetime.datetime(2012, 6, 30, i, 39)
			if i in (0, 5, 7, 9, 10, 11, 12, 13, 15, 17, 20, 23,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_hybrid
	def test_hybrid_DEx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Disabled Exception Raising) """
		self._test_hybrid(False)
	def test_hybrid_REx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Enabled Exception Raising) """
		self._test_hybrid(True)
		# self.assertRaises(ValueError, self._test_hybrid, True)
	# ### def test_hybrid

	def _test_directfeed_1(self, raise_error):
		""" check if the parser can work correctly with directly feed integer """

		ruleset = crontimesequence.parse_cronstring_hour(6, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 24):
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if 6 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_1
	def test_directfeed_1_DEx(self):
		""" check if the parser can work correctly with directly feed integer  (Disabled Exception Raising) """
		self._test_directfeed_1(False)
	def test_directfeed_1_REx(self):
		""" check if the parser can work correctly with directly feed integer  (Enabled Exception Raising) """
		self._test_directfeed_1(True)
		# self.assertRaises(ValueError, self._test_directfeed_1, True)
	# ### def test_directfeed_1

	def _test_directfeed_2(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value True """

		ruleset = crontimesequence.parse_cronstring_hour(True, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 24):
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if 1 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_2
	def test_directfeed_2_DEx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Disabled Exception Raising) """
		self._test_directfeed_2(False)
	def test_directfeed_2_REx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Enabled Exception Raising) """
		self._test_directfeed_2(True)
		# self.assertRaises(ValueError, self._test_directfeed_2, True)
	# ### def test_directfeed_2

	def _test_directfeed_3(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value False """

		ruleset = crontimesequence.parse_cronstring_hour(False, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 24):
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if 0 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_3
	def test_directfeed_3_DEx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Disabled Exception Raising) """
		self._test_directfeed_3(False)
	def test_directfeed_3_REx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Enabled Exception Raising) """
		self._test_directfeed_3(True)
		# self.assertRaises(ValueError, self._test_directfeed_3, True)
	# ### def test_directfeed_3

	def _test_directfeed_4(self, raise_error):
		""" check if the parser can work correctly with directly feed negative range start """

		ruleset = crontimesequence.parse_cronstring_hour(-3, 10, raise_error=raise_error)
		self.assertEqual(len(ruleset), 11)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(0, 24):
			candidate_val = datetime.datetime(2012, 6, 30, i, 39)
			if (0 <= i) and (10 >= i):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_4
	def test_directfeed_4_DEx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Disabled Exception Raising) """
		self._test_directfeed_4(False)
	def test_directfeed_4_REx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Enabled Exception Raising) """
		self._test_directfeed_4(True)
		# self.assertRaises(ValueError, self._test_directfeed_4, True)
	# ### def test_directfeed_4

	def _test_directfeed_5(self, raise_error):
		""" check if the parser can work correctly with directly feed alphabet as range end """

		ruleset = crontimesequence.parse_cronstring_hour(-3, 'abc', raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_directfeed_5
	def test_directfeed_5_DEx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Disabled Exception Raising) """
		self._test_directfeed_5(False)
	def test_directfeed_5_REx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_directfeed_5, True)
	# ### def test_directfeed_5
# ### class Test_parse_cronstring_hour


class Test_parse_cronstring_day(unittest.TestCase):
	""" test the parse_cronstring_day function """

	def _test_star(self, raise_error):
		""" check if the generated rule set of "*" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day("*", raise_error=raise_error)
		self.assertEqual(len(ruleset), 31)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 32)], True)
	# --- def _test_star
	def test_star_DEx(self):
		""" check if the generated rule set of "*" have correct rule items  (Disabled Exception Raising) """
		self._test_star(False)
	def test_star_REx(self):
		""" check if the generated rule set of "*" have correct rule items  (Enabled Exception Raising) """
		self._test_star(True)
		# self.assertRaises(ValueError, self._test_star, True)
	# ### def test_star

	def _test_range_1(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day("6-31", raise_error=raise_error)
		self.assertEqual(len(ruleset), 26)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(6, 32)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 6)], False)
	# --- def _test_range_1
	def test_range_1_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Disabled Exception Raising) """
		self._test_range_1(False)
	def test_range_1_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Enabled Exception Raising) """
		self._test_range_1(True)
		# self.assertRaises(ValueError, self._test_range_1, True)
	# ### def test_range_1

	def _test_range_2(self, raise_error):
		""" check if the generated rule set of "X-" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_day("3-", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_2
	def test_range_2_DEx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_2(False)
	def test_range_2_REx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_2, True)
	# ### def test_range_2

	def _test_range_3(self, raise_error):
		""" check if the generated rule set of "-Y" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_day("-20", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_3
	def test_range_3_DEx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_3(False)
	def test_range_3_REx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_3, True)
	# ### def test_range_3

	def _test_range_4(self, raise_error):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day("0-10", raise_error=raise_error)
		self.assertEqual(len(ruleset), 10)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 11)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(11, 32)], False)
	# --- def _test_range_4
	def test_range_4_DEx(self):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items  (Disabled Exception Raising) """
		self._test_range_4(False)
	def test_range_4_REx(self):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items  (Enabled Exception Raising) """
		self._test_range_4(True)
		# self.assertRaises(ValueError, self._test_range_4, True)
	# ### def test_range_4

	def _test_divide_1(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star """

		ruleset = crontimesequence.parse_cronstring_day("*/5", raise_error=raise_error)
		self.assertEqual(len(ruleset), 7)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			step = i
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			if 0 == ((step-1) % 5):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_1
	def test_divide_1_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Disabled Exception Raising) """
		self._test_divide_1(False)
	def test_divide_1_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Enabled Exception Raising) """
		self._test_divide_1(True)
		# self.assertRaises(ValueError, self._test_divide_1, True)
	# ### def test_divide_1

	def _test_divide_2(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range """

		ruleset = crontimesequence.parse_cronstring_day("3-19/3", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(3, 20):
			step = i - 3
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			if 0 == (step % 3):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_2
	def test_divide_2_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Disabled Exception Raising) """
		self._test_divide_2(False)
	def test_divide_2_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Enabled Exception Raising) """
		self._test_divide_2(True)
		# self.assertRaises(ValueError, self._test_divide_2, True)
	# ### def test_divide_2

	def _test_divide_3(self, raise_error):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_day("1-9/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 9)
	# --- def _test_divide_3
	def test_divide_3_DEx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_3(False)
	def test_divide_3_REx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_3, True)
	# ### def test_divide_3

	def _test_divide_4(self, raise_error):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_day("1-b/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_4
	def test_divide_4_DEx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_4(False)
	def test_divide_4_REx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_4, True)
	# ### def test_divide_4

	def _test_divide_5(self, raise_error):
		""" check if the generated rule set of "X-/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_day("1-/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_5
	def test_divide_5_DEx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_5(False)
	def test_divide_5_REx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_5, True)
	# ### def test_divide_5

	def _test_divide_6(self, raise_error):
		""" check if the generated rule set of "/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_day("/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_6
	def test_divide_6_DEx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_6(False)
	def test_divide_6_REx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_6, True)
	# ### def test_divide_6

	def _test_divide_7(self, raise_error):
		""" check if the generated rule set of "/" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_day("/", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_7
	def test_divide_7_DEx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_7(False)
	def test_divide_7_REx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_7, True)
	# ### def test_divide_7

	def _test_comma_1(self, raise_error):
		""" check if the generated rule set of "Z,Y,X" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day("3,7,11,16,20,23,31", raise_error=raise_error)
		self.assertEqual(len(ruleset), 7)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 32):
			d = datetime.datetime(2012, 7, i, 9, 39)
			if i in (3, 7, 11, 16, 20, 23, 31,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_1
	def test_comma_1_DEx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Disabled Exception Raising) """
		self._test_comma_1(False)
	def test_comma_1_REx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Enabled Exception Raising) """
		self._test_comma_1(True)
		# self.assertRaises(ValueError, self._test_comma_1, True)
	# ### def test_comma_1

	def _test_comma_2(self, raise_error):
		""" check if the generated rule set of "Z,Y," have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day(",3,7,11,,16,20,23, 31,", raise_error=raise_error)
		self.assertEqual(len(ruleset), 7)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 32):
			d = datetime.datetime(2012, 7, i, 9, 39)
			if i in (3, 7, 11, 16, 20, 23, 31,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_2
	def test_comma_2_DEx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Disabled Exception Raising) """
		self._test_comma_2(False)
	def test_comma_2_REx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_2, True)
	# ### def test_comma_2

	def _test_comma_3(self, raise_error):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values """

		ruleset = crontimesequence.parse_cronstring_day( ",".join([str(v) for v in range(-3, 90)]) , raise_error=raise_error)
		self.assertEqual(len(ruleset), 31)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 32)], True)
	# --- def _test_comma_3
	def test_comma_3_DEx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Disabled Exception Raising) """
		self._test_comma_3(False)
	def test_comma_3_REx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_3, True)
	# ### def test_comma_3

	def _test_last_day_of_month(self, raise_error):
		""" check if the last day of month rule can work correctly """

		ruleset = crontimesequence.parse_cronstring_day("L", raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		delta_1_day = datetime.timedelta(days=1)

		for y in range(1990, 2039):
			month_day_count_map = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31,]
			if (0 == (y % 400)) or ( (0 != (y % 100)) and (0 == (y % 4)) ):
				month_day_count_map[2] = 29

			for m in range(1, 13):
				candidate_val = datetime.datetime(y, m, 1, 9, 39)
				month_day_count = month_day_count_map[m]

				while m == candidate_val.month:
					if month_day_count == candidate_val.day:
						is_rule_dateset_compatible(self, ruleset, (candidate_val,), True)
					else:
						is_rule_dateset_compatible(self, ruleset, (candidate_val,), False)

					candidate_val = candidate_val + delta_1_day
	# --- def _test_last_day_of_month
	def test_last_day_of_month_DEx(self):
		""" check if the last day of month rule can work correctly  (Disabled Exception Raising) """
		self._test_last_day_of_month(False)
	def test_last_day_of_month_REx(self):
		""" check if the last day of month rule can work correctly  (Enabled Exception Raising) """
		self._test_last_day_of_month(True)
		# self.assertRaises(ValueError, self._test_last_day_of_month, True)
	# ### def test_last_day_of_month

	def _test_nearest_workday_1(self, raise_error):
		""" check if "xW" syntax can work correctly """

		ruleset = crontimesequence.parse_cronstring_day("1W", raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 31):
			d = datetime.datetime(2012, 9, i, 9, 39)
			if 3 == i:
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_nearest_workday_1
	def test_nearest_workday_1_DEx(self):
		""" check if "xW" syntax can work correctly  (Disabled Exception Raising) """
		self._test_nearest_workday_1(False)
	def test_nearest_workday_1_REx(self):
		""" check if "xW" syntax can work correctly  (Enabled Exception Raising) """
		self._test_nearest_workday_1(True)
		# self.assertRaises(ValueError, self._test_nearest_workday_1, True)
	# ### def test_nearest_workday_1

	def _test_nearest_workday_2(self, raise_error):
		""" check if "xW,yW,zW" syntax can work correctly """

		ruleset = crontimesequence.parse_cronstring_day("1W,22W,18W", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 32):
			d = datetime.datetime(2012, 7, i, 9, 39)
			if i in (2, 18, 23,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_nearest_workday_2
	def test_nearest_workday_2_DEx(self):
		""" check if "xW,yW,zW" syntax can work correctly  (Disabled Exception Raising) """
		self._test_nearest_workday_2(False)
	def test_nearest_workday_2_REx(self):
		""" check if "xW,yW,zW" syntax can work correctly  (Enabled Exception Raising) """
		self._test_nearest_workday_2(True)
		# self.assertRaises(ValueError, self._test_nearest_workday_2, True)
	# ### def test_nearest_workday_2

	def _test_nearest_workday_3(self, raise_error):
		""" check if "errW" syntax can handled correctly with unparsable err value """

		ruleset = crontimesequence.parse_cronstring_day("abcW", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nearest_workday_3
	def test_nearest_workday_3_DEx(self):
		""" check if "errW" syntax can handled correctly with unparsable err value  (Disabled Exception Raising) """
		self._test_nearest_workday_3(False)
	def test_nearest_workday_3_REx(self):
		""" check if "errW" syntax can handled correctly with unparsable err value  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_nearest_workday_3, True)
	# ### def test_nearest_workday_3

	def _test_nearest_workday_4(self, raise_error):
		""" check if "errW" syntax can handled correctly with err out of range (< 1) """

		ruleset = crontimesequence.parse_cronstring_day("0W", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nearest_workday_4
	def test_nearest_workday_4_DEx(self):
		""" check if "errW" syntax can handled correctly with err out of range (< 1)  (Disabled Exception Raising) """
		self._test_nearest_workday_4(False)
	def test_nearest_workday_4_REx(self):
		""" check if "errW" syntax can handled correctly with err out of range (< 1)  (Enabled Exception Raising) """
		self._test_nearest_workday_4(True)
		# self.assertRaises(ValueError, self._test_nearest_workday_4, True)
	# ### def test_nearest_workday_4

	def _test_nearest_workday_5(self, raise_error):
		""" check if "errW" syntax can handled correctly with err out of range (> 31) """

		ruleset = crontimesequence.parse_cronstring_day("99W", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nearest_workday_5
	def test_nearest_workday_5_DEx(self):
		""" check if "errW" syntax can handled correctly with err out of range (> 31)  (Disabled Exception Raising) """
		self._test_nearest_workday_5(False)
	def test_nearest_workday_5_REx(self):
		""" check if "errW" syntax can handled correctly with err out of range (> 31)  (Enabled Exception Raising) """
		self._test_nearest_workday_5(True)
		# self.assertRaises(ValueError, self._test_nearest_workday_5, True)
	# ### def test_nearest_workday_5

	def _test_hybrid(self, raise_error):
		""" check if the generated rule set with hybrid syntax have correct rule items """

		ruleset = crontimesequence.parse_cronstring_day("*/9, 5-15/2, 10,11,12, 17-23/3, 28-32,", raise_error=raise_error)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 32):
			d = datetime.datetime(2012, 7, i, 9, 39)
			if i in (1, 5, 7, 9, 10, 11, 12, 13, 15, 17, 19, 20, 23, 28, 29, 30, 31,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_hybrid
	def test_hybrid_DEx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Disabled Exception Raising) """
		self._test_hybrid(False)
	def test_hybrid_REx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_hybrid, True)
	# ### def test_hybrid

	def _test_directfeed_1(self, raise_error):
		""" check if the parser can work correctly with directly feed integer """

		ruleset = crontimesequence.parse_cronstring_day(6, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			if 6 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_1
	def test_directfeed_1_DEx(self):
		""" check if the parser can work correctly with directly feed integer  (Disabled Exception Raising) """
		self._test_directfeed_1(False)
	def test_directfeed_1_REx(self):
		""" check if the parser can work correctly with directly feed integer  (Enabled Exception Raising) """
		self._test_directfeed_1(True)
		# self.assertRaises(ValueError, self._test_directfeed_1, True)
	# ### def test_directfeed_1

	def _test_directfeed_2(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value True """

		ruleset = crontimesequence.parse_cronstring_day(True, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			if 1 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_2
	def test_directfeed_2_DEx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Disabled Exception Raising) """
		self._test_directfeed_2(False)
	def test_directfeed_2_REx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Enabled Exception Raising) """
		self._test_directfeed_2(True)
		# self.assertRaises(ValueError, self._test_directfeed_2, True)
	# ### def test_directfeed_2

	def _test_directfeed_3(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value False """

		ruleset = crontimesequence.parse_cronstring_day(False, raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			if 0 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_3
	def test_directfeed_3_DEx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Disabled Exception Raising) """
		self._test_directfeed_3(False)
	def test_directfeed_3_REx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Enabled Exception Raising) """
		self._test_directfeed_3(True)
		# self.assertRaises(ValueError, self._test_directfeed_3, True)
	# ### def test_directfeed_3
# ### class Test_parse_cronstring_day


class Test_parse_cronstring_month(unittest.TestCase):
	""" test the parse_cronstring_month function """

	def _test_star(self, raise_error):
		""" check if the generated rule set of "*" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month("*", raise_error=raise_error)
		self.assertEqual(len(ruleset), 12)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(1, 13)], True)
	# --- def _test_star
	def test_star_DEx(self):
		""" check if the generated rule set of "*" have correct rule items  (Disabled Exception Raising) """
		self._test_star(False)
	def test_star_REx(self):
		""" check if the generated rule set of "*" have correct rule items  (Enabled Exception Raising) """
		self._test_star(True)
		# self.assertRaises(ValueError, self._test_star, True)
	# ### def test_star

	def _test_range_1(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month("6-12", raise_error=raise_error)
		self.assertEqual(len(ruleset), 7)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(6, 13)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(1, 6)], False)
	# --- def _test_range_1
	def test_range_1_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Disabled Exception Raising) """
		self._test_range_1(False)
	def test_range_1_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Enabled Exception Raising) """
		self._test_range_1(True)
		# self.assertRaises(ValueError, self._test_range_1, True)
	# ### def test_range_1

	def _test_range_2(self, raise_error):
		""" check if the generated rule set of "X-" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_month("3-", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_2
	def test_range_2_DEx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_2(False)
	def test_range_2_REx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_2, True)
	# ### def test_range_2

	def _test_range_3(self, raise_error):
		""" check if the generated rule set of "-Y" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_month("-12", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_3
	def test_range_3_DEx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_3(False)
	def test_range_3_REx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_3, True)
	# ### def test_range_3

	def _test_range_4(self, raise_error):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month("0-10", raise_error=raise_error)
		self.assertEqual(len(ruleset), 10)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(1, 11)], True)
		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(11, 13)], False)
	# --- def _test_range_4
	def test_range_4_DEx(self):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items  (Disabled Exception Raising) """
		self._test_range_4(False)
	def test_range_4_REx(self):
		""" check if the generated rule set of "X-Y" with negative X have correct rule items  (Enabled Exception Raising) """
		self._test_range_4(True)
		# self.assertRaises(ValueError, self._test_range_4, True)
	# ### def test_range_4

	def _test_divide_1(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star """

		ruleset = crontimesequence.parse_cronstring_month("*/5", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 13):
			step = i
			candidate_val = datetime.datetime(2012, i, 3, 9, 39)
			if 0 == ((step-1) % 5):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_1
	def test_divide_1_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Disabled Exception Raising) """
		self._test_divide_1(False)
	def test_divide_1_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Enabled Exception Raising) """
		self._test_divide_1(True)
		# self.assertRaises(ValueError, self._test_divide_1, True)
	# ### def test_divide_1

	def _test_divide_2(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range """

		ruleset = crontimesequence.parse_cronstring_month("3-10/3", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(3, 11):
			step = i - 3
			candidate_val = datetime.datetime(2012, i, 3, 9, 39)
			if 0 == (step % 3):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_2
	def test_divide_2_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Disabled Exception Raising) """
		self._test_divide_2(False)
	def test_divide_2_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Enabled Exception Raising) """
		self._test_divide_2(True)
		# self.assertRaises(ValueError, self._test_divide_2, True)
	# ### def test_divide_2

	def _test_divide_3(self, raise_error):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_month("1-9/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 9)
	# --- def _test_divide_3
	def test_divide_3_DEx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_3(False)
	def test_divide_3_REx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_3, True)
	# ### def test_divide_3

	def _test_divide_4(self, raise_error):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_month("1-b/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_4
	def test_divide_4_DEx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_4(False)
	def test_divide_4_REx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_4, True)
	# ### def test_divide_4

	def _test_divide_5(self, raise_error):
		""" check if the generated rule set of "X-/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_month("1-/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_5
	def test_divide_5_DEx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_5(False)
	def test_divide_5_REx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_5, True)
	# ### def test_divide_5

	def _test_divide_6(self, raise_error):
		""" check if the generated rule set of "/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_month("/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_6
	def test_divide_6_DEx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_6(False)
	def test_divide_6_REx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_6, True)
	# ### def test_divide_6

	def _test_divide_7(self, raise_error):
		""" check if the generated rule set of "/" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_month("/", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_7
	def test_divide_7_DEx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_7(False)
	def test_divide_7_REx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_7, True)
	# ### def test_divide_7

	def _test_comma_1(self, raise_error):
		""" check if the generated rule set of "Z,Y,X" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month("3,7,11", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 13):
			d = datetime.datetime(2012, i, 3, 9, 39)
			if i in (3, 7, 11,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_1
	def test_comma_1_DEx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Disabled Exception Raising) """
		self._test_comma_1(False)
	def test_comma_1_REx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Enabled Exception Raising) """
		self._test_comma_1(True)
		# self.assertRaises(ValueError, self._test_comma_1, True)
	# ### def test_comma_1

	def _test_comma_2(self, raise_error):
		""" check if the generated rule set of "Z,Y," have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month(",3 ,7,11,, ,", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 13):
			d = datetime.datetime(2012, i, 3, 9, 39)
			if i in (3, 7, 11,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_comma_2
	def test_comma_2_DEx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Disabled Exception Raising) """
		self._test_comma_2(False)
	def test_comma_2_REx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_2, True)
	# ### def test_comma_2

	def _test_comma_3(self, raise_error):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values """

		ruleset = crontimesequence.parse_cronstring_month( ",".join([str(v) for v in range(-3, 90)]) , raise_error=raise_error)
		self.assertEqual(len(ruleset), 12)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, i, 3, 9, 39) for i in range(1, 13)], True)
	# --- def _test_comma_3
	def test_comma_3_DEx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Disabled Exception Raising) """
		self._test_comma_3(False)
	def test_comma_3_REx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_3, True)
	# ### def test_comma_3

	def _test_hybrid(self, raise_error):
		""" check if the generated rule set with hybrid syntax have correct rule items """

		ruleset = crontimesequence.parse_cronstring_month("*/9, 5-15/2, 10,11,12, 17-23/3, 28-32,", raise_error=raise_error)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 13):
			d = datetime.datetime(2012, i, 3, 9, 39)
			if i in (1, 5, 7, 9, 10, 11, 12,):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)

		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_hybrid
	def test_hybrid_DEx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Disabled Exception Raising) """
		self._test_hybrid(False)
	def test_hybrid_REx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_hybrid, True)
	# ### def test_hybrid

	def _test_directfeed_1(self, raise_error):
		""" check if the parser can work correctly with directly feed integer """

		ruleset = crontimesequence.parse_cronstring_month(6, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 13):
			candidate_val = datetime.datetime(2012, i, 3, 9, 39)
			if 6 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_1
	def test_directfeed_1_DEx(self):
		""" check if the parser can work correctly with directly feed integer  (Disabled Exception Raising) """
		self._test_directfeed_1(False)
	def test_directfeed_1_REx(self):
		""" check if the parser can work correctly with directly feed integer  (Enabled Exception Raising) """
		self._test_directfeed_1(True)
		# self.assertRaises(ValueError, self._test_directfeed_1, True)
	# ### def test_directfeed_1

	def _test_directfeed_2(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value True """

		ruleset = crontimesequence.parse_cronstring_month(True, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 13):
			candidate_val = datetime.datetime(2012, i, 3, 9, 39)
			if 1 == i:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_2
	def test_directfeed_2_DEx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Disabled Exception Raising) """
		self._test_directfeed_2(False)
	def test_directfeed_2_REx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Enabled Exception Raising) """
		self._test_directfeed_2(True)
		# self.assertRaises(ValueError, self._test_directfeed_2, True)
	# ### def test_directfeed_2

	def _test_directfeed_3(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value False """

		ruleset = crontimesequence.parse_cronstring_month(False, raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 13):
			candidate_val = datetime.datetime(2012, i, 3, 9, 39)
			test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_3
	def test_directfeed_3_DEx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Disabled Exception Raising) """
		self._test_directfeed_3(False)
	def test_directfeed_3_REx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Enabled Exception Raising) """
		self._test_directfeed_3(True)
		# self.assertRaises(ValueError, self._test_directfeed_3, True)
	# ### def test_directfeed_3
# ### class Test_parse_cronstring_month


class Test_parse_cronstring_weekday(unittest.TestCase):
	""" test the parse_cronstring_weekday function """

	def _test_star(self, raise_error):
		""" check if the generated rule set of "*" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("*", raise_error=raise_error)
		self.assertEqual(len(ruleset), 7)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 32)], True)
	# --- def _test_star
	def test_star_DEx(self):
		""" check if the generated rule set of "*" have correct rule items  (Disabled Exception Raising) """
		self._test_star(False)
	def test_star_REx(self):
		""" check if the generated rule set of "*" have correct rule items  (Enabled Exception Raising) """
		self._test_star(True)
		# self.assertRaises(ValueError, self._test_star, True)
	# ### def test_star

	def _test_range_1(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("3-5", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if (3 <= tweekday) and (5 >= tweekday):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_range_1
	def test_range_1_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Disabled Exception Raising) """
		self._test_range_1(False)
	def test_range_1_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items  (Enabled Exception Raising) """
		self._test_range_1(True)
		# self.assertRaises(ValueError, self._test_range_1, True)
	# ### def test_range_1

	def _test_range_2(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as start """

		ruleset = crontimesequence.parse_cronstring_weekday("0-2", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (1, 2, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_range_2
	def test_range_2_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as start  (Disabled Exception Raising) """
		self._test_range_2(False)
	def test_range_2_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as start  (Enabled Exception Raising) """
		self._test_range_2(True)
		# self.assertRaises(ValueError, self._test_range_2, True)
	# ### def test_range_2

	def _test_range_3(self, raise_error):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as end """

		ruleset = crontimesequence.parse_cronstring_weekday("5-7", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (5, 6, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_range_3
	def test_range_3_DEx(self):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as end  (Disabled Exception Raising) """
		self._test_range_3(False)
	def test_range_3_REx(self):
		""" check if the generated rule set of "X-Y" have correct rule items with Sunday as end  (Enabled Exception Raising) """
		self._test_range_3(True)
		# self.assertRaises(ValueError, self._test_range_3, True)
	# ### def test_range_3

	def _test_range_4(self, raise_error):
		""" check if the generated rule set of "X-" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("3-", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_4
	def test_range_4_DEx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_4(False)
	def test_range_4_REx(self):
		""" check if the generated rule set of "X-" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_4, True)
	# ### def test_range_4

	def _test_range_5(self, raise_error):
		""" check if the generated rule set of "-Y" is ignored correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("-7", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_range_5
	def test_range_5_DEx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Disabled Exception Raising) """
		self._test_range_5(False)
	def test_range_5_REx(self):
		""" check if the generated rule set of "-Y" is ignored correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_range_5, True)
	# ### def test_range_5

	def _test_divide_1(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star """

		ruleset = crontimesequence.parse_cronstring_weekday("*/2", raise_error=raise_error)
		self.assertEqual(len(ruleset), 4)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (1, 3, 5, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_1
	def test_divide_1_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Disabled Exception Raising) """
		self._test_divide_1(False)
	def test_divide_1_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with star  (Enabled Exception Raising) """
		self._test_divide_1(True)
		# self.assertRaises(ValueError, self._test_divide_1, True)
	# ### def test_divide_1

	def _test_divide_2(self, raise_error):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range """

		ruleset = crontimesequence.parse_cronstring_weekday("0-7/3", raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (3, 6, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_divide_2
	def test_divide_2_DEx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Disabled Exception Raising) """
		self._test_divide_2(False)
	def test_divide_2_REx(self):
		""" check if the generated rule set of "X-Y/Z" have correct rule items with range  (Enabled Exception Raising) """
		self._test_divide_2(True)
		# self.assertRaises(ValueError, self._test_divide_2, True)
	# ### def test_divide_2

	def _test_divide_3(self, raise_error):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("1-6/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 6)
	# --- def _test_divide_3
	def test_divide_3_DEx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_3(False)
	def test_divide_3_REx(self):
		""" check if the generated rule set of "X-Y/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_3, True)
	# ### def test_divide_3

	def _test_divide_4(self, raise_error):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("1-b/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_4
	def test_divide_4_DEx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_4(False)
	def test_divide_4_REx(self):
		""" check if the generated rule set of "X-ERR/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_4, True)
	# ### def test_divide_4

	def _test_divide_5(self, raise_error):
		""" check if the generated rule set of "X-/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("1-/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_5
	def test_divide_5_DEx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_5(False)
	def test_divide_5_REx(self):
		""" check if the generated rule set of "X-/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_5, True)
	# ### def test_divide_5

	def _test_divide_6(self, raise_error):
		""" check if the generated rule set of "/ERR" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("/a", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_6
	def test_divide_6_DEx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_6(False)
	def test_divide_6_REx(self):
		""" check if the generated rule set of "/ERR" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_6, True)
	# ### def test_divide_6

	def _test_divide_7(self, raise_error):
		""" check if the generated rule set of "/" can be handled correctly """

		ruleset = crontimesequence.parse_cronstring_weekday("/", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_divide_7
	def test_divide_7_DEx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Disabled Exception Raising) """
		self._test_divide_7(False)
	def test_divide_7_REx(self):
		""" check if the generated rule set of "/" can be handled correctly  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_divide_7, True)
	# ### def test_divide_7

	def _test_comma_1(self, raise_error):
		""" check if the generated rule set of "Z,Y,X" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("3,7,11", raise_error=raise_error)
		self.assertEqual(len(ruleset), 2)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (3, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_comma_1
	def test_comma_1_DEx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Disabled Exception Raising) """
		self._test_comma_1(False)
	def test_comma_1_REx(self):
		""" check if the generated rule set of "Z,Y,X" have correct rule items  (Enabled Exception Raising) """
		self._test_comma_1(True)
		# self.assertRaises(ValueError, self._test_comma_1, True)
	# ### def test_comma_1

	def _test_comma_2(self, raise_error):
		""" check if the generated rule set of "Z,Y," have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday(",3 ,7,11,, ,", raise_error=raise_error)
		self.assertEqual(len(ruleset), 2)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (3, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_comma_2
	def test_comma_2_DEx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Disabled Exception Raising) """
		self._test_comma_2(False)
	def test_comma_2_REx(self):
		""" check if the generated rule set of "Z,Y," have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_2, True)
	# ### def test_comma_2

	def _test_comma_3(self, raise_error):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values """

		ruleset = crontimesequence.parse_cronstring_weekday( ",".join([str(v) for v in range(-3, 90)]) , raise_error=raise_error)
		self.assertEqual(len(ruleset), 8)

		is_rule_dateset_compatible(self, ruleset, [datetime.datetime(2012, 7, i, 9, 39) for i in range(1, 32)], True)
	# --- def _test_comma_3
	def test_comma_3_DEx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Disabled Exception Raising) """
		self._test_comma_3(False)
	def test_comma_3_REx(self):
		""" check if the generated rule set of "X,Y,Z" have correct rule items and can accept all possible values  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_comma_3, True)
	# ### def test_comma_3

	def _test_last_weekday_1(self, raise_error):
		""" check if the generated rule set of "xL" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("3L", raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		delta_7_day = datetime.timedelta(days=7)
		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			next_week_day = candidate_val + delta_7_day
			if (3 == candidate_val.isoweekday()) and (7 != next_week_day.month):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_last_weekday_1
	def test_last_weekday_1_DEx(self):
		""" check if the generated rule set of "xL" have correct rule items  (Disabled Exception Raising) """
		self._test_last_weekday_1(False)
	def test_last_weekday_1_REx(self):
		""" check if the generated rule set of "xL" have correct rule items  (Enabled Exception Raising) """
		self._test_last_weekday_1(True)
		# self.assertRaises(ValueError, self._test_last_weekday_1, True)
	# ### def test_last_weekday_1

	def _test_last_weekday_2(self, raise_error):
		""" check if can correctly handle "errL" where error is not integer """

		ruleset = crontimesequence.parse_cronstring_weekday("aL", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_last_weekday_2
	def test_last_weekday_2_DEx(self):
		""" check if can correctly handle "errL" where error is not integer  (Disabled Exception Raising) """
		self._test_last_weekday_2(False)
	def test_last_weekday_2_REx(self):
		""" check if can correctly handle "errL" where error is not integer  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_last_weekday_2, True)
	# ### def test_last_weekday_2

	def _test_last_weekday_3(self, raise_error):
		""" check if can correctly handle "errL" where error out of range """

		ruleset = crontimesequence.parse_cronstring_weekday("9L", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_last_weekday_3
	def test_last_weekday_3_DEx(self):
		""" check if can correctly handle "errL" where error out of range  (Disabled Exception Raising) """
		self._test_last_weekday_3(False)
	def test_last_weekday_3_REx(self):
		""" check if can correctly handle "errL" where error out of range  (Enabled Exception Raising) """
		self._test_last_weekday_3(True)
		# self.assertRaises(ValueError, self._test_last_weekday_3, True)
	# ### def test_last_weekday_3

	def _test_nth_weekday_1(self, raise_error):
		""" check if the generated rule set of "x#n" have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("3#2", raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		nth_count = 0
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if 3 == tweekday:
				nth_count = nth_count + 1
			if (3 == tweekday) and (2 == nth_count):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_nth_weekday_1
	def test_nth_weekday_1_DEx(self):
		""" check if the generated rule set of "x#n" have correct rule items  (Disabled Exception Raising) """
		self._test_nth_weekday_1(False)
	def test_nth_weekday_1_REx(self):
		""" check if the generated rule set of "x#n" have correct rule items  (Enabled Exception Raising) """
		self._test_nth_weekday_1(True)
		# self.assertRaises(ValueError, self._test_nth_weekday_1, True)
	# ### def test_nth_weekday_1

	def _test_nth_weekday_2(self, raise_error):
		""" check if can correctly handle "err#n" where err is not integer """

		ruleset = crontimesequence.parse_cronstring_weekday("a#2", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nth_weekday_2
	def test_nth_weekday_2_DEx(self):
		""" check if can correctly handle "err#n" where err is not integer  (Disabled Exception Raising) """
		self._test_nth_weekday_2(False)
	def test_nth_weekday_2_REx(self):
		""" check if can correctly handle "err#n" where err is not integer  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_nth_weekday_2, True)
	# ### def test_nth_weekday_2

	def _test_nth_weekday_3(self, raise_error):
		""" check if can correctly handle "x#err" where err is not integer """

		ruleset = crontimesequence.parse_cronstring_weekday("3#b", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nth_weekday_3
	def test_nth_weekday_3_DEx(self):
		""" check if can correctly handle "x#err" where err is not integer  (Disabled Exception Raising) """
		self._test_nth_weekday_3(False)
	def test_nth_weekday_3_REx(self):
		""" check if can correctly handle "x#err" where err is not integer  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_nth_weekday_3, True)
	# ### def test_nth_weekday_3

	def _test_nth_weekday_4(self, raise_error):
		""" check if can correctly handle "err#n" where err out of range """

		ruleset = crontimesequence.parse_cronstring_weekday("9#2", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nth_weekday_4
	def test_nth_weekday_4_DEx(self):
		""" check if can correctly handle "err#n" where err out of range  (Disabled Exception Raising) """
		self._test_nth_weekday_4(False)
	def test_nth_weekday_4_REx(self):
		""" check if can correctly handle "err#n" where err out of range  (Enabled Exception Raising) """
		self._test_nth_weekday_4(True)
		# self.assertRaises(ValueError, self._test_nth_weekday_4, True)
	# ### def test_nth_weekday_4

	def _test_nth_weekday_5(self, raise_error):
		""" check if can correctly handle "x#err" where err out of range """

		ruleset = crontimesequence.parse_cronstring_weekday("3#9", raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_nth_weekday_5
	def test_nth_weekday_5_DEx(self):
		""" check if can correctly handle "x#err" where err out of range  (Disabled Exception Raising) """
		self._test_nth_weekday_5(False)
	def test_nth_weekday_5_REx(self):
		""" check if can correctly handle "x#err" where err out of range  (Enabled Exception Raising) """
		self._test_nth_weekday_5(True)
		# self.assertRaises(ValueError, self._test_nth_weekday_5, True)
	# ### def test_nth_weekday_5

	def _test_hybrid(self, raise_error):
		""" check if the generated rule set with hybrid syntax have correct rule items """

		ruleset = crontimesequence.parse_cronstring_weekday("*/9, 5-15/2, 10,11, 2L,12, 17-23/3, 28-32,2#3 ,", raise_error=raise_error)

		positive_dateset = []
		negative_dateset = []
		for i in range(1, 32):
			d = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = d.isoweekday()
			if (tweekday in (1, 5, 7,)) or ( (2 == tweekday) and (i in (17, 31,)) ):
				positive_dateset.append(d)
			else:
				negative_dateset.append(d)
		is_rule_dateset_compatible(self, ruleset, positive_dateset, True)
		is_rule_dateset_compatible(self, ruleset, negative_dateset, False)
	# --- def _test_hybrid
	def test_hybrid_DEx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Disabled Exception Raising) """
		self._test_hybrid(False)
	def test_hybrid_REx(self):
		""" check if the generated rule set with hybrid syntax have correct rule items  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_hybrid, True)
	# ### def test_hybrid

	def _test_directfeed_1(self, raise_error):
		""" check if the parser can work correctly with directly feed integer """

		ruleset = crontimesequence.parse_cronstring_weekday(6, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if 6 == tweekday:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_1
	def test_directfeed_1_DEx(self):
		""" check if the parser can work correctly with directly feed integer  (Disabled Exception Raising) """
		self._test_directfeed_1(False)
	def test_directfeed_1_REx(self):
		""" check if the parser can work correctly with directly feed integer  (Enabled Exception Raising) """
		self._test_directfeed_1(True)
		# self.assertRaises(ValueError, self._test_directfeed_1, True)
	# ### def test_directfeed_1

	def _test_directfeed_2(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value True """

		ruleset = crontimesequence.parse_cronstring_weekday(True, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if 1 == tweekday:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_2
	def test_directfeed_2_DEx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Disabled Exception Raising) """
		self._test_directfeed_2(False)
	def test_directfeed_2_REx(self):
		""" check if the parser can work correctly with directly feed bool value True  (Enabled Exception Raising) """
		self._test_directfeed_2(True)
	# ### def test_directfeed_2

	def _test_directfeed_3(self, raise_error):
		""" check if the parser can work correctly with directly feed bool value False """

		ruleset = crontimesequence.parse_cronstring_weekday(False, raise_error=raise_error)
		self.assertEqual(len(ruleset), 1)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if 7 == tweekday:
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_3
	def test_directfeed_3_DEx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Disabled Exception Raising) """
		self._test_directfeed_3(False)
	def test_directfeed_3_REx(self):
		""" check if the parser can work correctly with directly feed bool value False  (Enabled Exception Raising) """
		self._test_directfeed_3(True)
	# ### def test_directfeed_3

	def _test_directfeed_4(self, raise_error):
		""" check if the parser can work correctly with directly feed negative range start """

		ruleset = crontimesequence.parse_cronstring_weekday(-3, 2, raise_error=raise_error)
		self.assertEqual(len(ruleset), 3)

		test_candidate_positive = []
		test_candidate_negative = []
		for i in range(1, 32):
			candidate_val = datetime.datetime(2012, 7, i, 9, 39)
			tweekday = candidate_val.isoweekday()
			if tweekday in (1, 2, 7,):
				test_candidate_positive.append(candidate_val)
			else:
				test_candidate_negative.append(candidate_val)
		is_rule_dateset_compatible(self, ruleset, test_candidate_positive, True)
		is_rule_dateset_compatible(self, ruleset, test_candidate_negative, False)
	# --- def _test_directfeed_4
	def test_directfeed_4_DEx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Disabled Exception Raising) """
		self._test_directfeed_4(False)
	def test_directfeed_4_REx(self):
		""" check if the parser can work correctly with directly feed negative range start  (Enabled Exception Raising) """
		self._test_directfeed_4(True)
	# ### def test_directfeed_4

	def _test_directfeed_5(self, raise_error):
		""" check if the parser can work correctly with directly feed alphabet as range end """

		ruleset = crontimesequence.parse_cronstring_weekday(-3, 'abc', raise_error=raise_error)
		self.assertEqual(len(ruleset), 0)
	# --- def _test_directfeed_5
	def test_directfeed_5_DEx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Disabled Exception Raising) """
		self._test_directfeed_5(False)
	def test_directfeed_5_REx(self):
		""" check if the parser can work correctly with directly feed alphabet as range end  (Enabled Exception Raising) """
		self.assertRaises(ValueError, self._test_directfeed_5, True)
	# ### def test_directfeed_5
# ### class Test_parse_cronstring_weekday


class Test_IntegratingFunction(unittest.TestCase):
	""" test integrating function """

	def _test_parse_rulestring(self, raise_error):
		""" check if generate rule to expected element """

		rulearray = crontimesequence.parse_cronstring("19", "5", "*", "*", "*")
		self.assertEqual(len(rulearray[0]), 1)
		self.assertEqual(len(rulearray[1]), 1)
		self.assertTrue(rulearray[2] is None)
		self.assertTrue(rulearray[3] is None)
		self.assertTrue(rulearray[4] is None)

		rulearray = crontimesequence.parse_cronstring("19", "*", "*", "*", "*", raise_error)
		self.assertEqual(len(rulearray[0]), 1)
		self.assertTrue(rulearray[1] is None)
		self.assertTrue(rulearray[2] is None)
		self.assertTrue(rulearray[3] is None)
		self.assertTrue(rulearray[4] is None)

		rulearray = crontimesequence.parse_cronstring("*", "3", "*", "*", "*", raise_error)
		self.assertTrue(rulearray[0] is None)
		self.assertEqual(len(rulearray[1]), 1)
		self.assertTrue(rulearray[2] is None)
		self.assertTrue(rulearray[3] is None)
		self.assertTrue(rulearray[4] is None)

		rulearray = crontimesequence.parse_cronstring("*", "*", "7", "*", "*", raise_error)
		self.assertTrue(rulearray[0] is None)
		self.assertTrue(rulearray[1] is None)
		self.assertEqual(len(rulearray[2]), 1)
		self.assertTrue(rulearray[3] is None)
		self.assertTrue(rulearray[4] is None)

		rulearray = crontimesequence.parse_cronstring("*", "*", "*", "11", "*", raise_error)
		self.assertTrue(rulearray[0] is None)
		self.assertTrue(rulearray[1] is None)
		self.assertTrue(rulearray[2] is None)
		self.assertEqual(len(rulearray[3]), 1)
		self.assertTrue(rulearray[4] is None)

		rulearray = crontimesequence.parse_cronstring("*", "*", "*", "*", "5", raise_error)
		self.assertTrue(rulearray[0] is None)
		self.assertTrue(rulearray[1] is None)
		self.assertTrue(rulearray[2] is None)
		self.assertTrue(rulearray[3] is None)
		self.assertEqual(len(rulearray[4]), 1)
	# --- def test_parse_rulestring
	def test_parse_rulestring_DEx(self):
		""" check if generate rule to expected element (Disabled Exception Raising) """
		self._test_parse_rulestring(False)
	def test_parse_rulestring_REx(self):
		""" check if generate rule to expected element (Enabled Exception Raising) """
		self._test_parse_rulestring(True)
	# ### def test_parse_rulestring

	def _test_every_3_hr_get_ruleset_n_filter_VALIDATE(self, rulearray):
		""" generate rule set for 19 */3 * * * rule (validate result) """

		self.assertEqual(len(rulearray), 5)
		self.assertEqual(len(rulearray[0]), 1)
		self.assertEqual(len(rulearray[1]), 8)
		self.assertTrue(rulearray[2] is None)
		self.assertTrue(rulearray[3] is None)
		self.assertTrue(rulearray[4] is None)

		d_s = datetime.datetime(2012, 7, 20, 10, 39, 20)
		d_e = datetime.datetime(2012, 7, 22, 23, 5, 27)

		result = crontimesequence.filter_range_by_rule(rulearray, d_s, d_e)

		for d in result:
			self.assertEqual(d.second, 0)
			self.assertEqual(d.minute, 19)
			self.assertTrue(0 == (d.hour % 3))

		self.assertEqual(len(result), 20)
	# --- def _test_every_3_hr_get_ruleset_n_filter
	def _test_every_3_hr_get_ruleset_n_filter(self, raise_error):
		""" generate rule set for 19 */3 * * * rule """

		rulearray = crontimesequence.parse_cronstring("19", "*/3", "*", "*", "*", raise_error)
		self._test_every_3_hr_get_ruleset_n_filter_VALIDATE(rulearray)
	# --- def test_every_3_hr_get_ruleset_n_filter
	def test_every_3_hr_get_ruleset_n_filter(self):
		""" generate rule set for 19 */3 * * * rule """

		rulearray = crontimesequence.parse_cronstring("19", "*/3", "*", "*", "*")
		self._test_every_3_hr_get_ruleset_n_filter_VALIDATE(rulearray)
	# --- def test_every_3_hr_get_ruleset_n_filter
	def test_every_3_hr_get_ruleset_n_filter_DEx(self):
		""" generate rule set for 19 */3 * * * rule (Disabled Exception Raising)"""
		self._test_every_3_hr_get_ruleset_n_filter(False)
	def test_every_3_hr_get_ruleset_n_filter_REx(self):
		""" generate rule set for 19 */3 * * * rule (Enabled Exception Raising)"""
		self._test_every_3_hr_get_ruleset_n_filter(True)
	# ### def test_every_3_hr_get_ruleset_n_filter

	def _test_every_3_hr_get_sequence(self, raise_error):
		""" generate sequence by 19 */3 * * * rule """

		d_s = datetime.datetime(2012, 7, 20, 10, 39, 20)
		d_e = datetime.datetime(2012, 7, 22, 23, 5, 27)

		result = crontimesequence.get_datetime_by_cronrule("19", "*/3", "*", "*", "*", d_s, d_e, raise_error)

		for d in result:
			self.assertEqual(d.second, 0)
			self.assertEqual(d.minute, 19)
			self.assertTrue(0 == (d.hour % 3))

		self.assertEqual(len(result), 20)
	# --- def test_every_3_hr_get_sequence
	def test_every_3_hr_get_sequence_DEx(self):
		""" generate sequence by 19 */3 * * * rule (Disabled Exception Raising) """
		self._test_every_3_hr_get_sequence(False)
	def test_every_3_hr_get_sequence_REx(self):
		""" generate sequence by 19 */3 * * * rule (Enabled Exception Raising) """
		self._test_every_3_hr_get_sequence(True)
	# ### def test_every_3_hr_get_sequence

	def _test_annually_get_sequence(self, raise_error):
		""" generate sequence by 19 3 7 1 * rule """

		d_s = datetime.datetime(2000, 9, 13, 1, 47, 16)
		d_e = datetime.datetime(2003, 12, 22, 23, 5, 27)

		result = crontimesequence.get_datetime_by_cronrule("19", "3", "7", "1", "*", d_s, d_e, raise_error)

		for d in result:
			self.assertEqual(d.second, 0)
			self.assertEqual(d.minute, 19)
			self.assertEqual(d.hour, 3)
			self.assertEqual(d.day, 7)
			self.assertEqual(d.month, 1)

		self.assertEqual(len(result), 3)
	# --- def test_annually_get_sequence
	def test_annually_get_sequence_DEx(self):
		""" generate sequence by 19 3 7 1 * rule (Disabled Exception Raising) """
		self._test_annually_get_sequence(False)
	def test_annually_get_sequence_REx(self):
		""" generate sequence by 19 3 7 1 * rule (Enabled Exception Raising) """
		self._test_annually_get_sequence(True)
	# ### def test_annually_get_sequence

	def _test_weekend_get_sequence(self, raise_error):
		""" generate sequence by 19 3 * * 6,7 rule """

		d_s = datetime.datetime(2012, 7, 20, 10, 39, 20)
		d_e = datetime.datetime(2012, 8, 22, 23, 5, 27)

		result = crontimesequence.get_datetime_by_cronrule("19", "3", "*", "*", "6,7", d_s, d_e, raise_error)

		for d in result:
			self.assertEqual(d.second, 0)
			self.assertEqual(d.minute, 19)
			self.assertEqual(d.hour, 3)
			self.assertTrue(d.isoweekday() in (6, 7,))

		self.assertEqual(len(result), 10)
	# --- def _test_weekend_get_sequence
	def test_weekend_get_sequence_DEx(self):
		""" generate sequence by 19 3 * * 6,7 rule (Disabled Exception Raising) """
		self._test_weekend_get_sequence(False)
	def test_weekend_get_sequence_REx(self):
		""" generate sequence by 19 3 * * 6,7 rule (Enabled Exception Raising) """
		self._test_weekend_get_sequence(True)
	# ### def test_weekend_get_sequence
# ### class Test_IntegratingFunction



if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr)

	unittest.main()
# <<< if __name__ == '__main__':


# vim: ts=4 sw=4 ai nowrap
