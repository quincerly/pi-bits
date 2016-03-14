#!/usr/bin/env python

import scrollphat
import math
import time
import numpy as np
import sys

scrollphat.rotate = True

nballs=3
rmax=1.25
rmax2=rmax**2
fwhm=rmax
sig2=(fwhm/2.35)**2
period=1.5
#speed=np.linspace(1, 1.1, nballs, endpoint=True) #np.ones(nballs)
#phase0=np.zeros(nballs) #np.linspace(0, 0.4, nballs, endpoint=True)
speed=np.ones(nballs)
phase0=np.linspace(0, 1, nballs, endpoint=False)
#speed=np.array(speed.tolist()+speed.tolist())
#phase0=np.array(phase0.tolist()+(phase0+0.07).tolist())
#phase0=np.linspace(0, 0.2, nballs, endpoint=True)


class Bitmap:
    def __init__(self):
        y, x=np.mgrid[0:5, 0:11]
        self._bits=2**y
        self.x=x+0.5
        self.y=y+0.5
        #self.im=np.zeros((5, 11), dtype=int)
        self.im=np.zeros((5, 11))
        self._im2=np.zeros((5, 11), dtype=int)
    def show(self, dither=False):
        if dither:
            r=np.random.uniform(size=(5, 11))
            self._im2[:]=0
            self._im2[np.where(r<self.im)]=1
            scrollphat.buffer=np.sum(self._im2*self._bits, axis=0).tolist()
        else:
            self._im2=np.round(self.im).astype(int)
            scrollphat.buffer=np.sum(self._im2*self._bits, axis=0).tolist()
        scrollphat.update()

bm=Bitmap()

while True:

    try:
    
        t0=time.time()
        frames=0
        while True and time.time()-t0<5:
            phase=(time.time()-t0)/period
            cx=-np.cos(speed*2*3.1415926536*(phase-phase0))*(11-2*rmax)*0.5+5.5
            cy=np.sin(speed*4*3.1415926536*(phase-phase0))*(5-2*rmax)*0.5+2.5
            bm.im=np.zeros_like(bm.x)
            for c in zip(cx, cy):
                r2=(bm.x-c[0])**2+(bm.y-c[1])**2
                ind=np.where(r2<rmax2)
                bm.im[ind]+=(1-r2[ind]/rmax2)
            bm.show(True)
            frames+=1
            time.sleep(0.005)
        print("Average %g frames per second" % (frames/(time.time()-t0)))

        t0=time.time()
        tmax=5
        while True and time.time()-t0<tmax:
            #scrollphat.write_string("%3.1f" % (tmax-(time.time()-t0)))
            scrollphat.write_string("%3d" % (100*(1-(time.time()-t0)/tmax)))
            #scrollphat.scroll()
            time.sleep(0.1)

    except KeyboardInterrupt:

        scrollphat.clear()
        sys.exit(-1)
