#coding=utf-8

import re

import subprocess
from scrapy import log
import psutil 
from ec2.scrapy import crawler

CrawlerRule = re.compile('/crawler_.+\.tac')

class MoniterMiddleWare(crawler.BaseCrawlerMiddleWare):
    
    mw_name = 'mem_moniter'
    def __init__(self, controller, settings):
        crawler.BaseCrawlerMiddleWare.__init__(self,controller, settings)

        self.remote_connect(self.on_overflow,'mem_overflow')


    #------------------------------------
    def _do_process(self):  pass
        cur = psutil.used_phymem()
        if cur<self.LIMIT:  return

        log.msg('begin free memory<%d>'%cur,log.DEBUG)
        for e in psutil.process_iter():
            self._check_process(e) 

        cur = psutil.used_phymem()
        log.msg('end free memory<%d>'%cur,log.DEBUG)

    def _check_process(self,p):
        if p.name !='twistd' or len(p.cmdline) <2 :
            return
        
        tac = p.cmdline[-2]
        if not CrawlerRule.findall(tac):    return
        
        mem = p.get_memory_info()
        if mem.rss< 100*1024*1024:  return

        
        mem.kill()
        mem.wait()
        
        subprocess.call(' '.join(p.cmdline), shell=True) 
        





if __name__=='__main__':
    pass    
