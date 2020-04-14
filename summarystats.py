#!/usr/bin/env python3

# upload modules
import pandas as pd
import numpy as np
import re
import glob
import csv
import sys

# open files
path = "genome_stats/*.txt"

text = []
for filename in glob.glob(path):
	with open (filename, 'r') as f:
		for line in f: 
			# change : to an =, and use sample ID instead
			line = line.replace("Assembly statistics for:", "SampleID =")
			# remove the end of the text name
			line = line.replace(".fna", "")
			#print (line)
			# separate by =
			for word in line.split (" = "):
			# remove space at the end
				word = word.strip('\n')
				text.append(word)

sorted = [text[i:i+2] for i in range(0, len(text), 2)]

# Creating a dataframe object from listoftuples
dfObj = pd.DataFrame(sorted) 

# transposed
df1_transposed = dfObj.T



for chunk in np.array_split(dfObj, 246):  # 50 chunks
	chunk = chunk.T
	#print (chunk)
	file = open('output.txt', 'a')
	sys.stdout = file
	print(chunk) 
