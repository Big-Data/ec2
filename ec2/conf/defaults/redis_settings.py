#coding=utf-8

from ec2.utils import misc

_default = {
        'port':     6379,
        'password': 'dfhe2004!@#',
        'db':0,
}

_Config = {
    'local':    misc.apply({'host': '127.0.0.1',},_default),

    'node@120': misc.apply({'host': '172.16.1.120',},_default),
    'node@122': misc.apply({'host': '172.16.1.122',},_default),

    'office@230': misc.apply({'host': '192.168.1.230',},  _default),
}

pre_db = 'ec2'
channel_timeout = 60
expiredpool_timeout = 5

worker_base = 'ec2.worker'
worker_debug = True
worker_reload = True



