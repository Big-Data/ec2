#coding=utf-8
from gevent import monkey;monkey.patch_all()

import json, time, copy
import logging
import urllib2
from ec2.utils import urllib
from ec2.dm.captcha import Decoder
from ec2.conf.enabled import sz_conf


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
class InitHandler(object):
    
    _url = 'http://cgs1.stc.gov.cn/Login.aspx'
    def __call__(self, ctrl, message=None):

        pid = message.get('pid',None)
        if not pid: return

        req = urllib.make_request(self._url)
        
        try:
            resp = urllib2.urlopen(req,sz_conf['header']())
        except:
            return
        
        e = self._read(req, resp)
        if not e : 
            logging.info('warning: init, can not find x,y!')
            return
        
        e['state'] = 'prelogin'    
        ctrl.db.update_table('sz_users', pid, e)
        ctrl.db.queue_push('queue:srv',{
            'handler':      'user.%sHandler'%(e['state'].capitalize(),),
            'pid':          pid,
        })

    def _read(self , req, resp, db):
        body=None
        try:
            body = resp.read()
        except:
            return
        
        if not body:
            logging.info('>>> body is null!')
            return

        hxs = xpath.body2hxs(body)
        x = xpath.extract(hxs,'//input[@id="__VIEWSTATE"]/@value')
        y = xpath.extract(hxs,'//input[@id="__EVENTVALIDATION"]/@value')
        if not x or not y: 
            return 

        return {
            '__VIEWSTATE':          x,
            '__EVENTVALIDATION':    y,
        }

#------------------------------------------
class PreloginHandler(object):
    
    _url = 'http://cgs1.stc.gov.cn/Login.aspx'
    def __call__(self, ctrl, message=None):

        pid = message.get('pid',None)
        if not pid:     return
        user = ctrl.db.select_from('sz_users', pid)
        if not user:    return 

        sid = self._get_sid(ctrl.db)
        if not sid:
            logging.info('>>> shortage sid!')
            ctrl.db.queue_push('queue:srv',{
                'handler':      'image.NewHandler',
                'num':          1,
            })
            
            return

        req = urllib.make_request(self._url,
            header = sz_conf['header']({
                'Cookie':'ASP.NET_SessionId=%s'%_sid
            }),
            data = {
                '__VIEWSTATE':  user['__VIEWSTATE'],
                '__EVENTVALIDATION': user['__EVENTVALIDATION'],
                'userCode': user['pid'],  
                'userPassword': user['pwd'],                   
                'txtVail':  sid['code'],                
                'Button1':  '',                             
            }
        )
        




pids = self.redis().smembers(self._ns['task']%'login_s0')
        print 'login_s1:\t%s'%len(pids)
        
        sids = self.redis().smembers(self._ns['sid']%'check')
        
        rs = []
        for pid,sid in zip(pids,sids):
            user = self.db().select_from('users',pid)
            sid = self.db().select_from('images',sid)

            header = copy.deepcopy(Data.base_header)
            header.update({
                'Cookie':'ASP.NET_SessionId=%s'%sid['pid'],
            })
            data = self._make_data({
                '__VIEWSTATE':  user['__VIEWSTATE'],
                '__EVENTVALIDATION': user['__EVENTVALIDATION'],
                'userCode': user['pid'],  
                'userPassword': user['pwd'],                   
                'txtVail':  sid['code'],                
                'Button1':  '',                             
            })

            request = urllib2.Request( self._urls['s0'], data, header)
            proxy =  random.choice(self.proxies)
            t,_,_,h = urllib2._parse_proxy(proxy)
            request.set_proxy(h,t)
            request._user = user

            rs.append( (rs,self._login_cb ))

        for body in Pool.imap(fetch2, rs):
            if body is None: continue






    
   
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