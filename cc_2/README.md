# Instructions

Summarize the statistics files in a folder.
One file per genome, the files list some summary stats for an assembly.

The files are named XXX.stats where XXX is the name of the genome. The files contain fields that look like:
```
INFO = VALUE
```
with white space padding
Here is a real example:

```
Assembly statistics for: Aetokthonos_hydrillicola_B3-Florida.fna
   CONTIG COUNT  =  115
   TOTAL LENGTH  =  9699671
            MIN  =  3098
            MAX  =  631503
         MEDIAN  =  44005
           MEAN  =  84344.97
            L50  =  18
            N50  =  164048
            L90  =  59
            N90  =  42492
```

Write a script (python most likely) to read all of these file in and produce a summary table like this which has a line for each genome in the report. This example only shows one
```
SampleID	CONTIG COUNT	TOTAL LENGTH	MIN	MAX	MEDIAN	MEAN	L50	N50	L90	N90	
Aetokthonos_hydrillicola_B3-Florida	115	9699671	3098	631503	44005	84344.97	18	164048	59	42492
```
