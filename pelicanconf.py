#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Rob Day'
SITENAME = "RKD's Blog"
SITETITLE = "RKD's Blog"
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
         ('Rands in Repose', 'http://randsinrepose.com/'),
         ('Coding Horror', 'http://blog.codinghorror.com/'),
         ('Ask a Manager', 'http://www.askamanager.org/'),
         ('Project Clearwater blog', 'http://www.projectclearwater.org/latest-news/'),
         ('Paul Graham\'s Essays', 'http://www.paulgraham.com/articles.html'),
         )

# Social widget
SOCIAL = (('github', 'https://www.github.com/rkday'),
          ('twitter', 'https://twitter.com/day_rk'),
          ('stack-overflow', 'http://stackoverflow.com/users/1628317/rkday'),
          )

DEFAULT_PAGINATION = 5

THEME = "Flex/"
SITELOGO = "/static/profile.jpg"

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
