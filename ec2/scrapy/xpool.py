#coding=utf-8

from ec2.redis  import API
from ec2.redis  import cache
from ec2.utils.rand import random_ip


class XPooler(object):

    _DefaultConf = {
        'response_ok':      -1,
        'response_fail':    2,
        'response_except':  8,
                        
        'proxy_loading':    1.2,
    }
    def __init__(self, settings):
        self._dbname =  settings.get('xpool_db', 'cache')
        self._holding = cache.SetCache('cache','proxy_holding', 60*60)
        self._caching = cache.ZsetCache('cache','proxy_caches', 4*60*60)
        self._xfwd =    cache.HashCache('cache','proxy_xfwd',   24*60*60)

        self._conf =  self._DefaultConf.copy()
        self._redis = API.redis(self._dbname)



    #-use for update
    def check_proxy(self, ip, is_good):
        if not is_good:
            self._holding.sadd(ip)
            return

        if ip in self._holding:  return
        self._caching.zincrby( ip, 0)

    def update_qulity(self, ip, what=None):
        weight = self._conf.get('response_%s'%what,None)
        if weight is None:  return

        self._caching.zincrby( ip, weight)


    #-httpproxy--------------------------------
    def select_proxies(self, limit=1):
        return self._caching.zrangbyscore(0, 'inf', start=0, num=limit)        

    def query_xfwd(self,ip):
        xfwd = self._xfwd.hget(ip)
        if not xfwd:
            xfwd = random_ip()
            self._xfwd.hset(ip, xfwd)
        
        return xfwd

    #-for settings---------------------------
    def has_conf(self, key):
        return self._conf.has_key(key)

    def update_conf(self,k,v):
        self._conf[k] = v
