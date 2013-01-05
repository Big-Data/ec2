#coding=utf-8

import json, time
import logging

from ec2.redis  import API
#from ec2.utils.decorator import *
from ec2.utils  import misc, decorator

db = API.db()

_default = {
    'url':              None,
    'page_begin':       None,
    'page_end':         None,
    'timeout':          4*3600,
    'queue':            'queue:cron',
    'cron_handler':     'proxylist.on_weblist',
    'response_handler': None,
}

_Conf = {
    'lonmen':   misc.apply({'url':  'http://www.loamen.com/ws/proxyservice.php',
                    'queue':    'queue:soap',
                    'cron_handler': 'proxylist.on_soaplist',
                },_default),

    'ct0592':   misc.apply({'url': 'http://www.ct0592.com/loadproxy.htm',
                    'response_handler': 'proxylist.on_resp_s0',
                }, _default), 
    
    '5753':   misc.apply({'url': 'http://www.5753.net/proxy/today.txt',
                    'timeout':  6*3600,
                    'response_handler': 'proxylist.on_resp_s10',
                }, _default), 
    
    'proxyhttp':misc.apply({'url': 'http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/%d',
                    'page_begin':  1, 'page_end':   10,
                    'response_handler': 'proxylist.on_resp_s20',
                }, _default), 
    
    'my-proxy':misc.apply({'url': 'http://proxies.my-proxy.com/proxy-list-%d.html',
                    'page_begin':  1, 'page_end':   11,
                    'response_handler': 'proxylist.on_resp_s50',
                }, _default), 
    
}


def _init_proxy(k,conf):
    db.update_table('cron:proxylist', k, misc.apply({
        'pid':  k,
        'table':        'conf:cron:proxylist',
        'retry':        3, #24*6*30*12
    },conf))

    API.expire({
        'pid':      k,
        'table':    'cron:proxylist',
    },5)    


def _init_check():
    db.update_table('cron:proxylist', 'checkurl', {
        'pid':      'checkurl',
        'table':    'conf:cron:proxylist',
        'retry':    3, #24*6*30*12
        'timeout':  10,
    
        'queue':    'queue:cron',
        'cron_handler': 'proxylist.on_checkurls',
    })
    API.expire({
        'pid':      'checkurl',
        'table':    'cron:proxylist',
    },5)    
    


def init_conf():
    for k,v in _Conf.items():
        _init_proxy(k,v)
    _init_check()



#------------------------------------------
@decorator.filters( decorator.has_keys('pid','table') )
def on_weblist(ctrl, message):
    pass

@decorator.filters( decorator.has_keys('pid','table') )
def on_soaplist(ctrl, message):
    pass

@decorator.filters( decorator.has_keys('pid','table') )
def on_checkurls(ctrl, message):
    pass





if __name__=='__main__':
    init_conf()
