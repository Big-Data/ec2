import logging, json , time
logging.basicConfig(level=logging.DEBUG)

from ec2.redis import RedisDb

db = RedisDb(pre='MQ')


def test_ws():
    db.queue_push('chnl:test', {
        'handler':  'echo.Handler',
        'srv-ts': int(time.time()),
        #'expire': 15,
    })
    

def test_Logger():
    pass

def test_json():
    o = {
        'ts': int(time.time()),
        'src': 'hello:world',
        'pid': 123,
    }
    db.redis().setex( '~%s'%json.dumps(o),'',10)


def test_cron():
    db.update_table('conf:cron', 'ttt', {
        'expire':   5,
        'retry':    100,
    })
    
    db.redis().set(
        db.ns_of('test:xxx'), ''
    )

    db.expire({
        #'on_expired':   'expired.Handler',
        'src':          'test:xxx',
        'handler':      'logger.Handler',
    },15)    

    db.expire({
        'on_expired':   'expired.CronHandler',
        'src':          'conf:cron:ttt',
        'queue':        'queue:cron',
        'handler':      'logger.Handler',
    },15)    

    



def test_table():
    obj = {
        'a':    1,
    }
    db.insert_into('xxx',obj,20)
    
    #print db.redis().hincrby('xxx' , 'retry', -1)
    #db.redis().hset( 'xxx', 'expire' , 1)
    #v =  db.redis().hget( 'xxx', 'expire')
    #print v, type(v)
    #rs = db.redis().hmget('NULL', ['x', 'y'])
    #print rs


def test_srv2client():
    db.redis().delete(db.ns_of('www:test2'))
    
    i = 0
    while True:
        db.queue_push( 'www:test2', {'msg':i,} )
        i +=1
        time.sleep(1)


def test_client2srv():
    i = 0    
    while True:
        db.queue_push( 'client:echo', {
            'queue':    'test2',
            'handler':  'test.dump',
            'idx':  i,
        } )
        i +=1
        time.sleep(1)



if __name__=='__main__':
    #test_cron()
    #test_ws()
    #test_json()
    #test_table()
    #for e in db.select_all('xxx'):
    #    print e
    
    test_srv2client()
    #test_client2srv()
    print '---- over ---'