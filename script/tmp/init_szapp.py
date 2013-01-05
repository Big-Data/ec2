#coding=utf-8


import logging, json 


from ec2.redis import RedisDb

logging.basicConfig(level=logging.INFO) #DEBUG)
db = RedisDb(pre='MQ')

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



_users = {
  '360502198502241612':{
    'exam': '2',
    'name': '肖春辉',
  },          
  '511121197802126810':{
    'exam': '2',
    'name': '李建国',
  },          
  '440924197111233418':{
    'exam': '2',
    'name': '叶忠基',
  },          
  '411528198407171918':{
    'exam': '2',
    'name': '王闯',
  },          
  '431026198109303816':{
    'exam': '2',
    'name': '赖新华',
  },          
  '440982198910144970':{
    'exam': '2',
    'name': '陈恩荣',
  },          
  '522321198810021216':{
    'exam': '4',
    'name': '李文勇',
  },          
  '510282198108277514':{
    'exam': '4',
    'name': '刘贵湘',
  },          
  '512221197401216678':{
    'exam': '4',
    'name': '廖良兵',
  },          
  '412822197708208336':{
    'exam': '4',
    'name': '刘广峰',
  },          
  '420682198210185536':{
    'exam': '4',
    'name': '刘连忠',
  },          
  '420983198512077250':{
    'exam': '4',
    'name': '吴讲义',
  },          
  '431023199110215843':{
    'exam': '4',
    'name': '李郸',
  },          
  '429006197906115186':{
    'exam': '4',
    'name': '田甜',
  },          
  '431122199003042915':{
    'exam': '4',
    'name': '唐海宾',
  },          
  '412822197007107698':{
    'exam': '4',
    'name': '马永兴',
  },          
  '610115199108285015':{
    'exam': '3',
    'name': '赵宣',
  },
  '522321198810021216':{
    'exam': '4',
    'name': '李文勇',
  },
  '510282198108277514':{
    'exam': '4',
    'name': '刘贵湘',
  },
  '512221197401216678':{
    'exam': '4',
    'name': '廖良兵',
  },
  '440823197002102038':{
    'exam': '4',
    'name': '郑荣胜',
    'pwd':  '123456',
  },
  '362103198310204426':{
    'exam': '4',
    'name': '刘玉红',
    'pwd':  '123456',
  },
  '231124198207152519':{
    'exam': '4',
    'name': '马龙',
    'pwd':  '123456',
  },
  '420626198107023036':{
    'exam': '4',
    'name': '柳祥华',
    'pwd':  '123456',
  },

}


_task_conf = {
    '2': 15698,
    '3': 19801,
    '4': 15724,

    '八': 0,
	'九':1,
	'十':2,
	'十一':3,
	'十二':4,
	'十三':5,
	'十四':6,
	'十五':7,
	'十六':8,
	'十七':9,
	'十八':10,
	'十九':11,
	'二十':12,
}

def _normal(m):
    rs = {}
    for k,v in m.items():
        v['pid'] = k
        if not v.get('pwd', None):
            v['pwd'] = '1'
        
        rs[k] = v
    return rs


def init_users():
    for e in _normal(_users).values():
        db.update_table('sz_users',e['pid'], e)

def init_szconf():
    db.update_table('conf:sz', 'base_header', _base_header)    
    db.update_table('conf:sz', 'task', _task_conf)    


def init_crons():
    db.update_table('conf:cron','chnl_ping',{
        'pid':      'chnl_ping',
        'handler':  'watchdog.SendPing',
        'expire':   60,
        'retry':    0 #1<<30,
    })

    db.update_table('conf:cron','sz_images',{
        'pid':      'sz_images',
        'handler':  'sz.ImageHandler',
        'expire':   10*60,
        'retry':    1<<30,
    })

    db.update_table('conf:cron','sz_proxies',{
        'pid':      'sz_proxies',
        'handler':  'sz.ProxyHandler',
        'expire':   10*60,
        'retry':    0 #1<<30,
    })

    db.update_table('conf:cron','sz_cookies',{
        'pid':      'sz_cookies',
        'handler':  'sz.CookieHandler',
        'expire':   10*60,
        'retry':    0 #1<<30,
    })

    db.update_table('conf:cron','sz_users',{
        'pid':      'sz_users',
        'handler':  'sz.UserHandler',
        'expire':   10*60,
        'retry':    1<<30,
    })



if __name__=='__main__':
    db.redis().flushdb()
    init_szconf()
    init_users()
    init_crons()
