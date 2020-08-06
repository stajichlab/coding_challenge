Ying's coding challenge- organizing and subsetting data- methylation

Instructions


Question: How do you make this more efficient? 
=============

Goal: 
1. For each coordinate defined in the bedfile
2. Expand the coordinate to a particular window (for example 100 bp (which is 50 bp on each side)), try to make this amenable to change
3. Get the data that fall within the coordinate from each of the tables
4. For each data for each table, calculate
5. How many total C's
6. How many methylated C's
7. What is the % of methylated C's 
8. How many total CG
9. How many methylated C's
10. What is the % of methylated C's 
11. How many total CHG
12. How many methylated C's
13.What is the % of methylated C's 
14.How many total CHH
15. Print output in text format, tab delimited where the columns look like this
	

```
Chromosome number
Start position
Stop position
# a set of data like this for every .tsv file
All C's
All methylated C's	
% of methylated C's relative to All C's
All C's that are categorized as CGs
All methylated C's that are categorized as CGs
% of methylated C's relative to C's that are categorized as CGs
All C's that are categorized as CHGs
All methylated C's that are categorized as CHGs
% of methylated C's relative to C's that are categorized as CHGs
All C's that are categorized as CHHs
All methylated C's that are categorized as CHHs
% of methylated C's relative to C's that are categorized as CHHs

#######
Example headers:
mPingChr 
mPingSTART 
mPingSTOP                              
mPingDetails   
A119_allC 
A119_allmethylated
A119_._allmethylated 
A119_CG A119_CGmethylated 
A119_._CGmethylated 
A119_CHG 
A119_CHGmethylated
A119_._CHGmethylated 
A119_CHH 
A119_CHHmethylated 
A119_._CHHmethylated 
A123_allC A123_allmethylated
A123_._allmethylated 
A123_CG 
A123_CGmethylated 
A123_._CGmethylated 
A123_CHG A123_CHGmethylated
A123_._CHGmethylated 
A123_CHH 
A123_CHHmethylated 
A123_._CHHmethylated 
EG4_allC EG4_allmethylated
EG4_._allmethylated 
EG4_CG EG4_CGmethylated 
EG4_._CGmethylated 
EG4_CHG 
EG4_CHGmethylated 
EG4_._CHGmethylated
EG4_CHH 
EG4_CHHmethylated 
EG4_._CHHmethylated 
HEG4_allC 
HEG4_allmethylated 
HEG4_._allmethylated 
HEG4_CG
HEG4_CGmethylated 
HEG4_._CGmethylated 
HEG4_CHG 
HEG4_CHGmethylated 
HEG4_._CHGmethylated 
HEG4_CHH
HEG4_CHHmethylated 
HEG4_._CHHmethylated
#######
----
Input: 
- a bedfile with coordinates


### Data looks like this- this is a bedfile with sites
#### Columns are: Chr, start, stop, extra information
```
1       1041521 1041523 Chr1_1041521;Strains=A119_2;GT=homozygous
1       1116559 1116561 Chr1_1116559;Strains=EG4_2;GT=homozygous
1       1193505 1193507 Chr1_1193505;Strains=A123_2;GT=homozygous
1       1374937 1374939 Chr1_1374937;Strains=A123_2;GT=homozygous
1       14384274        14384276        Chr1_14384274;Strains=HEG4_2;GT=homozygous
```

----

- 4 zipped tables of data- these are tsv files of 5mC data processed
```
#short_allc_A119.tsv.gz
#short_allc_A123.tsv.gz
#short_allc_EG4.tsv.gz
#short_allc_HEG4.tsv.gz
```

### longer length files can be found here: /bigdata/wesslerlab/ysun/cc_3
```
############ Data looks like this #########################################################################
Chr1    1041    +       CCC     0       4       0
Chr1    1042    +       CCT     1       4       0
Chr1    1043    +       CTA     1       4       0
Chr1    1048    +       CCC     0       4       0
Chr1    1049    +       CCT     0       4       0
Chr1    1050    +       CTA     1       4       0
############################################################################
```
```
### columns are ######
Column1: chromosome
Column2: cytosine position
Column3: strand
Column4: CNN (N = A, T, C, G)
Column5: methylated cytosines at this site
Column6: methylated and unmethylated cytosines at this site
Column7: binomial test, 1 = pass, 0 = fail
```

Example code is available in script `ying_bash_solution.sh`

# define window from bedfile (this case it's 50 bp from each side)

```awk -v proximal=50 -v distal=50 '{print $1 "\t" $2-proximal "\t" $3+distal "\t" $4}' all_empty_sites.bed > all_empty_sites.50_window.bed```

# create individual files for all the coordinates

```
#!/bin/bash
#SBATCH -p short

module load bcftools

BEDFILE="all_empty_sites.50_window.bed"

cat $BEDFILE | while read CHROM START END DETAILS
do
 #echo "Chrom=$CHROM START=$START END=$END"
 Chrom=$CHROM 
 START=$START 
 END=$END
 DETAILS=$DETAILS
 tabix allc_A119.tsv.gz Chr${Chrom}:${START}-${END} > "./newbedfiles/A119_Chr${Chrom}:${START}-${END}.bed"
 tabix allc_A123.tsv.gz Chr${Chrom}:${START}-${END} > "./newbedfiles/A123_Chr${Chrom}:${START}-${END}.bed"
 tabix allc_EGH.tsv.gz Chr${Chrom}:${START}-${END} > "./newbedfiles/EGH_Chr${Chrom}:${START}-${END}.bed"
 tabix allc_HEG4.tsv.gz Chr${Chrom}:${START}-${END} > "./newbedfiles/HEG4_Chr${Chrom}:${START}-${END}.bed"
 #tabix allc_A119.tsv.gz Chr1:9000-9100 > "./newbedfiles/${Chrom}:${START}-${END}.bed"
done
```
# takes each file and subset by CG, CHG, CHH then calculate associated


# plotting in R
plot using `ying_plot.R` R script











