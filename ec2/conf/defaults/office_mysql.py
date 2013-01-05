#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults import mysql_settings 

conf = Settings(defaults=mysql_settings )
conf.update({
    'default':  mysql_settings._Config['feed@office-235'],
})
