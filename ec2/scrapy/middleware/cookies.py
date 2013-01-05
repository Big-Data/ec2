#coding=utf-8

try:
    import cPickle as pickle
except ImportError:
    import pickle

from scrapy import log
from scrapy.http import Response
from scrapy.http.cookies import CookieJar

from ec2.conf.enabled import scrapy_conf 
from ec2.redis import cache

class CookiesMiddleware(object):
    """This middleware enables working with sites that need cookies"""
    debug = scrapy_conf.getbool('COOKIES_DEBUG', False)

    def __init__(self):
        self._cache = cache.HashCache('cache', 'cookies', 3*24*3600)

    def _load_cookie(self,pid):
        value = self._cache.hget(pid)

        if not value:   return CookieJar()
        return pickle.loads(value) 

    def _update_cookie(self, user, jar):
        value = pickle.dumps(jar) 
        self._cache.hset(user, value)

    def _clear_cookie(self,user):
        self._cache.hdel(user)

    def process_request(self, request, spider):
        if not request.meta.get('enable_cookies', None): return
        
        pid = request.meta.get('cookie_pid', None)
        if not pid:    return
        
        if request.meta.get('clear_cookies', False):
            self._clear_cookie(pid)
            return

        jar = self._load_cookie(pid)
        cookies = self._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)
        self._debug_cookie(request)

    def process_response(self, request, response, spider):
        if not request.meta.get('enable_cookies',None):
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        pid = request.meta.get('cookie_pid', None)
        if not pid:    return response
        
        if response.headers.getlist('Set-Cookie'):
            jar = self._load_cookie(pid)
            jar.extract_cookies(response, request)

            self._update_cookie( pid, jar )
            self._debug_set_cookie(response)

        return response

    def _debug_cookie(self, request):
        """log Cookie header for request"""
        if self.debug:
            c = request.headers.get('Cookie')
            c = c and [p.split('=')[0] for p in c.split(';')]
            log.msg('Cookie: %s for %s' % (c, request.url), log.DEBUG)

    def _debug_set_cookie(self, response):
        """log Set-Cookies headers but exclude cookie values"""
        if self.debug:
            cl = response.headers.getlist('Set-Cookie')
            res = []
            for c in cl:
                kv, tail = c.split(';', 1)
                k = kv.split('=', 1)[0]
                res.append('%s %s' % (k, tail))
            log.msg('Set-Cookie: %s from %s' % (res, response.url),log.DEBUG)


    def _get_request_cookies(self, jar, request):
        headers = {'Set-Cookie': ['%s=%s;' % (k, v) for k, v in request.cookies.iteritems()]}
        response = Response(request.url, headers=headers)
        cookies = jar.make_cookies(response, request)
        return cookies

if __name__=='__main__':
    pass
