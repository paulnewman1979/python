#!/usr/bin/perl

use warnings;
use strict;

my $line;
my $product;
my $image;
my $delPrice;
my $price;

my %product_hash;
my %url_hash;
my %schema_hash;

my $curIndex = 0;
my $count;
my $index;

my $page_index = 1;
my $html_count = 0;

my $file = $ARGV[0];

open(FILE, "../conf/index.conf");
while ($line=<FILE>) {
    chomp $line;
    if ($line ne "") {
        $curIndex = $line;
    }
}
close(FILE);

$count = 0;
open(FILE, "../data/result.txt");
while ($line=<FILE>) {
    $count ++;
}
close(FILE);
$count = $count / 5;
my $pageTotal = int($count / 40) + 1;

open(OUT, ">../conf/index.mapping.new.csv");
open(OUTSH, "> ../images/download.sh");

$count = 0;
open(FILE, "../data/result.txt");
while ($line=<FILE>) {
    chomp $line;
    $count ++;
    $line=~s/^\t//g;

    if ($count % 5 == 1) {
        $product = $line;
    } elsif ($count % 5 == 2) {
        $image = $line;
    } elsif ($count % 5 == 3) {
        $price = $line;
        $price=~s/,//g;
    } elsif ($count % 5 == 4) {
        $delPrice = $line;
        $delPrice=~s/,//g;
    } elsif ($count % 5 == 0) {
        $url = $line;

        if (exists($product_hash{$product})) {
            print STDERR "DEBUG: duplicate product $product\n";
        } elsif (exists($url_hash{$url})) {
            print STDERR "DEBUG: duplicate url $url\n";
        } else {
            ++ $curIndex;
            print OUT "$curIndex,$product,$image,$price,$delPrice,$url\n";
            print_html($curIndex, $product,$price);
            print_download($curIndex, $image);
            if ($count % 50 == 0) {
                print OUTSH "wait\n";
            }
        }
    }
}
close(FILE);

close(OUT);
close(OUTSH);
close(OUTHTML);

sub print_download {
    my $index = shift;
    my $image = shift;
    print OUTSH "curl \"$image\" > $curIndex.jpg &\n"
}

sub print_head {
    my $header='<!DOCTYPE html>
<html class="no-js" lang="en">
<head>
<product>Coach</product>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="generator" content="JACPKMALPHTCSJDTCR" />
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<meta name="format-detection" content="telephone=no" />
<link href="css/base.css" type="text/css" rel="stylesheet">
<link href="css/min.css" type="text/css" rel="stylesheet"/>
<link href="css/browse.css" rel="stylesheet" type="text/css" />
<link href="css/browse.grid.css" rel="stylesheet" type="text/css" />
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width" />
<product>Coach</product>
</head>
<div id="doc3">
<a name="top"></a>
<div id="bd">
<div class="row">
<div class="small-12 columns">
<div id="GlobalLayout">
<div id="search_landing_product">
<ul class="thumbnails large-block-grid-5" data-thumb-cat="cat">
<!-- header footer-->';
    print OUTHTML "$header\n";
}

sub print_tail {
    my $page_index = shift;
    my $tail1 = '<!-- tail footer-->
</ul>
</div>
<div class="filters">
<div class="pagination ">
<span class="pageText">Page</span>';
    my $tail2 = '
</div>
</div>
</div>
<br class="clearboth"/>
</div>
<div class="hidden">
<div class="hd">&nbsp;</div>
<div class="bd" id="quickViewbody">
<div class="right">
<div id="qvAddToBagValidateMsgBox">
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</div>
</body>
</html>';
    print OUTHTML "$tail1\n";

    my $cur_index;
    if ($page_index > 2) {
        $cur_index = $page_index - 2;
        print OUTHTML "<a href=\"$cur_index.html\">$cur_index</a>\n";
    }
    if ($page_index > 1) {
        $cur_index = $page_index - 1;
        print OUTHTML "<a href=\"$cur_index.html\">$cur_index</a>\n";
    }
    print OUTHTML "<span class=\"currentPage\">$page_index</span>\n";
    $cur_index = $page_index + 1;
    if ($cur_index <= $pageTotal) {
        print OUTHTML "<a href=\"$cur_index.html\">$cur_index</a>\n";
    }
    $cur_index = $page_index + 2;
    if ($cur_index <= $pageTotal) {
        print OUTHTML "<a href=\"$cur_index.html\">$cur_index</a>\n";
    }

    print OUTHTML "$tail2\n";
}

sub cal_price {
    my $price = shift;
    $price=~s/\$//g;

    my $new_price = $price * 1.0875 * 6.6;
    $new_price = int($new_price/10) * 10;
    $new_price += 500;

    return $new_price;
}

sub print_item {
    my $index = shift;
    my $product = shift;
    my $price = shift;

    my $new_price = cal_price($price);

    print OUTHTML "<li class=\"productThumbnail borderless\">\n";
    print OUTHTML "  <div class=\"innerWrapper\">\n";
    print OUTHTML "    <div class=\"fullColorOverlayOff\">\n";
    print OUTHTML "      <a href=\"about:blank\" style=\"display:block;width:170px;height:208px;\" class=\"imageLink productThumbnailLink absolutecrossfade\">\n";
    print OUTHTML "        <span id=\"main_images_holder_2688518_0_cat\">\n";
    print OUTHTML "          <img class=\"thumbnailImage crossfadeImage thumbnailMainImage\" src=\"images/$index.jpg\" name=\"CATimage\" border=\"0\" >\n";
    print OUTHTML "        </span>\n";
    print OUTHTML "      </a>\n";
    print OUTHTML "      <div class=\"overlayImgBox jumbo_Swatch_without_flexibleIcon color-swatches-overlay\" id=\"overlayImgBox_2688518_0_cat\"></div>\n";
    print OUTHTML "      <div class=\"offers crossfadeOffers\"></div>\n";
    print OUTHTML "    </div>\n";
    print OUTHTML "    <div class=\"shortDescription\">\n";
    print OUTHTML "      <a href=\"about:blank\" class=\"productThumbnailLink\">$product</a>\n";
    print OUTHTML "    </div>\n";
    print OUTHTML "    <div class=\"prices\">\n";
    print OUTHTML "      <span class=\"priceSale\">价格: ¥$new_price</span><br/>\n";
    print OUTHTML "      <span class=\"price\">编号: $index</span>\n";
    print OUTHTML "    </div>\n";
    print OUTHTML "  </div>\n";
    print OUTHTML "</li>\n";
}

sub print_html {
    my $index = shift;
    my $product = shift;
    my $price = shift;

    $html_count ++;  
    if ($html_count == 1) {
        #print html start
        open(OUTHTML, ">../result/$page_index.html");
        print_head();
        print_item($index, $product, $price);
    } elsif ($html_count == 40) {
        #print html end
        print_item($index, $product, $price);
        print_tail($page_index);
        close(OUTHTML);
        $page_index ++;
        $html_count = 0;
    } else {
        #print body
        print_item($index, $product, $price);
    }
}

