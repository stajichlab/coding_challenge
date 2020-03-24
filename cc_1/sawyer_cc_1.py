
from operator import itemgetter
bedfile=open("features.bed",'r')

num_feat=0
num_gene=0

feat_list=set()
feat_dict={}
length_dict={}
list=[]
for line in bedfile:
	num_feat +=1
	linearr=line.split()
	feature = linearr[3].split('-')
	if "Gene" in feature[0]:
		num_gene+=1
	
	if feature[0] not in feat_dict:
		feat_dict[feature[0]]=0
		length_dict[feature[0]]=0
	feat_dict[feature[0]]+=1
	feat_list.add(feature[0])
	length=abs(int(linearr[2])-int(linearr[1]))
	length_dict[feature[0]]+=length
	list.append(linearr)
	list[-1].append(length)
print "How many features are in the file? " + str(num_feat)
print "How many genes are in the file? " + str(num_gene)

items=' '
for item in feat_list:
	items+=item + ', '

print "The features in the file are" + items
for key,value in feat_dict.items():
	print "There are " + str(value) + " of feature " + key

for key,value in length_dict.items():
        print "The total length of all " + key + " is " + str(value)


sorted_list=sorted(list,key=itemgetter(4),reverse=True)

for line in sorted_list:
	if "Gene" in line[3]:
		print line[3] + " " + str(line[4])
