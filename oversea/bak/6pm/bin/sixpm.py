#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
from htmlentitydefs import entitydefs

from sixpmParser import sixpmParser
from sixpmDetailParser import sixpmDetailParser

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print "usage: %s filename" % sys.argv[0]
    else:
        filename = sys.argv[1]
        input = open(filename, "r")
        html = input.read()
        input.close()
            
        parser = sixpmParser()
        parser.feed(html)

        detailParser = sixpmDetailParser()
        productHash = parser.productHash
        count = 0
        for url in productHash:
            print "processing %s" % url
            detailParser.reinit()
            htmlDetail = urllib.urlopen(url).read()
            detailParser.feed(htmlDetail)
            for key in detailParser.productInfoHash:
                productHash[url][key] = detailParser.productInfoHash[key]
            count = count + 1

        output = open(filename + ".json", "w+")
        output.write(json.dumps(productHash))
        output.close()


