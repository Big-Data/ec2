#coding=utf-8

import sys, time , math, json

#from scrapy import log
from ec2.redis import API
from ec2.utils import misc
          
#--------------------------------------
class BaseCache(object):

    _KeyName = 'table'
    _ValueName = 'pid'
    _Handler = None
    def __init__(self, dbname, name, timeout):
        self._timeout = timeout
        self._dbname = dbname
        self._keyname = name
        self._redis = API.redis(self._dbname)
        self._ns = {
            'data':     API.ns_of(self._keyname),
        }

    def _cache_info(self, v):
        return  {
            'db':               self._dbname,
            'handler':          self._Handler,
            self._KeyName:      self._keyname,
            self._ValueName:    v,
        }

    def _expire(self, v, timeout=None):
        vv = misc.makelist(v)
        timeout = timeout or self._timeout
        API.expire( map(self._cache_info,vv), timeout=timeout)

    def _expire_rem(self, v):
        vv = misc.makelist(v)
        API.expire_rem(map(self._cache_info, vv))



#--------------------------------------
class  SetCache(BaseCache):
    
    _KeyName = 'set'
    _ValueName = 'value'
    _Handler = 'expired.cache_set'

    def __contains__(self, e):  return self.sismember(e)

    def sadd(self, rs, timeout=None):
        timeout = timeout or self._timeout
        rs = misc.makelist(rs)
        _rs = self._redis.sadd(self._ns['data'], *rs)
        self._expire(rs, timeout)
        
        return _rs

    def srem(self, *ee):
        rs = self._redis.srem(self._ns['data'], *ee)
        self._expire_rem( ee )
        
    def spop(self):
        el = self._redis.spop(self._ns['data'])
        self._expire_rem(el)
        return el

    #------------------------
    def scard(self):    return self._redis.scard(self._ns['data'])
    def srandmember(self):
        return self._redis.srandmember(self._ns['data'])

    def smembers(self):
        return self._redis.smembers(self._ns['data'])

    def sismember(self,e):
        return self._redis.sismember(self._ns['data'],e)


#--------------------------------------
class  HashCache(BaseCache):
    
    _KeyName = 'hash'
    _ValueName = 'field'
    _Handler = 'expired.cache_hash'

    def __contains__(self, e):  return self.hexists(e)

    def hset(self, k,v, timeout=None):
        timeout = timeout or self._timeout
        rs = self._redis.hset(self._ns['data'], k,v)
        self._expire(k, timeout)
        return rs

    def hdel(self, *e):
        rs = self._redis.hdel(self._ns['data'], *e)
        self._expire_rem( e )
        return rs
    #------------------------
    def hget(self, k):
        return self._redis.hget(self._ns['data'], k)

    def hexists(self,k):
        return self._redis.hexists(self._ns['data'],k)
    



#--------------------------------------
class  ZsetCache(BaseCache):
    
    _KeyName = 'zset'
    _ValueName = 'value'
    _Handler = 'expired.cache_zset'

    def __contains__(self, e):  return self._redis.zrank(self._ns['data'],e)!=None

    def zadd(self, k, v):
        v = self._redis.zadd(self._ns['data'], k,v)
        self._expire( k )
        return v
    
    def zincrby(self, k,v):
        _v = self._redis.zincrby(self._ns['data'], k,v)
        if int(_v-v)==0:    # add case
            self._expire(k)
        return _v

    def zrem(self, *k):
        rs = self._redis.zrem(self._ns['data'], *k)
        self._expire_rem(k)
        return rs
    
    #--------------------------------    
    def zcard(self):
        return self._redis.zcard(self._ns['data'])
    
    def zcount(self, min,max):
        return self._redis.zcount(self._ns['data'],min,max)
    
    def zscore(self, k):
        return self._redis.zscore(self._ns['data'], k)

    def zrank(self, k):
        return self._redis.zrank(self._ns['data'], k)

    def zrange(self, *args, **kwds):
        return self._redis.zrange(self._ns['data'], *args, **kwds)

    def zrangebyscore(self, *args, **kwds):
        return self._redis.zrangebyscore(self._ns['data'],*args, **kwds)

    def zrevrange(self, *args, **kwds):
        return self._redis.zrevrange(self._ns['data'], *args, **kwds)

    def zrevrangebyscore(self, *args, **kwds):
        return self._redis.zrevrangebyscore(self._ns['data'],*args, **kwds)




#--------------------------------------
if __name__=='__main__':
    pass    