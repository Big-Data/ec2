#coding=utf-8

from ec2.utils import misc

_default = {
        'port':     3306,
        'charset':  'utf8',
}

_Config = {
    'feed@local':    misc.apply({
        'host':     '127.0.0.1',
        'db':       'feed',
        'user':     'feed',
        'passwd':   'feed!@#',
    },_default),
    
    'feed@office-235':    misc.apply({
        'host':     '192.168.1.235',
        'db':       'feed',
        'user':     'feed',
        'passwd':   'feed!@#',
    },_default),
}


