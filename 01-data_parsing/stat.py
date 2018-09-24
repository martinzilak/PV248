#!/usr/bin/env python

import sys
import re
import codecs
from collections import Counter

MODES = ['composer', 'century']
YEAR_FORMATS = [r'Composition\s*Year:\s(\d{3,4}).*\n', r'Composition\s*Year:\s(\d*)\w{2}\scentury\n', r'Composition\s*Year:\s[a-z.]{2,3}\s(\d{3,4}).*\n']

if len(sys.argv) != 3:
    raise ValueError('Wrong number of arguments passed')
if sys.argv[2] not in MODES:
    raise ValueError('Unknown mode passed, possible values are: ', MODES)

#file = codecs.open(sys.argv[1], 'r', encoding = "cp1250", errors='ignore')
file = open(sys.argv[1], 'r', encoding="utf-8")
mode = sys.argv[2]

ctr = Counter()

#stolen from https://stackoverflow.com/a/36977549
suf = lambda n: "%d%s"%(n,{1:"st",2:"nd",3:"rd"}.get(n if n<20 else n%10,"th"))

def century(year):
    c = year // 100 + 1
    return(suf(c) + ' century')

if mode == 'composer':
    rcomposer = re.compile(r'Composer:\s(.*)\n')
    ryear = re.compile(r'(.*?)\(.*?\)')

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

for k, v in ctr.items():
    print(k, ': ', v, sep = '')

'''
found year formats:
XXXX
XXXX Leipzig
XXXX/XXXX
XXXX--XXXX
XXXX, Hamburg
\w*\s*Year:\s(\d{3,4}).*\n

XXth century
\w*\s*Year:\s(\d*)\w{2}\scentury\n

ca XXXX
ca. XXXX
\w*\s*Year:\s[a-z.]{2,3}\s(\d{3,4}).*\n
'''

