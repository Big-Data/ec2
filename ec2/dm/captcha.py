#coding=utf-8

import shutil
from StringIO import StringIO
import Image

import numpy as np

from scipy.spatial.kdtree import KDTree  
from  scipy import ndimage , misc
import cPickle

from ec2.utils import image as utils
from tinySVM.base_svm import BaseSVM 

class Decoder(object):
    chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    fonts = None 
    svm = {}
    Debug = 0

    def __init__(self, path='./data'):
        self._logger = None
        if not self.fonts:
            self.fonts = cPickle.load(open('%s/model/fonts.arrs'%path,'rb'))
        
        for k in self.chars:
            if self.svm.has_key(k): continue
            
            fn = '%s/model/%s.c_svm'%(path,k)
            if not shutil.os.path.exists(fn): continue
            
            self.svm[k] = BaseSVM.load(fn)
        

    def decode(self, arr, alpha=0.4, ks=None):
        arr = self._normal( arr )        
        rs = []
        ks = ks or self.fonts.keys()
        for k in ks:
            _arr = self._correlate( arr, k, alpha)
            roi = self._roi( _arr )
            if not roi : continue
            
            for xy in roi:
                v = self._info2vec( k, arr, xy)  
                if not self.svm.has_key(k):
                    score = 5
                else:
                    score = self.svm[k].predicate(v) 
                
                if self.Debug:
                    print '%s: <%s> %0.3f'% (k, xy, score )
                
                if score<0.4:   continue
                rs.append( (k,score,xy) )
        
        if not rs: return rs, arr
        
        rs = self._merge(rs)
        
        if self.Debug:
            print 'result:'
            _rs = ('%s: %s %0.3f'%(e[0], e[2], e[1]) for e in rs)
            print '\n'.join(_rs)

        return rs, arr

    def img2code(self, ss, alpha=0.4):
        im = Image.open(StringIO(ss))
        im = im.convert('L')
        arr = misc.fromimage(im)
        roi,res = self.decode(arr)
        if len(roi)!=4: return None
        
        return ''.join( e[0] for e in roi )
    

    def _merge(self, roi):
        points = [ e[2] for e in roi ]
        tree = KDTree(points)  
        pp = tree.query_pairs(4)
        #pp = sorted( pp , key=lambda e: max(roi[e[0]] , roi[e[1]]), reverse=True)
        skips = set()
        for i,j in pp:
            if self.Debug:
                print '%s(%.2f),%s(%.2f)'%(roi[i][0],roi[i][1], roi[j][0], roi[j][1] )
            
            if i in skips or j in skips: continue
            skip = i if roi[i][1]<roi[j][1] else j
            skips.add(skip)
    
        rs = ( e for i, e in enumerate(roi) if not i in skips )
        rs = sorted( rs , key=lambda e: e[1] )[-4:]
        return sorted( rs, key=lambda e: e[2][1] )

    #---------------------------------------
    def _correlate(self,arr, k, alpha=0.6):
        limit,V = self.fonts[k]
        rs = ndimage.correlate(arr,V, mode='constant', cval=0.0)
        h,w = rs.shape

        for ij in ( (i,j) for i in xrange(h) for j in xrange(w)):
            rs[ij] = rs[ij] if rs[ij]>limit*alpha else 0
        return ndimage.gaussian_filter(rs, 2)

    def _roi(self,arr):
        region =  utils.im_roi( arr )
        roi = np.nonzero(region>0)
        return zip(*roi)
        
    def _im2array(self, im):
        im = im.convert('L')
        return misc.fromimage(im)
        
    def _normal(self, arr):
        out = utils.im_fuse(arr/3)
        arr  = utils.im_reset(arr,out,mode='auto')
        
        arr = 255 - arr
        return utils.im_norm( arr )


    def _info2vec(self, k, arr, xy):
        h,w = self.fonts[k][1].shape
        x,y = xy
        
        v = np.ndarray( (h,w),dtype=arr.dtype)
        v.fill(0)
        e= arr[x-h/2:x+h/2,y-w/2:y+w/2]
        _h,_w = e.shape
        v[:_h,:_w] = e
        return  v.reshape((h*w,))



#----------------------------------
if __name__=='__main__':
    from ec2.redis import RedisDb

    db = RedisDb(pre='MQ')
    d = Decoder(path='../data')
    for i in xrange(10):
        e = db.select_fields('sz_images',i+1, ['body',])
        if not e['body']: continue

        fh = open('d:/temp/sz_%s.png'%(i+1) , 'wb')
        fh.write(e['body'])
        fh.close()

        #d.Debug = 1
        code = d.img2code(e['body'])
        print '%s:%s'%(i+1, code) 

    #im.save('d:/temp/szqqq.png')

