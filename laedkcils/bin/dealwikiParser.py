#!/usr/bin/python

import urllib
from html.parser import HTMLParser
import sys
from html.entities import entitydefs

class dealwikiParser(HTMLParser):
    inDealBox = False
    inProdImage = False
    inPostText = False
    inDealContent = False

    url = ''
    title = ''
    promo_hash = {}

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.__init__(self)
    
        self.inDealBox = False
        self.inProdImage = False
        self.inPostText = False
        self.inDealContent = False
        self.inTitle = False

    def handle_starttag(self, tag, attrs):
        url=''

        if tag == 'a':
            for name, value in attrs:
                if name == 'class':
                    if value != 'product-image':
                        break;
                    else:
                        self.inDealBox = True
                elif name == 'producturl':
                    self.url = value
        elif tag == 'img':
            if self.inDealBox:
                for name, value in attrs:
                    if name == 'src':
                        self.prodImage = value
                    elif name == 'alt':
                        self.title = value
                        self.promo_hash[self.title] = []
                        self.promo_hash[self.title].append(self.url)
                        self.promo_hash[self.title].append(self.prodImage)
                        self.title = ''

    def handle_endtag(self, tag):
        if tag == 'a':
            if self.inDealBox:
                self.inDealBox = False

    def handle_data(self, data):
        return

    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print('usage: ', sys.argv[0], ' filename')
    else:
        filename = sys.argv[1]
        input = open(filename, 'r')
        html = input.read()
        input.close()
            
        parser = dealwikiParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print('deal: %s\t%s\t%s' % (title, parser.promo_hash[title][0], parser.promo_hash[title][1]))

