#coding=utf-8

import json, logging
from socket import error as socket_error

import gevent
from gevent import queue

from ec2        import WarningErr, signals
from ec2.utils  import inspect, event


class Actor(gevent.Greenlet):

    _SleepLimit = 5
    def __init__(self, retry=10,  debug=False):
        gevent.Greenlet.__init__(self)

        self.running = False
        self.debug = debug
        
        self._RetryLimit = retry
    
    def recv(self): raise NotImplemented()
    def stop(self): self.running = False 

    def _run(self):
        self.running = True
        _retry = self._RetryLimit
        
        event.send( signal=signals.INIT, sender=self )        
        while self.running:
            gevent.sleep(0)
            try:
                msg = self.recv()
                if not msg: continue
                #logging.debug('!>>> recv|%s'%(msg,))
                event.send( signal=signals.RECV, sender=self, message=msg )        
            except WarningErr, e:
                logging.warning(e)
            except Exception ,e:
                logging.warning(str(e))
                if self.debug:
                    traceback.print_exc()
                    logging.warning('process fail: retry|%s'%self.retry)
                
                _retry -=1
                if _retry<0:   break    
                gevent.sleep(self._SleepLimit)
                event.send( signal=signals.INIT, sender=self )        
                continue
                            
            #-----------------------    
            _retry = self._RetryLimit
            

        event.send( signal=signals.STOP, sender=self )        


class QueuePuller(Actor):

    def __init__(self, retry=0,  debug=False):
        Actor.__init__(self, retry, debug)
        self._inbox = gevent.queue.Queue()

    def recv(self):
        return self._inbox.get()

    def send(self,message):
        return self._inbox.put(message)

