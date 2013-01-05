#coding=utf-8

import json, time
import logging

from ec2.redis           import API
from ec2.utils.misc      import makelist
from ec2.utils.decorator import *

#------------------------------------------
@filters( has_keys('pid','table') )
def handler(ctrl, message):
    _name = message.get('db', 'default')
    _ns = API.ns_of( message['table'], message['pid'])
    
    src = API.db(_name)
    rs = src.select_from(message['table'], message['pid'])

    if  not rs: return -1
    
    if  not rs.get('queue',None)    or \
        not rs.get('timeout', None) or \
        not rs.get('cron_handler', None) or \
        not rs.get('retry', None):
        src.delete_from( message['table'], message['pid'] )
        return -2

    _retry = src.redis().hincrby( _ns , 'retry', -1)
    if  _retry<1 :
        src.delete_from( message['table'], message['pid'] )
        return -1

    API.expire(message, rs['timeout'])
    API.queue_push( rs['queue'], {
        'pid':      message['pid'],
        'table':    message['table'],
        'handler':  rs['cron_handler'],
    })



@filters( has_keys('value','set') )
def cache_set(ctrl, message):
    _name = message.get('db', 'default')
    API.redis(_name).srem( API.ns_of( message['set'] ) , message['value'] ) 


@filters( has_keys('field','hash') )
def cache_hash(ctrl, message):
    _name = message.get('db', 'default')
    API.redis(_name).hdel( API.ns_of( message['hash'] ), message['field'] ) 


@filters( has_keys('value','zset') )
def cache_zset(ctrl, message):
    _name = message.get('db', 'default')
    API.redis(_name).zrem( API.ns_of( message['zset'] ), message['value'] ) 



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

