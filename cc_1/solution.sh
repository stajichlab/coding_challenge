#!/usr/bin/bash

FEATUREFILE=features.bed
echo "How many feature are in the file?"
wc -l $FEATUREFILE

echo "How many genes are in the file?"
grep -c "Gene" $FEATUREFILE

echo "What are the types features?"
cut -f4 $FEATUREFILE | cut -d\- -f1 | sort | uniq 

echo "How many of each type of feature?"
cut -f4 $FEATUREFILE | cut -d\- -f1 | sort | uniq -c

echo "How many bases are contained in each type of feature?"


echo "Print out the genes in order of their size"
grep Gene $FEATUREFILE | awk 'function abs(v) {return v < 0 ? -v : v}
    {print abs($3 - $2 ), $4 }' | sort -n
