#coding=utf-8

def init_scrapy(path=None):
    import os
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', path or 'ec2.conf.defaults.scrapy_settings')

def init_test():
    from .enabled import redis_conf
    redis_conf.update({
        'pre_db': 'test',
    })


'''

---MQ
    |---ExpiredPool
    |    
    |---conf
    |    |---task
    |    |   |---$name: $fields->$value     # weight/
    |    |   |---INDEX
    |    |
    |    |---cron
    |    |   |---$name: $fields->$value     # retry
    |    |   |---INDEX
    |    |
    |
    |---online
    |    |---sz_chnls:  $host->$weight       #zset
    |    
    |---cache
    |    |---$pid: $fields->$value          #hash temp data
    |    |---UUID
    |    |---INDEX
    |
    |---www
    |    |---$ws_client
    |    |---$ws_client
    |    |
    |    
    |---chnls
    |    |---$pid: $fields->$value          # pid|chnl|<ping>
    |    |---UUID
    |    |---INDEX
    |
    |---sz_users
    |    |---$pid: $fields->$value          #hash 
    |    |---UUID
    |    |---INDEX
    |
    |---sz_images
    |    |---$pid: $fields->$value          #hash 
    |    |---UUID
    |    |---INDEX
    |
    |---sz_proxies:  
    |    |---$pid: $fields->$value          #hash 
    |    |---UUID
    |    |---INDEX
    |
    |---ExpiredPool
    |---queue
    |    |
    |    |---logger    #message send from websocket clients
    |    |---cron      #client-ping
    |    |---watchdog  #ping/pong  
    |    |
    |    |---sz_login
    |    |---sz_image
    |    |---sz_captcha
    |    |---sz_reg
    |    |
    |    |
    |    |
    |    |
    |
    |




'''

