# Scrapy settings for leboncoin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'leboncoin'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['leboncoin.spiders']
NEWSPIDER_MODULE = 'leboncoin.spiders'
DEFAULT_ITEM_CLASS = 'leboncoin.items.LeboncoinItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

