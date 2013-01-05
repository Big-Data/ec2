#coding=utf-8

import json, time

class Handler(object):

    def __call__(self, ctrl, message=None):
        v = message.get('reload',None)
        if v is None:  return

        ctrl.set_reload( bool(v) )
        ctrl.feedback( json.dumps({
            'handler':   str(self.__class__),
            'success':   True,
        }) )
        
