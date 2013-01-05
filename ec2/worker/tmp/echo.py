#coding=utf-8

import json, time
import logging

from ec2.utils import misc
from ec2.conf.enabled import ws_conf

class Handler(object):

    def __call__(self, ctrl, message=None):
        logging.debug('>>> msg|%s'%message)
        message.update({
            'handler':  str(self.__class__),
            'success':  True,
        })
        ctrl.feedback( json.dumps(message) )
        


class ClientPing(object):
    def __call__(self, ctrl, message=None):
        msg = misc.apply({
            'handler':  'echo.ServerPong',
            'ts':   int(time.time()),
        },ws_conf['default']),

        ctrl.feedback( json.dumps(msg) )
    

class ServerPong(object):

    def __call__(self, ctrl, message=None):
        _host,_w = [message.get(e,None) for e in ('host','weight',)]
        if not _host or not _w:
            logging.warning('>>> invalid client|%s'%message)
            return

        



