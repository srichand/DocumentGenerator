#!/usr/bin/env python

import os, sys
from cache import PriorityCache, CacheItem
from fetcher import Fetcher
from log import get_logger
logger = get_logger(__name__)

def get_url_list(url_file):
    url_list = []
    with open(url_file, 'r') as urls:
        lines = urls.readlines()
        for line in lines:
            if not line.strip().startswith('#'):
                url_list.append(line.strip())
                
    return url_list

url_list = {
        "viewtext" : "http://viewtext.org/article?url=http://steveblank.com/2011/06/17/are-you-you-the-fool-at-the-table/",
        "steveblank" : "http://steveblank.com/2011/06/17/are-you-you-the-fool-at-the-table/",
        "nytimes" : "http://www.nytimes.com/2011/06/18/arts/video-games/duke-nukem-forever-is-released-after-14-years.html",
        "arstechnica" : "http://arstechnica.com/gaming/news/2011/06/week-in-gaming-duke-forever-battlefield-3-skyrim.ars"
        }

def fetch_all_pages():
    fetch = FetchPages("pages")
    for name, url in url_list.iteritems():
        fetch.fetch(name, url)

for html_file in os.listdir("pages"):
    link = url_list[html_file.split(".")[0]]
    page = os.path.join("pages", html_file)
    content = open(page, 'r').read()
    clean_content = grabContent(link, content)
    with open(html_file + ".clean", 'w+') as f:
        f.write(unicode_cleaner(clean_content))

def main():
    url_file = 'url.conf'
    url_list = get_url_list(url_file)
    cache = PriorityCache()
    fetchers = []
    for url in url_list:
        f = Fetcher(cache, url)
        fetchers.append(f)

    for f in fetchers:
        f.run()

if __name__ == "__main__":
    main()
