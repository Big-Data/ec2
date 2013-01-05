#coding=utf-8

import json, time
import logging



#------------------------------------------
'''class BaseHandler(object):

    def _update(self, db, e,state):
        action = '_on_%s'%state
        if not hasattr(self,action):
            logging.warning('undefine action: msg|%s' %(e,) )
            return False
            
        return getattr(self, action)(db, e)
'''


#------------------------------------------
class ImageHandler(object):
    _limit = 10
    def __call__(self, ctrl, message=None):
        rs = ctrl.db.select_all('sz_images')
        skips,oks = [],[]
        for e in rs:
            _pid, _state = [ e.get(k,None) for k in ('pid','state') ]
            if not _pid: continue
            if _state in (None, 'error',):
                skips.append( _pid )
                continue
                
            oks.append(_pid)
            ctrl.db.queue_push('queue:srv',{
                'handler':      'image.%sHandler'%(_state.capitalize(),),
                'pid':    e['pid'],
            })

        for pid in skips:
            ctrl.db.delete_from( 'sz_images', pid )

        if len(oks)>self._limit: return

        ctrl.db.queue_push('queue:srv',{
            'handler':      'image.NewHandler',
            'num':          self._limit - len(oks),
        })


#-----------------------------------
class UserHandler(object):

    def __call__(self, ctrl, message=None):
        rs = ctrl.db.select_all('sz_users')
        skips,oks = [],[]
        for e in rs:
            _pid, _state = [ e.get(k,None) for k in ('pid','state') ]
            if not _pid: continue
            if _state in (None, 'error', 'finished'):
                continue
                
            oks.append(_pid)
            ctrl.db.queue_push('queue:srv',{
                'handler':  'user.%sHandler'%(_state.capitalize(),),
                'pid':      e['pid'],
            })

