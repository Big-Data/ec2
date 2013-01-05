import logging, json , time
#logging.basicConfig(level=logging.DEBUG)

from ec2.worker import proxylist


if __name__=='__main__':
    proxylist.init_conf()
    print '---- over ---'