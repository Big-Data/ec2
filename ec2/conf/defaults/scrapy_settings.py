import os


#TRACK_REFS = True
#MEMDEBUG_ENABLED = True        # enable memory debugging

KEEP_ALIVE = True
CONCURRENT_ITEMS= 640 if os.name=='posix' else 128
RETRY_TIMES = 1 
REDIRECT_MAX_TIMES = 3

CONCURRENT_REQUESTS_PER_SPIDER = 8 if os.name=='posix' else 2
CONCURRENT_SPIDERS = 8 if os.name=='posix' else 2


DOWNLOAD_DELAY = 0
DOWNLOADER_HTTPCLIENTFACTORY = 'ec2.scrapy.http11.HTTP11ClientFactory'


EXTENSIONS = {
    'scrapy.contrib.corestats.CoreStats': None,
    'scrapy.webservice.WebService': None,
    'scrapy.telnet.TelnetConsole': None,
    'scrapy.contrib.memusage.MemoryUsage': None,
    'scrapy.contrib.memdebug.MemoryDebugger': None,
    'scrapy.contrib.closespider.CloseSpider': None,
    'scrapy.contrib.feedexport.FeedExporter': None,
    'scrapy.contrib.spidercontext.SpiderContext': None,
}


SCHEDULER_MIDDLEWARES ={
    'scrapy.contrib.schedulermiddleware.duplicatesfilter.DuplicatesFilterMiddleware': None,
}

SPIDER_MIDDLEWARES = {
    #'scrapy.contrib.spidermiddleware.httperror.HttpErrorMiddleware': 50,
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': None,
    #'scrapy.contrib.spidermiddleware.urllength.UrlLengthMiddleware': 800,
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': None,
}


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': None,
    #'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': None,
    #'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': None,
    'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': None,
    'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': None,
    'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': None,
    
     #---------------
    'ec2.scrapy.middleware.domains.DomainsMiddleware': 101,
#    'ec2.scrapy.middleware.transferencode.HttpTransferEncodingMiddleware': 799,

    'ec2.scrapy.middleware.retry.RetryExMiddleware': 501,
#    'ec2.scrapy.middleware.redirect.RedirectExMiddleware': 600,
    'ec2.scrapy.middleware.comment.RefererMiddleware': 700,
    'ec2.scrapy.middleware.xhr.XhrMiddleware': 705,
    'ec2.scrapy.middleware.cookies.CookiesMiddleware': 710,
    'ec2.scrapy.middleware.httpproxy.HttpProxyMiddleware': 751,
    'ec2.scrapy.middleware.httpcompression.HttpCompressionExMiddleware': 800,
}

DOWNLOADER_STATS = False

#DUPEFILTER_CLASS = 'scrapy.contrib.dupefilter.NullDupeFilter'

SQLITE_DB = ':memory:'

TELNETCONSOLE_ENABLED = 0
WEBSERVICE_ENABLED = False

#COOKIES_DEBUG = True
#SPIDER_CLOSE_DELAY = 180


USER_AGENT =  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1'


#from ec2.conf.sina.default_settings import *


#LOG_FILE = 'taobao_shop3.out'


