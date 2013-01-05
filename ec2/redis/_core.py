import redis, json, logging
import hashlib
from ec2.conf.enabled import redis_conf 
from ec2.utils  import misc

_redis_pool = {}
_db_pool = {}

def _redis_factory(name='default'):
    
    if not redis_conf.get(name,None):
        raise Exception('missing <%s> in redis config'%name) 
    
    conf = redis_conf[name]
    conf_key = '|'.join( '%s'%conf[e] for e in ('host','port','db'))    
    
    if not _redis_pool.has_key(conf_key) :
        _redis_pool[conf_key] = redis.Redis(**conf)
    
    return _redis_pool[conf_key]


def _db_factory(name='default'):
    if not _db_pool.has_key(name) :
        _db_pool[name] = RedisDb(name)
    
    return _db_pool[name]



class RedisDb(object):

    def __init__(self, name='default'):
        self._redis = _redis_factory(name)
    
    def redis(self):    return self._redis

    def insert_into(self, name, v,timeout=None ):
        pid = self._redis.incr(API.ns_of(name, 'UUID'))
        v['pid'] = str(pid)
        self.update_table(name,pid,v, timeout)
        return pid

    def delete_table(self, name ):
        pids = self._redis.smembers(API.ns_of(name,'INDEX')) or []
        if not pids:    return
        pids.extend(['UUID','INDEX',])
        pids = [API.ns_of(name,pid) for e in pids]
        self._redis.srem(*pids)

    def delete_from( self, name, pid ):  
        ns = API.ns_of(name, pid)
        self._redis.delete(ns)
        self._redis.srem(API.ns_of(name,'INDEX'), pid )
 
    def select_from( self, name, pid):
        _name = API.ns_of(name, pid)
        return self._redis.hgetall(_name)        

    def select_fields( self,name,pid, fields):
        _name = API.ns_of(name, pid)
        values =  self._redis.hmget(_name, fields)        
        return dict(zip(fields, values))

    def select_all( self, name):
        pids = self._redis.smembers(API.ns_of(name,'INDEX')) or []
        for pid in pids:
            rcd = self.select_from(name,pid)
            if not rcd: 
                self._redis.srem(API.ns_of(name,'INDEX'),pid)
                continue
            yield rcd

    def update_table(self, name, pid, mapping,timeout=None ):
        self._redis.hmset(API.ns_of(name,pid), mapping)
        self._redis.sadd(API.ns_of(name,'INDEX'), pid )
        if not timeout:  return
        
        self._redis.expire(API.ns_of(name,pid), timeout)

    
#------------------------------
class API(object):

    @staticmethod
    def db(name='default'):  return _db_factory(name)      

    @staticmethod
    def redis(name='default'):  return _db_factory(name).redis()

    @staticmethod    
    def expire( msg, timeout=3600, dbname='cache'):
        rs = misc.makelist(msg)
        for e in rs:
            API.redis(dbname).setex( '~%s'%json.dumps(e),'',timeout)

    @staticmethod    
    def expire_rem( msg, dbname='cache'):
        rs = misc.makelist(msg)
        rs = ('~%s'%json.dumps(e) for e in rs)
        API.redis(dbname).delete(*rs)

    @staticmethod    
    def ns_of(*args):
        return '%s:%s' % ( API._pre(),
            ':'.join(str(e) for e in args if e!=None) ,
        )
    
    @staticmethod    
    def queue_push( ns, obj, dbname='default'):
        API.redis(dbname).rpush( API.ns_of(ns),json.dumps(obj))

    @staticmethod    
    def queue_bpop( nss, timeout=60, dbname='default'):
        nss = [API.ns_of(e) for e in misc.makelist(nss)]
        res = API.redis(dbname).blpop(nss,timeout=timeout)
        if not res: return None,None
        return API._short(res[0]), res[1]

    @staticmethod    
    def _pre():     return redis_conf.get('pre_db', 'ec2') 

    @staticmethod    
    def _short(ns):
        if ns.startswith( '%s:'%API._pre() ):  return ns[len(API._pre())+1:]
        return ns
    
