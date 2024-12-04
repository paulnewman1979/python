#!/usr/local/bin/python

import urllib
from html.parser import HTMLParser
import sys
from html.entities import entitydefs

class bradsParser(HTMLParser):
    inDealBox = False
    inProdImage = False
    inPostText = False
    inDealContent = False
    ACount = 0
    inStrong = False

    url = ''
    title = ''
    promo_hash = {}
    prodImage = ''

    def __init__(self):
        self.promo_hash = {}
        HTMLParser.__init__(self)
    
        self.inTitle = False

    def handle_starttag(self, tag, attrs):
        url=''

        if tag == 'img':
            for name, value in attrs:
                if name == 'class' and value != 'base-image bd-image':
                    self.prodImage = None
                elif name == 'src':
                    self.prodImage = value
        elif tag == 'a':
            for name, value in attrs:
                if name == 'class' and value != '__nl text-gray-dark':
                    self.url = None
                elif name == 'href':
                    self.url = value
        elif tag == 'h3':
            for name, value in attrs:
                if name == 'class' and value == 'd-block mt-1 mb-4 line-clamp-3 display-4':
                    self.inTitle = True

    def handle_data(self, data):
        if self.inTitle:
            self.title += data
            self.promo_hash[self.title] = []
            self.promo_hash[self.title].append(self.url)
            self.promo_hash[self.title].append(self.prodImage)
            self.title = ""
            self.inTitle = False


    def handle_entityref(self, name):
        if entitydefs.has_key(name):
            self.handle_data(entitydefs[name]) 
        else: 
            self.handle_data('&'+name+';') 

if __name__ == '__main__':
    # reload(sys)
    # sys.setdefaultencoding('utf8')

    if len(sys.argv) < 2:
        print('usage: ', sys.argv[0], ' filename')
    else:
        filename = sys.argv[1]
        input = open(filename, 'r')
        html = input.read()
        input.close()
            
        parser = bradsParser()
        parser.feed(html)
        for title in parser.promo_hash:
            print('deal: %s\t%s\t%s' % (title, parser.promo_hash[title][0], parser.promo_hash[title][1]))

