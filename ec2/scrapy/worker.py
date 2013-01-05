#coding=utf-8

import json
#from scrapy.utils.signal import send_catch_log_deferred

from scrapy             import log
from scrapy.crawler     import Crawler  #, CrawlerProcess
from scrapy.http        import Request
from scrapy.xlib.pydispatch import dispatcher


from ec2        import WarningErr, signals
from ec2.utils  import inspect, event, decorator,misc
from ec2.gevent.worker  import BaseWorker
from ec2.scrapy.spider  import Spider
from ec2.conf.enabled   import redis_conf 

#-------------------------------
class Worker(BaseWorker):

    @decorator.safe_method()    
    def on_recv(self, response):
        if  not response or \
            not response.request or \
            not response.request.meta:
            return

        _cb = response.request.meta.get('handler', None)
        _cb = self._query_handler( _cb )
        _cb( request=response.request, response=response)
        

class Ctrl(object):

    def __init__(self, settings, puller, worker=None):
        self.settings = settings 
        self._puller = puller
        self._crawler = Crawler(settings)
        self._worker = worker or Worker(redis_conf)

        self._crawler.install()
        self._crawler.configure()    

        #can not using event module of ec2 for defer send, fix it!
        dispatcher.connect( self._on_recv_pull,  signal=signals.RECV,  sender=self._puller)
        dispatcher.connect( self._on_err,        signal=signals.ERROR, sender=self._puller)
        
        event.connect( self._worker.on_recv,signal=signals.RESPONSE, sender=event.Any)
        

    def start(self):
        self._puller.start()
        self._crawler.start()

    def stop(self):
        self._puller.stop()
        self._crawler.stop()


    @decorator.safe_method()    
    def _on_recv_pull(self, message):
        #log.msg('on_recv:%s'%(message,), log.DEBUG)
        requests = self._make_requests(message)
        if not requests: return
        self._requests_queue().append( (Spider(self.settings),requests) )
        
    def _requests_queue(self):   
        return self._crawler.queue.spider_requests

    def _on_err(self):
        self.stop()

    def _make_requests(self,message):
        if not message: return
        chnl,message = message
        
        #logging.info('1.>>> %s'%message )
        kwds = json.loads( message,object_hook=misc.json_decode_dict )
        if not kwds:    return

        #logging.info('3.>>> %s'%kwds )
        return ( Request(**e) for e in kwds )

    