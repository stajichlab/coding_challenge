#!/bin/bash -l

cut -d"=" -f1 genome_stats/*.stats.txt | tail -n 10 > firstline.txt
tr '\n' '\t' < firstline.txt > summary.txt
sed -i -e "s/^/SampleID/" summary.txt
for i in genome_stats/*.stats.txt
do
b=$(basename $i .stats.txt)
#d=$(cut -d"=" -f2 $i | tail -n 10)
cut -d"=" -f2 $i | tail -n 10 > nextline.txt
d2=$(tr '\n' '\t' < nextline.txt)
echo -e $b "\t" "$d2" >> summary.txt
done

rm firstline.txt nextline.txt 
