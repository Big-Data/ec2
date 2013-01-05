import Image, ImageFont
import pylab, scipy, numpy
import cPickle

from scipy import misc,  ndimage
from collections import defaultdict
from tinyImage import process_core as C
from tinyImage.process.meanshift import Processor

def im_loadL(name='big'):
    im = Image.open('./data/sz_%s.png'%name)
    im = im.convert('L')
    im = misc.fromimage(im)
    return (im.shape[0]/22,5), im 

def im_index(im,xy):
    x,y = xy
    x,y = x*22,y*49
    return im[x:x+22,y:y+49]

def im_fuse(arr, alpha=4):
    h = Processor()
    h.set_image(arr)
    h.set_params(minRegion=alpha)
    h.set_speed_threadhold()
    h.do_filter() 
    h.do_fuse()
    return h

def im_reset(arr,h, mode='auto'):
    im = numpy.ndarray(arr.shape, dtype=arr.dtype)
    im.fill(255)

    m = defaultdict(list)
    lb = h.get_labels()
    mpc = h.get_MPC()
    h,w = arr.shape
    for ij in ( (i,j) for i in xrange(h) for j in xrange(w) ):
        m[lb[ij]].append(ij)

    for k,xys in m.items():
        if len(xys)>h*w/2: continue
        
        if mode=='origin':
            for xy in xys:
                im[xy] = arr[xy]
            continue
 
        if mode=='auto':
            for xy in xys:
                v = 255 if arr[xy]>200 else 0
                im[xy] = v
            continue

        if mode=='mean':
            vs = [ arr[xy] for xy in xys ]
            v = sum( vs )/ len(xys)
        elif mode=='black':
            v = 0        
        elif mode=='white':
            v = 255

        for xy in xys:
            im[xy] = v

    return im

def im_norm(arr):
    arr = arr - numpy.mean(arr)
    return arr/ numpy.sqrt( numpy.var(arr) )

#-------------------------------
def _hessian(buf, xx,xy):
    V = buf.reshape((3,3))
    key = V[1,1]
    if  abs(key)<= 0.03: 
        return 0

    if not (V<=key).all() :
        return 0

    Dxx = sum(V[:,1]*xx)
    Dyy = sum( V[1,:]*xx)
    Dxy = sum(sum(V*xy)     )
    Det = Dxx*Dyy-Dxy*Dxy
    
    if  Det<0:  return 0
    
    Tr = Dxx+Dyy
    edge = Tr*Tr/Det
    return edge

def im_roi(arr):
    return ndimage.generic_filter(arr, _hessian, mode='constant', cval=0.0, size=(3,3), extra_keywords = {
        'xx' :  scipy.array([1,-2,1]),
        'xy':   scipy.array([ [ 1, 0, -1], [0,0,0], [-1,0,1] ] )/4.0,
    })


#-------------------------------------
def dump_info(arr, fh):
    h,w = arr.shape
    #print arr.dtype
    for i in xrange(h):
        if arr.dtype==numpy.uint8:
            fh.write('%s\n'%(' '.join( '%3d'%arr[(i,j)] for j in xrange(w))))
        else:    
            fh.write('%s\n'%(' '.join( '%.1f'%arr[(i,j)] for j in xrange(w))))
            
    fh.flush()

#-------------------------------------
def fonts_template(fn=None,ttf=None):
    ttf = ttf or 'c:/windows/fonts/ariali.ttf'
    fn = fn or 'd:/temp/fonts.arrs'

    m = dict()
    font = ImageFont.truetype(ttf, 18)
    for e in  '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        arr = font.getmask(e, mode='L')
        arr = Image.Image()._new(arr)
        arr = misc.fromimage(arr)
        h,w = arr.shape
        
        print '%s:<%s,%s> %s'%(e, h,w, arr[0,0])
        if w<10:
            tmp = numpy.ndarray( (h,10), dtype=arr.dtype )
            tmp.fill(0)
            i = (10-w)/2
            tmp[:,i:i+w] = arr
            arr = tmp
        #arr = arr[3:18,:]
        arr = arr[2:19,:]
        arr = im_norm(arr)
        rs = ndimage.correlate(arr,arr, mode='constant', cval=0.0)
        limit = numpy.max(rs)
        m[e] = (limit,arr)

    cPickle.dump(m, open(fn,'wb'))

    
def font_template(fn=None):
    fn = fn or './data/model/fonts.arrs'
    return cPickle.load(open(fn,'rb'))

if __name__=='__main__':
    #fonts_template()
    pass

