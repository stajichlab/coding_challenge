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
