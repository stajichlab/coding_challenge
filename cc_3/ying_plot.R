# This then combines all the data together (written in R)
library(plyr)

setwd ("/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest")

Main = read.table("/rhome/ysun/bigdata/epigenome/attack_ATAC/results/Closest/emptysiteRNA.txt", sep = '\t', header = TRUE, stringsAsFactors = FALSE)

Methyldata = read.table("./Methyl.bed", sep = ' ', header = FALSE, stringsAsFactors = FALSE)
Methyldata = rename(Methyldata, c("V1"="type", "V2"="chrom" , "V3"="start" , "V4"="stop" , "V5"="allC" , "V6"="allmethylated" , "V7"="all%methylated", "V8"="CG" , "V9"="CGmethylated" , "V10"="CG%methylated", "V11"="CHG" , "V12"="CHGmethylated" , "V13"="CHG%methylated", "V14"="CHH" , "V15"="CHHmethylated" , "V16"="CHH%methylated"))
Methyldata$`all%methylated` = round (Methyldata$`all%methylated`,2)
Methyldata$`CG%methylated` = round (Methyldata$`CG%methylated`,2)
Methyldata$`CHG%methylated` = round (Methyldata$`CHG%methylated`,2)
Methyldata$`CHH%methylated` = round (Methyldata$`CHH%methylated`,2)

A119_data = Methyldata[1:777,]
A119_data = rename(A119_data, c("allC"="A119_allC" , "allmethylated"="A119_allmethylated" , "all%methylated"="A119_%_allmethylated", "CG"="A119_CG" , "CGmethylated"="A119_CGmethylated" , "CG%methylated"="A119_%_CGmethylated", "CHG"="A119_CHG" , "CHGmethylated"="A119_CHGmethylated" , "CHG%methylated"="A119_%_CHGmethylated", "CHH"="A119_CHH" , "CHHmethylated"="A119_CHHmethylated" , "CHH%methylated"="A119_%_CHHmethylated"))
A123_data = Methyldata[778:1554, c(3, 5:16)]
A123_data = rename(A123_data, c("allC"="A123_allC" , "allmethylated"="A123_allmethylated" , "all%methylated"="A123_%_allmethylated", "CG"="A123_CG" , "CGmethylated"="A123_CGmethylated" , "CG%methylated"="A123_%_CGmethylated", "CHG"="A123_CHG" , "CHGmethylated"="A123_CHGmethylated" , "CHG%methylated"="A123_%_CHGmethylated", "CHH"="A123_CHH" , "CHHmethylated"="A123_CHHmethylated" , "CHH%methylated"="A123_%_CHHmethylated"))
EG4_data = Methyldata[1555:2331, c(3, 5:16)]
EG4_data = rename(EG4_data, c("allC"="EG4_allC" , "allmethylated"="EG4_allmethylated" , "all%methylated"="EG4_%_allmethylated", "CG"="EG4_CG" , "CGmethylated"="EG4_CGmethylated" , "CG%methylated"="EG4_%_CGmethylated", "CHG"="EG4_CHG" , "CHGmethylated"="EG4_CHGmethylated" , "CHG%methylated"="EG4_%_CHGmethylated", "CHH"="EG4_CHH" , "CHHmethylated"="EG4_CHHmethylated" , "CHH%methylated"="EG4_%_CHHmethylated"))
HEG4_data =  Methyldata[2332:3108, c(3, 5:16)]
HEG4_data = rename(HEG4_data, c("allC"="HEG4_allC" , "allmethylated"="HEG4_allmethylated" , "all%methylated"="HEG4_%_allmethylated", "CG"="HEG4_CG" , "CGmethylated"="HEG4_CGmethylated" , "CG%methylated"="HEG4_%_CGmethylated", "CHG"="HEG4_CHG" , "CHGmethylated"="HEG4_CHGmethylated" , "CHG%methylated"="HEG4_%_CHGmethylated", "CHH"="HEG4_CHH" , "CHHmethylated"="HEG4_CHHmethylated" , "CHH%methylated"="HEG4_%_CHHmethylated"))

joinA123 = left_join(A119_data, A123_data, by = "start")
joinEG4 = left_join(joinA123, EG4_data, by = "start")
joinHEG4 = left_join(joinEG4, HEG4_data, by = "start")

methylfinal = joinHEG4[, c(2:52)]
methylfinal$chrom = as.numeric(gsub( "Chr", "", as.character(methylfinal$chrom)))
methylfinal$start = methylfinal$start + 50
methylfinal$stop = methylfinal$stop - 50
methylfinalfinal = rename(methylfinal, c("chrom"="mPingChr" , "start"="mPingSTART" , "stop"="mPingSTOP"))

joinfinal = left_join(Main, methylfinalfinal, by = c("mPingChr", "mPingSTART", "mPingSTOP"))

write.table(joinfinal,"emptysiteRNAMethyl.txt",sep="\t",row.names=FALSE)
