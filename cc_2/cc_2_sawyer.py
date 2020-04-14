import sys
import os

if len(sys.argv) < 2: 
    print "Usage: cc_2_smaso.py filedir"
    exit

#filewriter = open("summary.stats",'w')


for file in os.listdir(sys.argv[1]):
    if file.endswith("stats.txt"):
        filename=sys.argv[1] + file
        filereader = open(filename, 'r')
        stats_dict={}
        for line in filereader:
            if ":" in line:
                linearr= line.split(':')
                sample_id=linearr[1].strip()
    
                stats_dict["SampleID"]=sample_id.strip(".fna") 
            elif "=" in line:
                linearr= line.split('=')
                stats_dict[linearr[0].strip()]=linearr[1].strip()

        filereader.close()
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (stats_dict["SampleID"],stats_dict["CONTIG COUNT"],stats_dict["TOTAL LENGTH"],stats_dict["MIN"],stats_dict["MAX"],stats_dict["MEDIAN"],stats_dict["MEAN"],stats_dict["L50"],stats_dict["N50"],stats_dict["L90"],stats_dict["N90"])
        
