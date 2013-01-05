#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults.ws_settings import _Config 

conf = Settings( )
conf.overrides.update( {
    'server':   _Config['server@node122'],
    'client':   _Config['client@node122'],
} )
