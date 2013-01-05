from nose import tools
import unittest, time
from ec2    import WarningErr
from ec2.redis import API
from ec2.utils.decorator    import * 
from ec2.conf.enabled import redis_conf


#from ec2.utils.logger  import NoseLogging as logger
#logger.start()
    


@filters( has_keys('pid', 'key') )
def foo(ctrl,message):
    return True

@filters( has_keys('pid',), pid2rcd('aaa') )
def foo2(ctrl,message):
    return message


class DecoratorTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')

    def tearDown(self):
        self._clear_keys()        
           
    def _clear_keys(self):
        for k in self.db._redis.keys('test:*'):
            self.db._redis.delete(k)

    
    @tools.raises(WarningErr)
    def testMsgNeed_1(self):
        foo(None,{})

    @tools.raises(WarningErr)
    def testMsgNeed_2(self):
        foo(None, {'_pid':None,})

    @tools.raises(WarningErr)
    def testMsgNeed_3(self):
        foo(None, {'pid':None,})

    @tools.raises(WarningErr)
    def testMsgNeed_4(self):
        tools.eq_(True, foo(None, {'pid':None,'key':None,}))

    def testMsgNeed_5(self):
        tools.eq_(True, foo(None, {'pid':1,'key':'a',}))

    @tools.raises(WarningErr)
    def testPid2Rcd_1(self):
        foo2(self, {})

    @tools.raises(WarningErr)
    def testPid2Rcd_2(self):
        foo2(self, {'pid':1,})

    def testPid2Rcd_3(self):
        pid = self.db.insert_into('aaa',{'hello':'world'})
        tools.eq_('world', foo2(self, {'pid':pid,})['hello'])
    

