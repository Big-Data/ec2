#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults.ws_settings import _Config 

conf = Settings( )
conf.overrides.update({
    'server':   _Config['server@local'],
    'client':   _Config['client@230'],
})

