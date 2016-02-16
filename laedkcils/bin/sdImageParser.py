#!/usr/bin/python

import urllib
import HTMLParser
import sys
from htmlentitydefs import entitydefs

class sdImageParser(HTMLParser.HTMLParser):
    images = []
    inDetailImage = False

    def __init__(self):
        self.images = []
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if value == 'detailImages' or value == 'postAttachments clearfix':
                        self.inDetailImage = True
        elif tag == "img" and self.inDetailImage:
            for name, value in attrs:
                if name == 'src':
                    self.images.append(value)

    def handle_endtag(self, tag):
        if tag == 'div' and self.inDetailImage:
            self.inDetailImage = False

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
            
    parser = sdImageParser()
    parser.feed(html)
    for image in parser.images:
        print "%s" % image

