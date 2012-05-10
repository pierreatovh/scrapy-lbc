#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Rolando Espinoza La fuente
#
# Changelog:
#     24/07/2011 - updated to work with scrapy 13.0dev
#     25/08/2010 - initial version. works with scrapy 0.9

from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider


class LeboncoinItem(Item):
    # define the fields for your item here like:
    # name = Field()

     name     = Field()
     photo    = Field()
     url      = Field()
     category = Field()


class LeboncoinSpider(BaseSpider):
    name = "leboncoin"
    allowed_domains = ["www.leboncoin.fr"]
    # we could use CrawlSpider, but result is not digestable... better generating last X urls
    categories = ['ameublement','decoration']
    start_urls= []
    for category in categories:
        for i in range(1,30):
            start_urls.append('http://www.leboncoin.fr/'+category+'/offres/nord_pas_de_calais/?o='+str(i))

    def parse(self, response):
      # hxs     = HtmlXPathSelector(response)
      # ads     = hxs.select('//div[@class="list-ads"]/a')
      # items   = []
      # for ad in ads:
      #     item = LeboncoinItem()
      #     item['name']    = ad.select('div[@class="ad-lbc"]/div[@class="detail"]/div[@class="title"]/text()').re('^\s*([\w\s]+\w)\s*')
      #     item['photo']   = ad.select('div[@class="ad-lbc"]/div[@class="image"]/div[@class="image-and-nb"]/img/@src').extract()
      #     item['url']     = ad.select('@href').extract()

           # self.log(item['name'])
            #print item['name'],':' ,item['photo'],'--->', item['url']
           #html = '<div><div style="width:150px;height:250px;float:left;text-align:center">\
           #<img src="%s" alt="" /><br />\
           #<p><a href="%s">%s</a></p>\
           #</div></div>' % (''.join(item['photo']), ''.join(item['url']), ''.join(item['name']) )

           ##print photo
           #items.append(item)
           ##   put in filename
           #filename = response.url.split("/")[-4]
           #open('/tmp/lbc/'+filename+'.html', 'a').write(html)
        #return items
        #yield items
        hxs = HtmlXPathSelector(response)
        for qxs in hxs.select('//div[@class="list-ads"]/a'):
            loader = XPathItemLoader(LeboncoinItem(), selector=qxs)
            loader.add_xpath('name'      ,  'div[@class="ad-lbc"]/div[@class="detail"]/div[@class="title"]/text()', re='^\s*([\w\s]+\w)\s*' )
            loader.add_xpath('photo'     ,  'div[@class="ad-lbc"]/div[@class="image"]/div[@class="image-and-nb"]/img/@src' )
            loader.add_xpath('url'       ,  '@href' )
            loader.add_value('category'  ,  response.url.split("/")[-4]  )

            yield loader.load_item()


def printItem(item):
    filename = ''.join(item['category'])
    # we don't care in fact
    #try:
    #    open(filename+'.html')
    #except IOError as e:
    #    # need to write header in file
    # we don't care in fact
    html = '<div><div style="width:150px;height:250px;float:left;text-align:center">\
    <img src="%s" alt="" /><br />\
    <p><a href="%s">%s</a></p>\
    </div></div>' % (''.join(item['photo']), ''.join(item['url']), ''.join(item['name']) )
    open(filename+'.html', 'a').write(html)


        
    


def main():
    """Setups item signal and run the spider"""
    # set up signal to catch items scraped
    from scrapy import signals
    from scrapy.xlib.pydispatch import dispatcher

    items = []

    def catch_item(sender, item, **kwargs):
        print "Got:", item
        items.append(item)
        printItem(item)

    dispatcher.connect(catch_item, signal=signals.item_passed)

    # shut off log
    from scrapy.conf import settings
    settings.overrides['LOG_ENABLED'] = False

    # set up crawler
    from scrapy.crawler import CrawlerProcess

    crawler = CrawlerProcess(settings)
    crawler.install()
    crawler.configure()

    # schedule spider
    crawler.crawl(LeboncoinSpider())

    # start engine scrapy/twisted
    print "STARTING ENGINE"
    crawler.start()
    print "ENGINE STOPPED"

    #printHTML(items)
    

if __name__ == '__main__':
    main()
