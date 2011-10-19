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
    S=open(samfile)
    out=open(outfile,'w')
    seq_i,qual_i,skip=False,False,False
    for line in S:
        line=line.strip('\n')
        if line[0]=='@':
            seq_i=True
            header=line[:-10]
            #header=line
            continue
        elif line[0]=='+':
            qual_i=True
            #header=line
            header=line[:-10]
            continue
        elif seq_i:
            seq=line
            seq_i=False
            #skip sites not matching MSP1 restriction cut sites
            cut_site=seq[:3]
            if not (cut_site=='CGG' or cut_site=='TGG'):
                skip=True
                continue
            #out.write(header+seq+'/1\n')
            #out.write(header+'\n')
            base1=seq[0]
            out.write(header+base1+' '+seq+'\n')
            seq_rest=seq[1:]
            convert_seq=base1+seq_rest.replace('C','T')
            out.write(convert_seq+'\n')
            continue
        elif qual_i:
            qual_i=False
            if skip:
                skip=False
                continue
            else:
                #out.write(header+seq+'/1\n')
                out.write(header+base1+' '+seq+'\n')
                #out.write(header+'\n')
                out.write(line+'\n')
                continue
        else: print line
    S.close()
    out.close()

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("--outfile", dest="outfile", default=None)
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    samfile=args[0]

    f(samfile,opts.outfile)

if __name__=='__main__': main()
