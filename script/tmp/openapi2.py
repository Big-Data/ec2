#coding=utf-8

import time, json
from collections import defaultdict

from ec2.utils import misc
from ec2.redis.core import TestTask
from ec2.tw.sina import client_factory,oauth_clients,get_oauth_client, bind_api
from ec2.utils.redis import * 

#-------------------------------------------------
class OpenApiTask(TestTask):
    def client(self,app,nice):
        return client_factory(app, nice, self.db())

    def me(self, app, nice):
        return self.client(app,nice).api.me()
    
    def trends_daily(self,client):
        rs = client.api.trends_daily()
        rs = ( e['query'] for e in rs['trends'].values()[0] )
        return ( e.encode('utf-8', 'ignore') for e in rs )
    
    def user_info(self,client,**kwds):
        _kwds={}
        for k in ('screen_name', 'user_id'):
            if not kwds.has_key(k): continue
            _kwds[k] = kwds[k]
            break
        if not _kwds:   return None
        return client.api.get_user(**_kwds)

    def feed_info(self,client,*mids):
        if not mids: return
        mids = ( str(e) for e in mids)
        return client.api.counts(ids=','.join(mids))

    def ws_follows(self,client):        
        ws = {
            '1813387710': set(),
            '1927394535': set(),
            '1927388525': set(),
        }
        
        #fh = open('d:/temp/ws_follows.txt' , 'w')
        for k,v in ws.items():
            cursor = (0,1)
            
            while cursor[1]>0:
                rs,cursor = client.api.followers_ids(user_id=k,cursor=cursor[1] )
                print '%s - %s' % (k, cursor[1])
                for e in rs['ids']:
                    v.add(e)
                    #fh.write('%s|%s|%s\n' %(k,cursor,e))

                #fh.flush()
                time.sleep(2)
        #fh.close()

        for k1 in ws.keys():
            for k2 in ws.keys():
                if k1<=k2: continue

                print '%s,%s = %s' % (k1,k2, len(ws[k1].intersection(ws[k2])) )

        v = ws.values()
        print 'total intersection: %s' % len(
            v[0].intersection(v[1]).intersection(v[2])        
        )

    def publish(self,client, txt):
        return client.api.update_status(txt)

    def repub(self,client,mid, txt):
        args = {
            'in_reply_to_status_id': mid,
            'status':  txt ,
        }
        return client.api.update_status(**args)


    def pub_image(self, client, img_data, img_type, txt):
        from ec2.utils import rand
        return client.api.upload_data(img_data, 'image/%s'%img_type, '/temp/%s.%s'%(
             rand.random_alpha(8),
             img_type
        ),txt)

        

    def detail_follows(self,client, uid):
        fh = open('%s_follows.txt'%uid , 'w')
        cursor = 1
        v = []
        
        while cursor>0 :
            rs, cur = client.api.followers(user_id=uid,cursor=cursor,count=500 )
            if cur[1]==0 or not rs:  break

            for e in rs:
                v.append(e)
                fh.write('%s|%s\t %s|%s|%s|%s\n'%(
                    int(e.id), e.name.encode('utf8','ignore'),
                    int(e.province), int(e.city), e.location.encode('utf8','ignore'),
                    e.gender.encode('utf8','ignore')
                ))

            fh.flush()
            print cur 
            cursor = cur[1]
            time.sleep(2)
        
        fh.close()
        return v

    def _write_user(self, fh, user):
        fh.write('%s|%s|%s|%d-%s|%s\t\n'%(
            user.id, 
            user.name.encode('utf8','ignore'),
            user.gender.encode('utf8','ignore'),
            user.followers_count,
            user.verified,
            user._txt,
        ))
        fh.flush()
    
    def _write_feed(self, fh, feed):
        fh.write('%s|%s|%s|%s\n'%(
            feed['id'], 
            feed['_ts'], 
            feed['_ca'], 
            feed['_txt'],
        ))
        fh.flush()

    def repost_timeline(self, client, fid, limit):
        mid = misc.decode62(fid) 
        fh = open('%s_repost.txt'%fid , 'a')
        kwds = {
            'id':   mid,
            'count': 100,
            'page': 1,
        }
        buf = []
        #while True:    
        for _ in xrange(1):        
            rs = client.api.repost_timeline(**kwds) or list()
            print 'page: %s,%s'%(kwds['page'], len(rs) )
            if not rs and kwds['page']>limit:  break
            if not rs: 
                print 'retry...'
                continue

            for e in rs:
                user = e.user
                txt = e.text.encode('utf8','ignore')
                user._txt = txt
                user._ts =  int(time.mktime(e.created_at.timetuple())), 
                user._ct =  e.created_at.strftime("%Y-%m-%d %H:%M:%S"),

                self._write_user(fh, user)
                buf.append( user )
            kwds['page'] +=1
            time.sleep(3)
        fh.close()
            
        fh = open('%s_repost2.txt'%fid , 'w')
        skips =set()
        buf.reverse()
        for user in buf:
            if user.id in skips: continue
            if '此微博已被删除' in user._txt: continue
            skips.add( user.id )
            
            self._write_user( fh, user )

        fh.close()

    def repost2_timeline(self, client, fid, limit):
        mid = misc.decode62(fid) 
        #fh = open('%s_repost2.txt'%fid , 'a')
        fh = open('%s_repost2.txt'%fid ,'w' )
        kwds = {
            'id':   mid,
            'count': 100,
            'page': 1,
        }
        iRetry = 0
        while True:    
            time.sleep(5)
            rs = client.api.repost_timeline(**kwds) or list()
            print 'page: %s,%s'%(kwds['page'], len(rs) )
            if not rs and kwds['page']>limit:  break
            if not rs: 
                print 'retry...'
                iRetry +=1
                if iRetry>3: break
                continue
            
            iRetry = 0
            print '... find %s'%len(rs)
            for e in rs:
                txt = e.text.encode('utf8','ignore'),
                #if not '@屈臣氏中国' in txt: continue 
                #user = e.user
                
                obj = {
                    'mid':  e.mid,
                    'txt': e.text.encode('utf8','ignore'),
                    'ts':  int(time.mktime(e.created_at.timetuple())), 
                    'ca':  e.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'user_name': e.user.screen_name.encode('utf8','ignore'),
                    'user_id':  e.user.id,
                }

                fh.write('%s\n'%json.dumps(obj))
                fh.flush()
            kwds['page'] +=1
        fh.close()
                
    def repost_3(self, fid):
        rs = open('%s_repost2.txt'%fid , 'r').readlines()
        rs = ( e.strip() for e in rs if bool(e) )
        rs = ( json.loads(e) for e in rs if bool(e) )
        buf = defaultdict(int)
        
        for e in rs:
            ts = int(e['ts']+8*3600)
            d = time.gmtime(ts)
            _m = 0 if d.tm_min<30 else 1
            _key = '%s-%02d-%02d %02d(%s)'%(
                d.tm_year, d.tm_mon, d.tm_mday, d.tm_hour, _m
            )
            buf[_key] +=1
        
        fh = open('%s_repost3.txt'%fid , 'w')
        rs =  buf.items()
        rs.sort(lambda x,y: cmp(x[0],y[0]))
        rs = ('%s:%s'%e for e in rs)
        fh.write('\n'.join(rs))
        fh.close()
    
    def repost_4(self, fid):
        rs = open('%s_repost2.txt'%fid , 'r').readlines()
        rs = ( e.strip() for e in rs if bool(e) )
        rs = ( json.loads(e) for e in rs if bool(e) )
        for e in rs:
            txt = e['txt'].encode('utf-8','ignore')
            if not '@' in txt: continue     
            yield e 


def bak_db_from(task):
    src = task.db('default')
    dest = task.db('local')

    cp_table(src, dest, 'wb_apps')
    cp_table(src, dest, 'wb_oauths')


if __name__=='__main__':
    task = OpenApiTask('default')
    
    #bak_db_from(task)
    
    #client = task.app_client('sina')
    #rs = client.api.rate_limit_status()
    #rs = client.api.search_users(q='春天优大奖',sort=1)
    #rs = client.api.get_user(screen_name='OCTOBER_羅')
    #print rs
    
    
    
    #print task.me('sina_android','1185702').name
    #print task.me('0','1000005').name
    
    #clients = oauth_clients('demo',task.db())
    #clients = [ task.client('demo',e) for e in clients]

    client = task.client('demo', 'ten_16921')
    #client = task.client('block', 'demo')
    #client = task.client('demo', 'ten_15377')
    #client = task.client('sina_android', '1185702')
    
    #rs = client.api.rate_limit_status()
    #print rs 

    #print u'\n'.join((e.decode('utf8') for e in task.trends_daily(client)))
    
    #user =  task.user_info(client, screen_name='hello_world')
    #user = task.user_info(client, user_id='2146226912')
    #print user
    rs = client.api.get_oauth2_token()
    print rs    
