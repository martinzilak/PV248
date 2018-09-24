#!/usr/bin/env python

import sys
import re
import codecs
from collections import Counter

MODES = ['composer', 'century']
YEAR_FORMATS = [r'Composition\s*Year:\s(\d{3,4}).*\n', r'Composition\s*Year:\s(\d*)\w{2}\scentury\n', r'Composition\s*Year:\s\D+\s(\d{3,4}).*\n', r'Composition\s*Year:\s\d*.\s\d*.\s(\d{3,4}).*\n']
COMPOSER = {'LINE': r'Composer:\s(.*)\n', 'YEAR': r'(.*?)\(.?\d+.*\)'}

if len(sys.argv) != 3:
    raise ValueError('Wrong number of arguments passed')
if sys.argv[2] not in MODES:
    raise ValueError('Unknown mode passed, possible values are: ', MODES)

file = open(sys.argv[1], errors = 'ignore')
mode = sys.argv[2]

ctr = Counter()

#stolen from https://stackoverflow.com/a/36977549
suf = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))

def century(year):
    c = year // 100 + (1 if year % 100 != 0 else 0)
    return(suf(c) + ' century')

if mode == 'composer':
    rcomposer = re.compile(COMPOSER['LINE'])
    ryear = re.compile(COMPOSER['YEAR'])

if mode == 'century':
    ryf = []
    for yf in YEAR_FORMATS:
        ryf.append(re.compile(yf))

for line in file:
    if mode == 'composer':
        mcomposer = rcomposer.match(line)
        if mcomposer:
            for name in mcomposer.group(1).split(';'):
                myear = ryear.match(name)
                n = myear.group(1) if myear else name
                n = n.strip()
                if len(n) > 0:
                    ctr[n] += 1
    if mode == 'century':
        for r in ryf:
            m = r.match(line)
            if m:
                y = m.group(1).strip()
                if len(y) > 2:
                    ctr[century(int(y))] += 1
                elif len(y) > 0:
                    ctr[suf(int(y)) + ' century'] += 1

for k, v in ctr.most_common():
    print(k, ': ', v, sep = '')
