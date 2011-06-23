#!/usr/bin/env python

import os, sys
import urllib2

# Page cleaner from http://nirmalpatel.com/fcgi/hn.py

class FetchPages(object):
    def __init__(self, directory):
        self.directory = directory
        pass

    def fetch(self, name, url):
        content = urllib2.urlopen(url)
        path = os.path.join(self.directory, name+".html")
        with open(path, 'w+') as f:
            f.write(content.read())


