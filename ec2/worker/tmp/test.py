#coding=utf-8

import json, time
import logging


#------------------------------------------
def dump(ctrl, message):
    print message





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

