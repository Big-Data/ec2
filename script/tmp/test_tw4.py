from ec2.conf import init_scrapy
init_scrapy()

#import logging
#logging.basicConfig(level=logging.DEBUG)

import time
from scrapy import log
#from scrapy.conf import settings

from ec2.redis import API
from ec2.scrapy.puller  import ChannelsPuller
from ec2.conf.enabled   import ws_conf

from ec2.scrapy.worker  import Ctrl
from ec2.utils  import event
from ec2.conf.enabled import scrapy_conf

log.start()



puller = ChannelsPuller(API.db(), 'xxx')
ctrl = Ctrl( scrapy_conf, puller )




url = 'http://%s/test/slow_echo/%%s_%%s'%ws_conf['client']
def test_data():
    for i in xrange(2):
        db.queue_push('xxx',[{
            'url':  url%( i, int(time.time()), ) ,
            'meta': {},
            'dont_filter': True,
        },])

if __name__=='__main__':
    from twisted.internet import reactor
    if 1:
        ctrl.start()
        reactor.run()
    else:
        test_data()


