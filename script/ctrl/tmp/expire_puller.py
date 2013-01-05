import logging, json , time
logging.basicConfig(level=logging.DEBUG)

from ec2.redis          import API
from ec2.redis.worker   import Ctrlet,ExpiredPoolWorker
from ec2.redis.puller   import ExpiredPoolPuller
from ec2.conf.enabled   import redis_conf


ctrl  = Ctrlet(
    puller = ExpiredPoolPuller(API.db()),
    worker = ExpiredPoolWorker(redis_conf)
)



if __name__=='__main__':
    try:
        ctrl.start()
    except KeyboardInterrupt:
        ctrl.stop()
        print '\nbye'
    
