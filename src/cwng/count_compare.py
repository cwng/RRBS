from __future__ import division
import sys, math, cPickle,os
import numpy as np
import scipy.stats
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot as plt
from optparse import OptionParser
from collections import defaultdict

#class rrbs_event(cond,):

def f(f1,f2,outfile,thres=20):
    F1=open(f1)
    F2=open(f2)
    #COUNT=defaultdict(list)
    M1,M2={},{}
    for line in F1:
        L=line.strip('\n').split('\t')
        ref,frac,C,T=L[0],float(L[1]),int(L[2]),int(L[3])
        #COUNT[ref].append((frac,C,T))
        M1[ref]=(frac,C,T)
    for line in F2:
        L=line.strip('\n').split('\t')
        ref,frac,C,T=L[0],float(L[1]),int(L[2]),int(L[3])
        M2[ref]=(frac,C,T)
        #COUNT[ref].append((frac,C,T))

    out=open(outfile,'w')
    DIFF=[]
    #for ref,mat in COUNT.items():
    for ref,tup in M1.items():
        meth1,C1,T1=tup
        try: meth2,C2,T2=M2[ref]
        except: continue
        #lfc=math.log((meth1+0.01)/(meth2+0.01),2)
        diff=meth1-meth2
        TOT=C1+C2+T1+T2
        if TOT<thres: continue
        #LFC.append(lfc)
        DIFF.append(diff)
        out.write('%s\t%f\t%f\t%i\t%i\t%f\t%i\t%i\t%i\n'%(ref,diff,meth1,C1,T1,meth2,C2,T2,TOT))
    
    out.close()
    plt.figure()
    plt.hist(DIFF,bins=40,normed=True)
    plt.savefig(outfile.replace('.txt','')+'diff.pdf')

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    #parser.add_option("-n", action="store_true", dest="n")
    parser.add_option("-t","--thres", dest="thres", type=float, default=20)
    #parser.add_option("--dist", dest="dist", type=int, default=1)
    parser.add_option("--outfile", dest="outfile", default=None)
    (opts, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments")

    f1=args[0]
    f2=args[1]

    f(f1,f2,opts.outfile,thres=opts.thres)

if __name__=='__main__': main()
