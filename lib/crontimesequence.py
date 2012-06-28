
# -*- coding: utf-8 -*-

""" build time sequence with cron syntax """

import re
import datetime


class CronRule(object):
	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to be check
		Return:
			True if given object is complied, False otherwise.
		"""

		return False
	# ### def is_accept
# ### class CronRule

class ScalarValue(CronRule):
	def __init__(self, v, fieldname):
		""" constructor of scalar value check rule.

		Argument:
			v - the value for comparison
			fieldname - the datetime component to be check (one of 'minute', 'hour', 'day', 'month', 'weekday')
		"""
		self.v = int(v)
		self.fieldname = fieldname
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""

		if 'weekday' == self.fieldname:
			if 0 == self.v:
				self.v = 7	# reset to ISO calendar
			if d.isoweekday() != self.v:
				return False
		elif getattr(d, self.fieldname) != self.v:
			return False

		return True
	# ### def is_accept
# ### class ScalarValue

class LastDayOfMonthValue(CronRule):
	def __init__(self):
		""" constructor of last day of month check rule.
		"""
		pass
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""

		aux = d + datetime.timedelta(days=1)
		
		if 1 == aux.day:
			return True
		
		return False
	# ### def is_accept
# ### class LastDayOfMonthValue

_cached_last_day_of_month = LastDayOfMonthValue()

class LastWeekdayOfMonthValue(CronRule):
	def __init__(self, v):
		""" constructor of last week day of month check rule.
		"""
		self.exp_weekday = int(v)
		if 0 == self.exp_weekday:
			self.exp_weekday = 7
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""

		if d.isoweekday() == self.exp_weekday:
			aux = d + datetime.timedelta(days=7)
			if aux.month != d.month:
				return True
		
		return False
	# ### def is_accept
# ### class LastWeekdayOfMonthValue

class NearestWorkDayValue(CronRule):
	def __init__(self, v):
		""" constructor of nearest work day of month check rule.
		"""
		self.exp_workday = int(v)
		
		self.__cached_accept_date = None
		self.__cached_reject_date = None
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""
	
		d_wd = d.isoweekday()
		d_date = d.date()
		
		if d_date == self.__cached_accept_date:
			return True
		if d_date == self.__cached_reject_date:
			return False
		
		result = False
		if (6 == d_wd) or (7 == d_wd):
			result = False
		elif (1 == d_wd):
			if (self.exp_workday == (d.day - 1)) or ( (1 == self.exp_workday) and (3 == d.day) ):
				result = True
		elif (5 == d_wd):
			if (self.exp_workday == (d.day + 1)):
				result = True
			else:
				aux = d + datetime.timedelta(days=3)
				if (self.exp_workday == (d.day + 2)) and (1 == aux.day):
					result = True
		
		if result:
			self.__cached_accept_date = d_date
		else:
			self.__cached_reject_date = d_date
		return result
	# ### def is_accept
# ### class NearestWorkDayValue

class LastWeekdayOfMonthValue(CronRule):
	def __init__(self, v):
		""" constructor of last week day of month check rule.
		"""
		self.exp_weekday = int(v)
		if 0 == self.exp_weekday:
			self.exp_weekday = 7
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""

		if d.isoweekday() == self.exp_weekday:
			aux = d + datetime.timedelta(days=7)
			if aux.month != d.month:
				return True
		
		return False
	# ### def is_accept
# ### class LastWeekdayOfMonthValue

class NthWeekdayOfMonthValue(CronRule):
	def __init__(self, v, nth):
		""" constructor of N-th week day of month check rule.
		"""
		self.exp_weekday = int(v)
		self.exp_nth = int(nth)
		if 0 == self.exp_weekday:
			self.exp_weekday = 7
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Argument:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""

		if d.isoweekday() == self.exp_weekday:
			aux_0 = d - datetime.timedelta(days=(7*self.exp_nth))
			aux_1 = d - datetime.timedelta(days=(7*(self.exp_nth-1)))
			if (aux_0.month != d.month) and (aux_1.month == d.month):
				return True
		
		return False
	# ### def is_accept
# ### class NthWeekdayOfMonthValue




def _parse_cronstring_common(v, subparser):
	if ',' in v:
		vseq = v.split(',')
		result = []
		for ele in vseq:
			result.extend( subparser(ele.strip()) )
		return result
	elif '/' in v:
		parted = v.split('/')
		vseq = subparser( parted[0].strip() )
		try:
			vstep = int(parted[1].strip())
			return [vseq[idx] for idx in range(len(vseq), step=vstep)]
		except:
			print "Syntax Err: cannot parse step value to integer (token=%r)" % (v,)
			return vseq
	elif '-' in v:
		parted = v.split('-')
		return subparser(parted[0].strip(), parted[1].strip())

	return None
# ### def _parse_cronstring_common


def parse_cronstring_minute(vL, vT=None):
	result = _parse_cronstring_common(v, parse_cronstring_minute)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 60:
					bR = 60
				return [ScalarValue(velem, 'minute') for velem in range(bL, bR)]
			except:
				print "Syntax Err: cannot convert one or both of range value (token=%r-%r)" % (vL, vT,)
		elif '*' == vL:
			return parse_cronstring_minute(0, 59)
		else:
			try:
				vv = int(vL)
				return (ScalarValue(vv, 'minute'),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		return ()
	else:
		return result
# ### def parse_cronstring_minute

def parse_cronstring_hour(vL, vT=None):
	result = _parse_cronstring_common(v, parse_cronstring_hour)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 24:
					bR = 24
				return [ScalarValue(velem, 'hour') for velem in range(bL, bR)]
			except:
				print "Syntax Err: cannot convert one or both of range value (token=%r-%r)" % (vL, vT,)
		elif '*' == vL:
			return parse_cronstring_hour(0, 23)
		else:
			try:
				vv = int(vL)
				return (ScalarValue(vv, 'hour'),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		return ()
	else:
		return result
# ### def parse_cronstring_hour

def parse_cronstring_day(vL, vT=None):
	result = _parse_cronstring_common(v, parse_cronstring_day)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 1:
					bL = 1
				if bR > 32:
					bR = 32
				return [ScalarValue(velem, 'day') for velem in range(bL, bR)]
			except:
				print "Syntax Err: cannot convert one or both of range value (token=%r-%r)" % (vL, vT,)
		elif '*' == vL:
			return parse_cronstring_day(1, 31)
		elif 'L' == vL:
			return (_cached_last_day_of_month,)
		elif (1 < len(vL)) and ('W' == vL[-1:]):
			try:
				nv = int(vL[:-1])
				return (NearestWorkDayValue(nv),)
			except:
				print "Syntax Err: cannot convert value (token=%r, rule=W)" % (vL,)
		else:
			try:
				vv = int(vL)
				return (ScalarValue(vv, 'day'),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		return ()
	else:
		return result
# ### def parse_cronstring_day

def parse_cronstring_month(vL, vT=None):
	result = _parse_cronstring_common(v, parse_cronstring_month)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 1:
					bL = 1
				if bR > 13:
					bR = 13
				return [ScalarValue(velem, 'month') for velem in range(bL, bR)]
			except:
				print "Syntax Err: cannot convert one or both of range value (token=%r-%r)" % (vL, vT,)
		elif '*' == vL:
			return parse_cronstring_month(1, 12)
		else:
			try:
				vv = int(vL)
				return (ScalarValue(vv, 'month'),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		return ()
	else:
		return result
# ### def parse_cronstring_month

def parse_cronstring_weekday(vL, vT=None):
	result = parse_cronstring_weekday(v, parse_cronstring_month)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 8:
					bR = 8
				return [ScalarValue(velem, 'weekday') for velem in range(bL, bR)]
			except:
				print "Syntax Err: cannot convert one or both of range value (token=%r-%r)" % (vL, vT,)
		elif '*' == vL:
			return parse_cronstring_weekday(1, 7)
		elif (2 == len(vL)) and ('L' == vL[1]):
			try:
				ww = int(vL[0])
				return (LastWeekdayOfMonthValue(ww),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		elif (3 == len(vL)) and ('#' == vL[1]):
			try:
				ww = int(vL[0])
				nth = int(vL[2])
				return (NthWeekdayOfMonthValue(ww, nth),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		else:
			try:
				vv = int(vL)
				return (ScalarValue(vv, 'weekday'),)
			except:
				print "Syntax Err: cannot convert value (token=%r)" % (vL,)
		return ()
	else:
		return result
# ### def parse_cronstring_month



# vim: ts=4 sw=4 ai nowrap
