import logging
logging.basicConfig(level=logging.DEBUG)

from twisted.internet import defer, reactor
from scrapy.xlib.pydispatch import dispatcher

from ec2    import signals
from ec2.redis import RedisDb
from ec2.scrapy.puller import ChannelsPuller

db = RedisDb(pre='MQ')


def on_recv( *args, **kwds):
    logging.debug( 'on_recv %s|%s'%(args,kwds) )

def on_err( *args, **kwds):
    logging.debug( 'on_err %s|%s'%(args,kwds) )
    

puller = ChannelsPuller(db, 'xxx')
    
dispatcher.connect( on_recv, signal=signals.RECV, sender=puller)
dispatcher.connect( on_err,  signal=signals.ERROR, sender=puller)



if __name__=='__main__':

    puller.start()
    reactor.run()
