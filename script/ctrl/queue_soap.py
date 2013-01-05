import logging, json , time
logging.basicConfig(level=logging.DEBUG)

from ec2.redis import API
from ec2.scrapy.tw      import Ctrlet
from ec2.scrapy.puller  import ChannelsPuller


ctrl  = Ctrlet( 
    ChannelsPuller(API.db(), 'queue:soap'),
)



if __name__=='__main__':
    try:
        ctrl.start()
    except KeyboardInterrupt:
        ctrl.stop() 
        print '\nbye'
    
