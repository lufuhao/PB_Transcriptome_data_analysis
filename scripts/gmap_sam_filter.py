#!/usr/bin/env python
import os, re, sys
from Bio import SeqIO
from collections import namedtuple
import BioReaders

def sam_filter(sam_filename, output_filename, min_coverage, min_identity, query_fasta_filename, prog):
    if prog == 'gmap':
        reader_func = BioReaders.GMAPSAMReader
    elif prog == 'blasr':
        reader_func = BioReaders.BLASRSAMReader
    else:
        reader_func = BioReaders.SAMReader

    query_len_dict = dict((r.id,len(r.seq)) for r in SeqIO.parse(open(query_fasta_filename),'fasta'))
    reader = reader_func(sam_filename, has_header=True, query_len_dict=query_len_dict)
    f = open(output_filename, 'w')
    f.write(reader.header)
    for r in reader:
        if r.sID == '*': continue
        if r.qCoverage is None:
            print >> sys.stder, "qCoverage field is None! SAM file must not have been generated by BLASR or pblalign.py. Abort!"
            sys.exit(-1)
        if r.sID!='*' and r.qCoverage >= min_coverage and r.identity >= min_identity:
            f.write(r.record_line + '\n')
    f.close()
    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("Filtering SAM output")
    parser.add_argument("-i", "--input-sam", dest="input", required=True, help="Input SAM filename")
    parser.add_argument("-o", "--output-sam", dest="output", required=True, help="Output SAM filename")
    parser.add_argument("--query-fasta", dest="query_fasta_filename", required=True, help="Query fasta filename (used for getting query length accurately)")
    parser.add_argument("--min-coverage", dest="cov", default=.9, type=float, help="Minimum alignment coverage (def: 0.9)")
    parser.add_argument("--min-identity", dest="iden", default=.8, type=float, help="Minimum alignment identity (def: 0.8)")
    parser.add_argument("--prog", required=True, choices=['gmap', 'blasr', 'bowtie'], help="Program used to generate SAM")

    args = parser.parse_args()
    
    if args.cov < 0 or args.cov > 1:
        print >> sys.stderr, "min-coverage must be between 0-1."
        sys.exit(-1)
    if args.iden < 0 or args.iden > 1:
        print >> sys.stderr, "min-identity must be between 0-1."
        sys.exit(-1)   
             
    sam_filter(args.input, args.output, args.cov, args.iden, args.query_fasta_filename, args.prog)