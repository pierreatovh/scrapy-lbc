from scrapy.spider      import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector    import HtmlXPathSelector
from leboncoin.items    import LeboncoinItem

#class LeBonCoinSpider(CrawlSpider):
class LeBonCoinSpider(BaseSpider):
    name = "leboncoin"
    allowed_domains = ["www.leboncoin.fr"]
    # we could use CrawlSpider, but result is not digestable... better generating last X urls
    categories = ['ameublement','decoration']
    start_urls= []
    for category in categories:
        for i in range(1,30):
            start_urls.append('http://www.leboncoin.fr/'+category+'/offres/nord_pas_de_calais/?o='+str(i))

    #start_urls = [
#   rules = (
#       # Extract links matching 'category.php' (but not matching 'subsection.php')
#       # and follow links from them (since no callback means follow=True by default).
#       #Rule(SgmlLinkExtractor(allow=('\?o=', ), deny=('subsection\.php', ))),
#       #Rule(SgmlLinkExtractor(allow=('\?o=', )), callback='parse_item',follow=True),
#       Rule(SgmlLinkExtractor(allow=('\?o=', )), callback='parse_item',follow=False),

#       # Extract links matching 'item.php' and parse them with the spider's method parse_item
#       #Rule(SgmlLinkExtractor(allow=('item\.php', )), callback='parse_item'),
#   )


#   def parse_item(self, response):
    def parse(self, response):
#	put in filename
#        filename = response.url.split("/")[-2]
#        open(filename, 'wb').write(response.body)
        hxs     = HtmlXPathSelector(response)
        ads     = hxs.select('//div[@class="list-ads"]/a')
        items   = []
        for ad in ads:
            item = LeboncoinItem()
            item['name']    = ad.select('div[@class="ad-lbc"]/div[@class="detail"]/div[@class="title"]/text()').re('^\s*([\w\s]+\w)\s*')
            item['photo']   = ad.select('div[@class="ad-lbc"]/div[@class="image"]/div[@class="image-and-nb"]/img/@src').extract()
            item['url']     = ad.select('@href').extract()
            self.log(item['name'])
            #print item['name'],':' ,item['photo'],'--->', item['url']
            html = '<div><div style="width:150px;height:250px;float:left;text-align:center">\
            <img src="%s" alt="" /><br />\
            <p><a href="%s">%s</a></p>\
            </div></div>' % (''.join(item['photo']), ''.join(item['url']), ''.join(item['name']) )

            #print photo
            items.append(item)
            #	put in filename
            filename = response.url.split("/")[-4]
            open('/tmp/lbc/'+filename+'.html', 'a').write(html)
        return items
