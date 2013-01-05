from twisted.web.client import _parse
from scrapy.core.downloader.webclient import ScrapyHTTPClientFactory, ScrapyHTTPPageGetter

class Http11PageGetter(ScrapyHTTPPageGetter):

    def sendCommand(self, command, path):
        scheme, host, port, path = _parse(path)
        path = path or '/'
        self.transport.write('%s %s HTTP/1.1\r\n' % (command, path))

    def endHeaders(self):
        self.transport.write('Connection: close\r\n') 
        self.transport.write('\r\n')


class HTTP11ClientFactory(ScrapyHTTPClientFactory):

     protocol = Http11PageGetter  

