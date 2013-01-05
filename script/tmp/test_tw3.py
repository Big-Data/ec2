import logging
logging.basicConfig(level=logging.DEBUG)

import time
from twisted.internet import defer, reactor
#from scrapy.xlib.pydispatch import dispatcher
from scrapy.crawler import Crawler, CrawlerProcess
from scrapy import log
from scrapy.http        import Request


from ec2    import signals
from ec2.redis import RedisDb
from ec2.scrapy.puller  import ChannelsPuller
from ec2.conf.enabled   import scrapy_conf

from ec2.scrapy.spider  import Spider
from ec2.utils  import event

log.start()
url = 'http://192.168.1.230:9090/test/slow_echo/%s'

def test_db():
    db = RedisDb(pre='MQ')


def test_cp():
    crawlerProcess = CrawlerProcess(scrapy_conf)
    crawlerProcess.install()
    crawlerProcess.configure()    

    crawlerProcess.queue.append_spider(myspider)
    crawlerProcess.start()

def _resp( sender, response):
    log.msg('%s|%s'%(sender, response,) )

def _requests(num):
    for i in xrange(num):
        _msg = '%s_%s'%(i,int(time.time()),)
        kwds = {
            'url':  url%_msg ,
            'meta': {},
            'dont_filter': True,
        }
        yield Request(**kwds)

def test_crawler():
    crawler = Crawler(scrapy_conf)
    crawler.install()
    crawler.configure()

    myspider = Spider(scrapy_conf)
    event.connect( _resp, signal=signals.RESPONSE, sender=event.Any)
    
    crawler.queue.spider_requests.append( (myspider, _requests(10)) )
    
    
    #crawler.queue.append_spider(myspider)
    
    crawler.start()
    reactor.run()





if __name__=='__main__':

    #puller.start()
    print "Starting crawler."
    test_crawler()
    print "Crawler stopped."


