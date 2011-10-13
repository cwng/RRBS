#!/bin/bash

ch_list="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 X Y"

genome_dir="/nfs/genomes/mouse_gp_jul_07/"

for c in $ch_list
do
    OUTFILE="../../annot/mm9_msp1_no_convert/chr$c.fa"
    CMD="/home/cwng/wqsub.py python find_msp_sites.py --bedFrag --outfile $OUTFILE $genome_dir/chr$c.fa"
    echo $CMD
    $CMD
done

