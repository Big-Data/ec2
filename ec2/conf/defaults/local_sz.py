import copy

_base_header = {
    'Host': 'cgs1.stc.gov.cn',
    'Connection': 'keep-alive',
    'Referer': 'http://cgs1.stc.gov.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0) Gecko/20100101 Firefox/10.0', 
}


def _header(h={}):
    header = copy.deepcopy(_base_header)
    header.update(h)
    return header


_Config = {
    'data_path':    'd:/pylibs/ec2-0.5/ec2/data',
    'header':       _header,
}

