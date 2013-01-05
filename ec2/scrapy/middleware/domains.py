#coding=utf-8

import re
from scrapy.utils.httpobj import urlparse_cached

from ec2 import WarningErr


_domain_cache = {}
def domain_cached(cfg):
    _key = '|'.join(cfg)
    if not _domain_cache.get(_key,None):
        cfg = (d.replace('.', r'\.') for d in cfg)
        regex = r'^(.*\.)?(%s)$' % '|'.join(cfg)
        _domain_cache[_key] = re.compile(regex)
    return _domain_cache[_key]


class DomainsMiddleware(object):

    def process_request(self, request, spider):
        allowed_domains = request.meta.get('enable_domains',None)
        if not allowed_domains:            return
        
        rule = domain_cached(allowed_domains)

        if not self.should_follow(request,rule) :
            raise NotAllowedDomain
        
    def should_follow(self, request, rule):
        host = urlparse_cached(request).hostname or ''
        return bool(rule.search(host))

    
