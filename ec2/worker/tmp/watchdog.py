#coding=utf-8

import json, time
import logging

from ec2.utils import misc
from ec2.conf.enabled import ws_conf


class SendPing(object):
    def __call__(self, ctrl, message=None):
        rs = ctrl.db.select_all('chnls')
        for e in rs:
            if  not e.get('pid', None):  continue

            wd = self._set_flag(ctrl.db, e)
            ctrl.db.queue_push(e['pid'],    {
                'handler':  'client.PingHandler',
                'wd_pid':   wd,
            })
         
    def _set_flag(self, db, e):
        wd = db.insert_into('cache',{
            'chnl_pid':          e['pid'],       
        },10*60)
        db.expire({
            'src':          'cache:%s'%wd,
            'on_expired':    'expired.WatchdogChnl',
        },e.get('ping',60))
        return wd


class RecvPong(object):

    def __call__(self, ctrl, message=None):
        
        _wdog = message.get('watchdog',None)
        if not _wdog :
            logging.warning('>>> invalid pong|%s'%message)
            return
        
        ctrl.db.delete_from('cache', _wdog)

