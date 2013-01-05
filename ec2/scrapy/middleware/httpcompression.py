#coding=utf-8

from scrapy.contrib.downloadermiddleware.httpcompression import HttpCompressionMiddleware
from ec2.scrapy.middleware.transferencode import HttpTransferEncodingMiddleware


_chuncked = HttpTransferEncodingMiddleware()

class HttpCompressionExMiddleware(HttpCompressionMiddleware):

    def process_response(self, request, response, spider):
        response = _chuncked.process_response(request, response, spider)        
        return HttpCompressionMiddleware.process_response(self,request, response, spider) 
