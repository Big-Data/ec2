from nose import tools
import unittest, time
from ec2.redis  import API
from ec2.redis  import cache

class ZsetCacheTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')
        self._cache = cache.ZsetCache('default', 'myzset', 1)

    def tearDown(self):
        self._clear_keys()        
        #pass
        
    def _clear_keys(self):
        for k in self.db._redis.keys('test:*'):
            self.db._redis.delete(k)

    def testZadd(self):
        tools.eq_( 0 , self._cache.zcard() )
        tools.ok_( not 'hello' in self._cache )
        self._cache.zadd( 'hello', 5 )
        tools.eq_( 1 , self._cache.zcard() )
        tools.ok_( 'hello' in self._cache )
        time.sleep(3)
        tools.eq_( 0 , self._cache.zcard() )
        tools.ok_( not 'hello' in self._cache )

        self._cache.zadd( 'aa', 2 )
        self._cache.zadd( 'a', 1 )
        self._cache.zadd( 'aaa', 3 )
        tools.eq_( 3 , self._cache.zcard() )
        tools.eq_( 1 , self._cache.zcount(0,1) )
        tools.eq_( 3 , self._cache.zcount(1,3) )

        tools.eq_( 2 , self._cache.zscore('aa') )
        tools.eq_( None , self._cache.zscore('b') )
        tools.eq_( 0 , self._cache.zrank('a') )
        tools.eq_( 2 , self._cache.zrank('aaa') )


    def testZincrby(self):
        tools.eq_( 0 , self._cache.zcard() )
        self._cache.zadd( 'aa', 2 )
        self._cache.zadd( 'a', 1 )
        self._cache.zadd( 'aaa', 3 )
        tools.eq_( 'a|aa|aaa', '|'.join(self._cache.zrange(0,-1)) )
        tools.eq_( 'aa|aaa', '|'.join(self._cache.zrangebyscore(2,4)) )
        tools.eq_( 'a|aa|aaa', '|'.join(self._cache.zrangebyscore('-inf','inf')) )
        tools.eq_( 'a|aa', '|'.join(self._cache.zrangebyscore('-inf','inf', start=0, num=2)) )


        self._cache.zincrby('a', 10)
        tools.eq_( 11 , self._cache.zscore('a') )
        tools.eq_( 'aa|aaa', '|'.join(self._cache.zrange(0,1)) )


    def testZrem(self):
        tools.eq_( 0 , self._cache.zcard() )
        self._cache.zadd( 'aa', 2 )
        self._cache.zadd( 'a', 1 )
        self._cache.zadd( 'aaa', 3 )
        tools.eq_( 'aaa|aa|a', '|'.join(self._cache.zrevrange(0,-1)) )
        tools.eq_( 'aaa|aa', '|'.join(self._cache.zrevrangebyscore(4,2)) )
        
        self._cache.zrem('aa')
        tools.eq_( 'aaa|a', '|'.join(self._cache.zrevrange(0,-1)) )

        