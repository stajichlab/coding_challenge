#!/usr/bin/env python3

# upload modules
import pandas as pd
import numpy as np
import re

# open file
content = pd.read_csv('/Carnegie/DPB/Data/Shared/Labs/Dinneny/Private/Ysun/2020/challenge/features.bed',sep='\t',names=["Chr", "Start", "End", "Features"])
print("This is what is in the file:")
print (content)

#How many features are in the file?
print("How many features are in the file?")
# count number of unique names in column 4

# python starts at 0, so to get the 4th column, it's 3 instead of 4

# len counts how many
# drop_duplicates removes duplicates
content.drop_duplicates(subset=["Features"], inplace=True)
# len is used to count
print(len(content.iloc[:,[3]]))

  
#How many genes are in the file?
print("How many genes are in the file?")

# found solution here https://stackoverflow.com/questions/51027453/count-how-many-times-a-column-contains-a-certain-value-in-pandas
columaftersplit = content["Features"].str.split('-', expand=True).stack().value_counts()
print (columaftersplit [0])


#What are the types of features?
print("What are the types of features?")
featuretype = content["Features"].str.split('-', expand=True)
verticallist = list(featuretype[0].unique())

	# to print vertically
print(*verticallist, sep = "\n") 
    
#How many of each type of feature?
print("How many of each type of feature?")

countfeaturetype = content["Features"].str.split('-', expand=True)
countfeaturetype.columns = ["Feature", "Featuretype"]
countfeatureoutput = countfeaturetype.groupby("Feature").count()
print (countfeatureoutput)

#How many bases are contained in each type of feature?
print("How many bases are contained in each type of feature?")

content["# of bases"] = abs(content["End"] - content["Start"])
#print (content)
# this will get you the 2 columns, not 3:4
basespairs = content.iloc[:,3:5]
print("\n# of bases for each type of feature :\n", basespairs) 

#Print out the Genes in order of largest to smallest.
print("Print out the Genes in order of largest to smallest")

search ="Gene"
bool_series = basespairs["Features"].str.startswith(search)
Geneonly = basespairs[bool_series]

final = Geneonly.sort_values(by="# of bases",ascending=False)

print (final)




