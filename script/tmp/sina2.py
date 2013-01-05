#coding=utf-8

import re
from scrapy import log

try:
    from weibopy.api2   import API
except ImportError:
    pass


def client_factory(access_token):
    return API(access_token)

if __name__=='__main__':
    x = client_factory('2.00ANLgMCHpMJ1Cf70e0ef55ah_X3xC')
    #rs = x.user_timeline(uid='1813387710', count=2, page=12, trim_user=1)
    #rs = x.home_timeline(screen_name = 'hello_world_11', trim_user=1)
    rs = x.counts(ids='3486203020566941')
    x = rs[0]
    print dir(x)
    
    #print x.update_status(status=':-(')
