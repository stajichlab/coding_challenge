#!/usr/bin/env perl
use strict;
use warnings;

my $file = "features.bed";

my (%features,%lengths);

my $count;
my $genes;
open(my $fh => $file) || die "cannot open $file: $!";

while(<$fh>) {
    $count ++;
    chomp;
    my @row = split(/\t/,$_);
    my ($chrom,$start,$end,$feature) = @row;
    # either split on -
    my ($type,$name) = split('-',$feature);
    # or use pattern
    #if ( $feature =~ /(\S+)-(\S+)/ ) {
    #($type,$name) = ($1,$2);
    #}
    push @{$features{$type}}, [ $chrom, $start, $end, $feature,
				abs($end - $start), $name];
    $lengths{$type} += abs($end - $start);
    if ( $type eq 'Gene' ) {
	$genes++;
    }
}

	
print "How many feature are in the file?\n";
print $count, "\n";

print "How many genes are in the file?\n";
print $genes,"\n";
# or could do it this way
# print scalar @{$features{'Gene'}}, "\n";

print "What are the types features?\n";
foreach my $ftype ( sort keys %features ) {
    print $ftype,"\n";
}
# could also write more compactly.
#print join("\n",( sort keys %features )),"\n";


print "How many of each type of feature?\n";
foreach my $ftype ( sort keys %features ) {
    printf "%d\t%s\n",scalar @{$features{$ftype}}, $ftype;
}


print "How many bases are contained in each type of feature?\n";
foreach my $ftype ( sort keys %lengths ) {
    printf "%d bp\t\t%s\n",$lengths{$ftype}, $ftype;
}

print "Print out the genes in order of their size\n";
my @genes =     @{$features{'Gene'}};
foreach my $genedat ( sort { $a->[4] <=> $b->[4] }
		      @genes ) {
    my ($chrom,$start,$end,$feature, $len) = @$genedat;
    print "$feature\t$len\n";
}
