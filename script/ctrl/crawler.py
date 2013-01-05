from ec2.conf import init_scrapy
init_scrapy()

import time
from scrapy import log

from ec2.redis import API
from ec2.scrapy.puller  import ChannelsPuller
from ec2.scrapy.worker  import Ctrl
from ec2.conf.enabled import scrapy_conf

log.start()

puller = ChannelsPuller(API.db(), 'request')
ctrl = Ctrl( scrapy_conf, puller )

if __name__=='__main__':
    from twisted.internet import reactor
    ctrl.start()
    reactor.run()
