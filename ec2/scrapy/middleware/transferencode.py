from scrapy import log
from scrapy.http import Response, TextResponse
try:
    from scrapy.core.downloader.responsetypes import responsetypes
except ImportError:
    from scrapy.responsetypes import responsetypes

CRLF = '\r\n'

class HttpTransferEncodingMiddleware(object):
    """This middleware allows merge chunked blockes to one to be
    received from web sites"""

    def process_request(self, request, spider):
        pass

    def process_response(self, request, response, spider):
        if not isinstance(response, Response): return response

        transfer_encoding = response.headers.getlist('Transfer-Encoding')
        if not  transfer_encoding:  return response

        encoding = transfer_encoding.pop()
        decoded_body = self._decode(response.body, encoding.lower())
        respcls = responsetypes.from_args(
            headers=response.headers, 
            url=response.url
        )
        kwargs = dict(cls=respcls, body=decoded_body)
        if issubclass(respcls, TextResponse):
            # force recalculating the encoding until we make sure the
            # responsetypes guessing is reliable
            kwargs['encoding'] = None
        response = response.replace(**kwargs)
        if not transfer_encoding:
            del response.headers['Transfer-Encoding']

        return response

    def _decode(self, body, encoding):
        if encoding != 'chunked':   return body

        value = []
        search_start = 0
        while True:
            crlf_pos = body.find(CRLF, search_start)
            if crlf_pos == 0:
                break
            head = body[search_start:crlf_pos]
            semi_colon_pos = head.find(';')
            if semi_colon_pos >= 0:
                head = head[:semi_colon_pos]
            chunk_len = int(head, 16)
            if chunk_len <= 0:
                break
            value.append(body[crlf_pos + 2:crlf_pos + 2 + chunk_len])
            search_start = crlf_pos + 2 + chunk_len  + 2; # tail 2 is chunk boundary
        body = ''.join(value)
        
        return body


