#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Rob Day'
SITENAME = "RKD's Blog"
SITEURL = 'http://rkd.me.uk'

PATH = 'content'
STATIC_PATHS=['static']

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Programming in the 21st Century', 'http://prog21.dadgum.com/'),
         ('matt.might.net', 'http://matt.might.net/articles/'),
         )

# Social widget
SOCIAL = (('Github', 'https://www.github.com/rkday'),
          ('Twitter', 'https://twitter.com/day_rk'),)

DEFAULT_PAGINATION = False

THEME = "../Flex/"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
