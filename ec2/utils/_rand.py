#coding=utf-8

import random
import bisect

_Alpha = 'abcdefghijklmnopkrstuvwxyz0123456789'
_Number = '0123456789'        
_AZ = 'abcdefghijklmnopkrstuvwxyz'


def random_alpha(limit=6):
    return ''.join(map(lambda e: random.choice(_Alpha), xrange(limit)))

def random_number(limit):
    return ''.join(map(lambda _: random.choice(_Number),xrange(limit)))

def random_az(limit):
    return ''.join(map(lambda _: random.choice(_AZ),xrange(limit)))

def weighted_choice(weights,idx=1):
    rnd = random.random() * sum((e[idx] for e in weights))
    for e in weights:
        rnd -= e[idx]
        if rnd < 0:
            return e

def make_user(namesize=6):
    return '%s%s'%(random_az(1),random_alpha(namesize-1))


def random_ip():
    v = ( random.randint(100,220) for _ in xrange(4) )
    v = ( str(e) for e in v)
    return '.'.join(v)

if __name__=='__main__':
    #print random_alpha()
    print random_ip()
