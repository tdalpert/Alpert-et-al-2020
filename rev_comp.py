import os
import sys
import glob
import re

# %cd C:\\Users\\taraa\\Documents\\_lab\\nanopore\\aid\\four_samples\\trimmed
files = glob.glob('./*rev2.fastq')
# print files

complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

for i in files:
    print(i)
    newfilename = re.sub('rev2.fastq' , 'revcomp.fastq' , i)
    with open(i, 'r') as f:
        with open(newfilename, 'w') as new:
            c = 0
            for line in f:
                c += 1
                line = line.strip('\n')
                if c!= 2:
                    new.write(line + '\n')
                if c == 2:
                    reverse_complement = "".join(complement.get(base, base) for base in reversed(line))
                    new.write(reverse_complement + '\n')
                if c == 4:
                    c = 0
