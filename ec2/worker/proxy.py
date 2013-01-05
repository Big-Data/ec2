#coding=utf-8

from ec2.scrapy.xpool    import XPooler
from ec2.utils.decorator import *
from ec2.conf.enabled    import redis_conf
 
xpooler = XPooler(redis_conf)

#------------------------------------------
@filters( has_keys('proxy','status') )
def on_check(message):
    xpooler.check_proxy(message['proxy'], message['status']) 


@filters( has_keys('proxy','status') )
def on_update(message):
    _status = 'ok'      if  message['status']==200 else None
    _status = 'fail'    if not _status and message['status']/100 in (4,5) else _status 
        
    if not _status: return
    xpooler.update_quality(message['proxy'], _status) 
 

@filters( has_keys('proxy','status') )
def on_except(message):
    xpooler.update_qulity(message['proxy'], message['status'])


@filters( has_keys('key','value') )
def on_conf(message):
    if not xpooler.has_conf(message['key']): return

    xpooler.update_conf( message['key'], message['value'])

