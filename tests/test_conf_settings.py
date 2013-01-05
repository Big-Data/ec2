from nose import tools
import unittest, time

try:
    from scrapy.conf import default_settings
except ImportError:
    from scrapy.settings import default_settings

from ec2.conf.settings import Settings


class SettingsTest(unittest.TestCase):
    
    def setUp(self): 
        pass

    def tearDown(self):
        pass
        

    def testDefault(self):
        conf = Settings(default_settings)
        tools.eq_( 'scrapybot', conf.get('BOT_NAME', None))
        tools.eq_( '1.0', conf.get('BOT_VERSION', None))
        tools.eq_( 1.0, conf.getfloat('BOT_VERSION', None))
        tools.eq_( [], conf.getlist('SPIDER_MODULES', None))
        tools.eq_( 180, conf.getint('DOWNLOAD_TIMEOUT', None))

    '''    
    def testDefault2(self):
        conf = scrapy_conf
        tools.eq_( 'scrapybot', conf['BOT_NAME'])
        tools.eq_( '1.0', conf['BOT_VERSION'])
        tools.eq_( 1.0, conf.getfloat('BOT_VERSION', None))
        tools.eq_( [], conf.getlist('SPIDER_MODULES', None))
        tools.eq_( 180, conf.getint('DOWNLOAD_TIMEOUT', None))
    '''


    def testSetting1(self):
        from ec2.conf.defaults import nose_test
        conf = Settings(
            defaults = default_settings,
            settings_module = nose_test
        )
        tools.eq_( 'scrapybot2', conf.get('BOT_NAME', None))
        tools.eq_( '11.0', conf.get('BOT_VERSION', None))
        tools.eq_( 11.0, conf.getfloat('BOT_VERSION', None))
        tools.eq_( [1,2], conf.getlist('SPIDER_MODULES', None))
        tools.eq_( 'world', conf.get('HELLO', None))
        tools.eq_( False, conf.getbool('COOKIES_DEBUG', None))

    def testSetting2(self):
        from ec2.conf.defaults import nose_test
        conf = Settings(
            defaults = default_settings,
            settings_module = nose_test,
            values = { 'COOKIES_DEBUG': 'good', }
        )
        tools.eq_( 'scrapybot2', conf.get('BOT_NAME', None))
        tools.eq_( '11.0', conf.get('BOT_VERSION', None))
        tools.eq_( 11.0, conf.getfloat('BOT_VERSION', None))
        tools.eq_( [1,2], conf.getlist('SPIDER_MODULES', None))
        tools.eq_( 'good', conf.get('COOKIES_DEBUG', None))


    def testSetting3(self):
        from ec2.conf.defaults import nose_test
        conf = Settings(
            defaults = default_settings,
        )
        conf.enable(nose_test) 
        tools.eq_( 'scrapybot2', conf.get('BOT_NAME', None))
        tools.eq_( '11.0', conf.get('BOT_VERSION', None))
        tools.eq_( 11.0, conf.getfloat('BOT_VERSION', None))
        tools.eq_( [1,2], conf.getlist('SPIDER_MODULES', None))
        tools.eq_( 180, conf.getint('DOWNLOAD_TIMEOUT', None))

    