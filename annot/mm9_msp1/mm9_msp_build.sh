#!/bin/bash

#EBWT="ch_list="chr1.fa,chr2.fa,chr3.fa,chr4.fa,chr5.fa,chr6.fa,chr7.fa 8.fa 9.fa 10.fa 11.fa 12.fa 13.fa 14.fa 15.fa 16.fa 17.fa 18.fa 19.fa chrX.fa,chrY.fa"
ch_list="2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 X Y"
REF="chr1.fa"
for c in $ch_list
do
    REF="$REF,chr$c.fa"
done

EBWT="./mm9_msp1.ebwt"

CMD="bowtie-build $REF $EBWT"
echo $CMD
$CMD
