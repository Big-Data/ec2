from nose import tools
import unittest, time
from ec2    import WarningErr
from ec2.utils import decorator 

    

class A(object):

    @decorator.safe_method(debug=False)
    def err(self):
        return 1/0
    
    @decorator.safe_method(debug=False)
    def err2(self):
        return 1/0
    
    @decorator.safe_method(debug=False,silent=True)
    def err3(self):
        return 1/0
    
#----------------------------------------
class DecoratorTest(unittest.TestCase):
    
    def setUp(self): 
        pass

    def tearDown(self):
        pass
        
    @tools.raises(WarningErr)
    def testMsgNeed_1(self):
        a = A()
        a.err()

    
    @tools.raises(WarningErr)
    def testMsgNeed_2(self):
        a = A()
        a.err2()

    def testMsgNeed_3(self):
        a = A()
        a.err3()



