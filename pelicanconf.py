#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'H.G.'
SITENAME = u'sitename'
# change in publishconf.py
# leave blank so that urls are relative while developing
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)
LINKS = None

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)
SOCIAL = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# --------------------
# my customizations
# --------------------
LOAD_CONTENT_CACHE = False # notebooks are not reloaded when changed if this is True
DELETE_OUTPUT_DIRECTORY = True
STATIC_PATHS = ['images', 'docs']

# --------------------
# theme-related
# --------------------
THEME = 'pelican-octopress-theme' # github.com/H-Gens/pelican-octopress-theme

# --------------------
# plugins
# --------------------
# https://github.com/getpelican/pelican-plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'liquid_tags.notebook',
    'liquid_tags.youtube',
    'liquid_tags.literal',
]

# --------------------
# notebook-related
# --------------------
NOTEBOOK_DIR = 'notebooks'
if not os.path.exists('_nb_header.html'):
    import warnings
    warnings.warn(
        "_nb_header.html not found. "
        "Rerun make html to finalize build."
    )
else:
    EXTRA_HEADER = open('_nb_header_modded.html').read().decode('utf-8')
# add to template: {% if EXTRA_HEADER %}{{ EXTRA_HEADER }}{% endif %}

