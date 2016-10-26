#-*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re

"""
Regular expression to match URLs as seen on http://daringfireball.net/2010/07/improved_regex_for_matching_urls
"""
URL_REGEX = re.compile(
    r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
    re.IGNORECASE)

"""
Regular expression to match email addresses as seen on http://www.wellho.net/resources/ex.php4?item=y115/relib.py
"""
EMAIL_REGEX = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)", re.IGNORECASE)
