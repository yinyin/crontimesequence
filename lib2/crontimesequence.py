
# -*- coding: utf-8 -*-

""" build time sequence with cron syntax """

import datetime
import logging
_log = logging.getLogger(__name__)



class CronRule(object):
	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
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

		Parameter:
			v - the value for comparison
			fieldname - the datetime component to be check (one of 'minute', 'hour', 'day', 'month', 'weekday')
		"""
		self.v = int(v)
		self.fieldname = fieldname
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
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

	def __repr__(self):
		return "%s.ScalarValue(%d, \"%s\")" % (self.__module__, self.v, self.fieldname,)
	# ### def __repr__
# ### class ScalarValue


class LastDayOfMonthValue(CronRule):
	def __init__(self):
		""" constructor of last day of month check rule.
		"""
		pass
	# ### def __init__

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""
		aux = d + datetime.timedelta(days=1)
		if 1 == aux.day:
			return True
		return False
	# ### def is_accept

	def __repr__(self):
		return "%s.LastDayOfMonthValue()" % (self.__module__,)
	# ### def __repr__
# ### class LastDayOfMonthValue

_cached_last_day_of_month = LastDayOfMonthValue()


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

		Parameter:
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
		else:
			if self.exp_workday == d.day:
				result = True
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

	def __repr__(self):
		return "%s.NearestWorkDayValue(%d)" % (self.__module__, self.exp_workday,)
	# ### def __repr__
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

		Parameter:
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

	def __repr__(self):
		return "%s.LastWeekdayOfMonthValue(%d)" % (self.__module__, self.exp_weekday,)
	# ### def __repr__
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

		Parameter:
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

	def __repr__(self):
		return "%s.NthWeekdayOfMonthValue(%d, %d)" % (self.__module__, self.exp_weekday, self.exp_nth,)
	# ### def __repr__
# ### class NthWeekdayOfMonthValue



def _parse_cronstring_common(v, subparser, raise_error=False):
	if not isinstance(v, basestring):
		return None
	elif ',' in v:
		vseq = v.split(',')
		result = []
		for ele in vseq:
			result.extend(subparser(ele.strip(), raise_error=raise_error))
		return result
	elif '/' in v:
		parted = v.split('/')
		vseq = subparser(parted[0].strip(), raise_error=raise_error)
		try:
			vstep = int(parted[1].strip())
			return [vseq[idx] for idx in xrange(0, len(vseq), vstep)]
		except Exception as e:
			_log.error("Syntax Error: cannot parse step value to integer (token=%r>%r, e=%r)", v, parted, e)
			if raise_error:
				raise
			return vseq
	elif '-' in v:
		parted = v.split('-')
		return subparser(parted[0].strip(), parted[1].strip(), raise_error=raise_error)

	return None
# ### def _parse_cronstring_common


def parse_cronstring_minute(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_minute, raise_error)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 60:
					bR = 60
				return [ScalarValue(velem, 'minute') for velem in xrange(bL, bR)]
			except:
				_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
				if raise_error:
					raise
		elif '*' == vL:
			return parse_cronstring_minute(0, 59)
		else:
			try:
				vv = int(vL)
				if (vv >= 0) and (vv <= 59):
					return (ScalarValue(vv, 'minute'),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		return ()
	else:
		return result
# ### def parse_cronstring_minute

def parse_cronstring_hour(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_hour, raise_error)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 24:
					bR = 24
				return [ScalarValue(velem, 'hour') for velem in xrange(bL, bR)]
			except:
				_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
				if raise_error:
					raise
		elif '*' == vL:
			return parse_cronstring_hour(0, 23)
		else:
			try:
				vv = int(vL)
				if (vv >= 0) and (vv <= 23):
					return (ScalarValue(vv, 'hour'),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		return ()
	else:
		return result
# ### def parse_cronstring_hour

def parse_cronstring_day(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_day, raise_error)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 1:
					bL = 1
				if bR > 32:
					bR = 32
				return [ScalarValue(velem, 'day') for velem in xrange(bL, bR)]
			except:
				_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
				if raise_error:
					raise
		elif '*' == vL:
			return parse_cronstring_day(1, 31)
		elif 'L' == vL:
			return (_cached_last_day_of_month,)
		elif isinstance(vL, basestring) and (1 < len(vL)) and ('W' == vL[-1:]):
			try:
				nv = int(vL[:-1])
				if (nv >= 1) and (nv <= 31):
					return (NearestWorkDayValue(nv),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r, rule=W)", vL)
				if raise_error:
					raise
		else:
			try:
				vv = int(vL)
				if (vv >= 1) and (vv <= 31):
					return (ScalarValue(vv, 'day'),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		return ()
	else:
		return result
# ### def parse_cronstring_day

def parse_cronstring_month(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_month, raise_error)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 1:
					bL = 1
				if bR > 13:
					bR = 13
				return [ScalarValue(velem, 'month') for velem in xrange(bL, bR)]
			except:
				_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
				if raise_error:
					raise
		elif '*' == vL:
			return parse_cronstring_month(1, 12)
		else:
			try:
				vv = int(vL)
				if (vv >= 1) and (vv <= 12):
					return (ScalarValue(vv, 'month'),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		return ()
	else:
		return result
# ### def parse_cronstring_month

def parse_cronstring_weekday(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_weekday, raise_error)

	if result is None:
		if vT is not None:
			try:
				bL = int(vL)
				bR = int(vT) + 1
				if bL < 0:
					bL = 0
				if bR > 8:
					bR = 8
				return [ScalarValue(velem, 'weekday') for velem in xrange(bL, bR)]
			except:
				_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
				if raise_error:
					raise
		elif '*' == vL:
			return parse_cronstring_weekday(1, 7)
		elif isinstance(vL, basestring) and (2 == len(vL)) and ('L' == vL[1]):
			try:
				ww = int(vL[0])
				if (ww >= 0) and (ww <= 7):
					return (LastWeekdayOfMonthValue(ww),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		elif isinstance(vL, basestring) and (3 == len(vL)) and ('#' == vL[1]):
			try:
				ww = int(vL[0])
				nth = int(vL[2])
				if (ww >= 0) and (ww <= 7) and (nth >= 1) and (nth <= 5):
					return (NthWeekdayOfMonthValue(ww, nth),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		else:
			try:
				vv = int(vL)
				if (vv >= 0) and (vv <= 7):
					return (ScalarValue(vv, 'weekday'),)
			except:
				_log.error("Syntax Error: cannot convert value (token=%r)", vL)
				if raise_error:
					raise
		return ()
	else:
		return result
# ### def parse_cronstring_weekday


def __parse_cronstring_impl(rulestring, ruleparsefunc, raise_error):
	try:
		rulestring = str(rulestring).strip()
		if "*" == rulestring:
			return None
		else:
			return ruleparsefunc(rulestring, raise_error=raise_error)
	except Exception as e:
		_log.exception("Err: cannot load rule %r: %r", rulestring, e)
		if raise_error:
			raise
		return None
# ### def __parse_cronstring_impl

def parse_cronstring(rule_minute, rule_hour, rule_day, rule_month, rule_weekday, raise_error=False):
	""" parsing given cron-rule-string and result array of rule set

	Parameter:
		rule_minute, rule_hour, rule_day, rule_month, rule_weekday - cron-style rule string
		raise_error=False - do not raise exception on wrong syntax (still sending error message to logging module)
	Return:
		5 element tuple which consists rule set for minute, hour, day, month, weekday respectively
		the element would be None if there is no restriction
	"""
	rs_minute = __parse_cronstring_impl(rule_minute, parse_cronstring_minute, raise_error)
	rs_hour = __parse_cronstring_impl(rule_hour, parse_cronstring_hour, raise_error)
	rs_day = __parse_cronstring_impl(rule_day, parse_cronstring_day, raise_error)
	rs_month = __parse_cronstring_impl(rule_month, parse_cronstring_month, raise_error)
	rs_weekday = __parse_cronstring_impl(rule_weekday, parse_cronstring_weekday, raise_error)

	return (rs_minute, rs_hour, rs_day, rs_month, rs_weekday,)
# ### def parse_cronstring


def check_timestamp_by_rule(rulearray, tstamp):
	""" check if given time-stamp is comply to the given rule array

	Parameter:
		rulearray - rule array generated by parse_cronstring
		tstamp - time-stamp to be check
	Return:
		True if given time-stamp complied, False otherwise
	"""
	complied = 0

	# {{{ check if timestamp is accept by rule array
	for rset in rulearray:
		is_complied = False

		if rset is None:
			is_complied = True
		else:
			for robj in rset:
				if robj.is_accept(tstamp):
					is_complied = True
					break

		if is_complied:
			complied = complied + 1
	# }}} check if timestamp is accept by rule array

	if 5 == complied:	# all rules are conquered
		return True
	return False
# ### def check_timestamp_by_rule

def filter_range_by_rule(rulearray, tstamp_start, tstamp_end):
	""" filter time-stamps within given range by given rule array

	Parameter:
		rulearray - rule array generated by parse_cronstring
		tstamp_start - range start (inclusive)
		tstamp_end - range end (exclusive)
	Return:
		list of datetime object which complies to given rule array
	"""
	increment_delta = datetime.timedelta(minutes=1)
	d = datetime.datetime(tstamp_start.year, tstamp_start.month, tstamp_start.day, tstamp_start.hour, tstamp_start.minute)

	result = []

	while d < tstamp_end:
		if check_timestamp_by_rule(rulearray, d):
			result.append(d)
		d = d + increment_delta

	return result
# ### def filter_range_by_rule


def get_datetime_by_cronrule(rule_minute, rule_hour, rule_day, rule_month, rule_weekday, tstamp_start, tstamp_end, raise_error=False):
	""" filter given time-stamp range with given rules

	Parameter:
		rule_minute, rule_hour, rule_day, rule_month, rule_weekday - cron-style rule string
		tstamp_start - range start (inclusive)
		tstamp_end - range end (exclusive)
		raise_error=False - do not raise exception on wrong syntax (still sending error message to logging module)
	Return:
		list of datetime object which complies to given rule array
	"""
	rulearray = parse_cronstring(rule_minute, rule_hour, rule_day, rule_month, rule_weekday, raise_error)
	return filter_range_by_rule(rulearray, tstamp_start, tstamp_end)
# ### def get_datetime_by_cronrule



# vim: ts=4 sw=4 ai nowrap
