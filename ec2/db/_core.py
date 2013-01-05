#coding=utf-8

from twisted.python         import log
import MySQLdb

from ec2.utils.decorator    import retry
from ec2.conf.enabled       import mysql_conf 



_db_pool ={}

def _self_err_cb(self,sql):
    log.err('db:err>> %s' % sql)
    self.reset()

class _MysqlDb(object):
    def __init__(self, db ):
        self.db = db
        self.cursor = self.db.cursor()

 
    def mapTable(self, sql):
        buf, fields = self.rowTable(sql)
        if not buf and not fields: return []

        rs =[]
        iFields = len(fields)

        for e in buf:
            obj = {}
            for i in range(iFields):
                obj[fields[i]] = e[i]
            rs.append( obj )
        return rs

    def rowTable(self, sql):
        try:
            self.execute(sql)
        except:
            self.reset()
            return [], []

        rs = self.cursor.fetchall()
        fields = [ e[0] for e in self.cursor.description ]
        return rs, fields


    @retry(Exception,  tries=2, errcb=_self_err_cb, delay=5)
    def execute(self,sql):
        self.cursor.execute(sql)
    
    def close(self):    
        self.db.close()

    def reset(self):
        if self.cursor:  self.cursor.close()
        self.cursor = self.db.cursor()
        self.ping(True)
    
    def ping(self, flag=True):
        return self.db.ping(flag)
        


#-------------------------------------------
class API(object):

    @staticmethod
    def db(name='default'):  
        if _db_pool.has_key(name):  return _db_pool[name]
            
        if not mysql_conf.get(name,None):
            raise Exception('missing <%s> in mysql config'%name) 
    
        conf = mysql_conf[name]
        _db_pool[name] = _MysqlDb( MySQLdb.connect(**conf) )            
        return _db_pool[name]    

    @staticmethod
    def pop(name):
        if not _db_pool.has_key(name): return
        return _db_pool.pop(name)
    
    @staticmethod
    def ping(name=None):
        if not name:
            dbs = _db_pool.values()
        elif _db_pool.has_key(name):
            dbs = ( _db_pool[name] , )
        else:
            return

        try:
            for e in dbs:
                e.ping(True)
        except:
            e.reset()
            log.err('db:ping fail')
        


if __name__=='__main__':
    pass