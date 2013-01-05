#coding=utf-8
import time, logging
import traceback
import functools

from pydispatch.robustapply import robustApply

from ec2 import WarningErr
from ec2.utils  import misc


#--------------------------------------
def retry(ExceptionToCheck, errcb=None, tries=3, delay=1, backoff=2):
    """Retry decorator
    original from http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            try_one_last_time = True
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                    try_one_last_time = False
                    break
                except ExceptionToCheck, e:
                    if bool(errcb): errcb(*args, **kwargs)

                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            if try_one_last_time:
                return f(*args, **kwargs)
            return
        return f_retry # true decorator
    return deco_retry


#----------------------------------------
def pid2rcd(table=None):
    def wrapper(fun):
        @functools.wraps(fun)
        def _wrapper(ctrl, message):
            _table = table if table else message.get('table',None)
            if not _table:
                raise WarningErr('table is none, msg|%s'%message)

            rs = ctrl.db.select_from(_table, message['pid'])
            if not rs:
                raise WarningErr('missing rcd: table|%s, pid|%s'%(
                    _table,message['pid'],
                ))
            
            message.update(rs)
            return fun(ctrl,message)
        return _wrapper
    return wrapper


def has_keys(*ks):

    def wrapper(fun):        
        @functools.wraps(fun)
        def _wrapper(ctrl, message):
            if not message:
                raise WarningErr('message is None')
            
            for k in ks:
                if not message.get(k,None) is None : continue
                raise WarningErr('missing field|%s, msg|%s'%(
                    k, message    
                ))
            return fun(ctrl, message)    
        return _wrapper
    return wrapper

def filters(*plugins):
    def wrapper(fun):    
        @functools.wraps(fun)
        def _wrapper(*args, **kwds):
            callback = fun
            _cb = misc.makelist(plugins)
            _cb.reverse()

            for e in _cb:
                callback = e(callback)    
            return callback(*args,**kwds)

        return _wrapper
    return wrapper

#--------------------------------------
def safe_method(debug=True, silent=False):
    def wrapper(fun):
        @functools.wraps(fun)
        def _wrapper(*args,**kwds):
            try:
                return  robustApply(fun, *args, **kwds)
            except Exception,e:
                if debug:
                    traceback.print_exc()
                if not silent:
                    raise WarningErr(str(e))

        return _wrapper
    return wrapper