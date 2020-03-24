#!/usr/bin/env python3

import csv

file="features.bed"

features = {}
lengths  = {}

feature_count = 0
gene_count = 0 

with open(file,'r') as fh:
    bedfile = csv.reader(fh,delimiter="\t")
    for row in bedfile:
        feature_count += 1
        type = row[3].split('-')[0]
        row.append(abs(int(row[2]) - int(row[1])))
        if type not in features:
            features[type] = []
            
        features[type].append(row)
        
        if row[3].startswith('Gene'):
            gene_count += 1

# while(<$fh>) {
#     $count ++;
#     chomp;
#     my @row = split(/\t/,$_);
#     my ($chrom,$start,$end,$feature) = @row;
#     # either split on -
#     my ($type,$name) = split('-',$feature);
#     # or use pattern
#     #if ( $feature =~ /(\S+)-(\S+)/ ) {
#     #($type,$name) = ($1,$2);
#     #}
#     push @{$features{$type}}, [ $chrom, $start, $end, $feature,
# 				abs($end - $start), $name];
#     $lengths{$type} += abs($end - $start);
#     if ( $type eq 'Gene' ) {
# 	$genes++;
#     }
# }

	
print("How many feature are in the file?")
print(feature_count)

print("How many genes are in the file?")
print(gene_count)


print("What are the types features?")
for type in features:
    print(type)

print("How many of each type of feature?")
for type in features:
    print("%d\t%s"%(len(features[type]),type))


print("How many bases are contained in each type of feature?")
for type in features:
    total = 0
    for f in features[type]:
        total += f[4]
    print("%d\t%s"%(total,type))


print("Print out the genes in order of their size");
for gene in sorted(features['Gene'],key=lambda g: g[4]):
    print("%s\t%d"%(gene[3],gene[4]))
