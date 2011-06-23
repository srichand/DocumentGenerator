import unicodedata
import re
from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser

def unescape(text):
    #print 'unescaping ', text
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def clean(text):
    text = text.encode('ascii', 'ignore')
    text = unicodedata.normalize("NFKD", unicode(text)).encode('ascii', 'ignore')
    text = unescape(text)
    return text


