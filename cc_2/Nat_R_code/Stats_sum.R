## This is a script for converting stats files and combine them all in a single summary file.
## This script will be called when "Genomes_Stats_Summary.sh" is run.

## Make a list of files.
files = list.files(pattern="_fix.txt")
## Read all file in the list, transpose, and add to dataframe
DF <- NULL
for (f in files) {
  dat = read.table(f, header=T, sep="", stringsAsFactors = F)
  dat.noequal = dat[, -2]
  t.dat = t(dat.noequal)
  DF = rbind(DF, t.dat)
}

colnames(DF) = DF[1, ]
DF = DF[-1, ]

DF = as.data.frame(DF)

NewDF = DF[c(T,F),]

write.csv(NewDF, file="Assembly_stats_summary.csv")