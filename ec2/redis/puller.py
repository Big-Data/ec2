#coding=utf-8

import traceback
import logging,json
from ec2    import WarningErr, signals
from ec2.utils import event, decorator
from ec2.gevent.actor import Actor
from ec2.redis  import API
from ec2.conf.enabled import redis_conf


class ChannelsPuller(Actor):

    def __init__(self, db, chnls,   retry=10,  debug=False):
        Actor.__init__(self, retry, debug)
        self.db = db
        self.chnls = chnls

    def recv(self):
        chnl,msg = API.queue_bpop(
            self.chnls, 
            timeout=redis_conf.getint('channel_timeout',60)
        )
        if not chnl or not msg:    return
        return (chnl,msg)


class ExpiredPoolPuller(Actor):
    def __init__(self, db,   retry=10,  debug=False):
        Actor.__init__(self, retry, debug)
        self.db = db

    def recv(self):
        res = self.db.redis().blpop(
            'ExpiredPool',
            timeout=redis_conf.getint('expiredpool_timeout',5)
        )
        if not res or not res[0] or not res[1]: return 
        
        return res


#-------------------------------
