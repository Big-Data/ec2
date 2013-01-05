#coding=utf-8

import json, time
import logging

class Handler(object):

    def __call__(self, ctrl, message=None):
        logging.info('>>> ts|%s  msg|%s'%(int(time.time()),message))
        
