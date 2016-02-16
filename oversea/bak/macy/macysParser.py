#!/usr/bin/python

import re
import json
import urllib
import HTMLParser
import sys
from htmlentitydefs import entitydefs

class macysParser(HTMLParser.HTMLParser):
    inScript = False
    inWrapper = False
    idColorPicHash = {}
    id = ""
    tmpid = ""
    inPriceSpan = False
    inPrice = False
    depthPrice = 0
    depthWrapper = 0
    prices = []
    idHash = {}
    inInput = 0
    discount = 0
    inBadge = False

    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
    
        self.inScript = False
        self.inWrapper = False
        self.idColorPicHash = {}
        self.id = ""
        self.tmpid = ""
        self.inPrice = False
        self.inPriceSpan = False
        self.prices = []
        self.depthWrapper = 0
        self.depthPrice = 0
        self.idHash = {}
        self.inInput = 0
        self.discount = 0
        self.inBadge = False

    def handle_starttag(self, tag, attrs):
        url=""

        if tag == 'script':
            self.inScript = True
        elif tag == 'li':
            for name, value in attrs:
                if name == 'id':
                    self.tmpid = value
                elif name == 'class' and value == 'productThumbnail borderless':
                    self.id = self.tmpid
                    self.idHash[self.id] = []
                    self.prices = []
        elif tag == 'div':
            if self.inWrapper:
                self.depthWrapper = self.depthWrapper + 1 
            else:
                for name, value in attrs:
                    if name == 'class':
                        if value == 'innerWrapper':
                            self.inWrapper = True
                            self.inInput = 1
                            self.depthWrapper = 1

            if self.inPrice:
                self.depthPrice = self.depthPrice + 1
            else:
                for name, value in attrs:
                    if name == 'class' and value == 'prices':
                        self.inPrice = True
                         #print "entering inPrice"
                        self.depthPrice = 1

            for name, value in attrs:
                if name == 'class' and value == 'hidden badgeJSON':
                     #print "entering badge"
                    self.inBadge = True
        elif tag == 'span':
            if self.inPrice:
                 #print "entering inPriceSpan"
                self.inPriceSpan = True
        elif tag == 'input':
            if self.inInput == 1:
                self.inInput = 0
                for name, value in attrs:
                    if name == 'value':
                         #print "id:url\t%s\t%s" % (self.id, value)
                        self.url = value
                        if len(self.idHash[self.id]) == 0:
                            self.idHash[self.id].append([])
                        self.idHash[self.id].append(self.url)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.inScript = False
        elif tag == 'div':
            if self.inPrice:
                self.depthPrice = self.depthPrice - 1
                if self.depthPrice == 0:
                     #if len(self.idHash[self.id]) == 1:
                         #self.idHash[self.id].append([]);
                     #for price in self.prices:
                         #print "id:price\t%s -> %s" % (self.id, price)
                    self.idHash[self.id].append(self.prices)
                     #print "leaving inPrice"
                    self.inPrice = False

            if self.inWrapper:
                self.depthWrapper = self.depthWrapper - 1
                if self.depthWrapper == 0:
                    self.inWrapper = False

            if self.inBadge:
                 #print "leaving badge"
                self.inBadge = False
        elif tag == 'span':
            if self.inPriceSpan:
                 #print "leaving inPriceSpan"
                self.inPriceSpan = False
            
    def process_image_map(self, image_map):
        decoder = json.JSONDecoder()
        #print "image_map = %s" % image_map
        image_map_obj = decoder.decode(image_map);
        for item in image_map_obj:
            for id in item:
                value = item[id]
                for color in value:
                    key = "%s:%s" % (id, color)
                    picUrl = value[color]
                    self.idColorPicHash[key] = picUrl
                     #print "map color:image\t%s -> %s" % (key, picUrl)

    def process_color_map(self, color_map):
        decoder = json.JSONDecoder()
        color_map_obj = decoder.decode(color_map)
        color_family = color_map_obj["colorFamily"]
        colors = []
        for color in color_family:
            colors.append(color)
            key = "%s:%s" % (self.id, color)
             #print "id:color\t%s -> %s" % (self.id, color)
        self.idHash[self.id].append(colors)

    def handle_comment(self, data):
        if self.inBadge:
            extra_match = re.compile("EXTRA 20%")
            extra_result = extra_match.findall(data)
            if len(extra_result) > 0:
                self.discount = 1
            else:
                self.discount = 0
             #print "id:discount\t%s -> %i" % (self.id, self.discount)
            self.idHash[self.id].append(self.discount)

    def handle_data(self, data):
         #print "data = %s" % data
        color_match = re.compile("MACYS.colorwayPrimaryImages = '[^']*'")
        json_match = re.compile("\[.*\]")
        colorFamily_match = re.compile("colorFamily")
        if self.inPriceSpan:
            self.prices.append(data)
        elif self.inScript:
            # hidden image mapping from color to url
            image_list = color_match.findall(data)
            if len(image_list) > 0:
                image_list = json_match = json_match.findall(data)
                self.process_image_map(image_list[0])
            else:
                colorFamilyList = colorFamily_match.findall(data)
                if len(colorFamilyList) > 0:
                    self.process_color_map(data) 
        
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
            
        parser = macysParser()
        parser.feed(html)

        nowprice_match = re.compile("Now $[0-9.]*")
        origprice_match = re.compile("Orig. $[0-9.]*")
        regprice_match = re.compile("Reg. $[0-9.]*")
        saleprice_match = re.compile("Sale. $[0-9.]*")
        price_match = re.compile("[0-9]+\.[0-9]+")
        
        index = 0
        for id in parser.idHash:
            colors = parser.idHash[id][0]
            url = parser.idHash[id][1]
            prices = parser.idHash[id][2]
            discount = parser.idHash[id][3]

            urlHash = {}
            realurl = "http://slimages.macysassets.com/is/image/MCY/products/%s_fpx.tif" % url
            realurl.rstrip()
            urlHash[realurl] = 1
            for price in prices:
                results = nowprice_match.findall(price)
                if len(results) > 0:
                    realprice = price_match.findall(price)
                    break
                results = saleprice_match.findall(price)
                if len(results) > 0:
                    realprice = price_match.findall(price)
                    break
                results = price_match.findall(price)
                if len(results) > 0:
                    realprice = price_match.findall(price)
                    break
            print "%s\t%s\t%s" % (realurl, realprice[0], discount)

            if len(colors) > 0:
                for color in colors:
                    key = "%s:%s" % (id, color)
                    if key in parser.idColorPicHash:
                        url = parser.idColorPicHash[key]
                    else:
                        continue
                    realurl = "http://slimages.macysassets.com/is/image/MCY/products/%s" % url
                    realurl.rstrip()
                    if realurl not in urlHash:
                        urlHash[realurl] = 1
                        print "%s\t%s\t%s" % (realurl, realprice[0], discount)


            '''
            print "\turl: http://slimages.macysassets.com/is/image/MCY/products/%s_fpx.tif" % url
            print "\tdiscount: %d" % discount

            if len(colors) > 0:
                for color in colors:
                    key = "%s:%s" % (id, color)
                    #print "key %s" % key
                    if key in parser.idColorPicHash:
                        url = parser.idColorPicHash[key]
                        print "\tcolor2url: http://slimages.macysassets.com/is/image/MCY/products/%s" % url
            for price in prices:
                print "\tprice: %s" % price
            '''
