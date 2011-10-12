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

def seq_msp(fafile,seqfile,genome='mm9'):
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
                if m=='ccgg': match.append(start+i)
            hang=seq[-3:]
            start+=len(l)

    print len(match)
    
    fa.close()
    FRAG=[]
    
    #find cut sites 40-220bp and save as tuple
    for x,y in zip(match[:-1],match[1:]):
        d=y-x
        if d>40 and d<250: FRAG.append((x,y))

    print len(FRAG)

    #nibDB the cut sites 40bp 5'-3' and
    #save each as a pair of Fasta items with keys chr:position(strand)
    seq_dict={}
    ids,loci=[],[]
    for x,y in FRAG:
        #for x
        start=x+1
        stop=x+41
        key=ch+':'+str(start)+'+'
        loc=(ch,start,stop,'+')
        ids.append(key)
        loci.append(loc)

        #for y
        start=y-37
        stop=y+3
        key=ch+':'+str(stop)+'-'
        loc=(ch,start,stop,'-')
        ids.append(key)
        loci.append(loc)

    if genome=='hg18':  DB=NibDB(nib_dirs='/nfs/genomes/human_gp_mar_06/')
    else:  DB=NibDB(nib_dirs=chipsequtil.get_org_settings('mm9')['genome_dir'])
    fa_ids,seqs=DB.get_fasta_batch(loci)
    for id,seq in zip(ids,seqs):
        biseq=seq.replace('c','t')
        if id[-1]=='+':
            seq_dict[id]=biseq
        else:
            #seq_dict[id]=seq[::-1]
            seq_dict[id]=biseq
    Fasta.write(seq_dict,seqfile)

def main():
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    #parser.add_option("--min_dist", dest="min_dist", type=int, default=40)
    #parser.add_option("--max_dist", dest="max_dist", type=int, default=220)
    parser.add_option("--genome", dest="genome", default='mm9')
    parser.add_option("--outfile", dest="outfile", default=None)
    (opts, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    a=args[0]

    seq_msp(a,opts.outfile,genome=opts.genome)

if __name__=='__main__': main()
