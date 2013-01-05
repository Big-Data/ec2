
import logging,sys
import gevent
from gevent import monkey;monkey.patch_all()

from ec2.redis  import RedisDb
from ec2.websocket import client

logging.basicConfig(level=logging.DEBUG)

MQ_PREFIX = 'MQ'
db   = RedisDb(pre=MQ_PREFIX)


#--------------------------------
def main():
    url = "ws://192.168.1.230:9090/ws/chnl/test2"
    #url = "ws://www.ectwo.com.cn/ws/chnl/test"
    
    #ctrl = client.DumpCtrlet(url)
    ctrl = client.EchoCtrlet(db, 'client:echo', url)
    
    try:
        ctrl.start()
    except KeyboardInterrupt:
        ctrl.stop()
        print '\nbye'



if __name__ == "__main__":
    #websocket.enableTrace(True)
    #websocket.setdefaulttimeout(5)
    #url = 'ws://echo.websocket.org'
    #url = "ws://www.ectwo.com.cn/ws/pub/test"
    #url = "ws://localhost:8080/ws/pipe/test"
    #gevent.signal(signal.SIGQUIT, gevent.shutdown)
    main()
 