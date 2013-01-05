#coding=utf-8

import logging
import logging.handlers

class AssertingHandler(logging.handlers.BufferingHandler):

    def __init__(self,capacity):
        logging.handlers.BufferingHandler.__init__(self,capacity)

    def assert_logged(self,test_case,msg):
        msg = msg.strip()
        s = None
        for record in self.buffer:
            s = self.format(record).strip()
            if s == msg: 
                self.flush()        
                return
        
        test_case.assertTrue(False, '%s|%s'%(s,msg) )


class NoseLogging(object):
    _handler = AssertingHandler(1024)

    @staticmethod
    def start():
        logging.getLogger().addHandler(NoseLogging._handler)        

    @staticmethod
    def stop():
        logging.getLogger().removeHandler(NoseLogging._handler)        

    @staticmethod
    def eq_( tc, msg):
        NoseLogging._handler.assert_logged(tc,msg)




