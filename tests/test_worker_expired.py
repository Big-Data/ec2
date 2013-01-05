from nose import tools
import unittest, time
from ec2        import WarningErr
from ec2.redis  import API
from ec2.worker import expired    

#from ec2.utils.logger  import NoseLogging as logger
#logger.start()




class ExpiredTest(unittest.TestCase):

    def setUp(self): 
        self.db = API.db('default')

    def tearDown(self):
        self._clear_keys()        
           
    def _clear_keys(self):
        self.db.redis().delete('ExpiredPool')
        for k in self.db.redis().keys('test:*'):
            self.db.redis().delete(k)

    
    @tools.raises(WarningErr)
    def testHandler_1(self):
        expired.handler(None, {})

    @tools.raises(WarningErr)
    def testHandler_2(self):
        expired.handler(None, {'pid':None,})

    @tools.raises(WarningErr)
    def testHandler_3(self):
        expired.handler(self, {'pid':1,'table':None})

    def testHandler_4(self):
        pid = self.db.insert_into('aaa',{'hello':'world'})
        tools.eq_(-2, expired.handler(self, {'pid': pid,'table':'aaa'}))
        tools.eq_({}, self.db.select_from('aaa', pid))

    def testHandler_5(self):
        pid = self.db.insert_into('aaa',{'retry': 2})
        tools.eq_(-2, expired.handler(self, {'pid': pid,'table':'aaa'}))
        tools.eq_({}, self.db.select_from('aaa', pid))

    def testHandler_6(self):
        pid = self.db.insert_into('aaa',{'retry': 2, 'queue': 'task',})
        tools.eq_(-2, expired.handler(self, {
            'pid': pid,
            'table':'aaa',
        }))
        tools.eq_({}, self.db.select_from('aaa', pid))

    def testHandler_7(self):
        tools.eq_(0, self.db.redis().llen('ExpiredPool') )
        pid = self.db.insert_into('aaa',{'retry': 2, 'queue':'task','timeout': 1,})
        tools.eq_(None, expired.handler(self, {
            'pid': pid,
            'table':'aaa',
        }))
        tools.eq_( '1', self.db.select_from('aaa', pid)['retry'])

        time.sleep(4)
        
        #tools.eq_(1, self.db.redis().llen('ExpiredPool') )
        tools.eq_('{"table": "aaa", "pid": 1}',  self.db.redis().rpop('test:task') )

