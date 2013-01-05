#coding=utf-8

import logging,json
import gevent
from gevent import Greenlet
from ec2    import WarningErr, signals
from ec2.utils import inspect, event, decorator

#-------------------------------
class BaseWorker(object):
    _caches = {}
    def __init__(self, settings ): 
        self._base = settings.get('worker_base', 'ec2.worker')
        self.reload = settings.getbool( 'worker_reload', False)
        self.debug =  settings.getbool( 'worker_debug', False) 
    
    def _query_handler(self, handler):
        if not handler: raise WarningErr('handler is null')

        _name = '%s.%s'%(self._base, handler)
        if not self.reload and self._caches.has_key(_name) :
            return self._caches[_name]
        
        _fun = inspect.str_to_class(_name, reload=self.reload, auto_reload=self.debug)
        if  not inspect.isfunction(_fun) :
            raise WarningErr('loading fun fail: %s'%_name)
        
        self._caches[_name] = _fun
        return self._caches[_name]

    def on_recv(self, message): raise NotImplementedError
        
    def decode_message(self,msg):  return json.loads(msg)
    def clear_caches(self):        self._caches = {}
    
#------------------------------
class Worker(BaseWorker):

    def __init__(self, settings ): 
        BaseWorker.__init__(self, settings)
        self._pool = set()
    
    @decorator.safe_method()    
    def on_recv(self, message):
        obj =  self.decode_message(message)
        if not obj: return 
        
        _cb   = self._query_handler( obj.get('handler',None) )
        if  _cb is None: return 
        g = Greenlet.spawn(_cb, self, message=obj)
        g.link(self._pool.remove)
        self._pool.add(g)
        
    def pool(self): return self._pool        
    
    def stop(self):
        gevent.joinall( self._pool, timeout=5*60 )
        gevent.killall( self._pool )        
    
