#!/usr/bin/python

import json
import glob
import sys

def load_json(filename, productHash):
    decoder = json.JSONDecoder()
    filehd=open(filename, "r")
    filecontent = filehd.read()
    filehd.close()
    fileobj = decoder.decode(filecontent)
    for obj in fileobj:
        productHash[obj] = fileobj[obj]

def printDetailWeb(productInfo, productIndex):
    filename = "../html/product.%d.html" % productIndex
    output=open(filename, "w")

    html = '<!doctype html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="shortcut icon" href="/favicon.ico" type="image/ico" />
<link rel="stylesheet" href="./main.p.css" type="text/css" media="all" />
<link rel="stylesheet" href="./matinee.p.css" type="text/css" media="all" />
<style type="text/css" media="screen">
a.zph:link {color:#369; text-decoration:none;}
a.zph:visited {color:#369; text-decoration:none;}
a.zph:hover {color:#369; text-decoration:underline;}
</style>
</head>
<body>
<div id="wrap">
<div id="content" class="productPage theater clearfix">
<div id="theater" class="clearfix" itemscope itemtype="http://schema.org/Product">
<div id="productStage">
<h1 class="title">%s %s</h1>
<div id="prdImage" class="stageItem clearfix stageFirstItem">
<div id="detailImageWrap" class="clearfix">
<div id="detailImage">
<img src="../images/%d.1.jpg" class="zoomHover gae-click*Product-Page*Zoom-In*Image-Click" /> </div>
</div>
<div id="productImages" class="frontrow">
<div id="frontrowSpotlight" class="frSpotlight"></div>
<div id="frontrowActive" class="frSpotlight"></div>
<ul>' % (productInfo["brand"], productInfo["product"], productIndex)

    imageIndex = 0
    for image in productInfo['smallImage']:
        imageIndex = imageIndex + 1
        html1 = '<li><a href="%d.2.%d.jpg"><span><img src="" itemprop="image" class="gae-click*Product-Page*PrImage*Thumbnail-Swap-Click" /></span></a></li>' % (productIndex, imageIndex)
        html += html1

    html2 = '</ul></div></div><div id="prdInfo" class="stageItem clearfix "><div id="prdInfoText" class="prdText"><h2 class="hc">产品信息</h2>
<div class="description" itemprop="description"><ul><li>商品号: %d</li></ul></div></div></div></div></div></div></body>' % productIndex
    html += html2
    output.write(html)
    output.close()

def printMainWeb(productInfo, productIndex)
    if productIndex % 

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: %s dirname" % sys.argv[0]
    else:
        productHash = {}
        dirname = sys.argv[1]
        dirPattern = "%s/*.json" % dirname
        filenames=glob.glob(dirPattern)
        for filename in filenames:
            load_json(filename, productHash)

        productIndex = 0
        for url in productHash:
            productIndex = productIndex + 1
            printDetailWeb(productHash[url], productIndex)
            printMainWeb(productHash[url], productIndex)
            printImageFetchShell(productHash[url], productIndex)
