# to plot the summary stats

genomestats <- read.csv("genome_stats.tsv",sep="\t",header=TRUE)

plot(genomestats$CONTIG.COUNT,genomestats$TOTAL.LENGTH)
hist(genomestats$N50,20)
hist(genomestats$CONTIG.COUNT,20)
