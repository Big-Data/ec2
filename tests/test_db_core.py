from nose import tools
import unittest, time
from ec2.db import API
from ec2.conf.enabled import mysql_conf


class DbTest(unittest.TestCase):
    
    def setUp(self): 
        self.db = API.db('default')

    def tearDown(self):
        pass
        
    def testDbPing(self):
        rs = self.db.ping()
        tools.eq_(None, rs) 

    def testPingall(self):
        API.ping()

    def testRowTable(self):
        sql = 'select count(*) as iCount from ec2_wb_users'
        rs = self.db.rowTable(sql)
        tools.eq_( 2, len(rs) )

    def testMapTable(self):
        sql = 'select count(*) as iCount from ec2_wb_users'
        rs = self.db.mapTable(sql)
        tools.ok_( rs[0]['iCount'] > 0 )



