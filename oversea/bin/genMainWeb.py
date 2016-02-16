#!/usr/bin/python
# coding=utf-8

import json
import glob
import sys

def calPrice(price):
    cur_price = float(price)
    add_price = 400
    if cur_price < 30.0:
        add_price = 150
    elif cur_price < 50.0:
        add_price = 200
    elif cur_price < 100:
        add_price = 300
    new_price = float(price) * 1.0875 * 6.6;
    new_price = int(new_price/10) * 10;
    new_price = new_price + add_price
    return new_price;

def genMainWebHead(output, pageIndex, pageSize):
    output.write('<!DOCTYPE html>\n')
    output.write('<html class="no-js" lang="en">\n')
    output.write('<head>\n')
    output.write('<title>Coach</title>\n')
    output.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
    output.write('<meta http-equiv="generator" content="JACPKMALPHTCSJDTCR" />\n')
    output.write('<meta http-equiv="X-UA-Compatible" content="IE=edge" />\n')
    output.write('<meta name="format-detection" content="telephone=no" />\n')
    output.write('<link href="css/base.css" type="text/css" rel="stylesheet">\n')
    output.write('<link href="css/min.css" type="text/css" rel="stylesheet"/>\n')
    output.write('<link href="css/browse.css" rel="stylesheet" type="text/css" />\n')
    output.write('<link href="css/browse.grid.css" rel="stylesheet" type="text/css" />\n')
    output.write('<meta charset="utf-8" />\n')
    output.write('<meta name="viewport" content="width=device-width" />\n')
    output.write('<title>Coach</title>\n')
    output.write('</head>\n')
    output.write('<div id="doc3">\n')
    output.write('<a name="top"></a>\n')
    output.write('<div id="bd">\n')
    output.write('<div class="row">\n')
    output.write('<div class="small-12 columns">\n')
    output.write('<div id="GlobalLayout">\n')
    output.write('<div id="search_landing_product">\n')
    output.write('<div class="pagination "><span class="pageText"></span>')
    if pageIndex > 2:
        curIndex = pageIndex - 2
        line = "<a href=\"%d.html\">%d</a>\n" % (curIndex, curIndex)
        output.write(line)
    if pageIndex > 1:
        curIndex = pageIndex - 1
        line = "<a href=\"%d.html\">%d</a>\n" % (curIndex, curIndex)
        output.write(line)
    line = "<span class=\"currentPage\">%d</span>\n" % pageIndex
    output.write(line)
    curIndex = pageIndex + 1
    if curIndex <= pageSize:
        line = "<a href=\"%d.html\">%d</a>\n" % (curIndex, curIndex)
        output.write(line)
    curIndex = pageIndex + 2
    if curIndex <= pageSize:
        line = "<a href=\"%d.html\">%d</a>\n" % (curIndex, curIndex)
        output.write(line)
    output.write('</div>\n')
    output.write('<ul class="thumbnails large-block-grid-3" data-thumb-cat="cat">\n')
    output.write('<!-- header footer-->\n')

def genMainWebTail(output):
    output.write('<!-- tail footer--></ul></div><div class="filters">')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('<br class="clearboth"/>\n')
    output.write('</div>\n')
    output.write('<div class="hidden">\n')
    output.write('<div class="hd">&nbsp;</div>\n')
    output.write('<div class="bd" id="quickViewbody">\n')
    output.write('<div class="right">\n')
    output.write('<div id="qvAddToBagValidateMsgBox">\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</div>\n')
    output.write('</body>\n')
    output.write('</html>\n')

def genMainWeb(output, productInfo, productIndex):
    output.write("<li class=\"productThumbnail borderless\">\n")
    output.write("  <div class=\"innerWrapper\">\n")
    output.write("    <div class=\"fullColorOverlayOff\">\n")
    line = "      <a href=\"./images/%d.jpg\" style=\"display:block;width:208px;height:208px;\" class=\"imageLink productThumbnailLink absolutecrossfade\">\n" % productIndex
    output.write(line)
    output.write("        <span id=\"main_images_holder_2688518_0_cat\">\n")
    line = "          <img class=\"thumbnailImage crossfadeImage thumbnailMainImage\" src=\"images/%d.jpg\" name=\"CATimage\" border=\"0\" >\n" % productIndex
    output.write(line)
    output.write("        </span>\n")
    output.write("      </a>\n")
    output.write("      <div class=\"overlayImgBox jumbo_Swatch_without_flexibleIcon color-swatches-overlay\" id=\"overlayImgBox_2688518_0_cat\"></div>\n")
    output.write("      <div class=\"offers crossfadeOffers\"></div>\n")
    output.write("    </div>\n")
    output.write("    <div class=\"shortDescription\">\n")
    line = "      <a href=\"about:blank\" class=\"productThumbnailLink\">%s</a>\n" % productInfo["product"]
    output.write(line)
    output.write("    </div>\n")
    output.write("    <div class=\"prices\">\n")
    newPrice = calPrice(productInfo["price"])
    line = "      <span class=\"priceSale\">价格: ¥%d</span><br/>\n" % newPrice
    output.write(line)
    line = "      <span class=\"price\">编号: %d</span>\n" % productIndex
    output.write(line)
    output.write("    </div>\n")
    output.write("  </div>\n")
    output.write("</li>\n")


def load_json(filename, productHash):
    decoder = json.JSONDecoder()
    filehd=open(filename, "r")
    filecontent = filehd.read()
    filehd.close()
    fileobj = decoder.decode(filecontent)
    for obj in fileobj:
        productHash[obj] = fileobj[obj]

def load_product_index_hash(filename, productIndexHash):
    decoder = json.JSONDecoder()
    filehd = json.JSONDecoder()
    filecontent = filehd.read()
    filehd.close()
    for obj in fileobj:
        productIndexHash[obj] = fileobj[obj]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: %s dirname product" % sys.argv[0]
    else:
        productHash = {}
        dirname = sys.argv[1]
        product = sys.argv[2]
        dirPattern = "%s/*.json" % dirname
        filenames=glob.glob(dirPattern)
        for filename in filenames:
            print "DEBUG: processing %s" % filename
            load_json(filename, productHash)

        productSize = 0
        for url in productHash:
            if productHash[url]["soldout"] == 1:
                continue
            productSize = productSize + 1
        pageSize = (productSize + 8) / 9
        productIndex = 0
        pageIndex = 0
        outputShell = open("image.copy.sh", "w");
        for url in productHash:
            if productHash[url]["soldout"] == 1:
                continue
            productIndex = productIndex + 1
            line = "cp %s ../result/images/%d.jpg\n" % (productHash[url]["image"], productIndex)
            outputShell.write(line)
            if productIndex % 9 == 1:
                pageIndex = pageIndex + 1
                filename = "../result/%d.html" % pageIndex
                output = open(filename, "w")
                genMainWebHead(output, pageIndex, pageSize)
                genMainWeb(output, productHash[url], productIndex)
            elif productIndex % 9 == 0:
                genMainWeb(output, productHash[url], productIndex)
                genMainWebTail(output)
                output.close()
            else:
                genMainWeb(output, productHash[url], productIndex)
        if productIndex % 9 != 0:
            genMainWebTail(output)
            output.close()
        outputShell.close()
