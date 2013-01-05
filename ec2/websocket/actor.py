#coding=utf-8

import logging
from ec2.gevent.actor   import Actor


class BasePuller(Actor):
    def __init__(self, ws,   retry=10,  debug=False):
        Actor.__init__(self, retry, debug)
        self._ws = ws

    def send(self,message):
        self._ws.send(message)

    def stop(self):
        self.running = False 
        #if self._ws.sock is None:
        #    return

        self._ws.close()

