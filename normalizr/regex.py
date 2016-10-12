#-*- coding: utf-8 -*-
# vim:fileencoding=utf-8
"""
Regular expression to match URLs as seen on http://daringfireball.net/2010/07/improved_regex_for_matching_urls
"""
URL_REGEX = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
