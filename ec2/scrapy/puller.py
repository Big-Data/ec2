#coding=utf-8

import signal
import redis

from twisted.internet import reactor, defer, threads

from scrapy import log
from scrapy.utils.signal    import send_catch_log_deferred
from scrapy.utils.ossignal  import install_shutdown_handlers,signal_names
from scrapy.crawler         import Crawler

from ec2        import signals
from ec2.redis  import API

class ChannelsPuller(object):

    def __init__(self, db, chnls):
        self.db = db
        self.chnls = chnls
        self.running = False

        install_shutdown_handlers(self._signal_shutdown)


    def start(self):
        log.msg('start %s'%(self.chnls,), log.DEBUG )

        d = threads.deferToThread(self._recv)
        return d

    def stop(self):
        log.msg('stop %s'%(self.chnls,), log.DEBUG )
        
        self.running = False
        self._stop_reactor()

    def _signal_shutdown(self, signum, _):
        install_shutdown_handlers(self._signal_kill)
        signame = signal_names[signum]
        log.msg("Received %s, shutting down gracefully. Send again to force " \
            "unclean shutdown" % signame, log.INFO)
        reactor.callFromThread(self.stop)

    def _signal_kill(self, signum, _):
        install_shutdown_handlers(signal.SIG_IGN)
        signame = signal_names[signum]
        log.msg('Received %s twice, forcing unclean shutdown' % signame, log.INFO)
        reactor.callFromThread(self._stop_reactor)
    
    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError: # raised if already stopped or in shutdown stage
            pass

    #----------------------------
    def _recv(self):
        self.running = True
        log.msg('recv begin: %s'%self.chnls,log.DEBUG)

        while self.running:
            try:
                chnl,msg = API.queue_bpop(self.chnls, timeout=5)
            except  redis.exceptions.ConnectionError, e:
                send_catch_log_deferred( 
                    signal=signals.ERROR,
                    sender=self
                )            
                self.stop()
            else:            
                if not chnl or not msg:    continue

                send_catch_log_deferred( 
                    signal=signals.RECV,
                    sender=self,
                    message=(chnl,msg)
                )
        log.msg('recv end: %s'%self.chnls,log.DEBUG)




