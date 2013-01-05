#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults.redis_settings import _Config 

conf = Settings()
conf.overrides.update({
    'default':  _Config['node@120'],
    'cache':    _Config['node@122'],
    'local':    _Config['local'],
})

