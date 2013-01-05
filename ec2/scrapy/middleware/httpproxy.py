#coding=utf-8

from scrapy import log
from scrapy.selector import HtmlXPathSelector

from ec2        import NotAllowedDomain
from ec2.redis  import API, cache


class HttpProxyMiddleware(object):

    _KEYS = {
            'response': ('url','body','encoding','flags','headers','meta','status','url'),
            'request':  ('url','method','meta'),
    }
    _CITICAL_EXCEPTIONS = (NotAllowedDomain,)

    def process_response(self, request, response, spider):
        if not 'proxy' in request.meta:     return response

        proxy = request.meta['proxy']
        if request.meta.get('check_proxy',None):
            self._on_check_proxy(proxy,response)
        else:
            self._on_normal_case(proxy,request,response)
        return response

    def process_exception(self, request, exception, spider):
        if not 'proxy' in request.meta:   return
        
        proxy = request.meta['proxy']

        if request.meta.get('check_proxy',None):
            self._send({
                'handler':  'proxy.on_check',
                'proxy':    proxy,
                'status':   False,
            })
            return

        _status = 'except' if isinstance(exception, self._CITICAL_EXCEPTIONS) else 'fail'
        self._send({
            'handler':  'proxy.on_except',
            'proxy':    proxy,
            'status':   _status,
        })
        
    def _send(self, msg):
        API.queue_push( 'queue:proxy', msg, 'cache')

    def _on_check_proxy(self, proxy, response):
        _status = bool(response.status in (200,))
        if _status:
            hxs = HtmlXPathSelector(response)
            _status = bool('百度' in xpath.extract(hxs, '//title/text()'))
        
        self._send({
            'handler':  'proxy.on_check',
            'proxy':    proxy,
            'status':   _status,
        })
        
    def _on_normal_case(self, proxy,request, response):
        self._send({
            'handler':  'proxy.on_update',
            'proxy':    proxy,
            'status':   response.status,
        })
        
if __name__=='__main__':
    pass
