from nose import tools
import unittest, time
from ec2    import WarningErr,signals
from ec2.utils import event , decorator
    
class A(object):
    
    def fire_init(self):
        event.send(signal=signals.INIT,sender=self)

    def fire_recv(self):
        event.send(signal=signals.RECV,sender=self, message='hello')

    def fire_stop(self):
        event.send(signal=signals.STOP,sender=self)

def on_init():
    pass

def on_recv(message):
    pass

@decorator.safe_method()
def on_stop():
    pass

a = A()

event.connect( on_init, signal=signals.INIT, sender=a)
event.connect( on_recv, signal=signals.RECV, sender=a)
event.connect( on_stop, signal=signals.STOP, sender=a)



#----------------------------------------
class DecoratorTest(unittest.TestCase):
    

    def setUp(self): 
        pass

    def tearDown(self):
        pass
        
    
    def testInit(self):
        a.fire_init()
        a.fire_recv()
        a.fire_stop()
