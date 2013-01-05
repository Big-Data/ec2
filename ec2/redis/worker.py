#coding=utf-8

import logging,json
from ec2    import WarningErr, signals
from ec2.utils import event, decorator
from ec2.gevent.worker import Worker
from ec2.conf.enabled  import redis_conf


#-------------------------------
class ExpiredPoolWorker(Worker):
    def decode_message(self, msg):  # skip channel_name/msg[0]
        obj = json.loads(msg[1][1:])
        if not obj.get('handler',None):
            obj['handler'] = 'expired.handler'
        return obj


class QueueWorker(Worker):
    def decode_message(self, msg):
        return json.loads(msg[1])


#-------------------------------
class Ctrlet(object):


    def __init__(self, puller, worker=None, retry=3, debug=False):
        self._puller = puller 
        self._worker = worker or QueueWorker(redis_conf)

        if hasattr(puller, 'db'):
            self._worker.db = puller.db

        event.connect( self._worker.on_recv, signal=signals.RECV, sender=self._puller)
        event.connect( self.stop, signal=signals.STOP, sender=self._puller)

    @decorator.safe_method()
    def stop(self):
        self._puller.stop()
        self._worker.stop()

    def start(self):
        self._puller.start()
        self._puller.join()
        
