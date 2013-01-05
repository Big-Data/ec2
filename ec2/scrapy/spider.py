#coding=utf-8

import time,random

#from scrapy             import log

from scrapy.spider      import BaseSpider
from scrapy.utils.signal import send_catch_log_deferred

from ec2        import signals
from ec2.utils  import event

class Spider(BaseSpider):
    
    def __init__(self, settings):
        BaseSpider.__init__(self, name=settings.get('DEFAULT_SPIDER', 'default'))
        
        self._settings = settings
        #self.max_concurrent_requests = settings.getint('CONCURRENT_REQUESTS_PER_SPIDER',128 )
        
            
    def parse(self, response):
        event.send( 
            signal=signals.RESPONSE,
            sender=self,
            response = response
        )            
    

    


if __name__=='__main__':
    pass

