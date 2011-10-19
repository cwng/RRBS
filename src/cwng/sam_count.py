from __future__ import division
import sys, math, cPickle,os
import numpy as np
import scipy.stats
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot as plt
from optparse import OptionParser
from collections import defaultdict

def f(samfile,outfile):
    sam=open(samfile)
    COUNT=defaultdict(list)
    for line in sam:
        L=line.split('\t')
        if int(L[1])==4: continue
        ref=L[2]
        base=L[0].split('#')[1]
        COUNT[ref].append(base)
    
    out=open(outfile,'w')
    METH=[]
    TOT=[]
    for ref,align in COUNT.items():
        C,T=0,0
        for a in align:
            if a=='C': C+=1
            elif a=='T': T+=1
        meth=C/(C+T)
        METH.append(meth)
        TOT.append(C+T)
        out.write('%s\t%f\t%i\t%i\n'%(ref,meth,C,T))
    
    out.close()
    plt.figure()
    plt.hist(METH,bins=40,normed=True)
    plt.savefig(outfile.replace('.txt','')+'meth_frac.pdf')

    plt.figure()
    plt.hist(TOT,bins=50,normed=True,range=(1,100))
    plt.savefig(outfile.replace('.txt','')+'tot_align.pdf')


def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    #parser.add_option("-n", action="store_true", dest="n")
    #parser.add_option("--thres", dest="thres", type=float, default=0.7)
    #parser.add_option("--dist", dest="dist", type=int, default=1)
    parser.add_option("--outfile", dest="outfile", default=None)
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    samfile=args[0]

    f(samfile,opts.outfile)

if __name__=='__main__': main()
