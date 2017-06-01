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
EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)

EMOJI_REGEX = re.compile(r'([\U00002600-\U000027BF\U0001F300-\U0001F64F\U0001F680-\U0001F6FF])')
