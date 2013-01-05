import logging, sys
from scrapy import log

from twisted.python import log as txlog
from twisted.application.service import Service, Application

def init_app(settings={}):

    appname = settings.get('APPNAME', 'ListenableService')
    loglevel = settings.get('LOG_LEVEL', 'DEBUG')
    logfile = settings.get('LOG_FILE', '%s.log'%appname)

    loglevel = logging.__dict__.get(loglevel, logging.DEBUG)
    logfile = sys.stderr if not logfile else open(logfile, 'a')

    app = Application(appname)
    app.setComponent(
        txlog.ILogObserver, 
        log.ScrapyFileLogObserver(logfile,loglevel).emit
    )
    return app


class Srv(Service):


    def startService(self):
        #d = Service.startService(self)
        #d.addCallback( self._log, 'start' )
        #return d
        self._log('start')
    
    def stopService(self):
        #d = Service.stopService(self)
        #d.addCallback( self._log, 'stop' )
        #return d
        self._log('stop')
    
    def _log(self, msg):
        #logging.debug('>>> %s'%msg)
        print '>>> %s'%msg

application = init_app()

srv = Srv()
srv.setServiceParent(application)

