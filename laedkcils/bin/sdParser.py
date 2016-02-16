#!/usr/bin/python

import HTMLParser
import sys
from htmlentitydefs import entitydefs

class sdParser(HTMLParser.HTMLParser):
    inTitleLine = 0
    isDeal = 0
    inSpan = 0

    url = ""
    title = ""
    promo_hash = {}

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.HTMLParser.__init__(self)
        self.isDeal = 0

    def handle_starttag(self, tag, attrs):
        url=""

        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'threadtitleline':
                    self.inTitleLine = 1
        elif tag == 'span':
            self.inSpan = 1;
        elif tag == "a" and self.inTitleLine == 1 and self.inSpan == 0:
            for name, value in attrs:
                if name == 'href':
                    self.url = value
                    self.isDeal = 1

    def handle_endtag(self, tag):
        if tag == 'span':
            self.inSpan = 0
        elif tag == 'div':
            self.inTitleLine = 0
        elif tag == 'a' and self.isDeal == 1:
            self.promo_hash[self.title] = []
            self.promo_hash[self.title].append(self.url)
            self.title = ""
            self.isDeal = 0

    def handle_data(self, data):
        if self.isDeal == 1:
            self.title += data;

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('latin1')

    if len(sys.argv) < 2:
        print "usage: %s filename" % sys.argv[0]
        sys.exit(1)
        
    filename = sys.argv[1];
    input = open(filename, "r");
    html = input.read();
    input.close()
            
    parser = sdParser()
    parser.feed(html)
    for title in parser.promo_hash:
        line = "%s\t%s" % (title, parser.promo_hash[title][0])
        print line

