#!/usr/bin/python

import json
import urllib
import HTMLParser
import sys
import re
from htmlentitydefs import entitydefs

class sixpmDetailParser(HTMLParser.HTMLParser):
    inNote = False
    inSKU = False
    inScript = False

    color = ""
    sku = ""
    image = ""
    imageMatcher = re.compile('pImgs\[[0-9]*\]\[\'[^\']*\']\[\'[p0-9]\'\] = \'[^\']*\'')
    imageUrlMatcher = re.compile('\[.*\]\[\'(.*)\'\]\[\'(.*)\'\] = [^\']*\'(http://[^\']*)\'');
    productInfoHash = {}

    def reinit(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inNote = False
        self.inSKU = False
        self.inScript = False
        self.productInfoHash = {}
        self.productInfoHash["smallImage"] = []
        self.productInfoHash["largeImage"] = []

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.inNote = False
        self.inSKU = False
        self.inScript = False
        self.productInfoHash = {}
        self.productInfoHash["smallImage"] = []
        self.productInfoHash["largeImage"] = []

        self.imageMatcher = re.compile('pImgs\[[0-9]*\]\[\'[^\']*\']\[\'[p0-9]\'\] = [^\']*\'[^\']*\'')
        self.imageUrlMatcher = re.compile('\[.*\]\[\'(.*)\'\]\[\'(.*)\'\] = [^\']*\'(http://[^\']*)\'');

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for name, value in attrs:
                if name == 'class' and value == 'note':
                    self.inNote = True
        elif tag == 'span':
            for name, value in attrs:
                if name == 'id' and value == 'sku':
                    self.inSKU = True
        elif tag == 'script':
            self.inScript = True

    def handle_endtag(self, tag):
        if tag == 'p':
            self.inNote = False
        elif tag == 'span':
            self.inSKU = False
        elif tag == 'script':
            self.inScript = False

    def processImages(self, data):
        imagesInfo = self.imageMatcher.findall(data)
        if imagesInfo > 0:
            for imageInfo in imagesInfo:
                m = self.imageUrlMatcher.search(imageInfo)
                index = 0
                if m.group(2) != 'p':
                    index = int(m.group(2))

                if m.group(1) == 'MULTIVIEW_THUMBNAILS':
                    self.productInfoHash["smallImage"].append(m.group(3))
                     #print "DEBUG: smallImage %s" % m.group(3)
                elif m.group(1) == '4x':
                    self.productInfoHash["largeImage"].append(m.group(3))
                elif m.group(1) == 'MULTIVIEW':
                    if index == 0:
                        self.image = m.group(3)
                    
            
    def handle_data(self, data):
        if self.inNote:
            self.productInfoHash["color"] = data
        elif self.inSKU:
            self.productInfoHash["sku"] = data
        elif self.inScript:
            self.processImages(data);

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

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
            
        parser = sixpmDetailParser()
        parser.feed(html)

        index = 0
        for key in parser.productInfoHash:
            print "%s" % key
            if key == 'smallImage':
                print "\tsmallImage"
                for image in parser.productInfoHash["smallImage"]:
                    print "\t\t%s" % image
            elif key == 'largeImage':
                print "\tlargeImage"
                for image in parser.productInfoHash["largeImage"]:
                    print "\t\t%s" % image
            else:
                print "\t%s" % parser.productInfoHash[key]
