#!/usr/bin/env python

import os, sys
import urllib2
import json
import unicodedata
import re
from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser
from tex import latex2pdf, escape_latex
from cache import PriorityCache, CacheItem
from log import get_logger
logger = get_logger(__name__)

from utils import unescape, clean

# JSON fields
# content
# url
# responseUrl
# title

view_text_json = "http://viewtext.org/api/text?url=%s&format=json&rl=false"
view_text_html = "http://viewtext.org/api/text?url=%s&format=html&rl=false"
class Node(object):
    """
    Simple DOM
    """
    def __init__(self):
        self.children = []
        self.tag = ""
        self.attrs = []
        self.data = ""

    def __str__(self):
        tag = self.tag.upper()
        print "%s %s %s" % (tag, self.data, tag)
        for child in self.children:
            print child
        
class MyHTMLParser(HTMLParser):
    def __init__(self, root):
        HTMLParser.__init__(self)
        self.state = ""
        self.cur_tag = []
        self.attr = []
        self.single_tags = ["img", "br"]
        self.cur_data = ""

        self.lines = []

        self.root = root
        self.cur_node = None

    def handle_starttag(self, tag, attrs):
        # FIXME We need to figure out startend tags
        if not tag in self.single_tags:
            self.cur_tag.append(tag)
        for (attribute, value) in attrs:
            self.attr.append((attribute, value))
        if not self.cur_node:
            self.cur_node = Node()
            self.cur_node.tag = tag
            self.root.append(self.cur_node)
            self.attrs.append(self.attr)

    def handle_endtag(self, tag):
        if not self.cur_tag[-1] == tag:
            print "TAG MISMATCH ERROR. CURRENTLY %s NOW SEEING %s" % \
                    (self.cur_tag[-1], tag)
        else:
            if "p" == tag:
                self.lines.append("\n")
            self.cur_tag.pop()
            if len(self.attr) > 0 and "center" == self.attr[-1]:
                self.lines.append("\\end{center}")
                self.attr.pop()


    def handle_charref(self, name):
        print 'HANDLING CHARREF', name
        #self.lines.append(clean(name))

    def handle_data(self, data):
        text_tags = ["p", "em", "span", "a"]
        tag = self.cur_tag[-1]
        data = data.rstrip('\r\n')
        data = unescape(data)

class Fetcher(object):
    """
    Fetches and caches a single object
    """
    def __init__(self, cache, url):
        self.cache = cache
        self.url = url

    def run(self):
        """
        Actual fetcher. Could this be threaded?
        """
        url = view_text_json % self.url
        logger.debug("Fetching URL: " + url)
        raw_content = urllib2.urlopen(url)
        json_content = json.loads(raw_content.read())
        test_content = json_content['content']
        test_content = unicodedata.normalize('NFKD',
                test_content).encode('ascii', 'ignore')

        # Here, we begin constructing the syntax tree
        parser = MyHTMLParser()
        parser.feed(test_content)

        string = """
\\documentclass[12pt]{article}
\\begin{document}
{\\Large %s}
            """ % clean(json_content['title'])

        for line in parser.lines:
            line = escape_latex(line)
            string += line
        
        string += """
\\end{document}
        """

        with open('temp.latex', 'wb+') as f:
            f.write(string)

        pdf = latex2pdf(string)
        with open('temp.pdf', 'wb+') as f:
            f.write(pdf)

        #for k, v in json_content.iteritems():
        #    print k
        #item = CacheItem()
        #self.cache.insert(item)

