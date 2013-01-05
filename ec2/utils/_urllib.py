#coding=utf-8

import urllib2,re, random
import hashlib 



class MyCookieProcessor(urllib2.BaseHandler):

    SidRule = re.compile('ASP\.NET_SessionId=(.+?);')
    def http_request(self, request):
        return request

    def http_response(self, request, response):
        sid = self._session_id(response)
        response._sid = sid
        
        return response

    
    def _session_id(self, response):
        rs = response.headers.get('Set-Cookie', None) or ''
        rs = self.SidRule.findall(rs)
        if not rs:  return 
        return rs[0]

    https_request = http_request
    https_response = http_response


#def rand_proxy():
#    proxy =  random.choice(Data.proxies)
#    return proxy

def _make_data( e ):
    rs = ( '%s=%s'%(k,urllib2.quote(v),) for k,v in e.items() )
    return '&'.join(rs)

def md5_code(s):
    m = hashlib.md5() 
    m.update(s) 
    return m.hexdigest() 

def make_request(url, header={}, data=None, proxy=None):
    #header = copy.deepcopy(sz_conf['header'])
    #header.update(h)
    data = _make_data(data) if data else None
    request = urllib2.Request( url, data, header)
        
    if not proxy:   return request

    t,_,_,h = urllib2._parse_proxy(p)
    request.set_proxy(h,t)
    return request
