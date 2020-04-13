#Tania Kurbessoian
#Coding Challenge 2 Submission
#Python

import glob
import sys


print("SampleID\tCONTIG COUNT\tTOTAL LENGTH\tMIN\tMAX\tMEDIAN\tMEAN\tL50\tN50\tL90\tN90")
for file in glob.glob("/rhome/tkurb001/bigdata/Workshops/coding_challenge/cc_2/genome_stats/*.txt"):
        f=open(file,"r")
        dictionary = {} #initializing an empty dictionary
        for line in f:
                #print(f)
                #print(line)
                if ":" in line:                                  #for the first line in the file, we want to save the name
                        header = line.split(":")                       #split when we see this
                        #print(header)
                        key = header[1].strip()                        #let's grab everything after the : and remove space
                        #print(key)
                        dictionary["SampleID"] = key.strip(".fna")   #editing the names to remove the .fna and saving into dictionary
                       #print(dictionary)
                elif "=" in line:                                #for lines underneath the first line
                        header = line.split("=")                       #splitting the line when we come across =
                        #print(header)
                        dictionary[header[0].strip()] = header[1].strip()	#saving words before = to be the key.   #The value on the right is the numbers after the =.

        print ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (dictionary["SampleID"], dictionary["CONTIG COUNT"], dictionary["TOTAL LENGTH"], dictionary["MIN"], dictionary["MAX"], dictionary["MEDIAN"], dictionary["MEAN"], dictionary["L50"], dictionary["N50"], dictionary["L90"], dictionary["N90"]))

        #last line long winded version of printing our results into one line.
