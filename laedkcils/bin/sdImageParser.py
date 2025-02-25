#!/usr/local/bin/python

#!/usr/bin/python

import urllib
from importlib import reload
from html.parser import HTMLParser
import sys
from html.entities import entitydefs
import re

class sdImageParser(HTMLParser):
    images = set()
    isImage = False

    def __init__(self):
        self.images = set()
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for name, value in attrs:
                if name == 'class':
                    if value == 'lazyImage dealImage__image':
                        self.isImage = True
                elif self.isImage == True and name == 'src':
                    if re.search(".thumb$", value):
                        self.images.add(f"https://slickdeals.net{value}")
                    self.isImage = False

    # def handle_endtag(self, tag):

if __name__ == '__main__':
    reload(sys)
    #sys.setdefaultencoding('latin1')

    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], " filename")
        sys.exit(1)

    filename = sys.argv[1];
    input = open(filename, "r");
    html = input.read();
    input.close()
            
    parser = sdImageParser()
    parser.feed(html)
    for image in list(parser.images):
        print(image)

