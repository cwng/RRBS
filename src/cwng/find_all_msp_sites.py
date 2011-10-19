from __future__ import division
import sys, math, cPickle,os
import numpy as np
import scipy.stats
import matplotlib
matplotlib.use('pdf')
from matplotlib import pyplot as plt
from optparse import OptionParser
from collections import defaultdict
import chipsequtil
from chipsequtil.nib import NibDB
from TAMO.seq import Fasta

def seq_msp(fafile,bedfile):
    start=-3
    hang='NNN'

    match=[]

    #find CCGG positions using Fasta file
    fa=open(fafile)
    for line in fa:
        l=line.strip('\n')
        if l[0]=='>':
            ch=l[1:]
            continue
        if l=='NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN':
            start+=len(l)
            hang=l[-3:]
            continue
        else:
            seq=hang+l
            mers=[seq[x:(x+4)] for x in range(len(seq)-4)]
            for i,m in enumerate(mers):
                if m=='ccgg': match.append([ch,str(start+i+1)])
            hang=seq[-3:]
            start+=len(l)

    print len(match)
    
    fa.close()
    np.savetxt(bedfile,match,fmt='%s',delimiter='\t')

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    #parser.add_option("--min_dist", dest="min_dist", type=int, default=40)
    #parser.add_option("--max_dist", dest="max_dist", type=int, default=220)
    parser.add_option("--outfile", dest="outfile", default=None)
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    a=args[0]

    seq_msp(a,opts.outfile)

if __name__=='__main__': main()
