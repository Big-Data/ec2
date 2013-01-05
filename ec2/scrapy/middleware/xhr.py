"""
RefererMiddleware: populates Request referer field, based on the Response which
originated it.
"""

class XhrMiddleware(object):

    def process_request(self, request, spider):
        if not request.meta.get('enable_xhr', None):  return
        
        request.headers.setdefault('X-Requested-With', 'XMLHttpRequest')
