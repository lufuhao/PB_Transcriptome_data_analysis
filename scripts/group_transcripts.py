#!/usr/bin/env python
import os, sys
import branch_simple

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("fasta_filename", help="fasta filename")
    parser.add_argument("sam_filename", help="GMAP SAM filename (must be sorted)")
    parser.add_argument("output_prefix", help="output prefix")
    parser.add_argument("--cov_threshold", default=2, type=int, help="Minimum coverage (of GMAP record), default: 2")

    args = parser.parse_args()


    b = branch_simple.BranchSimple(args.fasta_filename, cov_threshold=args.cov_threshold)
    b.run_on_gmap_sam(args.sam_filename, args.output_prefix)
