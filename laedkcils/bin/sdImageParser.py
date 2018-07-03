#!/usr/local/bin/python

#!/usr/bin/python

import urllib
from importlib import reload
from html.parser import HTMLParser
import sys
from html.entities import entitydefs

class sdImageParser(HTMLParser):
    images = []
    inDetailImage = False
    isImage = False
    divCount = 0

    def __init__(self):
        self.images = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            if self.divCount > 0:
                self.divCount += 1
            else:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'detailImages' or value == 'postAttachments clearfix':
                            self.inDetailImage = True
                            self.divCount = 1
        elif tag == "img" and self.inDetailImage:
            for name, value in attrs:
                if name == 'class':
                    if value == 'lazyimg alternateImage' or value == 'lazyimg':
                        self.isImage = True
                elif self.isImage == True and name == 'data-original':
                    self.images.append(value)
                    self.isImage = False

    def handle_endtag(self, tag):
        if tag == 'div' and self.inDetailImage:
            self.divCount -= 1
            if self.divCount == 0:
                self.inDetailImage = False

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
    for image in parser.images:
        print(image)

