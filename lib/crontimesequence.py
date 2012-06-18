
# -*- coding: utf-8 -*-

""" build time sequence with cron syntax """

import re


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



# vim: ts=4 sw=4 ai nowrap
