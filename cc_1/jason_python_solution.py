#!/usr/bin/env python3

import csv
file="features.bed"

# dictionary for storing the features
features = {}

# some convience counters to show basics (these are unnecessary
# if you just get the numbers from features dictionary
feature_count = 0
gene_count = 0 

# open the file in a protected 
with open(file,'r') as fh:
    bedfile = csv.reader(fh,delimiter="\t")
    for row in bedfile:
        feature_count += 1
        # feature types are encoded as
        # FEATURETYPE-NAME
        # separated by '-' so use split to break apart
        # in this case only want the type so we get the first
        # value in the array returned by split but using [0]
        type = row[3].split('-')[0]

        # caculate the length of the feature (end - start)
        # this value is then appended to the feature row
        # adding a new column to the dataset
        row.append(abs(int(row[2]) - int(row[1])))
        # for python we need to create an empty array if
        # this feature has not been stored before
        if type not in features:
            features[type] = []

        # now store the array in the dictionary
        # these will be stacked up by feature type
        # so the gene feature will have entries all under
        # the features['Gene'] slot in the dictionary
        features[type].append(row)

        # use our special counter just to count the number of genes
        # by checking to see if feature name starts with a type
        # sort of unnecessary but demonstrates some basic
        # python code
        if row[3].startswith('Gene'):
            gene_count += 1
	
    print("How many feature are in the file?")
    print(feature_count,"\n")

    print("How many genes are in the file?")
    print(gene_count,"\n")
    # could also do
    #print(len(features['Gene']),"\n")


    print("What are the types features?")
    for type in features:
        print(type)

    print() # an empty line
    print("How many of each type of feature?")
    for type in features:
        print("%d\t%s"%(len(features[type]),type))

    print() # some empty space
    print("How many bases are contained in each type of feature?")
    # to compute the feature lengths we just need to go through
    # and add up all the lengths for the feature type
    # eg 'Gene' 'tRNA' etc
    # remember we added an extra column which computed the feature
    # length this is stored in [4] in each feature array
    for type in features:
        total = 0
        for f in features[type]:
            total += f[4]
            print("%d\t%s"%(total,type))

    print() # empty line
    print("Print out the genes in order of their size");
    # use the sorted function in python to use
    # data stored for length of feature in last column of the array
    # for each feature
    for gene in sorted(features['Gene'],key=lambda g: g[4]):
        print("%s\t%d"%(gene[3],gene[4]))
