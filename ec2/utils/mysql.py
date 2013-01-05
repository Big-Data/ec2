#coding=utf-8

from scrapy import log
from MySQLdb import escape_string


def insert(db,table, v, step=1000, update=False,debug=False):
    if not v:   return
    v = list(v)
    keys = v[0].keys()
    update_keys = ','.join(( '`%s`=values(`%s`)'%(e,e) for e in keys ))
    
    sql_base ="insert into `%s`(`%s`) values ('%%s')"%(table,'`,`'.join(keys))
    for i in xrange(step):
        rs = v[i::step]
        if not rs:  continue
        
        vv =([escape_string('%s'%e.get(k, 'None')) for k in keys]  for e in rs)
        vv =( "','".join(e) for e in vv)
        vv = "'),('".join(vv)
        vv = vv.replace("'None'", "NULL")
        
        vv = sql_base%vv
        
        if bool(update):
            vv = '%s ON DUPLICATE KEY UPDATE %s' %(vv,update_keys)
        
        try:
            if  debug:
                log.msg( '>>>sql_insert:%s'%(vv,), log.DEBUG)
            db.execute( vv )
        except:
            db.reset()


def update(db,table, v, key,debug=False):
    if not v:   return
    sql_base ="update %s set %%s where `%s`='%%s' "%(table,key)
    
    for e in v:
        if not e.has_key(key):  continue

        kv = e.items()
        vv = ( "`%s`='%s'"%(kk,escape_string(str(vv)),) for kk,vv in kv if kk!=key ) 
        vv = ','.join(vv)
        vv = vv.replace("`='None'", "`=NULL")
        try:
            if debug:
                log.msg( '>>>sql_update:%s'%(sql_base%(vv,e[key]),), log.DEBUG)
            db.execute( sql_base%(vv,e[key]) )
        except:
            db.reset()

def delete_from(db,table, v, key,debug=False):
    if not v:   return
    
    sql_base ="delete from %s where `%s` in ('%%s')"%(table, key)
    rs = ( e[key] for e in v if e.has_key(key) )
    rs = ( str(e) for e in rs)
    rs = "','".join(rs)
    if not rs:  return
    
    try:
        if debug:
            log.msg( '>>>sql_del:%s'%(sql_base%rs,), log.DEBUG)
        db.execute( sql_base%rs )
    except:
        db.reset()


def safe_execute(db,sql, debug=False):
    try:
        if debug:
            log.msg( '>>>sql:%s'%(sql,), log.DEBUG)
        db.execute( sql )
    except:
        db.reset()
    


 
if __name__=='__main__':
    pass    

            
