#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup



# {{{ select package code folder
if sys.version_info[0] > 2:
	PACKAGE_FOLDER = 'lib3'
else:
	PACKAGE_FOLDER = 'lib2'
# }}} select package code folder


setup(name='CronTimeSequence',
		version='1.1.0',
		description='Generating datetime-sequence with crontab syntax in given datetime range',
		py_modules=['crontimesequence', ],
		package_dir={'': PACKAGE_FOLDER},
		classifiers=['Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 2.6',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3.0',
			'Programming Language :: Python :: 3.1',
			'Programming Language :: Python :: 3.2',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4', ],
		license='MIT License',
	)



# vim: ts=4 sw=4 ai nowrap
