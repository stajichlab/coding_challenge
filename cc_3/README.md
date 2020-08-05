Ying's coding challenge- organizing and subsetting data- methylation

Instructions


Question: How do you make this more efficient? 
############################################################################
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
############################################################################
Input: 
- a bedfile with coordinates

#### Data looks like this #####
#### Columns are: Chr, start, stop, extra information
1       1041521 1041523 Chr1_1041521;Strains=A119_2;GT=homozygous
1       1116559 1116561 Chr1_1116559;Strains=EG4_2;GT=homozygous
1       1193505 1193507 Chr1_1193505;Strains=A123_2;GT=homozygous
1       1374937 1374939 Chr1_1374937;Strains=A123_2;GT=homozygous
1       14384274        14384276        Chr1_14384274;Strains=HEG4_2;GT=homozygous
############################################################################
- 4 zipped tables of data
#short_allc_A119.tsv.gz
#short_allc_A123.tsv.gz
#short_allc_EG4.tsv.gz
#short_allc_HEG4.tsv.gz
### longer length can be found here: /rhome/ysun/bigdata/cc_3
############ Data looks like this #########################################################################
Chr1    1041    +       CCC     0       4       0
Chr1    1042    +       CCT     1       4       0
Chr1    1043    +       CTA     1       4       0
Chr1    1048    +       CCC     0       4       0
Chr1    1049    +       CCT     0       4       0
Chr1    1050    +       CTA     1       4       0
############################################################################

### columns are ######
Column1: chromosome
Column2: cytosine position
Column3: strand
Column4: CNN (N = A, T, C, G)
Column5: methylated cytosines at this site
Column6: methylated and unmethylated cytosines at this site
Column7: binomial test, 1 = pass, 0 = fail



########################################################################################################################################################
Below is a code that currently works- written in bash
########################################################################################################################################################

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
#!/bin/bash
#SBATCH -p short

