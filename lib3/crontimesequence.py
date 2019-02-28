# -*- coding: utf-8 -*-
""" build time sequence with cron syntax """

import datetime
import logging
_log = logging.getLogger(__name__)


class CronRule:
	def is_accept(self, d):  # pylint: disable=unused-argument
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
			d - the datetime object to be check
		Return:
			True if given object is complied, False otherwise.
		"""
		return False


class ScalarValue(CronRule):
	def __init__(self, v, fieldname):
		""" constructor of scalar value check rule.

		Parameter:
			v - the value for comparison
			fieldname - the datetime component to be check (one of 'minute', 'hour', 'day', 'month', 'weekday')
		"""
		self.v = int(v)
		self.fieldname = fieldname

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""
		if self.fieldname == 'weekday':
			if self.v == 0:
				self.v = 7  # reset to ISO calendar
			if d.isoweekday() != self.v:
				return False
		elif getattr(d, self.fieldname) != self.v:
			return False
		return True

	def __repr__(self):
		return "%s.ScalarValue(%d, \"%s\")" % (
				self.__module__,
				self.v,
				self.fieldname,
		)


class LastDayOfMonthValue(CronRule):
	def __init__(self):
		""" constructor of last day of month check rule.
		"""
		pass

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""
		aux = d + datetime.timedelta(days=1)
		if aux.day == 1:
			return True
		return False

	def __repr__(self):
		return "%s.LastDayOfMonthValue()" % (self.__module__, )


_cached_last_day_of_month = LastDayOfMonthValue()


class NearestWorkDayValue(CronRule):
	def __init__(self, v):
		""" constructor of nearest work day of month check rule.
		"""
		self.exp_workday = int(v)
		self.__cached_accept_date = None
		self.__cached_reject_date = None

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
		if d_wd in (6, 7):
			result = False
		else:
			if self.exp_workday == d.day:
				result = True
			elif d_wd == 1:
				if (self.exp_workday == (d.day - 1)) or ((self.exp_workday == 1) and (d.day == 3)):
					result = True
			elif d_wd == 5:
				if (self.exp_workday == (d.day + 1)):
					result = True
				else:
					aux = d + datetime.timedelta(days=3)
					if (self.exp_workday == (d.day + 2)) and (aux.day == 1):
						result = True
		if result:
			self.__cached_accept_date = d_date
		else:
			self.__cached_reject_date = d_date
		return result

	def __repr__(self):
		return "%s.NearestWorkDayValue(%d)" % (
				self.__module__,
				self.exp_workday,
		)


class LastWeekdayOfMonthValue(CronRule):
	def __init__(self, v):
		""" constructor of last week day of month check rule.
		"""
		self.exp_weekday = int(v)
		if self.exp_weekday == 0:
			self.exp_weekday = 7

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

	def __repr__(self):
		return "%s.LastWeekdayOfMonthValue(%d)" % (
				self.__module__,
				self.exp_weekday,
		)


class NthWeekdayOfMonthValue(CronRule):
	def __init__(self, v, nth):
		""" constructor of N-th week day of month check rule.
		"""
		self.exp_weekday = int(v)
		self.exp_nth = int(nth)
		if self.exp_weekday == 0:
			self.exp_weekday = 7

	def is_accept(self, d):
		""" test is the given datetime object d complied with the rule set in this object.

		Parameter:
			d - the datetime object to check
		Return:
			True if given object is complied, False otherwise.
		"""
		if d.isoweekday() == self.exp_weekday:
			aux_0 = d - datetime.timedelta(days=(7 * self.exp_nth))
			aux_1 = d - datetime.timedelta(days=(7 * (self.exp_nth - 1)))
			if (aux_0.month != d.month) and (aux_1.month == d.month):
				return True
		return False

	def __repr__(self):
		return "%s.NthWeekdayOfMonthValue(%d, %d)" % (
				self.__module__,
				self.exp_weekday,
				self.exp_nth,
		)


def _parse_cronstring_common(v, subparser, raise_error=False):
	if not isinstance(v, str):
		return None
	if ',' in v:
		vseq = v.split(',')
		result = []
		for ele in vseq:
			result.extend(subparser(ele.strip(), raise_error=raise_error))
		return result
	if '/' in v:
		parted = v.split('/')
		vseq = subparser(parted[0].strip(), raise_error=raise_error)
		try:
			vstep = int(parted[1].strip())
			return [vseq[idx] for idx in range(0, len(vseq), vstep)]
		except Exception as e:
			_log.error("Syntax Error: cannot parse step value to integer (token=%r>%r, e=%r)", v, parted, e)
			if raise_error:
				raise
			return vseq
	elif '-' in v:
		parted = v.split('-')
		return subparser(parted[0].strip(), parted[1].strip(), raise_error=raise_error)
	return None


def _cast_boundary(rawL, rawT, boundL, boundR):
	bL = max(boundL, int(rawL))
	bR = min(boundR, int(rawT) + 1)
	return (bL, bR)


def parse_cronstring_minute(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_minute, raise_error)
	if result is not None:
		return result
	if vT is not None:
		try:
			bL, bR = _cast_boundary(vL, vT, 0, 60)
			return [ScalarValue(velem, 'minute') for velem in range(bL, bR)]
		except Exception:
			_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
			if raise_error:
				raise
		return ()
	if vL == '*':
		return parse_cronstring_minute(0, 59)
	try:
		vv = int(vL)
		if 0 <= vv <= 59:
			return (ScalarValue(vv, 'minute'), )
	except Exception:
		_log.error("Syntax Error: cannot convert value (token=%r)", vL)
		if raise_error:
			raise
	return ()


def parse_cronstring_hour(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_hour, raise_error)
	if result is not None:
		return result
	if vT is not None:
		try:
			bL, bR = _cast_boundary(vL, vT, 0, 24)
			return [ScalarValue(velem, 'hour') for velem in range(bL, bR)]
		except Exception:
			_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
			if raise_error:
				raise
		return ()
	if vL == '*':
		return parse_cronstring_hour(0, 23)
	try:
		vv = int(vL)
		if 0 <= vv <= 23:
			return (ScalarValue(vv, 'hour'), )
	except Exception:
		_log.error("Syntax Error: cannot convert value (token=%r)", vL)
		if raise_error:
			raise
	return ()


def parse_cronstring_day(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_day, raise_error)
	if result is not None:
		return result
	if vT is not None:
		try:
			bL, bR = _cast_boundary(vL, vT, 1, 32)
			return [ScalarValue(velem, 'day') for velem in range(bL, bR)]
		except Exception:
			_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
			if raise_error:
				raise
		return ()
	if vL == '*':
		return parse_cronstring_day(1, 31)
	if vL == 'L':
		return (_cached_last_day_of_month, )
	if isinstance(vL, str) and (len(vL) > 1) and (vL[-1:] == 'W'):
		try:
			nv = int(vL[:-1])
			if 1 <= nv <= 31:
				return (NearestWorkDayValue(nv), )
		except Exception:
			_log.error("Syntax Error: cannot convert value (token=%r, rule=W)", vL)
			if raise_error:
				raise
		return ()
	try:
		vv = int(vL)
		if 1 <= vv <= 31:
			return (ScalarValue(vv, 'day'), )
	except Exception:
		_log.error("Syntax Error: cannot convert value (token=%r)", vL)
		if raise_error:
			raise
	return ()


def parse_cronstring_month(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_month, raise_error)
	if result is not None:
		return result
	if vT is not None:
		try:
			bL, bR = _cast_boundary(vL, vT, 1, 13)
			return [ScalarValue(velem, 'month') for velem in range(bL, bR)]
		except Exception:
			_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
			if raise_error:
				raise
	elif vL == '*':
		return parse_cronstring_month(1, 12)
	else:
		try:
			vv = int(vL)
			if 1 <= vv <= 12:
				return (ScalarValue(vv, 'month'), )
		except Exception:
			_log.error("Syntax Error: cannot convert value (token=%r)", vL)
			if raise_error:
				raise
	return ()


def parse_cronstring_weekday(vL, vT=None, raise_error=False):
	result = _parse_cronstring_common(vL, parse_cronstring_weekday, raise_error)
	if result is not None:
		return result
	if vT is not None:
		try:
			bL, bR = _cast_boundary(vL, vT, 0, 8)
			return [ScalarValue(velem, 'weekday') for velem in range(bL, bR)]
		except Exception:
			_log.error("Syntax Error: cannot convert one or both of range value (token=%r-%r)", vL, vT)
			if raise_error:
				raise
		return ()
	if vL == '*':
		return parse_cronstring_weekday(1, 7)
	if isinstance(vL, str) and (len(vL) == 2) and (vL[1] == 'L'):
		try:
			ww = int(vL[0])
			if 0 <= ww <= 7:
				return (LastWeekdayOfMonthValue(ww), )
		except Exception:
			_log.error("Syntax Error: cannot convert value (token=%r)", vL)
			if raise_error:
				raise
		return ()
	if isinstance(vL, str) and (len(vL) == 3) and (vL[1] == '#'):
		try:
			ww = int(vL[0])
			nth = int(vL[2])
			if (0 <= ww <= 7) and (1 <= nth <= 5):
				return (NthWeekdayOfMonthValue(ww, nth), )
		except Exception:
			_log.error("Syntax Error: cannot convert value (token=%r)", vL)
			if raise_error:
				raise
		return ()
	try:
		vv = int(vL)
		if 0 <= vv <= 7:
			return (ScalarValue(vv, 'weekday'), )
	except Exception:
		_log.error("Syntax Error: cannot convert value (token=%r)", vL)
		if raise_error:
			raise
	return ()


def __parse_cronstring_impl(rulestring, ruleparsefunc, raise_error):
	try:
		rulestring = str(rulestring).strip()
		if rulestring == "*":
			return None
		return ruleparsefunc(rulestring, raise_error=raise_error)
	except Exception as e:
		_log.exception("Err: cannot load rule %r: %r", rulestring, e)
		if raise_error:
			raise
		return None


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
	return (
			rs_minute,
			rs_hour,
			rs_day,
			rs_month,
			rs_weekday,
	)


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
	if complied == 5:  # all rules are conquered
		return True
	return False


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


# vim: ts=4 sw=4 ai nowrap
