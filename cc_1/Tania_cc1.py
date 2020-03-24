#Tania Kurbessoian
#Coding Challenge 1 Submission
#Python

import sys
import csv
import pandas

fname = sys.argv[1] #This allows user to input any bed file to be counted
print("How many features are in the file?")
count = 0 #start with zero
f = open(fname, "r")
for line in f:
 count += 1  #made each line iterate to be counted
print("Total number of lines are:", count)

print("How many genes are in the file?")
count = 0
with open(fname, 'r') as f:
    for line in f.readlines():
        if 'Gene' in line:
         count +=1 #iterating again
    print("Total number of genes are", count)

#couldn't figure this out without using pandas.
print("What are the types of features?")
feat = pandas.read_csv(fname, sep ='\t', header = None)
feature_types = feat[3].str.split("-", expand = True) #take fourth column, split when - is present
print("Types of features include", feature_types[0].unique()) #take first part before -, add unique to get unique features only

print("How many of each type of feature?")
feat = pandas.read_csv(fname,sep ='\t', header = None)
feature_types =	feat[3].str.split("-", expand =	True)
print("Total number of unique features are:")
print(feature_types[0].value_counts()) #take value counts of each feature type

print("How many bases in each type of feature?")
max = feat[2] 
min = feat[1]
feat[4] = abs(max - min) #made my own column with subtracted values of max and min, make sure to take the absolute value
print("Bases in each feature")
print(feat[feat.columns[3:5]]) #combined column 3 with new column 4

print("Print out the Genes in order of largest to smallest.")
genes=(feat[feat[3].str.contains('Gene')]) #look within column 3 for the word Gene
print(genes.sort_values(genes.columns[4], ascending = False).to_string(index = False)) #sort basepair values from largest to smallest.
