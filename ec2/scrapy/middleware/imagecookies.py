import urlparse

import re
from scrapy import signals
from scrapy.http import Response
from scrapy.conf import settings
from scrapy import log

ImageRule = re.compile('ULOGIN_IMG=(\d+);')

class ImageCookiesMiddleware(object):

    def process_response(self, request, response, spider):
        if 'dont_merge_cookies' in request.meta:
            return response
        if not request.meta.has_key('image_id'):    return response

        cl = response.headers.getlist('Set-Cookie')
        for c in cl:
            image_id = ImageRule.findall(c)
            if not image_id: continue

            request.meta['image_id'] = image_id[0]
            log.msg('Image Set-Cookie: %s' % (image_id[0],),log.DEBUG)

        return response
