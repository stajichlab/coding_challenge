# Nat_R_Code instructions

To summarize all genomes stats in a folder:
1. Copy [Genomes_Stats_Summary.sh](Genomes_Stats_Summary.sh) to genome_stats folder

```
cp Genomes_Stats_Summary.sh ../genome_stats
```

2. Copy [Stats_sum.R](Stats_sum.R) to genome_stats folder

```
cp Stats_sum.R ../genome_stats
```

3. Run Genomes_Stats_Summary.sh in genome_stats folder

```
bash Genomes_Stats_Summary.sh
```

4. Output is [Assembly_stats_summary.csv](Assembly_stats_summary.csv)

-Warning-these scripts will create new stat files(*_fix.txt)  which will work with Rscript and can be deleted when done. 