file=/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/*.bed

#file=/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/A123_Chr4:25028644-25028746.bed




for f in $file
do
	basename "$f"
	filename="$(basename -- $f)"
	echo "Processing $filename file ..."	
	
    types=$(echo "$filename" | cut -d'_' -f1)
    echo "$types"
    chrom=$(echo "$filename" | cut -d'_' -f2 | cut -d':' -f1)
    echo "$chrom"
    start=$(echo "$filename" | cut -d'_' -f2 | cut -d':' -f2 | cut -d'-' -f1)
    echo "$start"
    stop=$(echo "$filename" | cut -d'_' -f2 | cut -d':' -f2 | cut -d'-' -f2| cut -d'.' -f1)
    echo "$stop"
    
    #Subset by methylation status
    CG=$(grep "CG[ACT]" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename)
    CHG=$(grep "C[ACT]G" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename)
    CHH=$(grep "C[ACT][ACT]" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename)
	
	echo "listofCG $CG"
    echo "listofCHG $CHG"
    echo "listofCHH $CHH"

	#This is all C's
    allD=$(wc -l < /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename)
    echo "$allD"
    
    allCG=$(grep "CG[ACTG]" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename | wc -l)
    allCHG=$(grep "C[ACT]G" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename | wc -l)
    allCHH=$(grep "C[ACT][ACT]" /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename | wc -l)
    echo "allCG # $allCG"
    echo "allCHG # $allCHG"
    echo "allCHH # $allCHH"
    

    # This is all methylated
    methylatedD=$(awk -F"\t" '$7 == "1" { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7 }' /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/$filename | wc -l)
    echo "all methyl = $methylatedD"
    
    methylatedCG=$(echo "$CG" | awk -F"\t" '$7 == "1" { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7 }' | wc -l)
    methylatedCHG=$(echo "$CHG" | awk -F"\t" '$7 == "1" { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7 }' | wc -l)
    methylatedCHH=$(echo "$CHH" | awk -F"\t" '$7 == "1" { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6"\t"$7 }' | wc -l)
    
    echo "methylatedCG $methylatedCG"
    echo "methylatedCHG $methylatedCHG"
    echo "methylatedCHH $methylatedCHH"

    if (($allD > 0)); then
    divideD=$(echo $(echo "$methylatedD/$allD" | bc -l ))
    percentD=$(echo $(echo "$divideD * 100" | bc -l ))
    echo "calculated number for all is $divideD and then times 100 $percentD"
    else    
    percentD="NA"    
    echo "NA"
	fi

    if (($allCG > 0)); then
    divideCG=$(echo $(echo "$methylatedCG/$allCG" | bc -l ))
    percentCG=$(echo $(echo "$divideCG * 100" | bc -l ))
    echo "calculated number for CG is $divideCG and then times 100 $percentCG"
    else    
    percentCG="NA"   
    echo "NA"
	fi
	
	if (($allCHG > 0)); then
    divideCHG=$(echo $(echo "$methylatedCHG/$allCHG" | bc -l ))
    percentCHG=$(echo $(echo "$divideCHG * 100" | bc -l ))
    echo "calculated number for CHG is $divideCHG and then times 100 $percentCHG"
    else    
    percentCHG="NA"   
    echo "NA"
	fi
	
	if (($allCHH > 0)); then
    divideCHH=$(echo $(echo "$methylatedCHH/$allCHH" | bc -l ))
    percentCHH=$(echo $(echo "$divideCHH * 100" | bc -l ))
    echo "calculated number for CHH is $divideCHH and then times 100 $percentCHH"
    else    
    percentCHH="NA"  
    echo "NA"
	fi

    echo "$types"	"$chrom"	"$start"	"$stop"	"$allD"	"$methylatedD"	"$percentD"	"$allCG" "$methylatedCG"	"$percentCG" "$allCHG" "$methylatedCHG"	"$percentCHG" "$allCHH" "$methylatedCHH"	"$percentCHH"
    echo "$types"	"$chrom"	"$start"	"$stop"	"$allD"	"$methylatedD"	"$percentD"	"$allCG" "$methylatedCG"	"$percentCG" "$allCHG" "$methylatedCHG"	"$percentCHG" "$allCHH" "$methylatedCHH"	"$percentCHH" >> /rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/newbedfiles/"Methyl.bed"
done

# This then combines all the data together (written in R)
library(plyr)

setwd ("/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest")

Main = read.table("/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/emptysiteRNA.txt", sep = '\t', header = TRUE, stringsAsFactors = FALSE)

Methyldata = read.table("./Methyl.bed", sep = ' ', header = FALSE, stringsAsFactors = FALSE)
Methyldata = rename(Methyldata, c("V1"="type", "V2"="chrom" , "V3"="start" , "V4"="stop" , "V5"="allC" , "V6"="allmethylated" , "V7"="all%methylated", "V8"="CG" , "V9"="CGmethylated" , "V10"="CG%methylated", "V11"="CHG" , "V12"="CHGmethylated" , "V13"="CHG%methylated", "V14"="CHH" , "V15"="CHHmethylated" , "V16"="CHH%methylated"))
Methyldata$`all%methylated` = round (Methyldata$`all%methylated`,2)
Methyldata$`CG%methylated` = round (Methyldata$`CG%methylated`,2)
Methyldata$`CHG%methylated` = round (Methyldata$`CHG%methylated`,2)
Methyldata$`CHH%methylated` = round (Methyldata$`CHH%methylated`,2)

A119_data = Methyldata[1:777,]
A119_data = rename(A119_data, c("allC"="A119_allC" , "allmethylated"="A119_allmethylated" , "all%methylated"="A119_%_allmethylated", "CG"="A119_CG" , "CGmethylated"="A119_CGmethylated" , "CG%methylated"="A119_%_CGmethylated", "CHG"="A119_CHG" , "CHGmethylated"="A119_CHGmethylated" , "CHG%methylated"="A119_%_CHGmethylated", "CHH"="A119_CHH" , "CHHmethylated"="A119_CHHmethylated" , "CHH%methylated"="A119_%_CHHmethylated"))
A123_data = Methyldata[778:1554, c(3, 5:16)]
A123_data = rename(A123_data, c("allC"="A123_allC" , "allmethylated"="A123_allmethylated" , "all%methylated"="A123_%_allmethylated", "CG"="A123_CG" , "CGmethylated"="A123_CGmethylated" , "CG%methylated"="A123_%_CGmethylated", "CHG"="A123_CHG" , "CHGmethylated"="A123_CHGmethylated" , "CHG%methylated"="A123_%_CHGmethylated", "CHH"="A123_CHH" , "CHHmethylated"="A123_CHHmethylated" , "CHH%methylated"="A123_%_CHHmethylated"))
EG4_data = Methyldata[1555:2331, c(3, 5:16)]
EG4_data = rename(EG4_data, c("allC"="EG4_allC" , "allmethylated"="EG4_allmethylated" , "all%methylated"="EG4_%_allmethylated", "CG"="EG4_CG" , "CGmethylated"="EG4_CGmethylated" , "CG%methylated"="EG4_%_CGmethylated", "CHG"="EG4_CHG" , "CHGmethylated"="EG4_CHGmethylated" , "CHG%methylated"="EG4_%_CHGmethylated", "CHH"="EG4_CHH" , "CHHmethylated"="EG4_CHHmethylated" , "CHH%methylated"="EG4_%_CHHmethylated"))
HEG4_data =  Methyldata[2332:3108, c(3, 5:16)]
HEG4_data = rename(HEG4_data, c("allC"="HEG4_allC" , "allmethylated"="HEG4_allmethylated" , "all%methylated"="HEG4_%_allmethylated", "CG"="HEG4_CG" , "CGmethylated"="HEG4_CGmethylated" , "CG%methylated"="HEG4_%_CGmethylated", "CHG"="HEG4_CHG" , "CHGmethylated"="HEG4_CHGmethylated" , "CHG%methylated"="HEG4_%_CHGmethylated", "CHH"="HEG4_CHH" , "CHHmethylated"="HEG4_CHHmethylated" , "CHH%methylated"="HEG4_%_CHHmethylated"))

joinA123 = left_join(A119_data, A123_data, by = "start")
joinEG4 = left_join(joinA123, EG4_data, by = "start")
joinHEG4 = left_join(joinEG4, HEG4_data, by = "start")

methylfinal = joinHEG4[, c(2:52)]
methylfinal$chrom = as.numeric(gsub( "Chr", "", as.character(methylfinal$chrom)))
methylfinal$start = methylfinal$start + 50
methylfinal$stop = methylfinal$stop - 50
methylfinalfinal = rename(methylfinal, c("chrom"="mPingChr" , "start"="mPingSTART" , "stop"="mPingSTOP"))

joinfinal = left_join(Main, methylfinalfinal, by = c("mPingChr", "mPingSTART", "mPingSTOP"))

write.table(joinfinal,"emptysiteRNAMethyl.txt",sep="\t",row.names=FALSE)














