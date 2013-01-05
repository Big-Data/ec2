from ec2.conf import init_scrapy
init_scrapy()

import logging
logging.basicConfig(level=logging.DEBUG)

import time
from scrapy import log
from scrapy.conf import settings

from ec2.redis import RedisDb
from ec2.scrapy.puller  import ChannelsPuller
from ec2.conf.enabled   import ws_conf

from ec2.scrapy.worker  import Ctrl
from ec2.utils  import event

log.start()

db = RedisDb(pre='MQ')


puller = ChannelsPuller(db, 'xxx')
ctrl = Ctrl( settings, puller )




url = 'http://%s/test/slow_echo/%%s_%%s'%ws_conf['client']
def test_data():
    for i in xrange(200):
        db.queue_push('xxx',[{
            'url':  url%( i, int(time.time()), ) ,
            'meta': {},
            'dont_filter': True,
        },])

if __name__=='__main__':
    from twisted.internet import reactor
    if 0:
        ctrl.start()
        reactor.run()
    else:
        test_data()


