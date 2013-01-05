#coding=utf-8

import gevent, logging, time, json
#from socket import error as socket_error
#from geventwebsocket import WebSocketError

from ec2                import WarningErr, signals
from ec2.utils          import event, decorator
from ec2.redis.puller   import ChannelsPuller
from ec2.gevent.actor   import QueuePuller
from ec2.websocket      import actor


class WsPuller(actor.BasePuller):
    def recv(self):
        if self._ws.socket is None:
            self.stop()
            return
        
        return self._ws.receive()


class Ctrlet(object):

    def __init__(self,db,chnl, ws):
        self._db = db
        self._chnl = chnl
        self._pullers = {
            'db':   ChannelsPuller(db,chnl),   
            'ws':   WsPuller(ws),
        }

        #--- recv
        event.connect(  self._on_db_recv, 
            signal=signals.RECV, 
            sender=self._pullers['db']
        )
        event.connect(  self._on_ws_recv, 
            signal=signals.RECV, 
            sender=self._pullers['ws']
        )
        #-- stop
        event.connect(  self._on_stop, 
            signal=signals.STOP, 
            sender=self._pullers['db']
        )
        event.connect(  self._on_stop, 
            signal=signals.STOP, 
            sender=self._pullers['ws']
        )

        #---------
        self._db.update_table('chnls', self._chnl, {
            'pid':      self._chnl,
            #'ping':     60,
        })


    #@decorator.safe_method()
    def _on_db_recv(self, message):
        chnl,message = message
        self._pullers['ws'].send(message)
    
    @decorator.safe_method()
    def _on_ws_recv(self,message):
        obj = json.loads(message)
        if not obj or not obj.get('queue',None):
            return
       
        self._db.queue_push('queue:%s'%obj['queue'], obj)
        
    @decorator.safe_method()
    def _on_stop(self):
        for e in self._pullers.values(): e.stop()
        gevent.killall(self._pullers.values(), timeout= 60*5)


    def start(self):
        for e in self._pullers.values(): e.start()
        gevent.joinall(self._pullers.values())



