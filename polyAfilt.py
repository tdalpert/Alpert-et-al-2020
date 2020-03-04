import sys
import pandas as pd
import os
import re
import glob

data_files = glob.glob('*.sam')

def filter_pA(data):
    c = 0
    counter = 0

    # filename = data.split('/')[ len(data.split('/')) - 1 ]
    filename = data.split('.sam')[0]
    filename = filename + '_filtered.sam'

    filt = open(filename, 'w')
    with open(data, 'r') as da:
        for line in da:
            linefull = line.strip('\n')
            line = linefull.split('\t')
            if line[0][0] == '@':
                filt.write(linefull + '\n')
                continue
            c += 1
 
            # reset indexF for every line
            indexF = []

            cigar = line[5]
            read = line[9]

            # index from front of cigar
            indexF = cigar.find('S', 0, 4)
            if indexF != -1:
                clippedF = read[ 0: int(cigar[0:indexF]) ]

            # clipped bases from end of cigar
            if re.search('[0-9]{0,3}(?=S$)' , cigar) != None:
                m = re.search('[0-9]{0,3}(?=S$)' , cigar)
                numberE = int(m.group(0))
                clippedE =  read[ : (-1*(numberE+1)) : -1 ]
                clippedE = clippedE[::-1]

            switch = False
            # if clipped bases have stretch of 6 A's or T's on either end and are shorter than 30, then flip the switch
            if clippedF.find('AAAAAA') != -1 or clippedF.find('TTTTTT') != -1 and len(clippedF) < 30:
                switch = True
            if clippedE.find('AAAAAA') != -1 or clippedE.find('TTTTTT') != -1 and len(clippedE) < 30:
                switch = True

            # for longer clippings, must have 10 A's or T's to flip switch:
            if clippedF.find('AAAAAAAAAA') != -1 or clippedF.find('TTTTTTTTTT') != -1 and len(clippedF) >= 30:
                switch = True
            if clippedE.find('AAAAAAAAAA') != -1 or clippedE.find('TTTTTTTTTT') != -1 and len(clippedE) >= 30:
                switch = True

            if switch:
                counter += 1
            if switch == False:
                filt.write(linefull + '\n')

    filt.close()

for data in data_files:
    filter_pA(data)

# print 'Number of polyA reads filtered out: ' + str(counter)
# print 'Total number of reads: ' + str(c)
