#!/usr/bin/env python

# -*- coding: utf-8 -*-

from distutils.core import setup



setup(name='CronTimeSequence',
		version='1.00',
		description='Generating datetime-sequence with crontab syntax in given datetime range',
		py_modules=['crontimesequence', ],
		package_dir={'': 'lib'},
		classifiers=['Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 2.6',
			'Programming Language :: Python :: 2.7', ],
		license='MIT License',
	)



# vim: ts=4 sw=4 ai nowrap
