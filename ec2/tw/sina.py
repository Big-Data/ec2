#coding=utf-8

from ec2.redis  import API as redis_api


try:
    from weibopy.api2   import API as tw_api
except ImportError:
    pass


#>>>2.00OmEpLCHpMJ1Cad6fa4f96c5E8ObD<<<
def client_factory(app, client):
    k = '%s-%s'%(app,client)
    e = redis_api.db().select_from( 'wb_oauth2', k)
    if not e or not e.get('access_token',None):   
        return 

    return tw_api(e['access_token'])
    

if __name__=='__main__':
    pass

