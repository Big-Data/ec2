#coding=utf-8

class _BaseErr(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return  repr(self.msg)



class WarningErr(_BaseErr):  pass
class NotAllowedDomain(_BaseErr): pass


def _enum(*evts):
    evts = list( e.upper() for e in evts )
    return type( 'Enum', (), dict(zip(evts,evts)) )

signals = _enum(
    'INIT',  'RETRY', 'STOP', 'ERROR',
    'RECV',  'RESPONSE',   
)



