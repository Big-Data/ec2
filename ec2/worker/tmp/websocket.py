#coding=utf-8

import json, time
import logging

#from ec2.redis import actor
from ec2.utils.decorator import *

#------------------------------------------
@filters( has_keys('pid','table') )
def handler(ctrl, message):
    _db = message.get('db', 'default')
    _ns = ctrl.db.ns_of( message['table'], message['pid'])
    _retry = ctrl.db.redis(_db).hincrby( _ns , 'retry', -1)
    if  _retry<1 :
        ctrl.db.redis(_db).delete( _ns )
        return -1

    _queue = message.get('queue', None)
    _timeout = message.get('expire', None)
    if  not _queue or \
        _timeout==None or int(_timeout)<1:
        ctrl.db.redis(_db).delete( _ns )
        return  -2        #'%s|%s'%(_queue,_timeout)

    ctrl.db.expire(message, _timeout)
    ctrl.db.queue_push( _queue, {
        'pid':      message['pid'],
        'table':    message['table'],    
    }, dbname=_db )







'''
class WatchdogChnl(object):
    
    def __call__(self, ctrl, message=None):
        _db = message.get('db', 'default')
        _src = message.get('src', None)
        if not _src:    return

        e = ctrl.db.new_db(_db).select_from(_src, None) #
        if not e or not e.get('chnl_pid',None):   return

        logging.warning('>>>watchdog raise|%s'%message)
        ctrl.db.new_db(_db).delete_from('chnls', e['chnl_pid'] )
        
'''       

