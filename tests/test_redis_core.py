from nose import tools
import unittest, time
from ec2.redis import API
from ec2.conf.enabled import redis_conf


class RedisTest(unittest.TestCase):
    
    def setUp(self): 
        self.redis = API.redis('default')

    def tearDown(self):
        pass
        
    def testRedis(self):
        rs = self.redis.ping()
        tools.eq_(True, rs) 
        
        rs = self.redis.info()
        tools.ok_(rs) 
  

        
class DbTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')

    def tearDown(self):
        self._clear_keys()        
           
    def _clear_keys(self):
        for k in self.db._redis.keys('test:*'):
            self.db._redis.delete(k)

    
    def testNs(self):
        rs = API.ns_of('a')
        tools.eq_('test:a', rs) 
        
        rs = API.ns_of('a','b')
        tools.eq_('test:a:b', rs) 
        
    def testInsert(self):
        pid = self.db.insert_into('aaa',{'a':'a'})
        tools.eq_(1, pid) 
        
        rs = self.db.select_from('aaa', pid)
        tools.eq_("{'a': 'a', 'pid': '1'}", str(rs))

