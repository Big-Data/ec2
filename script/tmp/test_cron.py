import logging, json , time
logging.basicConfig(level=logging.DEBUG)

from ec2.redis  import API

db = API.db()

def init():
    db.update_table('conf:cron', 'test', {
        'pid':      'test',
        'table':    'conf:cron',
        'queue':    'queue:cron',
        #'handler':  'expired.handler',     #no need
        'cron_handler': 'cron.dump',
        'retry':    20,
        'timeout':  5,
    })
    

    API.expire({
        'pid':      'test',
        'table':    'conf:cron',
    },5)    

    



if __name__=='__main__':
    init()
    print '---- over ---'