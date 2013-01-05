#coding=utf-8

#from scrapy import log
from scrapy.http import HtmlResponse
from scrapy.utils.url import urljoin_rfc
from scrapy.utils.response import get_meta_refresh

from scrapy.contrib.downloadermiddleware.redirect import RedirectMiddleware



class RedirectExMiddleware(RedirectMiddleware):

    def process_response(self, request, response, spider):
        redirected,status = self._check_redirect(request, response)
        if  not redirected:      return response
        
        if 'dont_redirect' in request.meta : return response
        
        return self._redirect(redirected, request, spider, status)

    def _check_redirect(self, request, response):
        if request.method.upper() == 'HEAD':
            if response.status in [301, 302, 303, 307] and 'Location' in response.headers:
                redirected_url = urljoin_rfc(request.url, response.headers['location'])
                redirected = request.replace(url=redirected_url)
                return redirected,response.status
            else:
                return None,None

        if response.status in [302, 303] and 'Location' in response.headers:
            redirected_url = urljoin_rfc(request.url, response.headers['location'])
            redirected = self._redirect_request_using_get(request, redirected_url)
            return redirected,response.status

        if response.status in [301, 307] and 'Location' in response.headers:
            redirected_url = urljoin_rfc(request.url, response.headers['location'])
            redirected = request.replace(url=redirected_url)
            return redirected,response.status

        if  request.meta.get('meta_refresh',None) and  \
            isinstance(response, HtmlResponse):
            interval, url = get_meta_refresh(response)
            if url and interval < self.max_metarefresh_delay:
                redirected = self._redirect_request_using_get(request, url)
                return redirected,'meta refresh'

        return None,None

