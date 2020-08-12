#!/usr/bin/env python3
import csv, re, argparse, gzip, os

import tabix

# for speed see tabix
# https://github.com/slowkow/pytabix
from subprocess import Popen, PIPE

def bgzip(filename):
    """Call bgzip to compress a file."""
    bgzipfile = '%s.gz'%(filename)
    if os.path.exists()
    with open(bgzipfile, 'w') as output:
        Popen(['bgzip', '-f', '-c',filename],stdout=output)

def tabix_index(filename,
        preset="gff", chrom=1, start=4, end=5, skip=0, comment="#"):
    """Call tabix to create an index for a bgzip-compressed file."""
    chrom = "%d"%(chrom)
    start = "%d"%(start)
    end = "%d"%(end)
    skip = "%d"%(skip)
    print("index cmd is %s"%(" ".join(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
        '-S', skip, '-c', comment])))
    Popen(['tabix', '-p', preset, '-s', chrom, '-b', start, '-e', end,
        '-S', skip, '-c', comment])

def tabix_query(filename, chrom, start, end):
    """Call tabix and generate an array of strings for each line it returns."""
    query = '{}:{}-{}'.format(chrom, start, end)
    process = Popen(['tabix', '-f', filename, query], stdout=PIPE)
    for line in process.stdout:
        yield line.strip().split()


# this sets up command line parsing options

parser = argparse.ArgumentParser(prog="summarize_5mC", add_help=True,
    description='Compute summary stats about 5mC across windows')
parser.add_argument('-s','--sites', type=argparse.FileType('r'), required=True,
                    help='BEDfile of sites to study (eg all_empty_sites.bed)')

parser.add_argument('-w','--windowsize', type=int, default=50, required=False,
                    help='Window expansion of the sites.')

parser.add_argument('--allc', nargs='+',required=True,
                    help='allC files produced from 5mC analyses, one per strain to analyze')

parser.add_argument('-', '--outdir',default="output_summary",
                    help='Output directory')
args = parser.parse_args()

windows = []

bedparse = csv.reader(args.sites,delimiter="\t")
for bedline in bedparse:
    #print(bedline)
    # fix missing Chr in name
    if re.match(r'^\d+',bedline[0]):
        bedline[0] = "Chr%s"%(bedline[0])
    bedline[1] = int(bedline[1]) - args.windowsize
    if bedline[1] < 1:
        bedline[1] = 1
    # it is hard to know if we have extended past the end of a chrom
    bedline[2] = int(bedline[2]) + args.windowsize
    windows.append(bedline)

for infile in args.allc:
    bgzip(infile)
    tabix_index(infile)
    outfilename = os.path.splitext(infile)[0]+'.summary.tab'
    if infile == outfilename:
        print("did not properly setup outputfile ")
        exit
    if os.path.exists(outfilename+".tbi"):
        # running basically: tabix -s 1 -b 2 -e 2
        tabix_index(infile,"bed",1,2,2)
    with open(outfilename,"w") as outfh:
        outfh.write("hello\n")
