from nose import tools
import unittest, time
from ec2.redis  import API
from ec2.redis  import cache

class SetCacheTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')
        self._cache = cache.SetCache('default', 'myset', 1)

    def tearDown(self):
        self._clear_keys()        
        #pass
        
    def _clear_keys(self):
        for k in self.db._redis.keys('test:*'):
            self.db._redis.delete(k)


    def testSadd(self):
        tools.eq_( 0 , self._cache.scard() )
        self._cache.sadd('hello')
        tools.eq_( 1 , self._cache.scard() )
        tools.ok_( 'hello' in self._cache )
        time.sleep(6)
        tools.ok_( not 'hello' in self._cache )
        tools.eq_( 0 , self._cache.scard() )

          
    def testSrem(self):
        tools.eq_( 0 , self._cache.scard() )
        self._cache.sadd('hello')
        self._cache.sadd('hello2',timeout=5)
        tools.eq_( 2 , self._cache.scard() )
        time.sleep(3)
        tools.eq_( 1 , self._cache.scard() )

        self._cache.srem('hello2')
        tools.eq_( 0 , self._cache.scard() )

    def testSpop(self):
        tools.eq_( 0 , self._cache.scard() )
        self._cache.sadd('hello', timeout=3)
        e = self._cache.spop()
        tools.ok_( 'hello' , e )
        tools.eq_( 0 , self._cache.scard() )


    def testSmembers(self):
        tools.eq_( 0 , self._cache.scard() )
        self._cache.sadd('hello1', timeout=3)
        self._cache.sadd('hello2', timeout=3)
        tools.eq_( 'hello2|hello1' , '|'.join(self._cache.smembers()) )

