from nose import tools
import unittest, time
from ec2        import WarningErr 
from ec2.gevent import actor

#from ec2.utils.logger  import NoseLogging as logger
#logger.start()


_worker = actor.QueueWorker()
_worker.start()
_worker.join()
print '---- over ----'


