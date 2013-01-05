#coding=utf-8


def makelist(data): # This is just to handy
    if isinstance(data, (tuple, list, set)): return list(data)
    elif data: return [data]
    else: return []


def apply( m,default):
    cfg = {}
    cfg.update(default)
    cfg.update(m)
    return cfg

def list2map(rs,key):
    m ={}
    for e in rs:
        m[ str(e[key]) ] = e
    return m

def json_decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = json_decode_list(item)
        elif isinstance(item, dict):
            item = json_decode_dict(item)
        rv.append(item)
    return rv

def json_decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
           key = key.encode('utf-8')
        if isinstance(value, unicode):
           value = value.encode('utf-8')
        elif isinstance(value, list):
           value = json_decode_list(value)
        elif isinstance(value, dict):
           value = json_decode_dict(value)
        rv[key] = value
    return rv









_pow62 = '32103210321032103210321032103210'
_map62 = dict(zip(
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',range(62)
))
_map62_rv = dict(zip(
    range(62),'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
))

def decode62( s ):
    r = ( 62**int(e) for e in _pow62[-len(s):])
    x = [ a*b  for a,b in zip((_map62[e] for e in s),r) ][::-1]
    x = [ sum(x[i*4:i*4+4]) for i in xrange((len(x)+3)/4) ][::-1]
    x = [ '%07d'%e for e in x ]
    return ''.join(x).lstrip('0')

def encode62( s ):
    s = s[::-1]
    x = ( s[i*7:i*7+7] for i in xrange((len(s)+6)/7) )
    rs =[]
    for e in x:
        _buf = []
        e = e[::-1]
        v = int( ''.join(e) )
        while v>0:
            _buf.append( _map62_rv[v%62] )
            v = v/62
        for _ in xrange( 4-len(_buf)):
            _buf.append('0')
        _buf.reverse()
        rs.append(''.join(_buf))
    rs.reverse()
    return ''.join(rs).lstrip('0')


class LazyLog(object):
    def __init__(self, limit=1):
        self._limit = limit
        self._num = 0

    def __call__(self, fn, *args):
        if self._num==0:
            fn( *args )
            
        self._num = (self._num+1)%self._limit
            
    

if __name__=='__main__':
    pass
