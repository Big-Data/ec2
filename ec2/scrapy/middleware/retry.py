#coding=utf-8

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware


class RetryExMiddleware(RetryMiddleware):

    def process_exception(self, request, exception, spider):
        if  not request.meta.get('enable_retry',None):    return
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            return self._retry(request, exception, spider)

