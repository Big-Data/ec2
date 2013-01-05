#coding=utf-8

import json

from twisted.internet import reactor, threads
from scrapy     import log
from scrapy.xlib.pydispatch import dispatcher


from ec2        import  WarningErr, signals
from ec2.utils  import  decorator
from ec2.gevent.worker  import BaseWorker
from ec2.conf.enabled   import redis_conf 

#-------------------------------
class Worker(BaseWorker):

    @decorator.safe_method()    
    def on_recv(self, message):
        obj =  self.decode_message(message)
        if not obj: return 
        
        _cb   = self._query_handler( obj.get('handler',None) )
        if  _cb is None: return 
        threads.deferToThread(_cb, obj)
    
    def decode_message(self, msg):
        return json.loads(msg[1])
        

class Ctrlet(object):

    def __init__(self, puller, worker=None):
        self._puller = puller
        self._worker = worker or Worker(redis_conf)

        #can not using event module of ec2 for defer send, fix it!
        dispatcher.connect( self._worker.on_recv,   signal=signals.RECV,  sender=self._puller)
        dispatcher.connect( self._on_err,           signal=signals.ERROR, sender=self._puller)
        

    def start(self):
        self._puller.start()
        reactor.run()

    def stop(self):
        self._puller.stop()

    def _on_err(self):
        self.stop()

   