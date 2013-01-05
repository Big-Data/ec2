import logging, json
from gevent import monkey;monkey.patch_all()

import gevent
from bottle import run, debug, abort, request, response, get, post, route
from bottle.ext.websocket import GeventWebSocketServer
from ec2.websocket.server import Ctrlet
from ec2.redis  import API
from ec2.conf.enabled import ws_conf

logging.basicConfig(level=logging.DEBUG)


Chnls = set()

def channel(callback):
    def wrapper(chnl=None):
        if chnl is None: abort(404, "No queue given")
        callback(chnl)
    return wrapper


def websocket_ex(callback):
    def wrapper(*args, **kwargs):
        ws = request.environ.get('wsgi.websocket',None)
        if ws is None:  abort(400, 'Expected WebSocket request.')
        callback(ws, *args, **kwargs)
    return wrapper


#------------------------
@get('/test/echo/:msg')
def callback(msg):
    return msg

@get('/test/slow_echo/:msg')
def callback(msg):
    gevent.sleep(5)    
    return 'slow-%s'%msg


@get('/ws/')
def callback():
    return 'It works!'

@get('/ws/info')
def callback():
    return json.dumps({
        'chnls': len(Chnls),
    })

@get('/ws/chnl/:chnl', apply=[channel,websocket_ex,])
def callback(wsock, chnl = None):
    Chnls.add(wsock)
    logging.debug('>>> new|%s|%d'%(wsock,len(Chnls)))

    ctrl = Ctrlet(API.db(),'www:%s'%chnl,wsock)
    ctrl.start()
    Chnls.remove(wsock)
    logging.debug('>>> del|%s|%d'%(wsock,len(Chnls)))


debug(True)
_host,_port = ws_conf['server'].split(':')
run(host=_host, port=_port, server=GeventWebSocketServer)

