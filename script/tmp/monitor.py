import logging, json 

import gevent
from gevent import monkey;monkey.patch_all()

from ec2.redis import RedisDb
#from ec2.redis import actor

#logging.basicConfig(level=logging.INFO) #DEBUG)
logging.basicConfig(level=logging.DEBUG)
db = RedisDb(pre='MQ')




def main():
    _all = [
        actor.Cronlet ( db, period=10*60  ), 
        actor.Clocker ( db, ['ExpiredPool',], retry=2 ), 
        actor.Dumb    ( db, ['queue:logger',], retry=2 ), 
        
        actor.Worker  ( db, ['queue:cron',],  retry=2 ), 
        #actor.Worker  ( db, ['queue:recvq',],  retry=2 ), 
        actor.Worker  ( db, ['queue:srv',],  retry=2 ), 
    ]
    try:
        [e.start() for e in _all]
        gevent.joinall( _all )
    except KeyboardInterrupt:
        gevent.killall( _all )
        #gevent.shutdown()
        print '\nbye'


if __name__=='__main__':
    main()
