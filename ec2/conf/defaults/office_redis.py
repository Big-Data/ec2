#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults.redis_settings import _Config 

conf = Settings()
conf.overrides.update({
    'default':  _Config['office@230'],
    'cache':    _Config['office@230'],
    'local':    _Config['local'],

    'expiredpool_timeout': 1,
})
