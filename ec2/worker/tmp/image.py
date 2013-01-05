#coding=utf-8
from gevent import monkey;monkey.patch_all()

import json, time, copy
import logging
import urllib2
from ec2.utils import urllib
from ec2.dm.captcha import Decoder
from ec2.conf.enabled import sz_conf


opener = urllib2.build_opener(
    urllib.MyCookieProcessor,
)
urllib2.install_opener(opener) 


#------------------------------------------
'''class BaseHandler(object):

    def _update(self, db, e,state):
        action = '_on_%s'%state
        if not hasattr(self,action):
            logging.warning('undefine action: msg|%s' %(e,) )
            return False
            
        return getattr(self, action)(db, e)
'''


#------------------------------------------
class NewHandler(object):

    def __call__(self, ctrl, message=None):

        num = message.get('num',None)
        if not num: return

        for _ in xrange(num):
            pid = ctrl.db.insert_into('sz_images',{
                'state':    'init',    
            },60*60)
            ctrl.db.queue_push('queue:srv',{
                'handler':      'image.InitHandler',
                'pid':    pid,
            })



class InitHandler(object):
    
    _url = 'http://cgs1.stc.gov.cn/ValidateCode_SANXUE.aspx'
    def __call__(self, ctrl, message=None):

        pid = message.get('pid',None)
        if not pid: return

        req = self._make_request(self._url)
        
        try:
            resp = urllib2.urlopen(req,req.get_data())
        except:
            return
        
        e = self._read(req, resp, ctrl.db, needsid=(sid is None))
        if not e : return
        
        ctrl.db.update_table('sz_images', pid, e)
        ctrl.db.queue_push('queue:srv',{
            'handler':      'image.%sHandler'%(e['state'].capitalize(),),
            'pid':          pid,
        })

    def _make_request(self, url, h={}, d=None, p=None):
        header = copy.deepcopy(sz_conf['header'])
        header.update(h)
        data = urllib.make_data(d) if d else None
        request = urllib2.Request( url, data, header)
        
        if p:
            t,_,_,h = urllib2._parse_proxy(p)
            request.set_proxy(h,t)

        return request
    
    def _read(self , req, resp, db):
        body=None
        try:
            body = resp.read()
        except:
            return
        
        _needsid = not 'ASP.NET_SessionId' in req.header.get('Cookie','')
        if not body or ( _needsid and not resp._sid ):
            logging.debug('>>> body is null or missing _sid!')
            return

        _code = urllib.md5_code(body)
        if db.redis().sismember(db.ns_of('image_cache'), _code):
            logging.debug('>>> image exist!')
            return
        
        db.redis().sadd(db.ns_of('image_cache'), _code)
        e = {
            'body':     body,
            'state':    'decode',
        }
        if _needsid:    
            e['sid'] =          resp._sid
            e['cookie_ts'] =    int(time.time())
        
        return e

    
   
#-----------------------------------
class ReInitHandler(InitHandler):
    
    def __call__(self, ctrl, message=None):
        pid = message.get('pid',None)
        if not pid: return
        
        img = ctrl.db.select_fields('sz_images', pid, ['sid','cookie_ts',])
        if not self._is_valide(img):
            logging.debug('>>> reinit skip|%s'%pid)
            ctrl.db.delete_from('sz_images', pid)
            ctrl.db.queue_push('queue:srv',{
                'handler':      'image.NewHandler',
                'num':          1,
            })
            return

        req = self._make_request(self._url,h={
            'Cookie':'ASP.NET_SessionId=%s'%img['sid'],
        })
        
        try:
            resp = urllib2.urlopen(req,req.get_data())
        except:
            return
        
        e = self._read(req, resp, ctrl.db)
        if not e : return
        
        logging.debug( '>>> reinit ok|%s'%pid )
        ctrl.db.update_table('sz_images', pid, e)
        ctrl.db.queue_push('queue:srv',{
            'handler':      'image.%sHandler'%(e['state'].capitalize(),),
            'pid':          pid,
        })

    def _is_valide(self,img):
        return  img['sid'] and img['cookie_ts'] and \
                int(time.time()) - int(img['cookie_ts']) < 30*60

        
#-----------------------------------
class DecodeHandler(object):
    _decoder = Decoder(path=sz_conf['data_path'])

    def __call__(self, ctrl, message=None):
        pid = message.get('pid',None)
        if not pid :
            logging.warning('>>> pid is empty|%s'%message)
            return

        e,_sid = ctrl.db.select_fields('sz_images', pid, ['body','sid',])
        if not e['body']:
            logging.warning('>>> body is empty|%s'%message)
            return

        code = self._decoder.img2code( e['body'] )
        if not code:
            logging.debug('>>> cannot decode image')
            ctrl.db.update_table('sz_images',pid, {
                'state':    'reinit',
            })
            ctrl.db.queue_push('queue:srv',{
                'handler':      'image.ReinitHandler',
                'pid':          pid,
            })
            return

        ctrl.db.update_table('sz_images', pid, {
            'code':     code,
            'state':    'valide',
        })
        ctrl.db.queue_push('queue:srv',{
            'handler':      'image.ValideHandler',
            'pid':    pid,
        })



class ValideHandler(object):

    def __call__(self, ctrl, message=None): pass
        #rand user ,query check


class OkHandler(object):

    def __call__(self, ctrl, message=None): pass
        #check timeout

#-----------------------------------
if __name__=='__main__':
    pass