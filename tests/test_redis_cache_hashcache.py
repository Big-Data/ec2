from nose import tools
import unittest, time
from ec2.redis  import API
from ec2.redis  import cache


class HashCacheTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')
        self._cache = cache.HashCache('default', 'myhash', 1)

    def tearDown(self):
        self._clear_keys()        
        #pass
        
    def _clear_keys(self):
        for k in self.db._redis.keys('test:*'):
            self.db._redis.delete(k)

    def _hgetall(self):
        return self.db.redis().hgetall(API.ns_of('myhash'))

    def testHset(self):
        tools.eq_( {} , self._hgetall() )
        self._cache.hset('hello', 'world')
        tools.eq_( {'hello': 'world'} , self._hgetall() )
        tools.eq_( 'world' , self._cache.hget('hello') )
        tools.ok_( 'hello' in self._cache )
        tools.ok_( not 'missing' in self._cache )
        
        time.sleep(3)
        tools.eq_( {} , self._hgetall() )

    
    def testHdel(self):
        tools.eq_( {} , self._hgetall() )
        self._cache.hset('hello', 'world')
        tools.ok_( self._cache.hexists('hello') )
        self._cache.hdel( 'hello' )        
        tools.eq_( {} , self._hgetall() )
        tools.ok_( not 'hello' in  self._cache )

    
    


