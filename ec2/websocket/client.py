#coding=utf-8

import gevent ,logging
#from socket import error as socket_error

import websocket
from ec2    import signals
from ec2.websocket.actor    import BasePuller
from ec2.redis.puller       import ChannelsPuller

from ec2.utils      import event, decorator


class WsPuller(BasePuller):
    def recv(self):
        return self._ws.recv()


class DumpCtrlet(object):
    
    def __init__(self, url):
        self._url = url
        self._ws = websocket.WebSocket()
        self._puller = WsPuller(self._ws,retry=3)
        
        event.connect( self._on_init, signal=signals.INIT, sender=self._puller)
        event.connect( self._on_recv, signal=signals.RECV, sender=self._puller)
        event.connect( self._on_stop, signal=signals.STOP, sender=self._puller)

    @decorator.safe_method(silent=True)   
    def _on_init(self):
        self._ws.settimeout(5)
        self._ws.connect(self._url)
        self._ws.settimeout(None)

    
    def _on_recv(self,message):
        logging.debug('>>>recv: %s'%message)

    def _on_stop(self):
        self._puller.stop()
        self._puller.kill(timeout= 60*5)

    def start(self):
        self._puller.start()
        self._puller.join()

    def stop(self): self._on_stop()


#---------------------------------
class EchoCtrlet(object):
    
    def __init__(self, db, chnls, url):
        self._url = url
        self._ws = websocket.WebSocket()
        self._pullers = {
            'ws':   WsPuller(self._ws,retry=3),
            'db':   ChannelsPuller(db,chnls),
        }
        
        event.connect( self._on_init, signal=signals.INIT, sender=self._pullers['ws'])
        event.connect( self._on_stop, signal=signals.STOP, sender=self._pullers['ws'])
        event.connect( self._on_stop, signal=signals.STOP, sender=self._pullers['db'])
        event.connect( self._on_ws_recv, 
            signal=signals.RECV, 
            sender=self._pullers['ws']
        )
        event.connect( self._on_db_recv, 
            signal=signals.RECV, 
            sender=self._pullers['db']
        )

    @decorator.safe_method(silent=True)   
    def _on_init(self):
        self._ws.settimeout(5)
        self._ws.connect(self._url)
        self._ws.settimeout(None)

    def _on_ws_recv(self,message):
        logging.debug('>>>recv: %s'%message)
        
    
    @decorator.safe_method()   
    def _on_db_recv(self,message):
        self._pullers['ws'].send( message[1] )

    @decorator.safe_method()   
    def _on_stop(self):
        for e in self._pullers.values():    e.stop()

        gevent.killall( self._pullers.values(), timeout=5*60)

    def start(self):
        for e in self._pullers.values():    e.start()
        gevent.joinall( self._pullers.values() )

    def stop(self): self._on_stop()

