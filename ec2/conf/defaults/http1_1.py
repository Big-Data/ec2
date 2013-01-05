import os

KEEP_ALIVE = True
CONCURRENT_ITEMS= 640 if os.name=='posix' else 200
CONCURRENT_REQUESTS_PER_SPIDER = 128 if os.name=='posix' else 8
RETRY_TIMES = 1 
REDIRECT_MAX_TIMES = 3

DOWNLOADER_HTTPCLIENTFACTORY = 'ec2.scrapy.http11.HTTP11ClientFactory'

EXTENSIONS = {
    'scrapy.contrib.spidercontext.SpiderContext': None,
    'scrapy.webservice.WebService': None,
    'scrapy.telnet.TelnetConsole': None,

#    'scrapy.contrib.spiderclosedelay.SpiderCloseDelay': 0,
    
}

#SPIDER_MODULES = ['ec2.scrapy.taobao.shopspider']
SCHEDULER_MIDDLEWARES ={
    'scrapy.contrib.schedulermiddleware.duplicatesfilter.DuplicatesFilterMiddleware': None,
}

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.requestlimit.RequestLimitMiddleware': None,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None,

    'ec2.scrapy.middleware.domains.DomainsMiddleware': 101,
#    'ec2.scrapy.middleware.transferencode.HttpTransferEncodingMiddleware': 799,

    'ec2.scrapy.middleware.retry.RetryExMiddleware': 501,
    'ec2.scrapy.middleware.redirect.RedirectExMiddleware': 600,
    'ec2.scrapy.middleware.comment.RefererMiddleware': 700,
    'ec2.scrapy.middleware.httpproxy.HttpProxyMiddleware': 751,
    'ec2.scrapy.middleware.httpcompression.HttpCompressionExMiddleware': 800,
}


#DUPEFILTER_CLASS = 'scrapy.contrib.dupefilter.NullDupeFilter'

ITEM_PIPELINES =[
#    'ec2.scrapy.taobao.pipeline.shop.ShopPipeline',
]

TELNETCONSOLE_ENABLED = 0
WEBSERVICE_ENABLED = False

#COOKIES_DEBUG = True
#SPIDER_CLOSE_DELAY = 180


USER_AGENT =  'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3'

from ec2.conf.sina.default_settings import *


#LOG_FILE = 'taobao_shop3.out'

