#!/usr/bin/bash

# To use this script, copy Genomes_Stats_Summary.sh and Stats_sum.R to a folder containing all genomes stats files.
# Do " bash Genomes_Stats_Summary.sh " inside a folder. 


for file in *.stats.txt; do
   sed  "s:Assembly statistics:Assembly_statistics:g; s:CONTIG COUNT:CONTIG_COUNT:g; s:TOTAL LENGTH:TOTAL_LENGHT:g" "$file" > "${file}_fix.txt"
done 

if [ ! -f Assembly_stats_summary.csv ]; then
   Rscript Stats_sum.R
fi
