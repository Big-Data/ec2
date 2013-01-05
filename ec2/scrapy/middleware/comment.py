#coding=utf-8

class RefererMiddleware(object):

    def process_request(self, request, spider):
        referer = request.meta.get('header_referer', None)
        if not referer: return
        
        request.headers.setdefault('Referer', referer)

