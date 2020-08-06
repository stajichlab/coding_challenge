Ying's coding challenge- organizing and subsetting data- methylation

Instructions


Question: How do you make this more efficient? 
=============

Goal: 
1. For each coordinate defined in the bedfile
2. Get the data that fall within the coordinate from each of the tables
3. For each data for each table, calculate
4. How many total C's
5. How many methylated C's
6. What is the % of methylated C's 
7. How many total CG
8. How many methylated C's
9. What is the % of methylated C's 
10. How many total CHG
11. How many methylated C's
12.What is the % of methylated C's 
13.How many total CHH
14. Print output in text format, tab delimited where the columns look like this
	
```
"$chrom"	
"$start"	
"$stop"	


# a set of data like this for every table of data
"$allD"	
"$methylatedD"	
"$percentD"	
"$allCG" 
"$methylatedCG"	
"$percentCG" 
"$allCHG" 
"$methylatedCHG"	
"$percentCHG" 
"$allCHH" 
"$methylatedCHH"	
"$percentCHH"
```
----
Input: 
- a bedfile with coordinates


### Data looks like this
#### Columns are: Chr, start, stop, extra information
```
1       1041521 1041523 Chr1_1041521;Strains=A119_2;GT=homozygous
1       1116559 1116561 Chr1_1116559;Strains=EG4_2;GT=homozygous
1       1193505 1193507 Chr1_1193505;Strains=A123_2;GT=homozygous
1       1374937 1374939 Chr1_1374937;Strains=A123_2;GT=homozygous
1       14384274        14384276        Chr1_14384274;Strains=HEG4_2;GT=homozygous
```

----

- 4 zipped tables of data
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
############
awk -v proximal=50 -v distal=50 '{print $1 "\t" $2-proximal "\t" $3+distal "\t" $4}' all_empty_sites.bed > all_empty_sites.50_window.bed

# create individual files for all the coordinates
############

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

# takes each file and subset by CG, CHG, CHH then calculate associated
############


# plotting in R
plot using `ying_plot.R` R script











