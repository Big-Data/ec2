#coding=utf-8

from ec2.conf.settings import Settings
from ec2.conf.defaults import scrapy_settings


try:
    from scrapy.settings import default_settings
except ImportError:
    from scrapy.conf     import default_settings


conf = Settings( default_settings , settings_module = scrapy_settings) 
